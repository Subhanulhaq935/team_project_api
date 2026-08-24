from fastapi import FastAPI , status , HTTPException
from pydantic import BaseModel , Field

app = FastAPI()

# temporary database
projects = []

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
    id: int
    name: str
    description: str | None
    status: str

@app.get("/health")
def health():
    return {"status": "ok"}

# Get all projects
@app.get("/api/v1/projects" , response_model=list[ProjectResponse])
def get_projects():
    return projects

# Get project by id
@app.get("/api/v1/projects/{project_id}" , response_model=ProjectResponse)
def get_project(project_id :int):
    for project in projects:
        if project["id"] == project_id:
            return project

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Project not found"
    )

# Create a new Project

@app.post("/api/v1/projects" , status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
def create_project(project: ProjectCreate):
    new_project = {
        "id": len(projects) + 1,
        "name": project.name,
        "description": project.description,
        "status": project.status
    }

    projects.append(new_project)
    return new_project

# Update a project
@app.patch("/api/v1/projects/{project_id}" , response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate):
    for existing_project in projects:
        if existing_project["id"] == project_id:
            if project.name is not None:
                existing_project["name"] = project.name
            if project.description is not None:
                existing_project["description"] = project.description
            if project.status is not None:
                existing_project["status"] = project.status
            return existing_project

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found"
    )

# Delete a project

@app.delete("/api/v1/projects/{project_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            projects.remove(project)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found"
    )





