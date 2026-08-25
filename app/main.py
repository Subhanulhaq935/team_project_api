from fastapi import FastAPI , status , HTTPException , Depends
from app.db.base import Base
from app.db.session import engine , SessionLocal
from app.models.project import Project
from app.schemas.project import ProjectCreate , ProjectUpdate , ProjectResponse
from app.services import project_service
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

# Get all projects
@app.get("/api/v1/projects" , response_model=list[ProjectResponse])
def get_projects(db : Session = Depends(get_db)):
    return project_service.get_projects(db)

# Get project by id
@app.get("/api/v1/projects/{project_id}" , response_model=ProjectResponse)
def get_project(project_id :int , db : Session = Depends(get_db)):
    project = project_service.get_project_by_id(db , project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project

# Create a new Project

@app.post("/api/v1/projects" , status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
def create_project(project: ProjectCreate , db : Session = Depends(get_db)):
    return project_service.create_project(db , project)
    

# Update a project
@app.patch("/api/v1/projects/{project_id}" , response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate , db : Session = Depends(get_db)):
    updated_project = project_service.update_project(db , project_id , project)

    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return updated_project
    

# Delete a project

@app.delete("/api/v1/projects/{project_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int , db : Session = Depends(get_db)):
    delete = project_service.delete_project(db , project_id)

    if delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return None






