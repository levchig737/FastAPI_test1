from models.user import User
from sqlalchemy.orm import Session
from dto import user


def create_user(data: user.User, db: Session):
    """
    Добавления пользователя в таблицу
    :param data: Пользователь
    :param db: текущая сессия
    :return: добавленный пользователь
    """
    user = User(name=data.name)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return user


def get_user(id: int, db: Session):
    """
    Возвращает пользователя по id
    :param id:
    :param db:
    :return:
    """
    return db.query(User).filter(User.id == id).first()


def update(id: int, data: user.User, db: Session):
    user = db.query(User).filter(User.id == id).first()
    user.name = data.name
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def remove(id: int, db: Session):
    user = db.query(User).filter(User.id == id).delete()
    db.commit()

    return user