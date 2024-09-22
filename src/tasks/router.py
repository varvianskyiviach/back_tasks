from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from tasks import crud
from tasks.models import Task
from tasks.permissions import TaskAccessControl
from tasks.schemas import (
    Message,
    TaskCreateSchema,
    TaskMultiResponseSchema,
    TaskResponseSchema,
    TaskSchema,
    TaskUpdateSchema,
)
from tasks.utils import background_email_task
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
    db: SessionDep, schema: TaskCreateSchema, current_user: User = Depends(get_current_user)
) -> TaskResponseSchema:
    new_task: Task = crud.create_task(
        db=db,
        schema=schema,
        current_user=current_user,
    )
    task_response = TaskSchema.model_validate(new_task)

    return TaskResponseSchema(result=task_response)


@router.patch("/{id}")
def update(
    db: SessionDep,
    id: int,
    schema: TaskUpdateSchema,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
) -> Any:
    task: Task = db.get(Task, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task not found",
        )
    task_access: TaskAccessControl = TaskAccessControl(current_user, task=task, schema=TaskUpdateSchema)

    if not task_access.access_update_task():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden! Only admin or responsible person or assignee member can change task",
        )
    if schema.priority is not None and not task_access.is_admin_user() and not task_access.is_responsible_user():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only admin or responsible person can change priority."
        )
    if (
        schema.responsible_person_id is not None
        and not task_access.is_admin_user()
        and not task_access.is_responsible_user()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or responsible person can change responsible person.",
        )

    previous_status = task.status

    updated_task: Task = crud.update_task(
        db=db,
        task=task,
        schema=schema,
    )

    background_email_task(
        db=db,
        id=id,
        previous_status=previous_status,
        current_status=updated_task.status,
        background_tasks=background_tasks,
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
