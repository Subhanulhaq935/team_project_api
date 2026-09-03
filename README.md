# 🚀 Team Project & Task Management REST API

A production-ready, relational REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy 2.0**, featuring robust JWT authentication, refresh token rotation, and granular Role-Based Access Control (RBAC).

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
| **Day 9** | Validation, Filtering, Pagination, Search & Sorting | `✅ Complete` |

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
| Method | Endpoint | Description | Query Parameters / Features |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/projects/{project_id}/tasks` | Get paginated, filtered, searchable & sorted tasks | `page`, `page_size`, `status`, `priority`, `assigned_to`, `search`, `sort_by`, `sort_order` |
| `POST` | `/api/v1/projects/{project_id}/tasks` | Create task inside project (with priority) | Body: `TaskCreate` |
| `GET` | `/api/v1/projects/{project_id}/tasks/{task_id}` | Retrieve specific task | - |

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
│   │   └── project_summary_service.py # Aggregation service
│   │
│   └── main.py                        # FastAPI application instance & routing
│
├── alembic/
│   ├── versions/
│   │   ├── 1b07815f2c08_001_create_projects.py
│   │   ├── a2dfe78749d3_002_create_users.py
│   │   ├── d00bc0b48ff3_003_add_client_name.py
│   │   ├── 92367f39c842_add_tasks_and_comments.py
│   │   ├── 6944abf37c78_add_project_members.py
│   │   ├── fc1d00a5b271_add_refresh_tokens.py
│   │   └── 8fc07d24f988_add_task_priority.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── .env.example
├── alembic.ini
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
JWT_SECRET_KEY=your_super_secret_jwt_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run Migrations & Start Server
```bash
# Apply migrations
alembic upgrade head

# Start FastAPI development server
uvicorn app.main:app --reload
```

Access Swagger UI at `http://127.0.0.1:8000/docs`.
