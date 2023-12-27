from pydantic import BaseModel


class User(BaseModel):
    """
    Передача данных между слоями приложения (database-services/user, database-routers/user)
    """
    name: str
