from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.access import get_session
from ..db.models import Admin
from ..db.users import role_from_class

from ..administration import make_account_manager
from ..security import user_from_token
from ..security.exceptions import ROLE_EXCEPTION

from ..schemes.user import UserIn, UserOut, UserFromToken


def _validate_admin(user: UserFromToken = Depends(user_from_token)):
    if user.role != role_from_class(Admin):
        raise ROLE_EXCEPTION
    return user


ROUTER = APIRouter(prefix='/admin', tags=['admin'], dependencies=[Depends(_validate_admin)])


@ROUTER.get('/admin')
async def get_all_admins(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
    admins = await Admin.get_all(session)
    return [UserOut(id=admin.id, username=admin.username) for admin in admins]


@ROUTER.post('/admin', status_code=status.HTTP_201_CREATED)
async def create_admin(user: UserIn, session: AsyncSession = Depends(get_session)) -> UserOut:
    return await make_account_manager(user, Admin).create(session)


@ROUTER.delete('/admin/{admin_id}')
async def delete_admin(admin_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await make_account_manager(admin_id, Admin).delete(session)