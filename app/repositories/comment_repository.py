from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment import Comment


def get_comments_by_task(db: Session, task_id: int):
    statement = select(Comment).where(Comment.task_id == task_id)
    result = db.execute(statement)
    return result.scalars().all()


def create_comment(db: Session, comment: Comment):
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment