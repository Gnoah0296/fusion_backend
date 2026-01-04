from sqlalchemy.orm import Session
from database.models.task import Task
from schemas.task_schema import TaskCreate, TaskUpdate


def get_all(db: Session, project_id: int):
    return db.query(Task).filter(Task.project_id == project_id).all()


def get_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create(db: Session, request: TaskCreate):
    new_task = Task(
        title=request.title,
        description=request.description,
        status=request.status,
        deadline=request.deadline,
        project_id=request.project_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update(db: Session, task_id: int, request: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()

    if request.title is not None:
        task.title = request.title
    if request.description is not None:
        task.description = request.description
    if request.status is not None:
        task.status = request.status
    if request.deadline is not None:
        task.deadline = request.deadline

    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()