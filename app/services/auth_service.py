from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, user_data: RegisterRequest):

    # Check if email already exists
    existing_user = user_repository.get_user_by_email(
        db,
        user_data.email
    )

    if existing_user is not None:
        return "already_exists"

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create User object
    user = User(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        email=user_data.email,
        password_hash=hashed_password
    )

    return user_repository.create_user(db, user)


def login_user(db: Session, user_data: LoginRequest):

    # Find user by email
    user = user_repository.get_user_by_email(
        db,
        user_data.email
    )

    if user is None:
        return None

    # Verify password
    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        return None

    # Create JWT
    access_token = create_access_token(
        user.id,
        user.role
    )

    return access_token