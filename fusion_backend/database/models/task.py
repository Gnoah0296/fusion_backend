from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.db import Base
import datetime


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(50), default="todo")  # todo / doing / done
    deadline = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)