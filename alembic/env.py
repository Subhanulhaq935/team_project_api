from logging.config import fileConfig
import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

from app.db.base import Base
from app.models.project import Project
from app.models.user import User
from app.models.task import Task
from app.models.comment import Comment

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = os.getenv("DATABASE_URL")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    database_url = os.getenv("DATABASE_URL")

    print("ALEMBIC DATABASE:", database_url)

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# --- Missing execution dispatch ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
