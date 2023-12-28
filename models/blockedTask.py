from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# Модель связи между блокирующей и заблокированной задачами
class BlockingTask(Base):
    __tablename__ = "blocking_tasks"

    id = Column(Integer, primary_key=True, index=True)
    blocking_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    blocked_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)


