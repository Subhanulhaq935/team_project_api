# 🚀 Team Project & Task Management REST API

A production-ready, relational REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy 2.0**, featuring robust JWT authentication, refresh token rotation, Role-Based Access Control (RBAC), structured middleware logging, standardized global error handling, and comprehensive unit and integration test suites with 75%+ coverage.

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
* **Data Validation:** Pydantic v2 (with `email-validator`)
* **Database:** PostgreSQL (Neon Serverless)
* **ORM:** SQLAlchemy 2.0
* **Database Driver:** psycopg
* **Database Migrations:** Alembic
* **Password Hashing:** Argon2id (`pwdlib[argon2]`)
* **Authentication & Authorization:** PyJWT (Access Tokens) & Cryptographic Refresh Tokens (`secrets`)
* **Middleware & Observability:** Custom `RequestIDMiddleware` (`X-Request-ID`), structured logging & CORS
* **Testing & Quality Assurance:** `pytest`, `pytest-cov`, `httpx` / `TestClient`, `unittest.mock`
* **Architecture:** Layered Architecture (Models, Repositories, Services, Schemas, Dependencies)

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
| **Day 9** | Advanced Querying: Pagination, Filtering, Sorting & Search | `✅ Complete` |
| **Day 10** | Middleware, Structured Logging & Standardized Error Handling | `✅ Complete` |
| **Day 11** | Unit Testing & Mocking (Pytest & Service Layer Isolation) | `✅ Complete` |
| **Day 12** | Integration & End-to-End API Testing (Separate Test DB & 76% Coverage) | `✅ Complete` |

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

### Day 9 — Advanced Querying: Filtering, Sorting, Pagination & Search
* Added multi-field task filtering (`status`, `priority`, `assigned_to`).
* Implemented case-insensitive text search across task titles and descriptions.
* Added dynamic multi-column sorting with configurable sort order (`asc` / `desc`).
* Implemented generic standard pagination metadata (`page`, `page_size`, `total_items`, `total_pages`).

### Day 10 — Middleware, Logging & Global Error Handling
* **Request ID Middleware:** Attached a unique `X-Request-ID` UUID to every incoming HTTP request and response header.
* **Structured Logging Middleware:** Logs method, path, HTTP status, request duration, and user ID.
* **Standardized Exception Handlers:** Centralized error response format across validation errors (`422`), custom application exceptions (`400`, `401`, `403`, `404`, `409`), and uncaught internal server errors (`500`).

### Day 11 — Unit Testing & Mocking
* Implemented isolated unit test suites using `pytest` and `unittest.mock`.
* Mocked database sessions and repositories to thoroughly test core business logic in service layers (`auth_service`, `project_service`, `task_service`, `project_member_service`).

### Day 12 — Integration & End-to-End API Testing
* **Isolated Test Database:** Configured independent test database runner ensuring test executions never touch Development or Production databases.
* **FastAPI Test Client (`HTTPX`):** Configured automated test fixtures with FastAPI `TestClient` overriding `get_db`.
* **Complete E2E Lifecycle Testing:**
  $$\text{Register} \longrightarrow \text{Login} \longrightarrow \text{Create Project} \longrightarrow \text{Add Member} \longrightarrow \text{Create Task} \longrightarrow \text{Add Comment} \longrightarrow \text{Get Project Summary}$$
