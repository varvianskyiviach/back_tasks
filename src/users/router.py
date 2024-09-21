from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from users import crud
from users.deps import SessionDep, get_current_role_admin
from users.models import User
from users.schemas import (
    Message,
    UserCreateSchema,
    UserMultiResponseScema,
    UserResponseSchema,
    UserSchema,
    UserUpdateSchema,
)

router = APIRouter(prefix="/users")


@router.get("/", dependencies=[Depends(get_current_role_admin)])
def list(db: SessionDep) -> Any:
    users: list[User] = crud.get_users(db=db)

    users_results: List[UserSchema] = []

    for user in users:
        users_results.append(UserSchema.model_validate(user))

    return UserMultiResponseScema(results=users_results)


@router.get("/{user_id}", dependencies=[Depends(get_current_role_admin)])
def get_user_by_id(db: SessionDep, user_id: int) -> Any:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    return UserResponseSchema(result=user)


@router.post("/")
def create(db: SessionDep, schema: UserCreateSchema) -> Any:
    db_user: User = crud.get_user_by_email(db=db, email=schema.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user: User = crud.create_user(db=db, schema=schema)
    user_response = UserSchema.model_validate(user)

    return UserResponseSchema(result=user_response)


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_role_admin)],
)
def update(db: SessionDep, user_id: int, user_in: UserUpdateSchema) -> Any:

    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = crud.get_user_by_email(db=db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
    db_user = crud.update_user(db=db, db_user=db_user, schema=user_in)

    return UserResponseSchema(result=UserSchema.model_validate(db_user))


@router.delete("/{user_id}")
def delete(
    db: SessionDep,
    user_id: int,
    current_user: User = Depends(
        get_current_role_admin,
    ),
) -> Message:

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if current_user.is_superuser and current_user == user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super users are not allowed to delete themselves",
        )
    db.delete(user)
    db.commit()

    return Message(message="User has been deleted successfully")
