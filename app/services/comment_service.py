from sqlalchemy.orm import Session

from app.repositories import comment_repository
from app.repositories import task_repository
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


def get_comments_by_task(
    db: Session,
    project_id: int,
    task_id: int
):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        return None

    if task.project_id != project_id:
        return None

    return comment_repository.get_comments_by_task(db, task_id)


def create_comment(
    db: Session,
    project_id: int,
    task_id: int,
    user_id: int,
    comment_data: CommentCreate
):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        return None

    if task.project_id != project_id:
        return None

    comment = Comment(
        task_id=task_id,
        user_id=user_id,
        comment=comment_data.comment
    )

    return comment_repository.create_comment(db, comment)