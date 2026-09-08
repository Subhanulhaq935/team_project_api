# 🚀 Team Project & Task Management REST API

A production-ready, relational REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy 2.0**, featuring robust JWT authentication, refresh token rotation, granular Role-Based Access Control (RBAC), and end-to-end **OWASP API Security Top 10 (API1–API10)** defenses.

---

## 📌 Live Demo & API Documentation

* **Interactive Swagger UI (Render):** [team-project-api-eakc.onrender.com/docs](https://team-project-api-eakc.onrender.com/docs#/)
* **Local Swagger UI:** `http://127.0.0.1:8000/docs`
* **Local ReDoc:** `http://127.0.0.1:8000/redoc`
* **Local OpenAPI JSON:** `http://127.0.0.1:8000/openapi.json`

---

## 🛠️ Tech Stack

* **Language:** Python 3.13
* **Framework:** FastAPI
* **ASGI Server:** Uvicorn
* **Data Validation & Serialization:** Pydantic v2 (with `email-validator`)
* **Database:** PostgreSQL (Neon Serverless)
* **ORM:** SQLAlchemy 2.0
* **Database Driver:** psycopg (v3)
* **Database Migrations:** Alembic
* **Password Hashing:** Argon2id (`pwdlib[argon2]`)
* **Authentication & Authorization:** PyJWT (Access Tokens) & Cryptographic Refresh Tokens (`secrets`)
* **Security & Defense:** OWASP API Security Top 10 Compliance (BOLA/BFLA prevention, SSRF defense, CORS hardening, Security Headers)
* **Architecture:** Layered Architecture (Models, Repositories, Services, Schemas, Dependencies, Core)

---

## 📊 Development Progress

| Milestone | Key Focus Area | Status |
| :--- | :--- | :---: |
| **Day 1** | FastAPI & REST Fundamentals | `✅ Complete` |
| **Day 2** | PostgreSQL & SQLAlchemy Integration | `✅ Complete` |
| **Day 3** | Alembic Migrations & Database Seeding | `✅ Complete` |
| **Day 4** | Tasks, Comments & Relational Architecture | `✅ Complete` |
| **Day 5** | Many-to-Many Relationships, Project Members & Transactions | `✅ Complete` |
| **Day 6** | User Authentication & JWT Authorization | `✅ Complete` |
| **Day 7** | Refresh Tokens, Token Rotation & Session Security | `✅ Complete` |
| **Day 8** | Role-Based Access Control (RBAC) & Project Access Authorization | `✅ Complete` |
| **Day 9** | Validation, Filtering, Pagination, Search & Sorting | `✅ Complete` |
| **Day 10** | Custom Middleware, Request Tracing & Global Exception Handling | `✅ Complete` |
| **Day 11** | Automated Testing with Pytest & Test DB Fixtures | `✅ Complete` |
| **Day 12** | API Performance, Indexing & Query Optimizations | `✅ Complete` |
| **Day 13** | OWASP API Security Top 10 (API1–API5 Hardening) | `✅ Complete` |
| **Day 14** | OWASP API Security Top 10 (API6–API10, SSRF Defense, API Inventory & Docs) | `✅ Complete` |

---

## 📅 Daily Milestones & Technical Log

### Day 1 — FastAPI & REST Fundamentals
* Built initial Health Check and CRUD endpoints for Projects.
* Configured Pydantic request and response schemas.
* Set up standard HTTP status codes and automatic OpenAPI docs.
* *Note:* Used an in-memory store before database persistence.

### Day 2 — PostgreSQL & SQLAlchemy
* Connected FastAPI with PostgreSQL using SQLAlchemy 2.0 Engine and Sessions.
* Created Declarative `Base` and the `Project` database model.
* Migrated CRUD operations from in-memory arrays to PostgreSQL queries.
* Managed runtime configurations via environment variables (`.env`).

### Day 3 — Alembic Migrations & Database Seeding
* Initialized Alembic and bound it to SQLAlchemy metadata.
* Implemented the `User` model with email uniqueness constraints.
* Created automated database seeding for default admin, manager, and projects.

### Day 4 — Tasks, Comments & Relational Architecture
* Added `Task` and `Comment` models with Foreign Key constraints.
* Implemented the Repository and Service architectural pattern for clean separation of concerns.
* Added relational integrity checks across Projects, Tasks, Users, and Comments.

### Day 5 — Many-to-Many Relationships, Project Members & Transactions
* **Many-to-Many Architecture:** Implemented a Many-to-Many relationship between `Projects` and `Users` using the `project_members` junction table.
* **Project Membership Management:** Added full CRUD functionality and dedicated endpoints to add, view, and remove project members.
* **Data Integrity:** Added a unique constraint on `(project_id, user_id)` to prevent duplicate member assignments.
* **Project Analytics:** Built a Project Summary API aggregating total members, tasks, task statuses, and comments.
* **Database Transactions & Consistency:**
  * Wrapped project creation in atomic transactions using `commit()` and `rollback()`.
  * Used `db.flush()` to generate and retrieve the `project_id` before creating the junction record.
  * Automatically assigned the project creator the `PROJECT_MANAGER` role.
* **API Testing:** Verified all new endpoints and relationship constraints via Swagger UI.

### Day 6 — User Authentication & JWT Authorization
* **Password Hashing:** Integrated modern password hashing with Argon2id using `pwdlib`.
* **User Registration (`POST /api/v1/auth/register`):** Enforces email uniqueness validation and securely stores hashed passwords.
* **User Login (`POST /api/v1/auth/login`):** Verifies user credentials and generates short-lived JWT access tokens with claims (`sub`, `role`, `iat`, `exp`, `jti`).
* **Protected Routes (`GET /api/v1/auth/me`):** Created `get_current_user` FastAPI dependency utilizing `HTTPBearer` to validate access tokens and attach the authenticated `User` to requests.

### Day 7 — Refresh Tokens, Token Rotation & Session Security
* **Database-Backed Refresh Tokens:** Created the `RefreshToken` database model and executed Alembic migration `fc1d00a5b271_add_refresh_tokens.py`.
* **Cryptographic Security:** Generated 64-byte URL-safe cryptographically secure random tokens (`secrets.token_urlsafe`) and stored Argon2-hashed copies in the database.
* **Token Rotation (`POST /api/v1/auth/refresh`):** Implemented refresh token rotation; every refresh request revokes the existing token and generates a brand-new access and refresh token pair.
* **Session Revocation / Logout (`POST /api/v1/auth/logout`):** Allows users to securely invalidate refresh tokens upon logging out.

### Day 8 — Role-Based Access Control (RBAC) & Project Authorization
* **Role Verification Dependency:** Implemented `require_roles(*allowed_roles)` in `app/dependencies/authorization.py` to enforce role permissions across endpoints.
* **Route Protection:** Restricted project listing (`GET /api/v1/projects`) exclusively to `admin` and `manager` roles.
* **Granular Project Access Control (`require_project_access`):**
  * `admin` role has unrestricted access across all projects.
  * `manager` role is validated to ensure they are designated as `PROJECT_MANAGER` for that project.
  * Standard members are checked against the `project_members` repository to ensure membership.
  * Unauthorized requests are rejected with `HTTP 403 Forbidden`.

### Day 9 — Validation, Filtering, Pagination, Search & Sorting
* **Task Priority & Schema Migration:** Added `priority` (`low`, `medium`, `high`, `urgent`) to the `Task` model and ran Alembic migration `8fc07d24f988_add_task_priority.py`.
* **Validation & Schemas Clean-up:** Enforced strict Pydantic validation on create, update, and response schemas. Protected sensitive fields (`id`, `project_id`, `role`, `is_active`, `created_at`) from user mutation.
* **Production-Style Pagination:** Implemented generic `PaginatedResponse[T]` supporting query parameters `?page=1&page_size=20` (capped at max 100) returning `items`, `total`, `page`, `page_size`, and `total_pages`.
* **Dynamic Multi-Field Filtering:** Added filter support for `?status=`, `?priority=`, and `?assigned_to=` with dynamic query building.
* **Search Capabilities:** Implemented case-insensitive search (`?search=`) across task title and description using SQLAlchemy `ilike` and `or_`.
* **Sorting & Whitelist Security:** Supported `?sort_by=` and `?sort_order=asc|desc` with strict server-side whitelisting (`created_at`, `due_date`, `priority`, `status`, `title`, `id`) returning `HTTP 400 Bad Request` on invalid fields.

### Day 10 — Middleware, Logging & Global Exception Handlers
* **Request Tracing:** Integrated `RequestIDMiddleware` attaching a unique UUID `X-Request-ID` to every HTTP request and response for end-to-end observability.
* **Structured Request Logging:** Added `LoggingMiddleware` measuring latency, tracking HTTP verbs, paths, and status codes.
* **Global Error Sanitization:** Centralized exception handlers for `AppException`, `StarletteHTTPException`, `RequestValidationError`, and `Exception` returning standardized error envelopes while concealing internal stack traces in production.

### Day 11 — Testing & Test Database Automation
* **Pytest Setup:** Configured `pytest` and `pytest-asyncio` with dedicated test database sessions and isolation.
* **Integration Tests:** Covered full user lifecycles (registration, login, token refresh, RBAC enforcement, project creation, task management, and comment workflows).

### Day 12 — Query Optimization & Performance
* **Relational Performance:** Added database indexes on foreign keys (`project_id`, `user_id`, `task_id`) and search columns (`status`, `priority`).
* **Optimized Aggregations:** Tuned project summary queries to execute optimized single-roundtrip aggregation queries.

### Day 13 — OWASP API Security Top 10 (Part 1: API1–API5)
* **API1 (BOLA):** Object-level ownership checks preventing cross-tenant project and task access.
* **API2 (Broken Auth):** Strong Argon2id password hashing, short-lived JWT access tokens (15m), and rotating refresh tokens.
* **API3 (BOPLA):** Prevented mass-assignment vulnerabilities using strict DTO schemas and `ConfigDict(extra='forbid')`.
* **API4 (Resource Consumption):** Hard limits on pagination (`max 100`), bounded string query lengths, and request rate limiting considerations.
* **API5 (BFLA):** Enforced function-level authorization via `require_roles("admin")` on destructive operations.

### Day 14 — OWASP API Security Top 10 (Part 2: API6–API10 & Documentation)
* **API6 (Sensitive Business Flows):** Protected critical flows (Login, Project Creation, Member Management, Role Mutation, Token Rotation) with strict authorization checks and anti-abuse safeguards.
* **API7 (SSRF Defense):** Built safe external HTTP request mechanisms with strict URL scheme validation, domain allowlists, and DNS resolution filtering against private networks (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`, and cloud metadata endpoints like `169.254.169.254`).
* **API8 (Security Misconfiguration):** Hardened production configurations (`DEBUG=false`, restricted CORS origins, HTTPS/HSTS enforcement, security headers `nosniff`, `DENY`, and zero stack trace leakages).
* **API9 (API Inventory):** Created comprehensive API catalog in `docs/api-inventory.md` documenting all endpoints, versioning (`/api/v1`), query parameters, and access roles.
* **API10 (Unsafe Consumption of External APIs):** Implemented `SafeAPIClient` featuring connect/read timeouts, enforced TLS certificate validation, response body size streaming caps (2MB), and Pydantic schema validation for untrusted external payloads.
* **Security Architecture Document:** Published comprehensive OWASP mapping and threat model in `docs/security.md`.

---

## 🛡️ OWASP API Security Top 10 Compliance Matrix

| OWASP Vulnerability | Risk / Vector | Implemented Mitigation |
| :--- | :--- | :--- |
| **API1: Broken Object Level Authorization (BOLA)** | Horizontal privilege escalation across projects | `require_project_access` dependency checks project membership on all project-scoped routes. |
| **API2: Broken Authentication** | Credential stuffing, weak tokens | Argon2id hashing, 15m JWT access tokens, cryptographic rotating refresh tokens. |
| **API3: Broken Object Property Level Authorization (BOPLA)** | Mass-assignment on sensitive fields | Strict Pydantic DTOs with `extra='forbid'`, protecting system fields (`id`, `role`, `created_at`). |
| **API4: Unrestricted Resource Consumption** | DoS via unbounded queries / payloads | Strict pagination (`page_size` max 100), bounded query lengths (`max_length=100`), 2MB body caps. |
| **API5: Broken Function Level Authorization (BFLA)** | Vertical privilege escalation | `require_roles("admin", "manager")` guards admin routes and destructive actions. |
| **API6: Unrestricted Access to Sensitive Business Flows** | Automated spamming & brute force | Role validation, anti-automation controls, and token reuse revocation on sensitive business flows. |
| **API7: Server-Side Request Forgery (SSRF)** | Attacks on localhost & cloud metadata (`169.254.169.254`) | Scheme validation, domain allowlisting, and DNS resolution filtering against private/cloud IP ranges. |
| **API8: Security Misconfiguration** | Stack trace leaks, open CORS, weak headers | Sanitized error handlers, strict CORS allowlist, security headers (`HSTS`, `nosniff`, `X-Frame-Options`). |
| **API9: Improper Inventory Management** | Shadow & undocumented endpoints | Strict versioning (`/api/v1`), automated OpenAPI schema generation, and `docs/api-inventory.md`. |
| **API10: Unsafe Consumption of APIs** | Blind trust in 3rd-party responses | `SafeAPIClient` with connect/read timeouts, mandatory TLS verification, 2MB size caps, and Pydantic parsing. |

---

## 🗄️ Database Relationships

* **Projects & Tasks:** One-to-Many (`Project` has many `Tasks`, `Task` belongs to one `Project`).
* **Users & Tasks:** One-to-Many (`User` can be assigned multiple `Tasks`).
* **Tasks & Comments:** One-to-Many (`Task` contains multiple `Comments`).
* **Users & Comments:** One-to-Many (`User` can post multiple `Comments`).
* **Projects & Users (Members):** Many-to-Many via `project_members` junction table with roles (`PROJECT_MANAGER`, `MEMBER`).
* **Users & Refresh Tokens:** One-to-Many (`User` can have active and revoked session `RefreshTokens`).

---

## 📡 API Endpoints Overview (`/api/v1`)

### 🔐 Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/register` | Register a new user account | Public |
| `POST` | `/api/v1/auth/login` | Authenticate user & issue token pair | Public |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile | Bearer Token |
| `POST` | `/api/v1/auth/refresh` | Rotate and issue a new token pair | Refresh Token |
| `POST` | `/api/v1/auth/logout` | Revoke active refresh token | Refresh Token |

### 📁 Projects (`/api/v1/projects`)
| Method | Endpoint | Description | Access / RBAC |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/projects` | List all projects | Admin, Manager |
| `POST` | `/api/v1/projects` | Create a new project | Admin, Manager |
| `GET` | `/api/v1/projects/{project_id}` | Retrieve project details | Project Member / Admin |
| `PATCH` | `/api/v1/projects/{project_id}` | Update project metadata | Project Manager / Admin |
| `DELETE` | `/api/v1/projects/{project_id}` | Delete a project | Admin Only |
| `GET` | `/api/v1/projects/{project_id}/summary` | Aggregate project statistics | Project Member / Admin |

### 👥 Project Members (`/api/v1/projects/{project_id}/members`)
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/projects/{project_id}/members` | List all members in a project | Project Member / Admin |
| `POST` | `/api/v1/projects/{project_id}/members` | Assign a user to a project | Project Manager / Admin |
| `DELETE` | `/api/v1/projects/{project_id}/members/{user_id}` | Remove user from project | Project Manager / Admin |

### ✅ Tasks (`/api/v1/projects/{project_id}/tasks`)
| Method | Endpoint | Description | Query Parameters / Features |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/projects/{project_id}/tasks` | Get paginated, filtered, searchable & sorted tasks | `page`, `page_size`, `status`, `priority`, `assigned_to`, `search`, `sort_by`, `sort_order` |
| `POST` | `/api/v1/projects/{project_id}/tasks` | Create task inside project (with priority) | Body: `TaskCreate` |
| `GET` | `/api/v1/projects/{project_id}/tasks/{task_id}` | Retrieve specific task details | Project Member / Admin |

### 💬 Comments (`/api/v1/projects/{project_id}/tasks/{task_id}/comments`)
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/projects/{project_id}/tasks/{task_id}/comments` | List comments on a task | Project Member / Admin |
| `POST` | `/api/v1/projects/{project_id}/tasks/{task_id}/comments` | Post a comment to a task | Project Member / Admin |

---

## 📂 Project Structure

```text
team-project-api/
│
├── app/
│   ├── core/
│   │   ├── security.py                # Password hashing, JWT creation/verification, token utils
│   │   ├── security_headers.py        # OWASP Security headers middleware
│   │   ├── external_api_client.py     # API10 Safe HTTP Client with timeouts & TLS validation
│   │   ├── middleware.py              # RequestID & structured logging middlewares
│   │   ├── error_handlers.py          # Centralized error handlers & trace sanitization
│   │   └── exceptions.py              # Custom application exception hierarchy
│   │
│   ├── db/
│   │   ├── base.py                    # SQLAlchemy Base declaration
│   │   ├── session.py                 # Engine & SessionLocal configuration
│   │   └── seed.py                    # Database seeding script
│   │
│   ├── dependencies/
│   │   └── authorization.py           # Role checking (RBAC) & project access dependencies
│   │
│   ├── models/
│   │   ├── project.py                 # Project ORM model
│   │   ├── user.py                    # User ORM model
│   │   ├── task.py                    # Task ORM model (with priority)
│   │   ├── comment.py                 # Comment ORM model
│   │   ├── project_member.py          # ProjectMember junction model
│   │   └── refresh_token.py           # RefreshToken ORM model
│   │
│   ├── repositories/
│   │   ├── project_repository.py      # Project DB queries
│   │   ├── task_repository.py         # Task DB queries (pagination, filters, search, sorting)
│   │   ├── comment_repository.py      # Comment DB queries
│   │   ├── project_member_repository.py # Project membership DB queries
│   │   ├── project_summary_repository.py# Analytics & aggregation queries
│   │   ├── refresh_token_repository.py# Refresh token DB queries
│   │   └── user_repository.py         # User DB queries
│   │
│   ├── schemas/
│   │   ├── auth.py                    # Auth request & response schemas
│   │   ├── user.py                    # User safe response & update schemas
│   │   ├── project.py                 # Project Pydantic schemas
│   │   ├── task.py                    # Task Pydantic schemas (with priority)
│   │   ├── pagination.py              # Generic PaginatedResponse schema
│   │   ├── comment.py                 # Comment Pydantic schemas
│   │   ├── project_member.py          # Membership schemas
│   │   └── project_summary.py         # Project analytics response schema
│   │
│   ├── services/
│   │   ├── auth_service.py            # Registration, login, token rotation logic
│   │   ├── project_service.py         # Project business logic
│   │   ├── task_service.py            # Task business logic (validation, sorting whitelist)
│   │   ├── comment_service.py         # Comment business logic
│   │   ├── project_member_service.py  # Member assignment logic
│   │   ├── project_summary_service.py # Aggregation service
│   │   └── ssrf_safe_client.py        # API7 SSRF defense client with DNS & IP filtering
│   │
│   └── main.py                        # FastAPI application instance & routing
│
├── docs/
│   ├── api-inventory.md               # API9 Complete API Inventory & Route Catalog
│   └── security.md                    # Complete OWASP API Security Top 10 Documentation
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── conftest.py                    # Pytest database fixtures and test client
│   └── test_api.py                    # Unit and integration test suites
│
├── .env.example
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started Locally

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/Subhanulhaq935/team_project_api.git
cd team-project-api

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql+psycopg://<username>:<password>@<host>/<database>?sslmode=require

# JWT & Authentication
JWT_SECRET_KEY=your_super_secret_jwt_key_here_minimum_32_characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Allowed Origins
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000
```

### 3. Run Migrations & Start Server
```bash
# Apply migrations
alembic upgrade head

# Start FastAPI development server
uvicorn app.main:app --reload
```

Access Swagger UI at `http://127.0.0.1:8000/docs`.

### 4. Run Test Suite
```bash
# Run pytest test suite
pytest -v

# Run with test coverage report
pytest --cov=app --cov-report=term-missing
```
