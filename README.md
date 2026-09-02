🚀 Team Project & Task Management REST API

A secure REST API for managing projects, tasks, comments, project
members, authentication, refresh tokens, and role-based project access.

📌 Live Demo & API Documentation

Interactive Swagger UI: Live Swagger
Docs

Local Swagger UI: http://127.0.0.1:8000/docs

Local OpenAPI JSON: http://127.0.0.1:8000/openapi.json

🛠️ Tech Stack

Technology           Purpose

Python 3.13      Programming language
FastAPI          REST API framework
Uvicorn          ASGI server
Pydantic v2      Request/response validation
PostgreSQL       Relational database
Neon             Serverless PostgreSQL hosting
SQLAlchemy 2.0   ORM and database interaction
psycopg          PostgreSQL database driver
Alembic          Database migrations
JWT              Access-token authentication
Argon2id         Password and refresh-token hashing

📊 Development Progress

Milestone           Key Focus Area                   Status

Day 1           FastAPI & REST                ✅ Complete
Fundamentals

Day 2           PostgreSQL &                  ✅ Complete
SQLAlchemy
Integration

Day 3           Alembic Migrations            ✅ Complete
& Database Seeding

Day 4           Tasks, Comments &             ✅ Complete
Relational
Architecture

Day 5           Many-to-Many,                 ✅ Complete
Project Members &
Transactions

Day 6           Authentication &              ✅ Complete
JWT Access Tokens

Day 7           Refresh Tokens,               ✅ Complete
Rotation & Logout

📅 Daily Milestones & Technical Log

Day 1 --- FastAPI & REST Fundamentals

Built the initial Health Check and CRUD endpoints for Projects.

Configured Pydantic request and response schemas.

Used standard HTTP status codes.

Set up automatic OpenAPI/Swagger documentation.

Used an in-memory store before database persistence.

Day 2 --- PostgreSQL & SQLAlchemy

Connected FastAPI with PostgreSQL using SQLAlchemy 2.0.

Configured the SQLAlchemy Engine and database Sessions.

Created the Declarative Base.

Created the Project database model.

Migrated CRUD operations from in-memory data to PostgreSQL queries.

Managed runtime configuration through environment variables.

Day 3 --- Alembic Migrations & Database Seeding

Initialized Alembic and connected it with SQLAlchemy metadata.

Created and applied database migrations.

Implemented the User model.

Added email uniqueness constraints.

Added database seeding for initial users and projects.

Learned how to use upgrade, downgrade, current, and history.

Day 4 --- Tasks, Comments & Relational Architecture

Added Task and Comment models.

Added Foreign Key constraints.

Implemented Project → Task → Comment relationships.

Built CRUD APIs for Tasks and Comments.

Implemented Repository → Service → API architecture.

Added relational integrity checks such as verifying that:

A Task belongs to the requested Project.

A Comment belongs to the requested Task.

Created and applied Alembic migrations for Tasks and Comments.

Core Relationships

Projects → Tasks: One-to-Many

Tasks → Comments: One-to-Many

Users → Tasks: One-to-Many

Users → Comments: One-to-Many

Day 5 --- Many-to-Many Relationships, Project Members & Transactions

Many-to-Many Architecture

Implemented a Many-to-Many relationship between Projects and
Users.

Created the project_members junction table.

Added a unique constraint on (project_id, user_id) to prevent
duplicate membership.

Project Membership Management

Added APIs to:

Add project members.

Get project members.

Remove project members.

Added project-level roles such as PROJECT_MANAGER and DEVELOPER.

Project Analytics

Built a Project Summary API.

Used SQL JOIN and aggregate functions such as COUNT.

Calculated project-level information including members, tasks, task
statuses, and comments.

Database Transactions

Used commit() to permanently save transactions.

Used rollback() to undo failed transactions.

Used flush() to send pending changes to the database and obtain
generated IDs before continuing within the same transaction.

Automatically assigned the project creator the PROJECT_MANAGER
role.

API Testing

Tested project member endpoints and relationship constraints using
Swagger UI.

Day 6 --- Authentication & JWT Access Tokens

Implemented user authentication.

Added password hashing using Argon2id.

Added login functionality.

Implemented JWT access tokens.

Added token expiration.

Added JWT claims such as:

sub

role

iat

exp

jti

Implemented get_current_user() dependency.

Protected authenticated endpoints using FastAPI dependencies.

Added checks for:

Invalid tokens.

Expired tokens.

Missing users.

Inactive users.

Authentication Flow

User Login
    ↓
Verify Email + Password
    ↓
Generate JWT Access Token
    ↓
Client sends Bearer Token
    ↓
get_current_user()
    ↓
Validate Token
    ↓
Find User
    ↓
Allow Protected Endpoint

Day 7 --- Refresh Tokens, Rotation & Logout

Created the refresh_tokens database table.

Stored refresh tokens securely as Argon2 hashes instead of plain
text.

Added refresh-token expiration.

Added token revocation.

Implemented refresh-token rotation.

Revoked the old refresh token when a new access/refresh token pair
was generated.

Implemented logout by revoking the refresh token.

Added database migration for refresh tokens.

Refresh Token Flow

Login
  ↓
Access Token + Refresh Token
  ↓
Access Token expires
  ↓
Send Refresh Token
  ↓
Verify stored token hash
  ↓
Revoke old refresh token
  ↓
Generate new Access Token + Refresh Token

Day 8 --- RBAC & Object-Level Authorization

Authentication vs Authorization

Authentication: Who is the user?

Authorization: What is the user allowed to do?

Role-Based Access Control (RBAC)

Implemented global roles:

ADMIN

MANAGER

USER

Created the reusable:

require_roles(...)

