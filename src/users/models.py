from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from db.config import Base
from tasks.models import Task  # noqa: F401, F403
from users.constants import RoleEnum

__all__ = ("User",)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)

    tasks = relationship("Task", back_populates="responsible_person")
    tasks_assignee = relationship("Task", secondary="task_assignees", back_populates="assignees")
