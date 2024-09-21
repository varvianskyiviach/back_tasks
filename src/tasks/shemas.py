from pydantic import BaseModel, Field

from tasks.constants import TaskPriorityEnum, TaskStatusEnum
from users.schemas import UserSchema


class TaskBaseSchema(BaseModel):
    title: str
    description: str
    priority: TaskPriorityEnum = Field(default=TaskPriorityEnum.LOW)
    responsible_person_id: int | None = Field(default=None)
    status: TaskStatusEnum = Field(default=TaskStatusEnum.TODO)


class TaskCreateShema(TaskBaseSchema):
    assignees: list[int] | None = Field(default=None)


class TaskUpdateShema(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    priority: TaskPriorityEnum | None = Field(default=None)
    status: TaskStatusEnum | None = Field(default=None)
    responsible_person_id: int | None = Field(default=None)
    assignees: list[int] | None = Field(default=None)


class TaskSchema(BaseModel):
    id: int
    title: str
    responsible_person: UserSchema | None
    assignees: list[UserSchema]

    class Config:
        from_attributes = True


class TaskResponseSchema(BaseModel):
    result: TaskSchema = Field(
        description="Result of Task response schema",
    )


class TaskMultiResponseSchema(BaseModel):
    results: list[TaskSchema] = Field(
        description="Includes the list of Users response schema",
        default_factory=list,
    )


class Message(BaseModel):
    message: str