dependency for role-based authorization.

Example:

current_user: User = Depends(
    require_roles("admin", "manager")
)

This allows only Admin and Manager users to access the endpoint.

Object-Level / Resource-Level Authorization

Implemented:

require_project_access(...)

This checks access to a specific project, not just the user's global
role.

Rules:

ADMIN
→ Can access all projects

MANAGER
→ Can access only projects where
   project_role = PROJECT_MANAGER

USER
→ Can access only projects where
   they are a member

Authorization Flow

Request
   ↓
JWT Authentication
   ↓
Get Current User
   ↓
Check Global Role
   ↓
Check Project Membership
   ↓
Check Project-Level Role
   ↓
Allow / Reject Request

Unauthorized project access returns:

403 Forbidden

Security Testing

Tested the authorization rules through Swagger:

Admin accessing projects → ✅ Allowed

Manager accessing a managed project → ✅ Allowed

Manager accessing a project they do not manage → ❌ 403

User accessing a project they do not belong to → ❌ 403

🏗️ Application Architecture

The project follows a layered architecture:

API / Endpoint
      ↓
Service Layer
      ↓
Repository Layer
      ↓
SQLAlchemy Session
      ↓
PostgreSQL

API Layer

Responsible for:

Receiving HTTP requests.

Reading path/query/body parameters.

Dependency injection.

Authentication/authorization dependencies.

Returning HTTP responses.

Service Layer

Responsible for:

Business logic.

Validation.

Transactions.

Coordinating multiple repository operations.

Repository Layer

Responsible for:

Database queries.

Creating records.

Updating records.

Deleting records.

Fetching records.

Database Layer

Responsible for:

SQLAlchemy Engine.

Database Sessions.

Models.

PostgreSQL persistence.

🔐 Security Features

JWT-based authentication.

Argon2id password hashing.

Argon2id refresh-token hashing.

Access-token expiration.

Refresh-token expiration.

Refresh-token rotation.

Refresh-token revocation.

Logout token revocation.

Active/inactive user checks.

Role-based authorization.

Project-level authorization.

Unique project membership constraint.

🔗 Core Relationships

User
 ├── Tasks
 ├── Comments
 └── Project Members
          │
          ↓
       Projects
          │
          ↓
        Tasks
          │
          ↓
       Comments

Relationship Summary

Relationship      Type

Project → Tasks   One-to-Many
Task → Comments   One-to-Many
User → Tasks      One-to-Many
User → Comments   One-to-Many
Project ↔ User    Many-to-Many through project_members

📂 Project Structure

team-project-api/
│
├── app/
│   ├── core/
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── seed.py
│   │
│   ├── dependencies/
│   │   └── authorization.py
│   │
│   ├── models/
│   │   ├── project.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── comment.py
│   │   ├── project_member.py
│   │   └── refresh_token.py
│   │
│   ├── repositories/
│   │   ├── project_repository.py
│   │   ├── task_repository.py
│   │   ├── comment_repository.py
│   │   ├── project_member_repository.py
│   │   ├── user_repository.py
│   │   └── refresh_token_repository.py
│   │
│   ├── schemas/
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── comment.py
│   │   ├── user.py
│   │   └── auth.py
│   │
│   ├── services/
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   ├── comment_service.py
│   │   ├── project_member_service.py
│   │   └── auth_service.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   │   ├── 001_create_projects.py
│   │   ├── 002_create_users.py
│   │   ├── 003_add_client_name.py
│   │   ├── add_tasks_and_comments.py
│   │   └── refresh_token_migration.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── .env
├── requirements.txt
└── README.md

Migration filenames may differ depending on the revision history in
your local repository.

⚙️ Database Migrations & Management

Generate a Migration

alembic revision --autogenerate -m "migration_message"

Apply All Pending Migrations

alembic upgrade head

Roll Back the Last Migration

alembic downgrade -1

Check Current Revision

alembic current

View Migration History

alembic history

▶️ Running the Project Locally

1. Create and activate a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

2. Install dependencies

pip install -r requirements.txt

3. Configure environment variables

Create a .env file with the required database and security
configuration.

Example:

DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Do not commit .env or other secrets to GitHub.

4. Apply migrations

alembic upgrade head

5. Start the FastAPI server

uvicorn app.main:app --reload

6. Open Swagger UI

http://127.0.0.1:8000/docs

🧪 API Testing

The API can be tested through:

Swagger UI.

JWT Bearer authentication.

CRUD endpoints.

Project/member relationship endpoints.

Authentication endpoints.

Refresh-token endpoints.

RBAC and project-level authorization scenarios.

🌿 Git Branching Workflow

Development was organized using feature branches:

feature/day-1
feature/day-2
feature/day-3-alembic
feature/day-4-relationships
feature/day-5-many-to-many
feature/day-6-authentication
feature/day-7-refresh-tokens
feature/day-8-rbac
        ↓
   development
        ↓
      main

Each feature was developed and tested separately before being merged
into the main development branch.

🎯 Current Project Status

Days 1--8 completed successfully. ✅

The project currently includes:

RESTful Project APIs

PostgreSQL persistence

SQLAlchemy ORM

Alembic migrations

Tasks and Comments

Project/User relationships

Many-to-Many project membership

Transactions

JWT authentication

Password hashing

Refresh-token rotation

Logout/revocation

RBAC

Object-level project authorization

Swagger/OpenAPI documentation

👨‍💻 Project Goal

The goal of this project is to build a production-style FastAPI backend
while learning:

REST API development

Database design

SQLAlchemy

PostgreSQL

Alembic

Repository/Service architecture

Authentication

Authorization

JWT security

Transactions

Relational database design

Many-to-Many relationships

Object-level access control
