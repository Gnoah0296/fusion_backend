from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="todo")
    priority: Optional[int] = Field(default=1, ge=1, le=5)
    due_date: Optional[datetime] = None



class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None



class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None



class TaskResponse(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

