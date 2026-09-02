from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories import project_member_repository


def require_roles(*allowed_roles: str):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role.lower() not in [
            role.lower() for role in allowed_roles
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_user

    return role_checker


def require_project_access(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ADMIN can access every project
    if current_user.role.lower() == "admin":
        return current_user

    # Check whether user belongs to this project
    project_member = project_member_repository.get_project_member(
        db,
        project_id,
        current_user.id
    )

    # User is not a member of this project
    if project_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project"
        )

    # MANAGER can access only projects they manage
    if current_user.role.lower() == "manager":
        if project_member.project_role != "PROJECT_MANAGER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the manager of this project"
            )

    return current_user