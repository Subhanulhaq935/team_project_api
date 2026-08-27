from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


def get_tasks_by_project(db: Session, project_id: int):
    statement = select(Task).where(Task.project_id == project_id)
    result = db.execute(statement)
    return result.scalars().all()

# we have to apply the validation... Dont only check the task_id exists check if the task belongs to the project
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