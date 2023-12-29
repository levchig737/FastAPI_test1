import uvicorn
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import engine
from auth.manager import get_user_manager
from dto.user import UserRead, UserCreate, UserUpdate
from models.user import User, Base

from routers import task as TaskRouter
from routers import user as UserRouter


app = FastAPI()


@app.on_event("startup")
async def startup():
    # Создание таблицы при запуске приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
#
#
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )


current_user = fastapi_users.current_user()


@app.get("/protected-route", tags=["auth"])
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


app.include_router(TaskRouter.router, prefix='/task')
app.include_router(UserRouter.router, prefix='/user')

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True, workers=3)
