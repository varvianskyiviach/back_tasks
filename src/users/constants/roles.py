from enum import Enum as PyEnum

__all__ = ["RoleEnum"]


class RoleEnum(str, PyEnum):
    ADMIN = "admin"
    USER = "user"
