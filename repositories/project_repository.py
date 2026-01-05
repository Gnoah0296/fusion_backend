from sqlalchemy.orm import Session
from database.models.project import Project
from schemas.project_schema import ProjectCreate, ProjectUpdate

def get_all_projects(db: Session):
    return db.query(Project).all()

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def create_project(db: Session, data: ProjectCreate, owner_id: int):
    new_project = Project(
        name=data.name,
        description=data.description,
        owner_id=owner_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def update_project(db: Session, project_id: int, data: ProjectUpdate):
    project = get_project(db, project_id)
    if not project:
        return None

    project.name = data.name
    project.description = data.description

    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int):
    project = get_project(db, project_id)
    if not project:
        return False

    db.delete(project)
    db.commit()
    return True
