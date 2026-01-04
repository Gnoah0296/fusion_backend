from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
import repositories.project_repository as project_repo
from schemas.project_schema import ProjectCreate, ProjectResponse

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.get("/", response_model=list[ProjectResponse])
def get_all(db: Session = Depends(get_db)):
    return project_repo.get_all(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_by_id(project_id: int, db: Session = Depends(get_db)):
    project = project_repo.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectResponse)
def create_project(request: ProjectCreate, db: Session = Depends(get_db)):
    existing = project_repo.get_by_name(db, request.name)
    if existing:
        raise HTTPException(status_code=400, detail="Project name already exists")

    return project_repo.create(db, request)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, request: ProjectCreate, db: Session = Depends(get_db)):
    project = project_repo.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project_repo.update(db, project_id, request)


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = project_repo.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_repo.delete(db, project_id)
    return {"message": "Project deleted successfully"}