from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any, Optional, Union
from datetime import datetime, timedelta

from .exceptions import INCOMPLETE_CREDENTIALS_EXCEPTION, INVALID_CREDENTIALS_EXCEPTION
from ..db.users import get_user
from ..schemes.user import UserInternal, UserFromToken


# TODO: implement better way to store the settings

with open('api/security/settings.txt') as settings:
    KEY = settings.readline().rstrip()
    ALGORITHM = settings.readline().rstrip()

_BCRYPT_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
_OAUTH2_BEARER = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(username: str, password: str,
                            session: AsyncSession) -> UserInternal:
    user = await get_user(session, username)
    if user is None:
        raise INVALID_CREDENTIALS_EXCEPTION

    if not _verify_password(password, user.pw_hash):
        raise INVALID_CREDENTIALS_EXCEPTION

    return user


def user_from_token(token: str = Depends(_OAUTH2_BEARER)) -> UserFromToken:
    try:
        payload = jwt.decode(token, KEY, ALGORITHM)
        username = payload.get('sub')
        user_id = payload.get('id')
        role = payload.get('role')

        if username is None or user_id is None:
            raise INCOMPLETE_CREDENTIALS_EXCEPTION

        return UserFromToken(
            id=user_id, username=username, role=role
        )

    except JWTError:
        raise INVALID_CREDENTIALS_EXCEPTION


def create_access_token(user: UserFromToken, expires_delta: Optional[timedelta] = None) -> str:
    encode = {
        'sub': user.username,
        'id': user.id,
        'role': user.role,
        'exp': (datetime.utcnow() + expires_delta if expires_delta is not None
                else datetime.utcnow() + timedelta(minutes=10))
    }

    return jwt.encode(encode, KEY, ALGORITHM)


def get_password_hash(password: str) -> str:
    return _BCRYPT_CONTEXT.hash(password)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return _BCRYPT_CONTEXT.verify(plain_password, hashed_password)
