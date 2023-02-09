from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, Type

from ..db.models import Admin, Employee, Customer
from ..schemes import UserInternal


def role_from_class(cls: Union[Type[Admin], Type[Employee], Type[Customer]]) -> str:
    return cls.__name__.lower()


async def get_user(session: AsyncSession, username: str) -> Union[UserInternal, None]:
    for cls in Customer, Employee, Admin:
        user = await cls.get(session, username)

        if user is not None:
            return UserInternal(
                id=user.id, username=user.username, pw_hash=user.password_hash, role=role_from_class(cls)
            )

    return None


async def user_exists(session: AsyncSession, username: str) -> bool:
    user = await get_user(session, username)
    if user is None:
        return False
    return True
