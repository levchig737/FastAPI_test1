from enum import Enum
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
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

    def to_int(self):
        return StatusTypeInt[self.name].value

    def __lt__(self, other):
        return self.to_int() < other.to_int()

    def __le__(self, other):
        return self.to_int() <= other.to_int()

    def __gt__(self, other):
        return self.to_int() > other.to_int()

    def __ge__(self, other):
        return self.to_int() >= other.to_int()

    @classmethod
    def from_string(cls, value: str):
        for status in cls:
            if status.value == value or status.name == value:
                return status
        raise ValueError(f"Invalid status: {value}")


class StatusTypeInt(int, Enum):
    to_do = 1
    in_progress = 2
    code_review = 3
    dev_test = 4
    testing = 5
    done = 6
    wontfix = 7


blocking_tasks_table = Table('blocking_tasks', Base.metadata,
                             Column('task_id', ForeignKey('tasks.id'), primary_key=True),
                             Column('blocked_task_id', ForeignKey('tasks.id'), primary_key=True)
                             )


class Task(Base):
    """
    Таблица tasks
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    task_number = Column(Integer, index=True, nullable=False)
    task_type: TaskType = Column(String, nullable=False)
    priority: Optional[PriorityType] = Column(String)
    status: StatusType = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description: Optional[str] = Column(String)
    creator = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    performer_id: Optional[int] = Column(Integer)

    # Заблокированные задачи
    blocking_tasks = relationship(
        'Task',
        secondary=blocking_tasks_table,
        primaryjoin=id == blocking_tasks_table.c.task_id,
        secondaryjoin=id == blocking_tasks_table.c.blocked_task_id,
        back_populates='blocked_by_tasks'
    )

    # Блокирующие задачи
    blocked_by_tasks = relationship(
        'Task',
        secondary=blocking_tasks_table,
        primaryjoin=id == blocking_tasks_table.c.blocked_task_id,
        secondaryjoin=id == blocking_tasks_table.c.task_id,
        back_populates='blocking_tasks'
    )
