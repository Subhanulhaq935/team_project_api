# Team Project & Task Management REST API

A REST API built with **Python and FastAPI** for managing projects, tasks, users, and comments.

## Tech Stack

* Python 3.13
* FastAPI
* Uvicorn
* Pydantic
* PostgreSQL
* SQLAlchemy
* Alembic
* psycopg

---

# Day 1 — FastAPI & REST Fundamentals

## Technologies

* Python 3.13
* FastAPI
* Uvicorn
* Pydantic

## Implemented

* Health Check API
* Project CRUD APIs
* Pydantic request/response validation
* HTTP status codes
* REST API fundamentals
* Swagger UI
* OpenAPI documentation

## API Documentation

Swagger UI:

`http://127.0.0.1:8000/docs`

OpenAPI JSON:

`http://127.0.0.1:8000/openapi.json`

## Database

Day 1 used a temporary in-memory Python list for project data.

PostgreSQL and SQLAlchemy were introduced in Day 2.

---

# Day 2 — PostgreSQL & SQLAlchemy

## Technologies

* PostgreSQL
* SQLAlchemy 2.0
* psycopg
* Python dotenv

## Implemented

* PostgreSQL database connection
* SQLAlchemy Engine
* SQLAlchemy Session
* Declarative `Base`
* Project SQLAlchemy model
* PostgreSQL `projects` table
* CRUD operations using SQLAlchemy
* Environment variables using `.env`

## Project Model

The `projects` table contains:

* `id`
* `name`
* `description`
* `status`
* `start_date`
* `end_date`
* `created_at`
* `updated_at`

---

# Day 3 — Alembic Migrations & Database Seeding

## Technologies

* Alembic
* PostgreSQL
* SQLAlchemy
* Neon PostgreSQL

## Implemented

* Initialized Alembic
* Configured Alembic with SQLAlchemy metadata
* Created version-controlled database migrations
* Added Users model
* Added Users table
* Added unique constraint on user email
* Added `client_name` to Projects through a separate migration
* Created database seed script
* Seeded Admin and Manager users
* Seeded initial projects
* Verified migration history
* Verified current migration HEAD

## Migrations

### 001 — Create Projects

Creates the `projects` table with project information and timestamps.

### 002 — Create Users

Creates the `users` table with:

* `id`
* `firstname`
* `lastname`
* `email`
* `password_hash`
* `role`
* `is_active`
* `created_at`
* `updated_at`

The email field has a unique constraint.

### 003 — Add Client Name

Adds the `client_name` column to the existing `projects` table.

## Migration Commands

Create a migration:

```bash
alembic revision --autogenerate -m "migration_message"
```

Apply migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

Rollback one migration:

```bash
alembic downgrade -1
```

## Database Seeding

Initial data can be inserted using:

```bash
python -m app.db.seed
```

The seed script creates:

* Admin user
* Manager user
* Initial projects

## Database Verification

The database was verified using PostgreSQL/Neon SQL queries.

Current tables:

* `alembic_version`
* `projects`
* `users`

---

# Project Progress

| Day   | Topic                        | Status     |
| ----- | ---------------------------- | ---------- |
| Day 1 | FastAPI & REST Fundamentals  | ✅ Complete |
| Day 2 | PostgreSQL & SQLAlchemy      | ✅ Complete |
| Day 3 | Alembic Migrations & Seeding | ✅ Complete |

---

# API Documentation

Swagger UI:

`http://127.0.0.1:8000/docs`

OpenAPI:

`http://127.0.0.1:8000/openapi.json`

---

# Repository Structure

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
│   │   └── user.py
│   │
│   └── ...
│
├── alembic/
│   ├── versions/
│   │   ├── 001_create_projects.py
│   │   ├── 002_create_users.py
│   │   └── 003_add_client_name.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── .env
└── README.md
```

> **Note:** `.env` contains local/database credentials and should not be committed to the repository.
