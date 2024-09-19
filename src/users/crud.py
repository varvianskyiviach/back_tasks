from sqlalchemy import select
from sqlalchemy.orm import Session

from users.models import User
from users.schemas import UserCreateSchema, UserStafCreateSchema, UserUpdateSchema
from utils.security import get_password_hash, verify_password


def get_users(db: Session) -> list[User]:
    users: list[User] = db.execute(select(User)).scalars().all()

    return users


def create_user(
    db: Session,
    schema: UserCreateSchema | UserStafCreateSchema,
) -> User:

    user_data: dict = schema.model_dump()
    user_data["hashed_password"] = get_password_hash(schema.password)
    user_data.pop("password", None)
    db_user: User = User(**user_data)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, db_user: User, schema: UserUpdateSchema) -> User:
    user_data: dict = schema.model_dump(exclude_unset=True)
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(schema.password)
        user_data.pop("password", None)

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user: User = db.execute(statement).scalars().first()

    return user


def authenticate(db: Session, email: str, password: str) -> User:
    db_user = get_user_by_email(db=db, email=email)
    if not db_user:
        return None
    if not verify_password(
        plain_password=password,
        hashed_password=db_user.hashed_password,
    ):
        return None

    return db_user
