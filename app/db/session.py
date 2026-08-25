from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:Subhan%40935@localhost:5432/team_project_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    autocommit = False
)