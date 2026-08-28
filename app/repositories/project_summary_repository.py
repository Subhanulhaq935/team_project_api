from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember
from app.models.task import Task
from app.models.comment import Comment


def get_project_statistics(
    db: Session,
    project_id: int
):
    total_members = db.scalar(
        select(func.count(ProjectMember.id))
        .where(ProjectMember.project_id == project_id)
    )

    total_tasks = db.scalar(
        select(func.count(Task.id))
        .where(Task.project_id == project_id)
    )

    pending_tasks = db.scalar(
        select(func.count(Task.id))
        .where(
            Task.project_id == project_id,
            Task.status == "pending"
        )
    )

    in_progress_tasks = db.scalar(
        select(func.count(Task.id))
        .where(
            Task.project_id == project_id,
            Task.status == "in_progress"
        )
    )

    completed_tasks = db.scalar(
        select(func.count(Task.id))
        .where(
            Task.project_id == project_id,
            Task.status == "completed"
        )
    )

    total_comments = db.scalar(
        select(func.count(Comment.id))
        .join(Task, Comment.task_id == Task.id)
        .where(Task.project_id == project_id)
    )

    return {
        "total_members": total_members or 0,
        "total_tasks": total_tasks or 0,
        "todo_tasks": pending_tasks or 0,
        "in_progress_tasks": in_progress_tasks or 0,
        "completed_tasks": completed_tasks or 0,
        "total_comments": total_comments or 0
    }