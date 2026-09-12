# 🚀 Team Project & Task Management REST API

A production-grade, relational REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy 2.0**, featuring robust JWT authentication, refresh token rotation, granular Role-Based Access Control (RBAC), and end-to-end **OWASP API Security Top 10** defenses.

---

## 📑 Table of Contents
- [1. Purpose & Overview](#-1-purpose--overview)
- [2. Architecture & Design Patterns](#-2-architecture--design-patterns)
- [3. Technology Stack](#-3-technology-stack)
- [4. Installation & Local Setup](#-4-installation--local-setup)
- [5. Environment Variables Configuration](#-5-environment-variables-configuration)
- [6. Database Migrations (Alembic)](#-6-database-migrations-alembic)
- [7. Database Seeding](#-7-database-seeding)
- [8. Running the Application](#-8-running-the-application)
- [9. Docker & Container Orchestration](#-9-docker--container-orchestration)
- [10. Running Automated Tests & Coverage](#-10-running-automated-tests--coverage)
- [11. Security Scanning & Static Analysis](#-11-security-scanning--static-analysis)
- [12. Interactive Swagger UI & API Documentation](#-12-interactive-swagger-ui--api-documentation)
- [13. CI/CD Pipeline Architecture](#-13-cicd-pipeline-architecture)
- [14. Production Deployment & Operational Runbook](#-14-production-deployment--operational-runbook)

---

## 🎯 1. Purpose & Overview

The **Team Project Management API** is a collaborative platform designed for engineering teams to manage workspaces, projects, tasks, and task comments with strict multi-tenant isolation and security boundaries.

### Key Capabilities:
* **Multi-Tier Identity Management:** User registration, secure login with Argon2id hashing, short-lived JWT access tokens, and rotating refresh tokens.
* **Granular Role-Based Access Control (RBAC):** Hierarchical permissions across `admin`, `manager`, and standard `user` roles, supplemented with per-project roles (`PROJECT_MANAGER`, `MEMBER`).
* **Relational Workflows:** Seamless project lifecycle management, member provisioning, task delegation with multi-attribute filtering, search, sorting, and threaded comments.
* **OWASP API Security Compliance:** Built-in defenses against BOLA/IDOR, Mass Assignment (BOPLA), Broken Authentication, BFLA, SSRF, and sensitive business flow abuse.

---

## 🏗️ 2. Architecture & Design Patterns

The project follows a clean **Layered Architecture** adhering to separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Clients / Frontend                  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             FastAPI Routers & Middleware Layer              │
│  - Request ID Tracing (X-Request-ID)   - Security Headers   │
│  - Logging Middleware                 - Centralized Errors  │
│  - CORS Hardening                     - Auth & RBAC Guards  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Service Layer                    │
│  - Business logic validation         - Token rotation       │
│  - Sorting whitelist checks           - SSRF-safe HTTP client│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Repository Layer                        │
│  - Relational queries (PostgreSQL)    - Aggregations        │
│  - Dynamic filtering & pagination    - Atomic transactions  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              Database / Persistence (PostgreSQL)            │
└─────────────────────────────────────────────────────────────┘
```

### Relational Schema Design:
* **Users:** Master user identity, credentials, system role (`admin`, `manager`, `user`).
* **Projects:** Workspace entity containing title, client details, lifecycle dates, and status.
* **Project Members:** Many-to-Many junction table (`project_members`) mapping users to projects with custom project roles (`PROJECT_MANAGER`, `MEMBER`).
* **Tasks:** Granular work items linked to projects and assigned to users, with priority (`low`, `medium`, `high`, `urgent`) and status (`pending`, `in_progress`, `completed`).
* **Comments:** Threaded discussions tied to individual tasks and authored by authenticated project members.
* **Refresh Tokens:** Cryptographically hashed session tokens with revocation and rotation tracking.

---

## 🛠️ 3. Technology Stack

| Category | Technology |
| :--- | :--- |
| **Language & Runtime** | Python 3.11+ / Python 3.13 |
| **Web Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ASGI Web Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Database** | [PostgreSQL](https://www.postgresql.org/) (Neon Serverless & Local Container) |
| **ORM & Database Driver** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) & [psycopg](https://www.psycopg.org/psycopg3/) (v3) |
| **Schema Migration Engine** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) (with `email-validator`) |
| **Cryptography & Auth** | Argon2id (`pwdlib[argon2]`), [PyJWT](https://pyjwt.readthedocs.io/), `secrets` |
| **Testing Suite** | [pytest](https://pytest.org/), `pytest-cov`, `pytest-asyncio`, `httpx` |
| **Code Quality & Typing** | [Ruff](https://astral.sh/ruff), [mypy](https://mypy-lang.org/) |
| **Security Scanning** | [Bandit](https://bandit.readthedocs.io/), [pip-audit](https://pypi.org/project/pip-audit/), [Trivy](https://trivy.dev/), [Gitleaks](https://github.com/gitleaks/gitleaks) |
| **Containerization** | Docker, Docker Compose, Multi-stage Slim Images |

---

## 💻 4. Installation & Local Setup

### Prerequisites
* Python 3.11 or higher
* PostgreSQL database or Docker installed
* Git

### Step-by-Step Setup:
```powershell
# 1. Clone repository
git clone https://github.com/Subhanulhaq935/team_project_api.git
cd team-project-api

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux / macOS:
source venv/bin/activate

# 4. Install all dependencies
pip install -r requirements.txt
```

---

## ⚙️ 5. Environment Variables Configuration

Create a `.env` file in the root directory (or copy from `.env.example`):

```env
# Application Settings
ENVIRONMENT=development
DEBUG=true
PORT=8000

# Database Connection (PostgreSQL or SQLite for quick local test)
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/team_project_db

# Cryptography & JWT Security
JWT_SECRET_KEY=change_this_to_a_secure_random_string_at_least_32_characters_long
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Allowed Origins (Comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000

# Optional Git SHA tracking for /api/v1/version
GIT_COMMIT_SHA=development
```

---

## 🔄 6. Database Migrations (Alembic)

Database schema evolution is managed through Alembic.

```powershell
# Apply all latest migrations
alembic upgrade head

# Rollback single migration
alembic downgrade -1

# Generate a new autogenerated migration after model updates
alembic revision --autogenerate -m "describe_schema_change"

# View current database revision
alembic current
```

---

## 🌱 7. Database Seeding

Populate the database with realistic demonstration users, projects, tasks, and comments:

```powershell
python -m app.db.seed
```

### Seeded Demonstration Accounts:
| Role | Email | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@example.com` | `AdminPassword123!` | System-wide administrative operations |
| **Manager** | `manager@example.com` | `ManagerPassword123!` | Project management and member assignment |
| **Developer (User A)** | `developer@example.com` | `DeveloperPassword123!` | Task assignment, status updates, comments |
| **User B (Isolated)** | `user_b@example.com` | `UserBPassword123!` | BOLA / IDOR security testing |

---

## ▶️ 8. Running the Application

### Development Mode (with hot-reloading)
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Production Mode
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🐳 9. Docker & Container Orchestration

### Multi-Container Stack (FastAPI + PostgreSQL) with Docker Compose
```powershell
# Build and start services in background
docker compose up --build -d

# Inspect status
docker compose ps

# Run migrations inside container
docker compose exec app alembic upgrade head

# Seed database inside container
docker compose exec app python -m app.db.seed

# Stop and tear down containers
docker compose down
```

### Standalone Production Docker Build
```powershell
# Build non-root hardened Docker image
docker build -t team-project-api:latest .

# Run image with environment file
docker run -d --name team-project-api -p 8000:8000 --env-file .env team-project-api:latest
```

---

## 🧪 10. Running Automated Tests & Coverage

The automated test suite exercises unit tests, integration tests, and security regression tests using an isolated test database.

```powershell
# Run full pytest suite with verbose output
pytest -v

# Run only authentication and security tests
pytest -v -k "auth or security or bola"

# Run tests with code coverage report
pytest --cov=app --cov-report=term-missing
```

---

## 🛡️ 11. Security Scanning & Static Analysis

Security analysis tools are integrated locally and into CI:

```powershell
# 1. Static Application Security Testing (SAST)
bandit -r app

# 2. Dependency Vulnerability Audit (CVE scanner)
pip-audit

# 3. Code Formatting & Linting
ruff check .

# 4. Static Type Checking
mypy app

# 5. Secret Leak Detection
gitleaks detect --source . -v

# 6. Container Vulnerability Scanning
trivy image team-project-api:latest
```

---

## 📖 12. Interactive Swagger UI & API Documentation

Once the server is running, explore and test the interactive API documentation:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Raw OpenAPI Specification:** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

For detailed endpoint catalog, query params, payloads, and response codes, refer to [`docs/api-inventory.md`](docs/api-inventory.md).

---

## ⚙️ 13. CI/CD Pipeline Architecture

Continuous Integration and Delivery is automated using **GitHub Actions** (`.github/workflows/ci.yml`):

```
Push / PR
  │
  ├─► Stage 1: Code Quality (Ruff Lint & Mypy Type Check)
  ├─► Stage 2: Security Scans (Bandit SAST, pip-audit CVEs, Gitleaks)
  ├─► Stage 3: Database & Migrations (PostgreSQL Service Container + Alembic)
  ├─► Stage 4: Automated Testing (Pytest + Coverage Thresholds)
  ├─► Stage 5: Container Build & Trivy Vulnerability Scan
  └─► Stage 6: Continuous Deployment (Cloud Hook / Trigger)
```

---

## 🚀 14. Production Deployment & Operational Runbook

### Health Probes & Monitoring:
* **Liveness Probe:** `GET /health/live` — Verifies HTTP server is responding (`{"status": "alive"}`).
* **Readiness Probe:** `GET /health/ready` — Verifies database connection with `SELECT 1` (returns `503 Service Unavailable` on DB disconnection).
* **Version Probe:** `GET /api/v1/version` — Returns application version, active environment, and Git commit hash.

### Rollback & Migration Strategy:
See the complete operational guide in [`docs/operations-and-rollback.md`](docs/operations-and-rollback.md) for:
* Zero-downtime 3-Phase Expand/Contract schema evolution.
* Alembic rollbacks (`alembic downgrade -1`).
* Instant container image rollbacks via cloud dashboard/Docker tags.
* Graceful server shutdowns via FastAPI `@asynccontextmanager` lifecycle hooks.

---

## 📄 License & Attribution
Developed as part of the backend engineering & API security curriculum. Licensed under the MIT License.
