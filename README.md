# 🚀 Team Project & Task Management REST API

---

## 📌 Live Demo & API Documentation

* **Interactive Swagger UI:** [team-project-api-eakc.onrender.com/docs](https://team-project-api-eakc.onrender.com/docs#/)
* **Local Swagger UI:** `http://127.0.0.1:8000/docs`
* **Local OpenAPI JSON:** `http://127.0.0.1:8000/openapi.json`

---

## 🛠️ Tech Stack

* **Language:** Python 3.13
* **Framework:** FastAPI
* **ASGI Server:** Uvicorn
* **Data Validation:** Pydantic
* **Database:** PostgreSQL (Neon Serverless)
* **ORM:** SQLAlchemy 2.0
* **Driver:** psycopg
* **Database Migrations:** Alembic

---

## 📊 Development Progress

| Milestone | Key Focus Area | Status |
| :--- | :--- | :---: |
| **Day 1** | FastAPI & REST Fundamentals | `✅ Complete` |
| **Day 2** | PostgreSQL & SQLAlchemy Integration | `✅ Complete` |
| **Day 3** | Alembic Migrations & Database Seeding | `✅ Complete` |
| **Day 4** | Tasks, Comments & Relational Architecture | `✅ Complete` |

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
* Implemented the Repository and Service architectural pattern for business logic.
* Added relational integrity checks across Projects, Tasks, Users, and Comments.

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
* Implemented the Repository and Service architectural pattern for business logic.
* Added relational integrity checks across Projects, Tasks, Users, and Comments.

### Core Relationships

* **Projects & Tasks:** One-to-Many (`Project` has many `Tasks`, `Task` belongs to one `Project`).
* **Users & Tasks:** One-to-Many (`User` can be assigned multiple `Tasks`).
* **Tasks & Comments:** One-to-Many (`Task` contains multiple `Comments`).
* **Users & Comments:** One-to-Many (`User` can post multiple `Comments`).

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

## 📂 Project Structure

```text
team-project-api/
│
├── app/
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── seed.py
│   │
│   ├── models/
│   │   ├── project.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── comment.py
│   │
│   ├── repositories/
│   │   ├── project_repository.py
│   │   ├── task_repository.py
│   │   └── comment_repository.py
│   │
│   ├── schemas/
│   │   ├── project.py
│   │   ├── task.py
│   │   └── comment.py
│   │
│   ├── services/
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   └── comment_service.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   │   ├── 001_create_projects.py
│   │   ├── 002_create_users.py
│   │   ├── 003_add_client_name.py
│   │   └── add_tasks_and_comments.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── .env
└── README.md
