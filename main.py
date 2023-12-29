import uvicorn
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import engine as UserEngine
from auth.manager import get_user_manager
from dto.user import UserRead, UserCreate

from models.user import Base as UserBase
from database import Base as TaskBase
from models.user import User
from database import engine as TaskEngine

from routers import user as UserRouter
from routers import task as TaskRouter

TaskBase.metadata.create_all(bind=TaskEngine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    # Создание таблицы при запуске приложения
    async with UserEngine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)




fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_user = fastapi_users.current_user()


@app.get("/protected-route", tags=["auth"])
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


app.include_router(UserRouter.router, prefix='/user')
app.include_router(TaskRouter.router, prefix='/task')

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True, workers=3)
