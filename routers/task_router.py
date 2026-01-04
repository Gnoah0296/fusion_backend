from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
import repositories.task_repository as task_repo
import repositories.project_repository as project_repo
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/project/{project_id}", response_model=list[TaskResponse])
def get_tasks_by_project(project_id: int, db: Session = Depends(get_db)):
    project = project_repo.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return task_repo.get_all(db, project_id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repo.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskResponse)
def create_task(request: TaskCreate, db: Session = Depends(get_db)):
    project = project_repo.get_by_id(db, request.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project does not exist")

    return task_repo.create(db, request)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, request: TaskUpdate, db: Session = Depends(get_db)):
    task = task_repo.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_repo.update(db, task_id, request)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repo.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_repo.delete(db, task_id)
    return {"message": "Task deleted successfully"}