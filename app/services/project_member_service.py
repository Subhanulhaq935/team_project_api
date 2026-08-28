from sqlalchemy.orm import Session

from app.repositories import project_member_repository
from app.repositories import project_repository
from app.repositories import user_repository
from app.models.project_member import ProjectMember
from app.schemas.project_member import ProjectMemberCreate


def get_project_members(db: Session, project_id: int):
    project = project_repository.get_project_by_id(db, project_id)

    if project is None:
        return None

    return project_member_repository.get_project_members(db, project_id)


def add_project_member(
    db: Session,
    project_id: int,
    member_data: ProjectMemberCreate
):
    # Check project exists
    project = project_repository.get_project_by_id(db, project_id)

    if project is None:
        return None

    # Check user exists
    user = user_repository.get_user_by_id(db, member_data.user_id)

    if user is None:
        return None

    # Check user is not already a member
    existing_member = project_member_repository.get_project_member(
        db,
        project_id,
        member_data.user_id
    )

    if existing_member is not None:
        return "already_exists"

    member = ProjectMember(
        project_id=project_id,
        user_id=member_data.user_id,
        project_role=member_data.project_role
    )

    return project_member_repository.create_project_member(db, member)


def remove_project_member(
    db: Session,
    project_id: int,
    user_id: int
):
    member = project_member_repository.get_project_member(
        db,
        project_id,
        user_id
    )

    if member is None:
        return None

    return project_member_repository.delete_project_member(db, member)