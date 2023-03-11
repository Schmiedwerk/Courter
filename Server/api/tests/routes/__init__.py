from fastapi.testclient import TestClient
from unittest.mock import create_autospec

from sqlalchemy.ext.asyncio import AsyncSession

from .. import ID
from api.main import APP
from api.db.access import get_session
from api.schemes.user import UserFromToken
from api.auth.token import user_from_token
from api.routes.admin import _validate_admin
from api.routes.employee import _validate_employee
from api.routes.customer import _validate_customer


async def override_get_session():
    return create_autospec(AsyncSession)


async def override_user_from_token():
    return create_autospec(UserFromToken)


async def override_validate_user():
    user = create_autospec(UserFromToken)
    user.id = ID
    return user


APP.dependency_overrides[get_session] = override_get_session
APP.dependency_overrides[user_from_token] = override_user_from_token
APP.dependency_overrides[_validate_admin] = override_validate_user
APP.dependency_overrides[_validate_employee] = override_validate_user
APP.dependency_overrides[_validate_customer] = override_validate_user

CLIENT = TestClient(APP)
