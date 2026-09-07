import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session


@pytest.fixture
def mock_db():
    """Mock SQLAlchemy Session fixture."""
    db = MagicMock(spec=Session)
    return db
