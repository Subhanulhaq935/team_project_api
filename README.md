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

---
📊 Development ProgressMilestoneKey Focus AreaStatusDay 1FastAPI & REST Fundamentals✅ CompleteDay 2PostgreSQL & SQLAlchemy Integration✅ CompleteDay 3Alembic Migrations & Database Seeding✅ CompleteDay 4Tasks, Comments & Relational Architecture✅ Complete
---

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
