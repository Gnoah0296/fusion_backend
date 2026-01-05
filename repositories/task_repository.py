from sqlalchemy.orm import Session
from database.models.task import Task
from schemas.task_schema import TaskCreate, TaskUpdate


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(
    db: Session,
    data: TaskCreate,
    creator_id: int
):
    """
    creator_id: user tạo task (lấy từ token)
    """
    new_task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        project_id=data.project_id,
        assignee_id=data.assignee_id,
        creator_id=creator_id   
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(
    db: Session,
    task_id: int,
    data: TaskUpdate
):
    task = get_task_by_id(db, task_id)
    if not task:
        return None

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status is not None:
        task.status = data.status
    if data.assignee_id is not None:
        task.assignee_id = data.assignee_id

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True
