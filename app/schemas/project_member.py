from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectMemberCreate(BaseModel):
    user_id: int
    project_role: str = Field(..., min_length=1, max_length=50)


class ProjectMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    user_id: int
    project_role: str
    joined_at: datetime