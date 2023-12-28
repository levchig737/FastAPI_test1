
from fastapi_users import schemas

from auth.database import UserRole


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: str
    username: str
    password: str
    role: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    email: str
    username: str
    password: str
    role: UserRole
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
