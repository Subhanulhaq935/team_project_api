from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

# Allowed statuses and priorities
TaskStatus = Literal["pending", "in_progress", "completed", "cancelled"]
TaskPriority = Literal["low", "medium", "high", "urgent"]


# Schema for creating a task
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str | None = Field(None, max_length=500)
    status: TaskStatus = "pending"
    priority: TaskPriority = "medium"
    assigned_to_user_id: int | None = None
    due_date: datetime | None = None


# Schema for updating a task (Protected fields like id, project_id, created_at excluded)
class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=200)
    description: str | None = Field(None, max_length=500)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assigned_to_user_id: int | None = None
    due_date: datetime | None = None


# Schema for returning a task
class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: str
    description: str | None
    status: str
    priority: str
    assigned_to_user_id: int | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
