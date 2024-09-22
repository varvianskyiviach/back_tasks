from fastapi import BackgroundTasks
from sqlalchemy.orm import Session, joinedload

from tasks.constants import TaskStatusEnum
from tasks.models import Task
from utils.email import mock_error_hendler_email, mock_send_email


def background_email_task(
    db: Session,
    id: int,
    previous_status: TaskStatusEnum,
    current_status: Task,
    background_tasks: BackgroundTasks,
) -> None:

    if previous_status != current_status:
        task = db.query(Task).options(joinedload(Task.responsible_person)).filter(Task.id == id).first()
        responsible_person = task.responsible_person
        if not responsible_person:
            background_tasks.add_task(mock_error_hendler_email)
            return None

        email_to = responsible_person.email
        subject = "Task status changed"
        html_content = f"Task '{task.title}' status changed to {task.status}."

        background_tasks.add_task(mock_send_email, email_to, subject, html_content)
