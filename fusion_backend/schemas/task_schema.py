from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"
    deadline: datetime | None = None
    project_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    deadline: datetime | None = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }