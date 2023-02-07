from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Type
from collections.abc import Iterable

from ..db.models import Admin, Employee, Customer
from ..db.users import user_exists, role_from_class

from ..auth import get_password_hash
from ..exceptions import USERNAME_UNAVAILABLE_EXCEPTION, bad_request, not_found
from ..schemes import UserIn, UserOut, UserFromToken


def make_account_manager(user: Union[UserFromToken, UserIn, int],
                         cls: Union[Type[Admin], Type[Employee], Type[Customer]] = None):
    if cls is None:
        if user.role == role_from_class(Admin):
            return _AdminManager(user)
        if user.role == role_from_class(Employee):
            return AccountManager(Employee, user)
        if user.role == role_from_class(Customer):
            return AccountManager(Customer, user)

    if cls is Admin:
        return _AdminManager(user)

    return AccountManager(cls, user)


class AccountCreator:
    def __init__(self, cls: Union[Type[Admin], Type[Employee], Type[Customer]], user: UserIn) -> None:
        self.cls = cls
        self.user = user

    async def create(self, session: AsyncSession) -> UserOut:
        username_unavailable = await user_exists(session, self.user.username)
        if username_unavailable:
            raise USERNAME_UNAVAILABLE_EXCEPTION

        pw_hash = get_password_hash(self.user.password)
        new_user = await self.cls.create(session, self.user.username, pw_hash)

        return AccountManager.user_out_from_user(new_user)


class AccountManager:
    def __init__(self, cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                 user: Union[UserFromToken, int]) -> None:
        self.cls = cls
        self.user = user
        self.user_db: Union[Admin, Employee, Customer, None] = None

    async def get(self, session: AsyncSession) -> UserOut:
        await self._ensure_fetched(session)
        return AccountManager.user_out_from_user(self.user_db)

    async def update_username(self, session: AsyncSession, new_username: str) -> UserOut:
        await self._ensure_fetched(session)
        await self.cls.update(session, self.user_db.id, username=new_username)
        await self._refetch(session)
        return AccountManager.user_out_from_user(self.user_db)

    async def update_password(self, session: AsyncSession, new_password: str) -> UserOut:
        await self._ensure_fetched(session)
        new_pw_hash = get_password_hash(new_password)
        await self.cls.update(session, self.user_db.id, pw_hash=new_pw_hash)
        await self._refetch(session)
        return AccountManager.user_out_from_user(self.user_db)

    async def delete(self, session: AsyncSession) -> None:
        await self._ensure_fetched(session)
        await self.cls.delete(session, self.user)
        self.user_db = None

    async def _ensure_fetched(self, session: AsyncSession) -> None:
        if self.user_db is None:
            user_id = self.user if isinstance(self.user, int) else self.user.id
            self.user_db = await self.cls.get(session, user_id)

            if self.user_db is None:
                raise not_found(detail='user not found')

    async def _refetch(self, session: AsyncSession) -> None:
        self.user_db = None
        await self._ensure_fetched(session)

    @staticmethod
    def user_out_from_user(user: Union[Admin, Employee, Customer]) -> UserOut:
        return UserOut(id=user.id, username=user.username)

    @staticmethod
    async def get_all(cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                      session: AsyncSession) -> Iterable[UserOut]:
        users = await cls.get_all(session)
        return (UserOut(id=user.id, username=user.username) for user in users)


class _AdminManager(AccountManager):
    def __init__(self, admin: Union[UserIn, UserFromToken, int]):
        AccountManager.__init__(self, Admin, admin)

    async def delete(self, session: AsyncSession) -> None:
        # make sure this is not the only admin
        admins = await Admin.get_all(session)
        count = sum(1 for _ in admins)
        if count < 2:
            raise bad_request('deletion of only admin disallowed')

        await AccountManager.delete(self, session)
