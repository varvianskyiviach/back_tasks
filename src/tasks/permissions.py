from tasks.models import Task
from tasks.schemas import TaskUpdateSchema
from users.constants import roles
from users.models import User


class TaskAccessControl:
    def __init__(self, current_user: User, task: Task, schema: TaskUpdateSchema):
        self.current_user = current_user
        self.task = task
        self.schema = schema

    def _is_admin_user(self) -> bool:
        return self.current_user.role == roles.RoleEnum.ADMIN

    def _is_responsible_user(self) -> bool:
        return self.current_user.id == self.task.responsible_person_id

    def _is_assignee_user(self) -> bool:
        return self.current_user.id in [assignee.id for assignee in self.task.assignees]

    def access_update_task(self) -> bool:
        if self._is_admin_user() or self._is_responsible_user():
            return True
        if self.task.assignees and self._is_assignee_user():
            return True
        return False

    def is_admin_user(self) -> bool:
        return self._is_admin_user()

    def is_responsible_user(self) -> bool:
        return self._is_responsible_user()
