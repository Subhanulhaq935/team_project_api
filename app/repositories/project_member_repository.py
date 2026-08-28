from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember


def get_project_members(
    db: Session,
    project_id: int
):
    statement = select(ProjectMember).where(
        ProjectMember.project_id == project_id
    )

    result = db.execute(statement)

    return result.scalars().all()


def get_project_member(
    db: Session,
    project_id: int,
    user_id: int
):
    statement = select(ProjectMember).where(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    )

    result = db.execute(statement)

    return result.scalars().one_or_none()


def create_project_member(
    db: Session,
    project_member: ProjectMember
):
    db.add(project_member)

    db.commit()

    db.refresh(project_member)

    return project_member


def delete_project_member(
    db: Session,
    project_member: ProjectMember
):
    db.delete(project_member)

    db.commit()