from models.task import Task
from sqlalchemy.orm import Session
from dto import task as TaskDTO


def create_task(data: TaskDTO.Task, db: Session) -> Task:
    blocking_tasks = db.query(Task).filter(Task.id.in_(data.blocking_tasks)).all()

    task_data = data.dict(exclude={'blocking_tasks'})
    task = Task(**task_data)
    task.blocking_tasks = blocking_tasks

    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except Exception as e:
        print(e)

    return task


def get_task(id: int, db: Session) -> Task | None:
    return db.query(Task).filter(Task.id == id).first()


def update(id: int, data: TaskDTO.Task, db: Session) -> Task | None:
    task = get_task(id, db)
    data_task = Task(**data.dict())
    if task:
        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)
        return task
    return None


def remove(id: int, db: Session) -> int:
    task = db.query(Task).filter(Task.id == id).delete()
    db.commit()

    return task
