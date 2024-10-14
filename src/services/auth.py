from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository import users as repository_users
import redis

from ..conf.config import settings
import pickle


class Auth:
    _pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    __SECRET_KEY = settings.secret_key
    __ALGORITHM = settings.algorithm
    _oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    _r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hash_password):
        """
        Compares entered password and hash of the password from database.

        :param plain_password: The password to be confirmed.
        :type plain_password: str
        :param hash_password: The hash password for confirmation.
        :type hash_password: str
        :return: True or False of verification.
        :rtype: Bool
        """
        return self._pwd_context.verify(plain_password, hash_password)

    def get_password_hash(self, password: str):
        """
        Create hashed password for databasec.

        :param password: The user's password.
        :type password: str
        :return: The hash of the password.
        :rtype: str
        """
        return self._pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Creates access token.

        :param data: The data required for token.
        :type data: dict
        :param expires_delta: The period of validity of the token.
        :type expires_delta: float
        :return: The hash of the password.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'access token'})
        encoded_access_token = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Creates refresh token.

        :param data: The data required for token.
        :type data: dict
        :param expires_delta: The period of validity of the token.
        :type expires_delta: float
        :return: The hash of the password.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({'iat': datetime.utcnow(), 'exp': expire, 'scope': 'refresh token'})
        encoded_refresh_token = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        Decodes the refresh token.

        :param refresh_token: The authorization refresh token.
        :type refresh_token: str
        :return: email of user.
        :rtype: str
        """
        try:
            payload = jwt.decode(refresh_token, self.__SECRET_KEY,algorithms=[self.__ALGORITHM])
            if payload['scope'] == 'refresh token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    def create_email_token(self, data: dict):
        """
        Creates token for email confirmation.

        :param data: The dict for email token.
        :type data: dict
        :return: email token.
        :rtype: str
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)
        return token

    async def get_current_user(self, token: str = Depends(_oauth2_scheme), db: Session = Depends(get_db)):
        """
        Retrieves the current user.

        :param token: user's token.
        :type token: str
        :param db: The database session.
        :type db: Session
        :return: email token.
        :rtype: str
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        try:
            payload = jwt.decode(token, self.__SECRET_KEY, algorithms=[self.__ALGORITHM])
            if payload['scope'] == 'access token':
                email = payload['sub']
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            print(e)
            raise credentials_exception
        user = self._r.get(f'user:{email}')

        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self._r.set(f'user:{email}', pickle.dumps(user))
            self._r.expire(f'user:{email}', 900)
        else:
            user = pickle.loads(user)
        return user

    async def get_email_from_token(self, token: str):
        """
        Retrieves the email of user by access token.

        :param token: user's token.
        :type token: str
        :return: user's email.
        :rtype: str
        """
        try:
            payload = jwt.decode(token, self.__SECRET_KEY, algorithms=[self.__ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()
