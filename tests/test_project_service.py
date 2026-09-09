from unittest.mock import patch

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services import project_service


# Test 1: Successful Project Creation
@patch("app.services.project_service.project_repository.create_project")
@patch("app.services.project_service.user_repository.get_user_by_id")
def test_create_project(mock_get_user, mock_create_project, mock_db):
    # Arrange: Mock user exists
    mock_get_user.return_value = User(id=1, email="admin@example.com")

    def side_effect(db, project):
        project.id = 100
        return project

    mock_create_project.side_effect = side_effect

    payload = ProjectCreate(
        name="Team Management System",
        description="Internal project tracking tool",
        status="ACTIVE",
        user_id=1,
    )

    # Act
    result = project_service.create_project(mock_db, payload)

    # Assert
    assert result is not None
    assert result.name == "Team Management System"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


# Test 2: Project Creation with Invalid / Non-existent User
@patch("app.services.project_service.user_repository.get_user_by_id")
def test_create_project_invalid_user(mock_get_user, mock_db):
    # Arrange: User not found in DB
    mock_get_user.return_value = None

    payload = ProjectCreate(
        name="Ghost Project",
        description="Created by non-existent user",
        status="ACTIVE",
        user_id=999,
    )

    # Act
    result = project_service.create_project(mock_db, payload)

    # Assert
    assert result is None
    mock_db.commit.assert_not_called()


# Test 3: Get Project by ID (Not Found)
@patch("app.services.project_service.project_repository.get_project_by_id")
def test_get_project_not_found(mock_get_project, mock_db):
    mock_get_project.return_value = None

    result = project_service.get_project_by_id(mock_db, project_id=999)

    assert result is None


# Test 4: Update Project Success
@patch("app.services.project_service.project_repository.update_project")
@patch("app.services.project_service.project_repository.get_project_by_id")
def test_update_project_success(mock_get_project, mock_update_project, mock_db):
    fake_project = Project(id=1, name="Old Name", description="Old Desc", status="ACTIVE")
    mock_get_project.return_value = fake_project
    mock_update_project.return_value = fake_project

    update_payload = ProjectUpdate(name="New Awesome Name")
    result = project_service.update_project(mock_db, project_id=1, project_data=update_payload)

    assert result is not None
    assert result.name == "New Awesome Name"
    mock_update_project.assert_called_once()
