from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import timedelta

from ..db.access import get_session
from ..db.models import Customer
from ..auth import authenticate_user
from ..auth.token import create_access_token
from ..administration.accounts import create_account
from ..schemes import UserInternal, AccessToken, UserIn, UserOut


ROUTER = APIRouter(tags=['login'])


@ROUTER.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_session)) -> AccessToken:
    print(form_data.username, form_data.password)
    user: UserInternal = await authenticate_user(form_data.username, form_data.password, session)
    token = create_access_token(user, expires_delta=timedelta(minutes=20))

    return AccessToken(access_token=token, token_type='bearer')


@ROUTER.post('/signup', response_model=UserOut)
async def sign_up(user: UserIn, session: AsyncSession = Depends(get_session)) -> Customer:
    # only customers can create an account this way
    customer = await create_account(session, Customer, user)
    return UserOut(id=customer.id, username=customer.username)
