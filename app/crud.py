from datetime import datetime

from sqlalchemy.orm import Session

from app.model import Users
import logging

logger = logging.getLogger(__name__)


def get_user_by_id(db: Session, id: int):
    """
    Getting a user from the database by his ID
    :param db:
    :param id:
    :return:
    """
    return db.query(Users).filter(Users.id == id).first()


def get_user_by_login(db: Session, login: str):
    """
    Getting a user from the database by his Login
    :param db:
    :param login:
    :return:
    """
    return db.query(Users).filter(Users.login == login).first()


def create_new_user(db: Session, login: str, password: str, name: str) -> int:
    """
    Сreating a user based on the entered username, password and username
    :param db:
    :param login:
    :param password:
    :param name:
    :return:
    """
    try:
        db_user = Users(login=login,
                        password=password,
                        name=name,
                        at_create=datetime.now())
        db.add(db_user)
        db.commit()
        return db_user.id
    except Exception as e:
        db.rollback()
        logger.error(e)
        return -1


def update_db_user(db: Session, user_id: int, new_login: str, new_name: str) -> bool:
    """
    Updating user data by User ID
    :param db:
    :param user_id:
    :param new_login:
    :param new_name:
    :return:
    """
    try:
        db.query(Users).filter(Users.id == user_id).update({
            'login': new_login,
            'name': new_name
        })
        db.commit()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(e)
        return False
