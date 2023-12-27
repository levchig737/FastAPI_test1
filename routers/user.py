from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from services import user as UserService
from dto import user as UserDTO


router = APIRouter()

"""
router - контроллер, обработчик маршрутов, который выполняет машинную логику, в нашем случае ассинхронно
"""


@router.post('/', tags=["user"])
async def create(data: UserDTO.User = None, db: Session = Depends(get_db)):
    return UserService.create_user(data, db)


@router.get('/{id}', tags=["user"])
async def get(id: int = None, db: Session = Depends(get_db)):
    return UserService.get_user(id, db)


@router.put('/{id}', tags=["user"])
async def update(id: int = None, data: UserDTO.User = None, db: Session = Depends(get_db)):
    return UserService.update(id, data, db)


@router.delete('/{id}', tags=["user"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return UserService.remove(id, db)

