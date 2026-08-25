from pydantic import BaseModel, Field, ConfigDict
# Pydantic Schema for creating a project
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3 , max_length=100)
    description: str | None = Field(None, max_length=500)
    status: str = "active"


# Pydantic Schema for updating a project
class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=3 , max_length=100)
    description: str | None = Field(None, max_length=500)
    status: str | None = None

# Pydantic Schema for returning a project
class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    status: str
