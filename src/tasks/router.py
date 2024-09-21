from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from tasks import crud
from tasks.models import Task
from tasks.shemas import (
    Message,
    TaskCreateShema,
    TaskMultiResponseSchema,
    TaskResponseSchema,
    TaskSchema,
    TaskUpdateShema,
)
from users.constants import RoleEnum
from users.deps import SessionDep, get_current_role_admin, get_current_user
from users.models import User

router = APIRouter(prefix="/tasks")


@router.get("/{task_id}", response_model=TaskResponseSchema, dependencies=[Depends(get_current_user)])
def get_task_by_id(db: SessionDep, task_id: int) -> TaskResponseSchema:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    result: TaskSchema = TaskSchema.model_validate(task)

    return TaskResponseSchema(result=result)


@router.get("/", response_model=TaskMultiResponseSchema, dependencies=[Depends(get_current_user)])
def list(db: SessionDep) -> TaskMultiResponseSchema:
    tasks = db.query(Task).options(joinedload(Task.responsible_person), joinedload(Task.assignees)).all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks not found",
        )
    results: List[TaskSchema] = [TaskSchema.model_validate(task) for task in tasks]

    return TaskMultiResponseSchema(results=results)


@router.post("/")
def create(
    db: SessionDep, schema: TaskCreateShema, current_user: User = Depends(get_current_user)
) -> TaskResponseSchema:
    new_task: Task = crud.create_task(
        db=db,
        schema=schema,
        current_user=current_user,
    )
    task_response = TaskSchema.model_validate(new_task)

    return TaskResponseSchema(result=task_response)


@router.patch("/{id}")
def update(db: SessionDep, id: int, schema: TaskUpdateShema, current_user: User = Depends(get_current_user)) -> Any:
    task: Task = db.get(Task, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task not found",
        )

    if current_user.role != RoleEnum.ADMIN:
        if current_user.id != task.responsible_person_id and not (
            task.assignees and current_user.id in [assignee.id for assignee in task.assignees]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden! Only admin or responsible person or assignee member can change task",
            )
    if (
        schema.priority is not None
        and current_user.role != RoleEnum.ADMIN
        and current_user.id != task.responsible_person_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only admin or responsible person can change priority."
        )

    updated_task: Task = crud.update_task(
        db=db,
        task=task,
        schema=schema,
    )

    return TaskResponseSchema(result=TaskSchema.model_validate(updated_task))


@router.delete("/{task_id}", response_model=Message, dependencies=[Depends(get_current_role_admin)])
def delete(db: SessionDep, task_id: int) -> Any:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    db.delete(task)
    db.commit()

    return Message(message="Task has been deleted successfully")
