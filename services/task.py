from typing import List, Type

from fastapi import HTTPException
from sqlalchemy import or_, desc

from models.task import Task, blocking_tasks_table
from sqlalchemy.orm import Session, joinedload
from dto import task as TaskDTO
from models.task import StatusType
from models.user import User

from services.user import get_user_by_id


def validate_data(performer: User, task: Task | TaskDTO.UpdateTaskStatusAndPerformer):
    if not performer:
        if task.performer_id != -1:
            raise HTTPException(status_code=422, detail="Performer doesnt exist in users table")
        if task.status == "In progress":
            raise HTTPException(status_code=422, detail="Task with status in progress should have performer")

    else:
        if performer.role == "manager":
            raise HTTPException(status_code=422, detail="Manager cant be performer")

        elif performer.role == "team_lead":
            pass

        elif performer.role == "test_engineer":
            if task.status == "In progress" or task.status == "Code review" or task.status == "Dev test":
                raise HTTPException(status_code=422, detail="test_engineer cant be performer on status in progress, "
                                                            "code review or dev test ")

        elif performer.role == "developer" and task.status == "Testing":
            raise HTTPException(status_code=422, detail="Developer cant be performer on status testing")


def create_task(data: TaskDTO.Task, db: Session) -> Task:
    """
    Создаем по переданным данным объект task и добавляем в бд
    :param data: данные task
    :param db: сессия/бд
    :return: созданный task
    """

    # Проверка условий на соответствие роли пользователя со статусом задачи
    performer = get_user_by_id(data.performer_id, db)
    validate_data(performer, data)

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

    return (
        db.query(Task)
        .options(joinedload(Task.blocking_tasks), joinedload(Task.blocked_by_tasks))
        .filter(Task.id == id)
        .first()
    )


def update(id: int, data: TaskDTO.Task, db: Session) -> Task | None:
    """
    Обновляем данные о task
    :param id: id task
    :param data: данные task, которые нужно обновить
    :param db: сессия/бд
    :return: измененный task или None если не нашли
    """
    task = get_task(id, db)

    # Проверка условий на соответствие роли пользователя со статусом задачи
    performer = get_user_by_id(data.performer_id, db)
    validate_data(performer, data)

    # Проверка соответствия нового статуса
    if task:
        task_status = StatusType.from_string(task.status)
        new_status = StatusType.from_string(data.status)
        diff_tasks = new_status.to_int() - task_status.to_int()
        # Проверка корректности перехода статусов
        if diff_tasks != 0 and diff_tasks != 1:
            # Проверка если статут to_do or wont_fix
            if (new_status == StatusType.to_do) or (new_status == StatusType.wontfix):
                pass
            else:
                raise HTTPException(status_code=422, detail="Invalid status")

        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        return task
    return None


def update_status_and_performer(id: int, data: TaskDTO.UpdateTaskStatusAndPerformer, db: Session) -> Task | None:
    task = get_task(id, db)

    # Проверка условий на соответствие роли пользователя со статусом задачи
    performer = get_user_by_id(data.performer_id, db)
    validate_data(performer, data)

    # Проверка соответствия нового статуса
    if task:
        task_status = StatusType.from_string(task.status)
        new_status = StatusType.from_string(data.status)
        diff_tasks = new_status.to_int() - task_status.to_int()
        # Проверка корректности перехода статусов
        if diff_tasks != 0 and diff_tasks != 1:
            # Проверка если статут to_do or wont_fix
            if (new_status == StatusType.to_do) or (new_status == StatusType.wontfix):
                pass
            else:
                raise HTTPException(status_code=422, detail="Invalid status")

        # Обновляем только те поля, которые присутствуют в data
        for field, value in data.dict(exclude_unset=True).items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        return task
    return None


def remove(id: int, db: Session) -> Type[Task] | None:
    """
    Удаляем task по id
    :param id: id task
    :param db: сессия/бд
    :return: кол-во удаленных строк (1)
    """
    task = db.query(Task).filter(Task.id == id).first()

    if task:
        db.execute(blocking_tasks_table.delete().where(
            (blocking_tasks_table.c.task_id == id) | (blocking_tasks_table.c.blocked_task_id == id)
        ))

        # Удаление задачи
        db.delete(task)
        db.commit()

    return task


def get_tasks(db: Session) -> list[Type[Task]]:
    return db.query(Task).all()


def search_tasks(db: Session, query: str) -> list[Type[Task]]:
    """
    Поиск задач по тексту (в заголовке и описании) или номеру.
    :param db: сессия/бд
    :param query: Текст для поиска
    :return: Список задач, удовлетворяющих запросу
    """
    return (
        db.query(Task)
        .filter(
            or_(
                Task.title.ilike(f"%{query}%"),
                Task.description.ilike(f"%{query}%"),
                Task.task_number == int(query) if query.isdigit() else False,
            )
        )
        .order_by(desc(Task.updated_at))
        .all()
    )
