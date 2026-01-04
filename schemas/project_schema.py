from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    owner: str


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int

    model_config = {
        "from_attributes": True
    }