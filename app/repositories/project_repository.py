from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project

def get_projects(db: Session):
    statement = select(Project)
    result = db.execute(statement)
    return result.scalars().all()

def get_project_by_id(db : Session , project_id : int):
    statement = select(Project).where(Project.id == project_id)
    result = db.execute(statement)
    return result.scalars().one_or_none()

def create_project(db : Session , project : Project):
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def update_project(db : Session , project : Project):
    db.commit()
    db.refresh(project)
    return project

def delete_project(db : Session , project : Project):
    db.delete(project)
    db.commit()