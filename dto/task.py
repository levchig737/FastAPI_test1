from typing import Optional, List

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
    performer_id: Optional[int] = -1
    creator: str
    blocking_tasks: Optional[List[int]] = []


class ReadTask(Task):
    blocked_by_tasks: Optional[List[int]] = []


class UpdateTaskStatusAndPerformer(BaseModel):
    status: StatusType
    performer_id: Optional[int] = -1
