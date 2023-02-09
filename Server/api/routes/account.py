from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union

from ..db.access import get_session
from ..db.models import Admin, Employee, Customer

from ..administration.accounts import make_account_manager
from ..auth.token import user_from_token
from ..schemes.user import (
    UserOut, UserFromToken, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH,
    PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
)


ROUTER = APIRouter(prefix='/account', tags=['account'])


@ROUTER.get('', response_model=UserOut)
async def get_info(user: UserFromToken = Depends(user_from_token),
                   session: AsyncSession = Depends(get_session)) -> Union[Admin, Employee, Customer]:
    return await make_account_manager(user).get(session)


@ROUTER.put('/username', response_model=UserOut)
async def change_username(new_username: str = Query(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH),
                          user: UserFromToken = Depends(user_from_token),
                          session: AsyncSession = Depends(get_session)) -> Union[Admin, Employee, Customer]:
    return await make_account_manager(user).update_username(session, new_username)


@ROUTER.put('/password', response_model=UserOut)
async def change_password(new_password: str = Query(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH),
                          user: UserFromToken = Depends(user_from_token),
                          session: AsyncSession = Depends(get_session)) -> Union[Admin, Employee, Customer]:
    return await make_account_manager(user).update_password(session, new_password)


@ROUTER.delete('')
async def delete_account(user: UserFromToken = Depends(user_from_token),
                         session: AsyncSession = Depends(get_session)) -> None:
    return await make_account_manager(user).delete(session)
