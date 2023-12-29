from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from auth.auth import auth_backend
from auth.manager import get_user_manager
from database import get_db
from models.user import User

from services import task as TaskService
from dto import task as TaskDTO
from services.task import search_tasks

router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.post('/', tags=["task"])
async def create(data: TaskDTO.Task = None, db: Session = Depends(get_db)):
    return TaskService.create_task(data, db)


@router.get('/{id}', tags=["task"])
async def get(id: int = None, db: Session = Depends(get_db)):
    return TaskService.get_task(id, db)


@router.put('/{id}', tags=["task1"])
async def update(id: int = None, data: TaskDTO.Task = None, db: Session = Depends(get_db)):
    return TaskService.update(id, data, db)


@router.put('/{id}/2', tags=["task2"])
async def update_status_and_performer(id: int = None, data: TaskDTO.UpdateTaskStatusAndPerformer = None,
                                      db: Session = Depends(get_db)):
    return TaskService.update_status_and_performer(id, data, db)


@router.delete('/{id}', tags=["task"])
async def delete(id: int = None, cur_user: User = Depends(fastapi_users.current_user()), db: Session = Depends(get_db)):
    if cur_user.role != "manager":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")

    return TaskService.remove(id, db)


@router.get('/', tags=["task"])
async def get_tasks(db: Session = Depends(get_db)):
    return TaskService.get_tasks(db)


@router.get("/tasks/search", tags=["task"])
async def search_task(
        query: str, db: Session = Depends(get_db), limit: Optional[int] = 10
):
    """
    Поиск задач по тексту (в заголовке и описании) или номеру.
    Сортировка по последнему обновлению.
    :param query: Текст для поиска
    :param db: сессия/бд
    :param limit: Лимит записей для вывода
    :return: Список задач, удовлетворяющих запросу
    """
    tasks = search_tasks(db, query)

    # Заменить None на datetime.min перед сортировкой
    tasks = [task if task.updated_at is not None else task for task in tasks]
    #
    # tasks_sorted = sorted(tasks, key=lambda x: x.updated_at if x.updated_at is not None else datetime.min,
    #                       reverse=True)[:limit]
    return tasks
