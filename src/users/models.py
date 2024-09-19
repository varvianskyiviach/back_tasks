from sqlalchemy import Boolean, Column, Enum, Integer, String

from db.config import Base
from users.constants import RoleEnum


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
