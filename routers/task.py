from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from services import task as TaskService
from dto import task as TaskDTO


router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""


@router.post('/', tags=["task"])
async def create(data: TaskDTO.Task = None, db: Session = Depends(get_db)):
    return TaskService.create_task(data, db)


@router.get('/{id}', tags=["task"])
async def get(id: int = None, db: Session = Depends(get_db)):
    return TaskService.get_task(id, db)


@router.put('/{id}', tags=["task"])
async def update(id: int = None, data: TaskDTO.Task = None, db: Session = Depends(get_db)):
    return TaskService.update(id, data, db)


@router.delete('/{id}', tags=["task"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return TaskService.remove(id, db)

