from enum import Enum as PyEnum


class TaskStatusEnum(str, PyEnum):
    TODO = "TODO"
    IN_PROGRESS = "In progress"
    DONE = "Done"


class TaskPriorityEnum(str, PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
