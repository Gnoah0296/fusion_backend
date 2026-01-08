from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.models.project import Project, ProjectMember
from database.models.task import Task
from database.models.user import User
from schemas.task import TaskCreate, TaskOut, TaskStatusUpdate, TaskUpdate
from security.jwt import get_current_user
from security.permissions import (
    ROLE_SYSTEM_ADMIN,
    ROLE_TENANT_ADMIN,
    ROLE_PM,
    ROLE_BA,
    ROLE_SUPPORT,
    ROLE_DEV,
    ROLE_QA,
    ROLE_CUSTOMER,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_project_or_404(db: Session, project_id: int, tenant_id: int) -> Project:
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.tenant_id == tenant_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def get_membership(db: Session, project_id: int, user_id: int) -> ProjectMember | None:
    return (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        .first()
    )


@router.post("/project/{project_id}", response_model=TaskOut)
def create_task(
    project_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {ROLE_PM, ROLE_BA, ROLE_SUPPORT}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    project = get_project_or_404(db, project_id, current_user.tenant_id)
    membership = get_membership(db, project_id, current_user.id)
    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    task = Task(
        title=payload.title,
        description=payload.description,
        status="OPEN",
        project_id=project.id,
        assignee_id=payload.assignee_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/project/{project_id}", response_model=list[TaskOut])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == ROLE_SYSTEM_ADMIN:
        raise HTTPException(status_code=403, detail="SYSTEM_ADMIN has no tasks")

    project = get_project_or_404(db, project_id, current_user.tenant_id)

    if current_user.role != ROLE_TENANT_ADMIN:
        membership = get_membership(db, project_id, current_user.id)
        if not membership:
            raise HTTPException(status_code=403, detail="Not a project member")

    return db.query(Task).filter(Task.project_id == project.id).all()


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = get_project_or_404(db, task.project_id, current_user.tenant_id)
    membership = get_membership(db, project.id, current_user.id)
    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    if current_user.role == ROLE_PM:
        pass
    elif current_user.id == task.assignee_id:
        pass
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    task.title = payload.title
    task.description = payload.description
    task.assignee_id = payload.assignee_id
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != ROLE_PM:
        raise HTTPException(status_code=403, detail="Only PM can delete tasks")

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = get_project_or_404(db, task.project_id, current_user.tenant_id)
    membership = get_membership(db, project.id, current_user.id)
    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


@router.put("/{task_id}/status", response_model=TaskOut)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role in {ROLE_CUSTOMER, ROLE_SYSTEM_ADMIN}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = get_project_or_404(db, task.project_id, current_user.tenant_id)

    if current_user.role in {ROLE_PM, ROLE_BA, ROLE_SUPPORT}:
        membership = get_membership(db, project.id, current_user.id)
        if not membership:
            raise HTTPException(status_code=403, detail="Not a project member")
    elif current_user.role in {ROLE_DEV, ROLE_QA}:
        if current_user.id != task.assignee_id:
            raise HTTPException(status_code=403, detail="Not assigned to task")
    elif current_user.role == ROLE_TENANT_ADMIN:
        pass
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    task.status = payload.status
    db.commit()
    db.refresh(task)
    return task
