# 🔄 Production Operations, Rollback Procedures & Database Migration Strategy

This document outlines standard operating procedures for **production deployments**, **application and database rollbacks**, **migration risk mitigation**, and **zero-downtime backward-compatible schema evolutions**.

---

## 📋 Table of Contents
1. [Deployment Architecture & Verification](#1-deployment-architecture--verification)
2. [Application Rollback Procedure](#2-application-rollback-procedure)
3. [Database Rollback Procedure (Alembic)](#3-database-rollback-procedure-alembic)
4. [Database Migration Risks in Production](#4-database-migration-risks-in-production)
5. [Backward-Compatible Schema Strategy (Expand/Contract Pattern)](#5-backward-compatible-schema-strategy-expandcontract-pattern)
6. [Emergency Incident Checklist](#6-emergency-incident-checklist)

---

## 1. Deployment Architecture & Verification

The production pipeline enforces an immutable artifact release flow:
```
Approved Docker Image ➔ Release Command (Alembic Migrations) ➔ App Deployment ➔ Liveness/Readiness Probes ➔ Smoke Tests
```

### Health & Observability Endpoints
| Endpoint | Probe Type | Purpose | Healthy Response |
| :--- | :--- | :--- | :--- |
| `GET /health/live` | **Liveness** | Checks if the container process is alive and accepting connections. | `200 OK {"status": "alive"}` |
| `GET /health/ready` | **Readiness** | Executes `SELECT 1` against PostgreSQL to confirm DB availability before traffic routing. | `200 OK {"status": "ready", "database": "connected"}` |
| `GET /api/v1/version` | **Version / Audit** | Exposes running semantic version, environment name, and Git commit SHA. | `200 OK {"version": "1.0.0", "environment": "production", ...}` |

---

## 2. Application Rollback Procedure

An application rollback is triggered when a new release introduces runtime bugs, unhandled exceptions, or performance regressions while the underlying database schema remains compatible.

### A. Managed Cloud (Render / Railway / Azure App Service)
1. **Instant Re-route**: In the hosting console (e.g. Render Dashboard), navigate to **Deploys** and select the previous stable deployment.
2. **Rollback Trigger**: Click **"Rollback to this deploy"** or redeploy the prior approved commit.
3. **Verify Routing**: Verify that incoming traffic routes to the healthy previous release within seconds without container rebuild overhead.

### B. Container & Docker Registry Rollback
If running standalone Docker / Container Registry:
```bash
# 1. Pull the previous verified image tag (e.g. v1.0.8)
docker pull myregistry.azurecr.io/team-project-api:v1.0.8

# 2. Restart container targeting the previous tag
docker stop team-project-api
docker rm team-project-api
docker run -d --name team-project-api --env-file .env -p 8000:8000 myregistry.azurecr.io/team-project-api:v1.0.8

# 3. Verify health
curl -f http://localhost:8000/health/ready || exit 1
```

---

## 3. Database Rollback Procedure (Alembic)

Database rollbacks revert schema changes when a migration introduces structural issues, indexing deadlocks, or unintended constraints.

> [!WARNING]
> **Data Loss Risk:** Downgrading migrations that dropped columns or altered constraints can cause irrevocable data loss or downtime if live application instances still depend on the newer schema. Always execute a database snapshot before running migrations.

### Step-by-Step Alembic Downgrade
```bash
# 1. Inspect current database revision and migration history
alembic current
alembic history --verbose

# 2. Rollback the most recent migration (1 step back)
alembic downgrade -1

# 3. OR Rollback to a specific target revision ID
alembic downgrade <revision_id>

# 4. Verify the active database head matches the rollback target
alembic current
```

### Point-in-Time Recovery (PITR) & Snapshots
For managed databases (AWS RDS, Neon, Supabase, Azure Database for PostgreSQL):
1. Take an automated or manual snapshot prior to any major schema release.
2. In the event of catastrophic data corruption, initiate Point-in-Time Recovery (PITR) to restore state prior to the migration timestamp.

---

## 4. Database Migration Risks in Production

| Risk Factor | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Exclusive Table Locks (`ACCESS EXCLUSIVE`)** | `ALTER TABLE ADD COLUMN NOT NULL` (without default in older DBs) or `ALTER COLUMN TYPE` locks the entire table against reads and writes. | Add columns with `DEFAULT` or as `NULLABLE`. Create indexes with `CONCURRENTLY`. |
| **Long-Running Backfills** | Migrations updating millions of rows saturate CPU/IOPS and exhaust connection pools. | Run batch backfills asynchronously in background jobs outside Alembic migration transactions. |
| **Irreversible Changes** | `DROP TABLE` or `DROP COLUMN` destroys historical data instantly. | Enforce deprecation periods. Do not drop columns until the new release has been stable in production for at least 1-2 sprint cycles. |
| **Schema/Code Desynchronization** | During rolling updates, old container replicas query a newly migrated schema and crash due to unexpected columns or missing constraints. | Follow the **Expand / Contract** pattern for all schema changes. |

---

## 5. Backward-Compatible Schema Strategy (Expand/Contract Pattern)

To achieve **Zero-Downtime Deployments**, never execute breaking schema changes in a single release. All structural changes must follow the **Expand / Contract (Parallel Run)** strategy across multiple releases.

```mermaid
flowchart LR
    subgraph Step 1: Expand
        A1[Add New Column NULLABLE] --> A2[Deploy App: Dual Writing]
    end
    subgraph Step 2: Transition
        B1[Backfill Historical Data] --> B2[Switch Reads to New Column]
    end
    subgraph Step 3: Contract
        C1[Stop Old Column Writes] --> C2[Drop Deprecated Column]
    end
    Step 1: Expand --> Step 2: Transition --> Step 3: Contract
```

### Example: Renaming a Column (`name` ➔ `project_name`)

#### Phase 1: Expand (Release N)
1. **Migration**: Add new column `project_name` as `NULLABLE`. Keep old column `name`.
2. **Application Code**:
   - Write to both `name` and `project_name` simultaneously.
   - Continue reading from `name` (or fallback to `project_name`).
3. **Deploy Release N**: Older and newer application instances can both run safely during rollout.

#### Phase 2: Transition & Backfill
1. Run background script to copy data from `name` to `project_name` for historical rows:
   ```sql
   UPDATE projects SET project_name = name WHERE project_name IS NULL;
   ```
2. **Application Code**: Update application reads to use `project_name`.

#### Phase 3: Contract (Release N+1)
1. **Application Code**: Remove all references to the legacy `name` column.
2. **Migration**: Apply migration to drop `name` column and set `project_name` to `NOT NULL`:
   ```python
   def upgrade():
       op.alter_column('projects', 'project_name', nullable=False)
       op.drop_column('projects', 'name')
   ```

---

## 6. Emergency Incident Checklist

When an incident occurs in Production:
- [ ] **Check Health Endpoints:** Check `GET /health/ready` and `GET /health/live`.
- [ ] **Inspect Logs:** Search structured logs by `request_id` or query error codes (`500 INTERNAL_SERVER_ERROR`).
- [ ] **Assess Blast Radius:** Determine if the issue is Application Code (HTTP 5xx, memory leak) or Database (deadlocks, migration failure).
- [ ] **Trigger Code Rollback:** If schema was not modified, immediately revert application container to previous release.
- [ ] **Trigger DB Rollback (if necessary):** If migration caused corruption, revert with `alembic downgrade -1` or restore latest PITR snapshot.
- [ ] **Run Post-Mortem:** Document root cause, timeline, customer impact, and action items to prevent recurrence.
