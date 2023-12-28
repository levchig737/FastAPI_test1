from typing import Optional

from pydantic import BaseModel
from models.task import TaskType, PriorityType, StatusType


class Task(BaseModel):
    """
    Передача данных между слоями приложения (database-services/user, database-routers/user)
    """
    task_number: int
    task_type: TaskType
    priority: Optional[PriorityType] = None
    status: StatusType
    title: str
    description: Optional[str] = None
    performer: Optional[str] = None
    creator: str
    # blocking_tasks: Optional[list] = None
