from sqlalchemy import select
from sqlalchemy.orm import Session

from config.settings import (
    FIRST_SUPERUSER_EMAIL,
    FIRST_SUPERUSER_FIRST_NAME,
    FIRST_SUPERUSER_LAST_NAME,
    FIRST_SUPERUSER_PASSWORD,
)
from users import crud
from users.constants import RoleEnum
from users.models import User
from users.schemas import UserStafCreateSchema


def init_db(db: Session) -> None:
    user = db.execute(select(User).where(User.email == FIRST_SUPERUSER_EMAIL)).first()
    if not user:
        user_in = UserStafCreateSchema(
            email=FIRST_SUPERUSER_EMAIL,
            password=FIRST_SUPERUSER_PASSWORD,
            first_name=FIRST_SUPERUSER_FIRST_NAME,
            last_name=FIRST_SUPERUSER_LAST_NAME,
            is_active=True,
            is_superuser=True,
            role=RoleEnum.ADMIN,
        )
        user = crud.create_user(db=db, schema=user_in)
