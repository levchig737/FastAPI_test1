from pydantic import BaseModel
from models.user import UserRole


class UserBase(BaseModel):
    username: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str
