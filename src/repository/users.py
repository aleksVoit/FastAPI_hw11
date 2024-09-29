from libgravatar import Gravatar
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from src.conf.config import settings

import redis

import pickle

r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user with specific email.

    :param email: User email.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: User.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates the user.

    :param body: Dictionary with user's data.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: User.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates token.

    :param user: specific user.
    :type user: User
    :param token: token to be overwritten.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Changes status of user to 'confirmed' after email confirmation.

    :param email: email to be confirmed.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Changes avatar of user.

    :param email: email of user.
    :type email: str
    :param url: url of the avatar image.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: User.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


