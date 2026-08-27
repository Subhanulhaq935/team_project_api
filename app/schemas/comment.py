from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CommentCreate(BaseModel):
    comment: str = Field(..., min_length=1, max_length=500)


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    user_id: int
    comment: str
    created_at: datetime
    updated_at: datetime