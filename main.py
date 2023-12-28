import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers import user as UserRouter
from routers import task as TaskRouter


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(UserRouter.router, prefix='/user')
app.include_router(TaskRouter.router, prefix='/task')

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True, workers=3)
