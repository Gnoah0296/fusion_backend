from pydantic import BaseModel, Field
from typing import Optional

class ProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Tên project (3–100 ký tự)"
    )
    description: Optional[str] = Field(
        None,
        max_length=255,
        description="Mô tả project"
    )
    status: str = Field(
        ...,
        pattern="^(active|inactive)$",
        description="Trạng thái: active | inactive"
    )

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3)

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, pattern="^(active|inactive)$")

class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True

