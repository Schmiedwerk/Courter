from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Type

from .users import role_from_class, user_exists
from ..db.models import Admin, Employee, Customer
from ..auth import get_password_hash
from ..exceptions import USERNAME_UNAVAILABLE_EXCEPTION, bad_request, not_found
from ..schemes import UserIn, UserFromToken


def make_account_manager(user: Union[UserFromToken, UserIn, int],
                         cls: Union[Type[Admin], Type[Employee], Type[Customer]] = None) -> _AccountManager:
    if cls is None:
        if user.role == role_from_class(Admin):
            return _AdminManager(user)
        if user.role == role_from_class(Employee):
            return _AccountManager(Employee, user)
        if user.role == role_from_class(Customer):
            return _AccountManager(Customer, user)

    if cls is Admin:
        return _AdminManager(user)

    return _AccountManager(cls, user)


async def create_account(session: AsyncSession, cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                         user: UserIn) -> Union[Admin, Employee, Customer]:
    username_unavailable = await user_exists(session, user.username)
    if username_unavailable:
        raise USERNAME_UNAVAILABLE_EXCEPTION

    password_hash = get_password_hash(user.password)
    new_user = cls(user.username, password_hash)
    await new_user.save(session)

    return new_user


class _AccountManager:
    def __init__(self, cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                 user: Union[UserFromToken, int]) -> None:
        self.cls = cls
        self.user = user
        self.user_db: Union[Admin, Employee, Customer, None] = None

    async def get(self, session: AsyncSession) -> Union[Admin, Employee, Customer]:
        await self._ensure_fetched(session)
        return self.user_db

    async def update_username(self, session: AsyncSession, new_username: str) -> Union[Admin, Employee, Customer]:
        await self._ensure_fetched(session)
        self.user_db.username = new_username
        await self.user_db.save(session)
        return self.user_db

    async def update_password(self, session: AsyncSession, new_password: str) -> Union[Admin, Employee, Customer]:
        await self._ensure_fetched(session)
        new_pw_hash = get_password_hash(new_password)
        self.user_db.password_hash = new_pw_hash
        await self.user_db.save(session)
        return self.user_db

    async def delete(self, session: AsyncSession) -> None:
        await self._ensure_fetched(session)
        await self.user_db.delete(session)
        self.user_db = None

    async def _ensure_fetched(self, session: AsyncSession) -> None:
        if self.user_db is None:
            user_id = self.user if isinstance(self.user, int) else self.user.id
            self.user_db = await self.cls.get(session, user_id)

            if self.user_db is None:
                raise not_found(detail=f'user with id {user_id} not found')

    async def _refetch(self, session: AsyncSession) -> None:
        self.user_db = None
        await self._ensure_fetched(session)


class _AdminManager(_AccountManager):
    def __init__(self, admin: Union[UserIn, UserFromToken, int]):
        _AccountManager.__init__(self, Admin, admin)

    async def delete(self, session: AsyncSession) -> None:
        # make sure this is not the only admin
        admins = await Admin.get_all(session)
        count = sum(1 for _ in admins)
        if count < 2:
            raise bad_request('deletion of only admin disallowed')

        await _AccountManager.delete(self, session)
