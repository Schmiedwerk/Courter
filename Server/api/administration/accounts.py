from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Type

from . import ManagerBase
from .users import role_from_class, user_exists
from ..db.models import Admin, Employee, Customer
from ..auth import get_password_hash
from ..exceptions import USERNAME_UNAVAILABLE_EXCEPTION, bad_request, not_found
from ..schemes import UserIn, UserFromToken


async def create_account(session: AsyncSession, cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                         user: UserIn) -> Union[Admin, Employee, Customer]:
    username_unavailable = await user_exists(session, user.username)
    if username_unavailable:
        raise USERNAME_UNAVAILABLE_EXCEPTION

    password_hash = get_password_hash(user.password)
    new_user = cls(user.username, password_hash)
    await new_user.save(session)

    return new_user


def make_account_manager(user: Union[UserFromToken, int],
                         cls: Union[Type[Admin], Type[Employee], Type[Customer]] = None) -> _AccountManager:
    if cls is None:
        if not isinstance(user, UserFromToken):
            raise TypeError('user must be a UserFromToken if cls is None')

        if user.role == role_from_class(Admin):
            return _AdminManager(user)
        if user.role == role_from_class(Employee):
            return _AccountManager(Employee, user)
        if user.role == role_from_class(Customer):
            return _AccountManager(Customer, user)

    if cls is Admin:
        return _AdminManager(user)

    return _AccountManager(cls, user)


class _AccountManager(ManagerBase):
    def __init__(self, cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                 user: Union[UserFromToken, int]) -> None:
        user_id = user if isinstance(user, int) else user.id
        ManagerBase.__init__(self, cls, user_id)

    async def update_username(self, session: AsyncSession, new_username: str) -> Union[Admin, Employee, Customer]:
        user_db = await self.get(session)
        user_db.username = new_username
        await user_db.save(session)
        return user_db

    async def update_password(self, session: AsyncSession, new_password: str) -> Union[Admin, Employee, Customer]:
        user_db = await self.get(session)
        new_pw_hash = get_password_hash(new_password)
        user_db.password_hash = new_pw_hash
        await user_db.save(session)
        return user_db


class _AdminManager(_AccountManager):
    def __init__(self, admin: Union[UserFromToken, int]):
        _AccountManager.__init__(self, Admin, admin)

    async def delete(self, session: AsyncSession) -> None:
        # make sure this is not the only admin
        admins = await Admin.get_all(session)
        count = sum(1 for _ in admins)
        if count < 2:
            raise bad_request('deletion of only admin disallowed')

        await _AccountManager.delete(self, session)
