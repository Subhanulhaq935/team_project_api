from sqlalchemy import select, func , or_ , asc , desc
from sqlalchemy.orm import Session

from app.models.task import Task

# Whitelist allowed sort fields mapping to model columns
SORT_FIELDS = {
    "id": Task.id,
    "title": Task.title,
    "status": Task.status,
    "priority": Task.priority,
    "due_date": Task.due_date,
    "created_at": Task.created_at,
    "updated_at": Task.updated_at,
}


def get_tasks_by_project(
    db: Session,
    project_id: int,
    skip: int = 0,
    limit: int = 20,
    status: str | None = None,
    priority: str | None = None,
    assigned_to: int | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    # Base filter
    filters = [Task.project_id == project_id]
    if status:
        filters.append(func.lower(Task.status) == status.lower())
    if priority:
        filters.append(func.lower(Task.priority) == priority.lower())
    if assigned_to is not None:
        filters.append(Task.assigned_to_user_id == assigned_to)
    if search:
        search_pattern = f"%{search}%"
        filters.append(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )
    # 1. Total count query
    count_stmt = select(func.count(Task.id)).where(*filters)
    total = db.execute(count_stmt).scalar() or 0
    # 2. Sorting clause
    sort_column = SORT_FIELDS.get(sort_by, Task.created_at)
    order_func = asc if sort_order.lower() == "asc" else desc
    # 3. Paginated + Sorted items query
    statement = (
        select(Task)
        .where(*filters)
        .order_by(order_func(sort_column))
        .offset(skip)
        .limit(limit)
    )
    result = db.execute(statement)
    items = result.scalars().all()
    return items, total

def get_task_by_id(db: Session, task_id: int):
    statement = select(Task).where(Task.id == task_id)
    result = db.execute(statement)
    return result.scalars().one_or_none()


def create_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task):
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
