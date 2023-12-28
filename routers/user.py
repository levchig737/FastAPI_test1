from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import user as UserService
from dto.user import UserCreate, UserUpdate
from models.user import User

router = APIRouter()


@router.post('/register', tags=["user"])
async def register_user(data: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserService.get_user_by_username(data.username, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return UserService.create_user(data, db)


@router.get('/{id}', tags=["user"])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get('/', tags=["user"])
async def get_users(db: Session = Depends(get_db)):
    return UserService.get_users(db)


@router.put('/{id}', tags=["user"])
async def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = UserService.update_user(id, data, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete('/{id}', tags=["user"])
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = UserService.delete_user(id, db)
    if user == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
