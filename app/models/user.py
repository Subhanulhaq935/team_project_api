from datetime import datetime
from sqlalchemy import String , DateTime , Boolean

from sqlalchemy.orm import Mapped , mapped_column

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname : Mapped[str] = mapped_column(String(50) , nullable=False)
    lastname : Mapped[str] = mapped_column(String(50) , nullable=False)

    email : Mapped[str] = mapped_column(
        String(100) , nullable=False , unique=True
    )

    password_hash : Mapped[str] = mapped_column(
        String(255) , nullable=False
    )

    role : Mapped[str] = mapped_column(
        String(50) , nullable=False , default="user"
    )

    is_active : Mapped[bool] = mapped_column(
        Boolean , nullable=False , default=True
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime , default=datetime.utcnow
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime , nullable=False , default=datetime.utcnow , onupdate=datetime.utcnow
    )