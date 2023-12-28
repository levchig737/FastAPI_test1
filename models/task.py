from enum import Enum
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


# Перечисление для типа задачи
class TaskType(str, Enum):
    bug = "bug"
    task = "task"


# Перечисление для типа приоритета
class PriorityType(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


# Перечисление для типа задачи
class StatusType(str, Enum):
    to_do = "To do"
    in_progress = "In progress"
    code_review = "Code review"
    dev_test = "Dev test"
    testing = "Testing"
    done = "Done"
    wontfix = "Wontfix"


class Task(Base):
    """
    Таблица tasks
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    task_number = Column(Integer, unique=True, index=True, nullable=False)
    task_type: TaskType = Column(String, nullable=False)
    priority: Optional[PriorityType] = Column(String)
    status: StatusType = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description: Optional[str] = Column(String)
    performer: Optional[str] = Column(String)
    creator = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # blocking_tasks = relationship("BlockingTask", back_populates="task")






