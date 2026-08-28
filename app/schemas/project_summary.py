from pydantic import BaseModel


class ProjectStatistics(BaseModel):
    total_members: int
    total_tasks: int
    todo_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    total_comments: int


class ProjectSummaryResponse(BaseModel):
    statistics: ProjectStatistics