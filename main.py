# import uvicorn
# from fastapi import FastAPI
# from database import engine, Base
# from routers import user as UserRouter
# from routers import task as TaskRouter
#
#
# Base.metadata.create_all(bind=engine)
# app = FastAPI()
# app.include_router(UserRouter.router, prefix='/user')
# app.include_router(TaskRouter.router, prefix='/task')
#
#
import uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import User, Base, engine
from auth.manager import get_user_manager
from auth.shemas import UserRead, UserCreate


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

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True, workers=3)
