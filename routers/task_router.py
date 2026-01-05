from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from security.deps import get_current_user, require_roles
import repositories.task_repository as repo

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "manager"))
):
    return repo.get_all_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("user", "manager", "admin"))
):
    task = repo.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role != "admin" and user.id not in (task.creator_id, task.assignee_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem task này"
        )

    return task

@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("user", "manager", "admin"))
):
    return repo.create_task(
        db=db,
        data=data,
        creator_id=user.id
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("user", "manager", "admin"))
):
    task = repo.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role != "admin" and user.id != task.creator_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ người tạo task mới được sửa"
        )

    return repo.update_task(db, task_id, data)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    success = repo.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Deleted successfully"}
