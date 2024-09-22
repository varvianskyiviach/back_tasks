from pydantic import BaseModel, Field

from users.constants import RoleEnum


class UserCreateSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserStafCreateSchema(UserCreateSchema):
    is_active: bool = True
    is_superuser: bool = True
    role: RoleEnum = RoleEnum.ADMIN


class UserUpdateSchema(UserStafCreateSchema):
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    is_active: bool | None = Field(default=False)
    is_superuser: bool | None = Field(default=False)


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: RoleEnum

    class Config:
        from_attributes = True


class UserResponseSchema(BaseModel):
    result: UserSchema = Field(
        description="Result of User response schema",
    )


class UserMultiResponseSchema(BaseModel):
    results: list[UserSchema] = Field(
        description="Includes the list of Users response schema",
        default_factory=list,
    )


class Message(BaseModel):
    message: str
