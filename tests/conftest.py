import os
from unittest.mock import MagicMock
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

load_dotenv()

# ==========================================
# Unit Test Fixture (Mock Database)
# ==========================================
@pytest.fixture
def mock_db():
    """Mock SQLAlchemy Session fixture for unit tests."""
    db = MagicMock(spec=Session)
    return db


# ==========================================
# Integration Test Fixtures (Real/Test Database)
# ==========================================
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")

if "sqlite" in TEST_DATABASE_URL:
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture(scope="function")
def db_session():
    """Create fresh database tables for each integration test and drop them after."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def create_user(db_session):
    """Helper fixture to create authenticated users with custom roles (admin, manager, user)."""
    def _create_user(email: str = "admin@example.com", role: str = "manager", firstname: str = "Test", lastname: str = "User"):
        from app.models.user import User
        from app.core.security import hash_password, create_access_token
        user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password_hash=hash_password("Password123!"),
            role=role,
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        token = create_access_token(user_id=user.id, role=user.role)
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "token": token,
            "headers": {"Authorization": f"Bearer {token}"}
        }
    return _create_user
