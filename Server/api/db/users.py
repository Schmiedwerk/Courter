from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Union

from .models import Customer, Employee, Admin
from ..schemes.user import UserInternal


async def get_user(session: AsyncSession, username: str) -> Union[UserInternal, None]:
    for cls in Customer, Employee, Admin:
        info = await cls.get(session, username)

        if info is not None:
            return UserInternal(
                id=info.id, username=info.username, pw_hash=info.pw_hash, role=role_from_class(cls)
            )

    return None


async def user_exists(session: AsyncSession, username: str) -> bool:
    user = await get_user(session, username)
    if user is None:
        return False
    return True


def role_from_class(cls: Any) -> str:
    return cls.__name__.lower()
