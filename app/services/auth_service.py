from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories import (
    user_repository,
    refresh_token_repository
)

from app.schemas.auth import RegisterRequest, LoginRequest

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    verify_refresh_token,
)


# ==========================================
# REGISTER
# ==========================================

def register_user(
    db: Session,
    user_data: RegisterRequest
):
    # Check if email already exists
    existing_user = user_repository.get_user_by_email(
        db,
        user_data.email
    )

    if existing_user is not None:
        return "already_exists"

    # Hash password
    hashed_password = hash_password(
        user_data.password
    )

    # Create user
    user = User(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        email=user_data.email,
        password_hash=hashed_password
    )

    return user_repository.create_user(
        db,
        user
    )


# ==========================================
# LOGIN
# ==========================================

def login_user(
    db: Session,
    user_data: LoginRequest
):
    # Find user
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

    # Create short-lived access token
    access_token = create_access_token(
        user.id,
        user.role
    )

    # Create refresh token
    refresh_token = create_user_refresh_token(
        db,
        user.id
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# ==========================================
# CREATE REFRESH TOKEN
# ==========================================

def create_user_refresh_token(
    db: Session,
    user_id: int
):
    # Generate random refresh token
    token = create_refresh_token()

    # Hash token before storing
    token_hash = hash_refresh_token(
        token
    )

    # Refresh token expires after 7 days
    expires_at = datetime.utcnow() + timedelta(days=7)

    # Save hashed token in database
    refresh_token_repository.create_refresh_token(
        db,
        user_id,
        token_hash,
        expires_at
    )

    # Return original token to client
    return token


# ==========================================
# REFRESH ACCESS TOKEN
# ==========================================

def refresh_access_token(
    db: Session,
    refresh_token: str
):
    # Get all active refresh tokens
    active_tokens = (
        refresh_token_repository
        .get_all_active_refresh_tokens(db)
    )

    # Find matching token
    stored_token = None

    for token_record in active_tokens:

        if verify_refresh_token(
            refresh_token,
            token_record.token_hash
        ):
            stored_token = token_record
            break

    # Token not found
    if stored_token is None:
        return None

    # Check expiration
    now = datetime.utcnow()

    if stored_token.expires_at < now:
        return None
    # Get user
    user = user_repository.get_user_by_id(
        db,
        stored_token.user_id
    )

    if user is None:
        return None

    # Check if user is active
    if not user.is_active:
        return None

    # Revoke old refresh token
    refresh_token_repository.revoke_refresh_token(
        db,
        stored_token
    )

    # Create new access token
    access_token = create_access_token(
        user.id,
        user.role
    )

    # Create new refresh token
    new_refresh_token = create_user_refresh_token(
        db,
        user.id
    )

    # Save changes
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }

def logout_user(
    db: Session,
    refresh_token: str
):
    # Get all active refresh tokens
    active_tokens = (
        refresh_token_repository
        .get_all_active_refresh_tokens(db)
    )

    # Find matching token
    stored_token = None

    for token_record in active_tokens:
        if verify_refresh_token(
            refresh_token,
            token_record.token_hash
        ):
            stored_token = token_record
            break

    # Token not found
    if stored_token is None:
        return False

    # Revoke refresh token
    refresh_token_repository.revoke_refresh_token(
        db,
        stored_token
    )

    db.commit()

    return True