from sqlalchemy.orm import Session

from app.repositories import task_repository
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks_by_project(db: Session, project_id: int):
    return task_repository.get_tasks_by_project(db, project_id)


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