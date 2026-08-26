from datetime import datetime
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped , mapped_column

from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100) , nullable=False)
    client_name: Mapped[str | None] = mapped_column(String(100),nullable=True)
    description: Mapped[str | None] = mapped_column(Text , nullable=True)
    status: Mapped[str] = mapped_column(String(50) , default="active")

    start_date:Mapped[datetime | None] = mapped_column(DateTime , nullable=True)
    end_date:Mapped[datetime | None] = mapped_column(DateTime , nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime , default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime , default=datetime.utcnow , onupdate=datetime.utcnow)
    