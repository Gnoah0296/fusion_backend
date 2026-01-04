from sqlalchemy.orm import Session
from database.models.project import Project
from schemas.project_schema import ProjectCreate


def get_all(db: Session):
    return db.query(Project).all()


def get_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_by_name(db: Session, name: str):
    return db.query(Project).filter(Project.name == name).first()


def create(db: Session, request: ProjectCreate):
    new_project = Project(
        name=request.name,
        owner=request.owner
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def update(db: Session, project_id: int, request: ProjectCreate):
    project = db.query(Project).filter(Project.id == project_id).first()
    project.name = request.name
    project.owner = request.owner
    db.commit()
    db.refresh(project)
    return project


def delete(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    db.delete(project)
    db.commit()