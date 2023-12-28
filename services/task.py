from models.task import Task
from sqlalchemy.orm import Session
from dto import task as TaskDTO


def create_task(data: TaskDTO.Task, db: Session) -> Task:
    """
    Создаем по переданным данным объект task и добавляем в бд
    :param data: данные task
    :param db: сессия/бд
    :return: созданный task
    """
    # Получаем все таски по id, переданные в data.blocking_tasks
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
    """
    Получаем task по id
    :param id: id task
    :param db: сессия/бд
    :return: task или None если не найден
    """
    return db.query(Task).filter(Task.id == id).first()


def update(id: int, data: TaskDTO.Task, db: Session) -> Task | None:
    """
    Обновляем данные о task
    :param id: id task
    :param data: данные task, которые нужно обновить
    :param db: сессия/бд
    :return: измененный task или None если не нашли
    """
    task = get_task(id, db)
    if task:
        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)
        return task
    return None


def remove(id: int, db: Session) -> int:
    """
    Удаляем task по id
    :param id: id task
    :param db: сессия/бд
    :return: кол-во удаленных строк (1)
    """
    task = db.query(Task).filter(Task.id == id).delete()
    db.commit()

    return task