* **Status Code Coverage:** Validated HTTP status codes `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, and `422 Unprocessable Content`.
* **Coverage:** Achieved **76%+ code coverage** across the application.

---

## 🧪 Testing & Code Coverage

### Run Full Test Suite
```bash
pytest
```

### Run Integration Tests Only
```bash
pytest tests/integration -v
```

### Run Tests with Coverage Report
```bash
pytest --cov=app --cov-report=term-missing
```

```text
---------- coverage: platform win32, python 3.13.13 ----------
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
app\core\error_handlers.py                          30      2    93%
app\core\exceptions.py                              28      1    96%
app\core\middleware.py                              36      2    94%
app\core\security.py                                53      8    85%
app\db\base.py                                       3      0   100%
app\db\session.py                                   13      4    69%
app\dependencies\authorization.py                   23     10    57%
app\main.py                                        142     37    74%
app\models\comment.py                               12      0   100%
app\models\project.py                               15      0   100%
app\models\project_member.py                        12      0   100%
app\models\refresh_token.py                         12      0   100%
app\models\task.py                                  16      0   100%
app\models\user.py                                  15      0   100%
app\repositories\comment_repository.py              12      3    75%
app\repositories\project_member_repository.py       19      5    74%
app\repositories\project_repository.py              22      8    64%
app\repositories\project_summary_repository.py      13      0   100%
app\repositories\refresh_token_repository.py        16      5    69%
app\repositories\task_repository.py                 39     23    41%
app\repositories\user_repository.py                 16      0   100%
app\schemas\auth.py                                 19      0   100%
app\schemas\comment.py                              12      0   100%
app\schemas\pagination.py                            9      0   100%
app\schemas\project.py                              16      0   100%
app\schemas\project_member.py                       12      0   100%
app\schemas\project_summary.py                      10      0   100%
app\schemas\task.py                                 31      0   100%
app\services\auth_service.py                        63     33    48%
app\services\comment_service.py                     20      7    65%
app\services\project_member_service.py              28      9    68%
app\services\project_service.py                     45     20    56%
app\services\project_summary_service.py              9      1    89%
app\services\task_service.py                        52     35    33%
--------------------------------------------------------------------
TOTAL                                              873    213    76%
```

---

## 🗄️ Database Relationships

* **Projects & Tasks:** One-to-Many (`Project` has many `Tasks`, `Task` belongs to one `Project`).
* **Users & Tasks:** One-to-Many (`User` can be assigned multiple `Tasks`).
* **Tasks & Comments:** One-to-Many (`Task` contains multiple `Comments`).
* **Users & Comments:** One-to-Many (`User` can post multiple `Comments`).
* **Projects & Users (Members):** Many-to-Many via `project_members` junction table with roles (`PROJECT_MANAGER`, `MEMBER`).
* **Users & Refresh Tokens:** One-to-Many (`User` can have active and revoked session `RefreshTokens`).

---

## 📡 API Endpoints Overview

### 🔐 Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/register` | Register a new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate user & issue tokens | No |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile | Bearer Token |
| `POST` | `/api/v1/auth/refresh` | Rotate and issue a new token pair | Refresh Token |
| `POST` | `/api/v1/auth/logout` | Revoke active refresh token | Refresh Token |

### 📁 Projects (`/api/v1/projects`)
| Method | Endpoint | Description | Access / RBAC |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/projects` | List all projects | Admin, Manager |
| `POST` | `/api/v1/projects` | Create a new project | Public / System |
| `GET` | `/api/v1/projects/{project_id}` | Retrieve project details | Project Members / Admin |
| `PATCH` | `/api/v1/projects/{project_id}` | Update project metadata | Public / System |
| `DELETE` | `/api/v1/projects/{project_id}` | Delete a project | Public / System |
| `GET` | `/api/v1/projects/{project_id}/summary` | Aggregate project statistics | Public / System |

### 👥 Project Members (`/api/v1/projects/{project_id}/members`)
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/projects/{project_id}/members` | List all members in a project | Public / System |
| `POST` | `/api/v1/projects/{project_id}/members` | Assign a user to a project | Public / System |
| `DELETE` | `/api/v1/projects/{project_id}/members/{user_id}` | Remove user from project | Public / System |

