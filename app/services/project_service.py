from sqlalchemy.orm import Session

from app.repositories import project_repository
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
def get_projects(db : Session):
    return project_repository.get_projects(db)


def get_project_by_id(db : Session , project_id : int):
    project = project_repository.get_project_by_id(db , project_id)

    if project is None:
        return None

    return project

def create_project(db : Session , project_data : ProjectCreate):
    project = Project(
        name = project_data.name,
        description = project_data.description,
        status = project_data.status
    )

    return project_repository.create_project(db , project)

def update_project(db : Session , project_id : int , project_data : ProjectCreate):
    project = project_repository.get_project_by_id(db , project_id)

    if project is None:
        return None

    if project_data.name is not None:
        project.name = project_data.name

    if project_data.description is not None:
        project.description = project_data.description

    if project_data.status is not None:
        project.status = project_data.status

    return project_repository.update_project(db , project)

def delete_project(db : Session , project_id : int):
    project = project_repository.get_project_by_id(db , project_id)

    if project is None:
        return None

    return project_repository.delete_project(db , project)


    