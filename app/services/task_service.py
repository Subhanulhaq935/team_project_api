import math
from sqlalchemy.orm import Session

from app.repositories import task_repository
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

from app.repositories.task_repository import SORT_FIELDS
ALLOWED_SORT_FIELDS = set(SORT_FIELDS.keys())



def get_tasks_by_project(
    db: Session,
    project_id: int,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    priority: str | None = None,
    assigned_to: int | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    # Whitelist validation
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise ValueError(
            f"Invalid sort field '{sort_by}'. Allowed fields: {', '.join(sorted(ALLOWED_SORT_FIELDS))}"
        )
    if sort_order.lower() not in ["asc", "desc"]:
        raise ValueError("Invalid sort order. Allowed values: 'asc', 'desc'")
    skip = (page - 1) * page_size
    items, total = task_repository.get_tasks_by_project(
        db,
        project_id=project_id,
        skip=skip,
        limit=page_size,
        status=status,
        priority=priority,
        assigned_to=assigned_to,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }



def get_task_by_id(db: Session, project_id: int, task_id: int):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        return None

    if task.project_id != project_id:
        return None

    return task


def create_task(db: Session, project_id: int, task_data: TaskCreate):
    task = Task(
        project_id=project_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        assigned_to_user_id=task_data.assigned_to_user_id,
        due_date=task_data.due_date
    )

    return task_repository.create_task(db, task)


def update_task(
    db: Session,
    project_id: int,
    task_id: int,
    task_data: TaskUpdate
):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        return None

    if task.project_id != project_id:
        return None

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.status is not None:
        task.status = task_data.status

    if task_data.priority is not None:
        task.priority = task_data.priority


    if task_data.assigned_to_user_id is not None:
        task.assigned_to_user_id = task_data.assigned_to_user_id

    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    return task_repository.update_task(db, task)


def delete_task(db: Session, project_id: int, task_id: int):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        return None

    if task.project_id != project_id:
        return None

    return task_repository.delete_task(db, task)