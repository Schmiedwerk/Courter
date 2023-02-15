from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from typing import Type, Union

from ..db.models import Admin, Employee, Customer
from ..administration.users import get_user, role_from_class
from .exceptions import (
    INCOMPLETE_CREDENTIALS_EXCEPTION, INVALID_CREDENTIALS_EXCEPTION, ROLE_EXCEPTION, INVALID_TOKEN_EXCEPTION
)
from ..schemes.user import UserInternal, UserFromToken

_BCRYPT_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def authenticate_user(username: str, password: str,
                            session: AsyncSession) -> UserInternal:
    user = await get_user(session, username)
    if user is None:
        raise INVALID_CREDENTIALS_EXCEPTION

    if not _verify_password(password, user.pw_hash):
        raise INVALID_CREDENTIALS_EXCEPTION

    return user


def validate_role(cls: Union[Type[Admin], Type[Employee], Type[Customer]], user: UserFromToken) -> UserFromToken:
    if user.role != role_from_class(cls):
        raise ROLE_EXCEPTION

    return user


def get_password_hash(password: str) -> str:
    return _BCRYPT_CONTEXT.hash(password)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return _BCRYPT_CONTEXT.verify(plain_password, hashed_password)
