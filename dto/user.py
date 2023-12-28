from pydantic import BaseModel


class User(BaseModel):
    """
    Передача данных между слоями приложения (database-services/task, database-routers/task)
    """
    name: str
