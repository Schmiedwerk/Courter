from datetime import timedelta, datetime
from typing import Optional

from decouple import config
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api.auth import INCOMPLETE_CREDENTIALS_EXCEPTION, INVALID_TOKEN_EXCEPTION
from api.schemes import UserFromToken


_ALGORITHM = 'HS256'
_KEY = config('KEY')


def create_access_token(user: UserFromToken, expires_delta: Optional[timedelta] = None) -> str:
    encode = {
        'sub': user.username,
        'id': user.id,
        'role': user.role,
        'exp': (datetime.utcnow() + expires_delta if expires_delta is not None
                else datetime.utcnow() + timedelta(minutes=10))
    }

    return jwt.encode(encode, _KEY, _ALGORITHM)


_OAUTH2_BEARER = OAuth2PasswordBearer(tokenUrl='token')


async def user_from_token(token: str = Depends(_OAUTH2_BEARER)) -> UserFromToken:
    try:
        payload = jwt.decode(token, _KEY, _ALGORITHM)
        username = payload.get('sub')
        user_id = payload.get('id')
        role = payload.get('role')

        if username is None or user_id is None:
            raise INCOMPLETE_CREDENTIALS_EXCEPTION

        return UserFromToken(
            id=user_id, username=username, role=role
        )

    except JWTError:
        raise INVALID_TOKEN_EXCEPTION
