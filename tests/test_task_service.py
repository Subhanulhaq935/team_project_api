from unittest.mock import patch

import pytest

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services import task_service


# Test 9: Create Task Successfully
@patch("app.services.task_service.task_repository.create_task")
def test_create_task(mock_create_task, mock_db):
    fake_created_task = Task(
        id=10,
        project_id=1,
        title="Setup Auth System",
        description="Implement JWT tokens",
        status="pending",
        priority="high",
    )
    mock_create_task.return_value = fake_created_task

    payload = TaskCreate(
        title="Setup Auth System",
        description="Implement JWT tokens",
        status="pending",
        priority="high",
    )

    result = task_service.create_task(mock_db, project_id=1, task_data=payload)

    assert result is not None
    assert result.id == 10
    assert result.title == "Setup Auth System"
    mock_create_task.assert_called_once()


# Test 10: Task Status Change (pending -> in_progress -> completed)
@patch("app.services.task_service.task_repository.update_task")
@patch("app.services.task_service.task_repository.get_task_by_id")
def test_task_status_change(mock_get_task, mock_update_task, mock_db):
    fake_task = Task(id=10, project_id=1, title="Test Task", status="pending")
    mock_get_task.return_value = fake_task
    mock_update_task.return_value = fake_task

    # Status change to in_progress
    update_payload = TaskUpdate(status="in_progress")
    result = task_service.update_task(mock_db, project_id=1, task_id=10, task_data=update_payload)

    assert result is not None
    assert result.status == "in_progress"
    mock_update_task.assert_called_once()


# Test 11: Update Task When Task Does Not Exist
@patch("app.services.task_service.task_repository.get_task_by_id")
def test_task_not_found(mock_get_task, mock_db):
    mock_get_task.return_value = None

    update_payload = TaskUpdate(status="completed")
    result = task_service.update_task(mock_db, project_id=1, task_id=999, task_data=update_payload)

    assert result is None


# Test 12: Mismatched Project ID (Task belongs to another project)
@patch("app.services.task_service.task_repository.get_task_by_id")
def test_get_task_by_id_wrong_project(mock_get_task, mock_db):
    # Task belongs to Project 2
    fake_task = Task(id=5, project_id=2, title="Project 2 Task")
    mock_get_task.return_value = fake_task

    # Requesting task 5 under Project 1 should return None
    result = task_service.get_task_by_id(mock_db, project_id=1, task_id=5)

    assert result is None


# Test 13: Invalid Sort Field Validation
def test_task_sorting_invalid_field(mock_db):
    with pytest.raises(ValueError, match="Invalid sort field"):
        task_service.get_tasks_by_project(db=mock_db, project_id=1, sort_by="unsupported_column")
