from sqlalchemy.orm import Session

from app.repositories import project_repository
from app.repositories import project_summary_repository


def get_project_summary(
    db: Session,
    project_id: int
):
    project = project_repository.get_project_by_id(
        db,
        project_id
    )

    if project is None:
        return None

    statistics = project_summary_repository.get_project_statistics(
        db,
        project_id
    )

    return {
        "statistics": statistics
    }