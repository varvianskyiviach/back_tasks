from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from tasks.models import Task
from tasks.shemas import TaskCreateShema, TaskUpdateShema
from users.constants import roles
from users.models import User


def create_task(db: Session, schema: TaskCreateShema, current_user: User) -> Task:
    if current_user.role == roles.RoleEnum.USER:
        user_id = current_user.id
    elif not schema.responsible_person_id:
        user_id = current_user.id
    else:
        user_id = schema.responsible_person_id

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="responsible person id is not valid")

    task_in_db: Task = Task(
        title=schema.title,
        description=schema.description,
        priority=schema.priority,
        status=schema.status,
        responsible_person=user,
    )

    if schema.assignees:
        users_assignees = db.query(User).filter(User.id.in_(schema.assignees)).all()
        task_in_db.assignees.extend(users_assignees)

    db.add(task_in_db)
    db.commit()

    return task_in_db


def update_task(db: Session, task: Task, schema: TaskUpdateShema) -> Task:
    task_data: dict = schema.model_dump(exclude_unset=True)

    for key, value in task_data.items():
        if key == "responsible_person_id":
            user = db.query(User).filter(User.id == schema.responsible_person_id).first()
            task.responsible_person = user
        elif key == "assignees":
            users_assignees = db.query(User).filter(User.id.in_(schema.assignees)).all()
            task.assignees = users_assignees
        else:
            setattr(task, key, value)

    db.commit()

    return task
