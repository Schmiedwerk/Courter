from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Type

from .db.models import Admin, Employee, Customer
from .db.users import user_exists, role_from_class

from .security import get_password_hash
from .exceptions import USERNAME_UNAVAILABLE_EXCEPTION, bad_request, not_found
from .schemes import UserIn, UserOut, UserFromToken


def make_account_manager(user: Union[UserFromToken, UserIn, int],
                         cls: Union[Type[Admin], Type[Employee], Type[Customer]] = None):
    if cls is None:
        if user.role == role_from_class(Admin):
            return _AdminManager(user)
        if user.role == role_from_class(Employee):
            return _AccountManager(Employee, user)
        if user.role == role_from_class(Customer):
            return _AccountManager(Customer, user)

    if cls is Admin:
        return _AdminManager(user)
    else:
        return _AccountManager(cls, user)


class _AccountManager:
    def __init__(self, cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                 user: Union[UserIn, UserFromToken, int]) -> None:
        self.cls = cls
        self.user_arg = user
        self.user_db: Union[Admin, Employee, Customer, None] = None

    async def create(self, session: AsyncSession) -> UserOut:
        username_unavailable = await user_exists(session, self.user_arg.username)
        if username_unavailable:
            raise USERNAME_UNAVAILABLE_EXCEPTION

        pw_hash = get_password_hash(self.user_arg.password)
        self.user_db = await self.cls.create(session, self.user_arg.username, pw_hash)

        return self._user_out_from_user()

    async def get(self, session: AsyncSession) -> UserOut:
        await self._ensure_fetched(session)
        return self._user_out_from_user()

    async def update_username(self, session: AsyncSession, new_username: str) -> UserOut:
        await self._ensure_fetched(session)
        await self.cls.update(session, self.user_db.id, username=new_username)
        await self._refetch(session)
        return self._user_out_from_user()

    async def update_password(self, session: AsyncSession, new_password: str) -> UserOut:
        await self._ensure_fetched(session)
        new_pw_hash = get_password_hash(new_password)
        await self.cls.update(session, self.user_arg.id, pw_hash=new_pw_hash)
        await self._refetch(session)
        return self._user_out_from_user()

    async def delete(self, session: AsyncSession) -> None:
        await self._ensure_fetched(session)
        await self.cls.delete(session, self.user_db.id)
        self.user_db = None

    async def _ensure_fetched(self, session: AsyncSession) -> None:
        if self.user_db is None:
            user_id = self.user_arg if isinstance(self.user_arg, int) else self.user_arg.id
            self.user_db = await self.cls.get(session, user_id)

            if self.user_db is None:
                raise not_found(detail='user not found')

    async def _refetch(self, session: AsyncSession) -> None:
        self.user_db = None
        await self._ensure_fetched(session)

    def _user_out_from_user(self) -> UserOut:
        return UserOut(id=self.user_db.id, username=self.user_db.username)


class _AdminManager(_AccountManager):
    def __init__(self, admin: Union[UserIn, UserFromToken, int]):
        _AccountManager.__init__(self, Admin, admin)

    async def delete(self, session: AsyncSession) -> None:
        # make sure this is not the only admin
        admins = await Admin.get_all(session)
        count = sum(1 for admin in admins)
        if count < 2:
            raise bad_request('deletion of only admin disallowed')

        await _AccountManager.delete(self, session)
