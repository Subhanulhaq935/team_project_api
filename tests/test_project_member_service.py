from unittest.mock import patch

from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.schemas.project_member import ProjectMemberCreate
from app.services import project_member_service


# Test 5: Successfully Assign Member to Project
@patch("app.services.project_member_service.project_member_repository.create_project_member")
@patch("app.services.project_member_service.project_member_repository.get_project_member")
@patch("app.services.project_member_service.user_repository.get_user_by_id")
@patch("app.services.project_member_service.project_repository.get_project_by_id")
def test_assign_member_success(
    mock_get_proj, mock_get_user, mock_get_member, mock_create_member, mock_db
):
    # Arrange
    mock_get_proj.return_value = Project(id=1, name="Backend API")
    mock_get_user.return_value = User(id=5, email="developer@example.com")
    mock_get_member.return_value = None  # Pehle se member nahi hai

    fake_member = ProjectMember(project_id=1, user_id=5, project_role="DEVELOPER")
    mock_create_member.return_value = fake_member

    payload = ProjectMemberCreate(user_id=5, project_role="DEVELOPER")

    # Act
    result = project_member_service.add_project_member(mock_db, project_id=1, member_data=payload)

    # Assert
    assert result == fake_member
    mock_create_member.assert_called_once()


# Test 6: Assign Member to Non-Existent Project
@patch("app.services.project_member_service.project_repository.get_project_by_id")
def test_invalid_project_member_project_not_found(mock_get_proj, mock_db):
    mock_get_proj.return_value = None

    payload = ProjectMemberCreate(user_id=5, project_role="DEVELOPER")
    result = project_member_service.add_project_member(mock_db, project_id=999, member_data=payload)

    assert result is None


# Test 7: Assign Non-Existent User to Project
@patch("app.services.project_member_service.user_repository.get_user_by_id")
@patch("app.services.project_member_service.project_repository.get_project_by_id")
def test_invalid_project_member_user_not_found(mock_get_proj, mock_get_user, mock_db):
    mock_get_proj.return_value = Project(id=1, name="Backend API")
    mock_get_user.return_value = None  # User not found

    payload = ProjectMemberCreate(user_id=999, project_role="DEVELOPER")
    result = project_member_service.add_project_member(mock_db, project_id=1, member_data=payload)

    assert result is None


# Test 8: Assign Member Who is Already a Member (Duplicate prevention)
@patch("app.services.project_member_service.project_member_repository.get_project_member")
@patch("app.services.project_member_service.user_repository.get_user_by_id")
@patch("app.services.project_member_service.project_repository.get_project_by_id")
def test_assign_member_already_exists(mock_get_proj, mock_get_user, mock_get_member, mock_db):
    mock_get_proj.return_value = Project(id=1, name="Backend API")
    mock_get_user.return_value = User(id=5, email="developer@example.com")
    mock_get_member.return_value = ProjectMember(project_id=1, user_id=5)  # Already exists!

    payload = ProjectMemberCreate(user_id=5, project_role="DEVELOPER")
    result = project_member_service.add_project_member(mock_db, project_id=1, member_data=payload)

    assert result == "already_exists"