### ✅ Tasks (`/api/v1/projects/{project_id}/tasks`)
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/projects/{project_id}/tasks` | Get all tasks for a project (Filter, Sort, Search, Paginate) | Public / System |
| `POST` | `/api/v1/projects/{project_id}/tasks` | Create task inside project | Public / System |
| `GET` | `/api/v1/projects/{project_id}/tasks/{task_id}` | Retrieve specific task | Public / System |

### 💬 Comments (`/api/v1/projects/{project_id}/tasks/{task_id}/comments`)
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/projects/{project_id}/tasks/{task_id}/comments` | List comments on a task | Public / System |
| `POST` | `/api/v1/projects/{project_id}/tasks/{task_id}/comments` | Post a comment to a task | Public / System |

---

## ⚙️ Database Migrations & Management

### Useful Alembic Commands

```bash
# Generate a new migration automatically
alembic revision --autogenerate -m "migration_message"

# Apply all pending migrations
alembic upgrade head

# Roll back the last migration
alembic downgrade -1

# Inspect current database revision
alembic current

# View migration history
alembic history
```

---

## 📂 Project Structure

```text
team-project-api/
│
├── app/
│   ├── core/
│   │   ├── error_handlers.py          # Global exception handlers
│   │   ├── exceptions.py              # Custom API exceptions
│   │   ├── middleware.py              # Request ID & logging middleware
│   │   └── security.py                # Password hashing, JWT creation/verification, token utils
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
│   │   ├── comment.py                 # Comment ORM model
│   │   ├── project.py                 # Project ORM model
│   │   ├── project_member.py          # ProjectMember junction model
│   │   ├── refresh_token.py           # RefreshToken ORM model
│   │   ├── task.py                    # Task ORM model
│   │   └── user.py                    # User ORM model
│   │
│   ├── repositories/
│   │   ├── comment_repository.py      # Comment DB queries
│   │   ├── project_member_repository.py # Project membership DB queries
│   │   ├── project_repository.py      # Project DB queries
│   │   ├── project_summary_repository.py# Analytics & aggregation queries
│   │   ├── refresh_token_repository.py# Refresh token DB queries
│   │   ├── task_repository.py         # Task DB queries
│   │   └── user_repository.py         # User DB queries
│   │
│   ├── schemas/
│   │   ├── auth.py                    # Auth request & response schemas
│   │   ├── comment.py                 # Comment Pydantic schemas
│   │   ├── pagination.py              # Generic pagination response schemas
│   │   ├── project.py                 # Project Pydantic schemas
│   │   ├── project_member.py          # Membership schemas
│   │   ├── project_summary.py         # Project analytics response schema
│   │   └── task.py                    # Task Pydantic schemas
│   │
│   ├── services/
│   │   ├── auth_service.py            # Registration, login, token rotation logic
│   │   ├── comment_service.py         # Comment business logic
│   │   ├── project_member_service.py  # Member assignment logic
│   │   ├── project_service.py         # Project business logic
│   │   ├── project_summary_service.py # Aggregation service
│   │   └── task_service.py            # Task business logic
│   │
│   └── main.py                        # FastAPI application instance & routing
│
├── tests/
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_auth.py               # Integration tests for auth routes
│   │   ├── test_comments.py           # Integration tests for comments
│   │   ├── test_e2e_flow.py           # End-to-End full user & project workflow
│   │   ├── test_members.py            # Integration tests for project members
│   │   ├── test_projects.py           # Integration tests for project CRUD & RBAC
│   │   └── test_tasks.py              # Integration tests for task routes
│   │
│   ├── conftest.py                    # Mock fixtures & TestClient / DB session fixtures
│   ├── test_auth_service.py           # Service unit tests
│   ├── test_project_member_service.py # Member service unit tests
│   ├── test_project_service.py        # Project service unit tests
│   └── test_task_service.py           # Task service unit tests
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
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
cd team_project_api

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
DATABASE_URL=postgresql+psycopg://<username>:<password>@<host>/<database>?sslmode=require
TEST_DATABASE_URL=sqlite:///:memory:
JWT_SECRET_KEY=your_super_secret_jwt_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
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
