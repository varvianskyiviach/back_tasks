from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from db.config import Base
from tasks.constants import TaskPriorityEnum, TaskStatusEnum

__all__ = ("Task",)


task_assignees = Table(
    "task_assignees",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=100))
    description = Column(Text)

    priority = Column(Enum(TaskPriorityEnum))
    status = Column(Enum(TaskStatusEnum))

    responsible_person_id = Column(Integer, ForeignKey("users.id"))

    responsible_person = relationship("User", back_populates="tasks")
    assignees = relationship(
        "User",
        secondary=task_assignees,
        back_populates="tasks_assignee",
        cascade="all",
    )
