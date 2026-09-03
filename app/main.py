from fastapi import FastAPI , status , HTTPException , Depends , Query
from app.db.base import Base
from app.db.session import engine, get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate , ProjectUpdate , ProjectResponse
from app.services import project_service
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse
from app.services import task_service
from app.models.user import User
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse
from app.services import comment_service
from app.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberResponse
)
from app.services import project_member_service
from app.schemas.project_summary import ProjectSummaryResponse
from app.services import project_summary_service
from app.schemas.auth import RegisterRequest
from app.services import auth_service
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth import RefreshTokenRequest, RefreshTokenResponse
from app.schemas.auth import RefreshTokenRequest
from app.dependencies.authorization import require_roles , require_project_access
from app.schemas.pagination import PaginatedResponse
from typing import Literal

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Get all projects
@app.get("/api/v1/projects", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "manager"))
):
    return project_service.get_projects(db)

# Get project by id
@app.get(
    "/api/v1/projects/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_project_access)
):
    project = project_service.get_project_by_id(
        db,
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project

# Create a new Project

@app.post("/api/v1/projects" , status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
def create_project(project: ProjectCreate , db : Session = Depends(get_db)):
    return project_service.create_project(db , project)
    

# Update a project
@app.patch("/api/v1/projects/{project_id}" , response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate , db : Session = Depends(get_db)):
    updated_project = project_service.update_project(db , project_id , project)

    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return updated_project
    

# Delete a project

@app.delete("/api/v1/projects/{project_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int , db : Session = Depends(get_db)):
    delete = project_service.delete_project(db , project_id)

    if delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return None


# Task routes

# Get all tasks of a project (Paginated, Filtered, Searchable & Sorted)
@app.get(
    "/api/v1/projects/{project_id}/tasks",
    response_model=PaginatedResponse[TaskResponse]
)
def get_tasks(
    project_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    status: str | None = Query(None, description="Filter by status (e.g. pending, completed)"),
    priority: str | None = Query(None, description="Filter by priority (e.g. low, medium, high, urgent)"),
    assigned_to: int | None = Query(None, description="Filter by assigned user ID"),
    search: str | None = Query(None, description="Search by title or description"),
    sort_by: str = Query("created_at", description="Sort by field (created_at, due_date, priority, status, title, id)"),
    sort_order: Literal["asc", "desc"] = Query("desc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db)
):
    try:
        return task_service.get_tasks_by_project(
            db=db,
            project_id=project_id,
            page=page,
            page_size=page_size,
            status=status,
            priority=priority,
            assigned_to=assigned_to,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



# Create a task inside a project
@app.post(
    "/api/v1/projects/{project_id}/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def create_task(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    return task_service.create_task(db, project_id, task)


# Get a specific task of a project
@app.get(
    "/api/v1/projects/{project_id}/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db)
):
    task = task_service.get_task_by_id(
        db,
        project_id,
        task_id
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found in this project"
        )

    return task

# Comments Routes

# Get comments of a task
@app.get(
    "/api/v1/projects/{project_id}/tasks/{task_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db)
):
    comments = comment_service.get_comments_by_task(
        db,
        project_id,
        task_id
    )

    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found in this project"
        )

    return comments


# Create comment on a task
@app.post(
    "/api/v1/projects/{project_id}/tasks/{task_id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse
)
def create_comment(
    project_id: int,
    task_id: int,
    user_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    created_comment = comment_service.create_comment(
        db,
        project_id,
        task_id,
        user_id,
        comment
    )

    if created_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found in this project"
        )

    return created_comment

# Project Member Routes

# Get all members of a project
@app.get(
    "/api/v1/projects/{project_id}/members",
    response_model=list[ProjectMemberResponse]
)
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db)
):
    members = project_member_service.get_project_members(
        db,
        project_id
    )

    if members is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return members


# Add member to project
@app.post(
    "/api/v1/projects/{project_id}/members",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectMemberResponse
)
def add_project_member(
    project_id: int,
    member: ProjectMemberCreate,
    db: Session = Depends(get_db)
):
    result = project_member_service.add_project_member(
        db,
        project_id,
        member
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or user not found"
        )

    if result == "already_exists":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this project"
        )

    return result


# Remove member from project
@app.delete(
    "/api/v1/projects/{project_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_project_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    result = project_member_service.remove_project_member(
        db,
        project_id,
        user_id
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project member not found"
        )

    return None

# Project Summary Routes
# Project Summary Route

@app.get(
    "/api/v1/projects/{project_id}/summary",
    response_model=ProjectSummaryResponse
)
def get_project_summary(
    project_id: int,
    db: Session = Depends(get_db)
):
    summary = project_summary_service.get_project_summary(
        db,
        project_id
    )

    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return summary

# Authentication Routes
@app.post("/api/v1/auth/register", status_code=201)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    result = auth_service.register_user(db, user_data)

    if result == "already_exists":
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return {
        "message": "User registered successfully",
        "user_id": result.id
    }

@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(
    user_data: LoginRequest,
    db: Session = Depends(get_db)
):
    result = auth_service.login_user(db, user_data)

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "token_type": "bearer"
    }

# Protected Route

@app.get("/api/v1/auth/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }

# Refresh Token Route

@app.post(
    "/api/v1/auth/refresh",
    response_model=RefreshTokenResponse
)
def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    result = auth_service.refresh_access_token(
        db,
        token_data.refresh_token
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "token_type": "bearer"
    }

@app.post("/api/v1/auth/logout")
def logout(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    result = auth_service.logout_user(
        db,
        token_data.refresh_token
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    return {
        "message": "Logged out successfully"
    }