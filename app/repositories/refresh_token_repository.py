from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


def create_refresh_token(
    db: Session,
    user_id: int,
    token_hash: str,
    expires_at: datetime
):
    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at
    )

    db.add(refresh_token)
    db.flush()

    return refresh_token


def get_all_active_refresh_tokens(
    db: Session
):
    result = db.execute(
        select(RefreshToken).where(
            RefreshToken.revoked_at.is_(None)
        )
    )

    return result.scalars().all()


def revoke_refresh_token(
    db: Session,
    refresh_token: RefreshToken
):
    refresh_token.revoked_at = datetime.now(timezone.utc)
    db.flush()

    return refresh_token