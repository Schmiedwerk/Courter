import pytest
from unittest.mock import patch

from .. import (
    ID, ADMIN_NAME, ADMIN_ROLE, EMPLOYEE_NAME, EMPLOYEE_ROLE, CUSTOMER_NAME, CUSTOMER_ROLE, PASSWORD, HASH
)
from api.db.models import Admin, Employee, Customer
from api.schemes import UserIn, UserFromToken
from api.exceptions import not_found, bad_request, USERNAME_UNAVAILABLE_EXCEPTION

from api.administration.accounts import create_account, make_account_manager, _AccountManager, _AdminManager


MODULE = 'api.administration.accounts.'


@pytest.fixture
def user_get():
    with patch.object(Customer, 'get', autospec=True) as customer_get_patch:
        yield customer_get_patch


@pytest.fixture
def user_db_target(user_get):
    user = Customer(CUSTOMER_NAME, HASH)
    user.id = ID
    user_get.return_value = user
    return user


@pytest.fixture
def account_manager(user_db_target):
    return _AccountManager(Customer, user_db_target.id)


@pytest.fixture
def get_password_hash():
    with patch(f'{MODULE}get_password_hash', autospec=True) as password_hash_patch:
        password_hash_patch.return_value = HASH
        yield password_hash_patch


@patch(f'{MODULE}user_exists', autospec=True)
async def test_create_account_non_existing_username(
        user_exists, user_db_target, base_save, session, get_password_hash):
    user_exists.return_value = False
    user = UserIn(username=user_db_target.username, password=PASSWORD)

    new_user = await create_account(session, type(user_db_target), user)

    base_save.assert_awaited_once()
    assert new_user == user_db_target


@patch(f'{MODULE}user_exists', autospec=True)
async def test_create_account_existing_username(
        user_exists, user_db_target, base_save, session, get_password_hash):
    user_exists.return_value = True
    user = UserIn(username=user_db_target.username, password=PASSWORD)

    with pytest.raises(type(USERNAME_UNAVAILABLE_EXCEPTION)):
        await create_account(session, type(user_db_target), user)

    get_password_hash.assert_not_called()
    base_save.assert_not_awaited()


@pytest.mark.parametrize(
    'user, cls, manager_type',
    [
        (UserFromToken(id=1, username=ADMIN_NAME, role=ADMIN_ROLE), None, _AdminManager),
        (UserFromToken(id=1, username=EMPLOYEE_NAME, role=EMPLOYEE_ROLE), None, _AccountManager),
        (UserFromToken(id=1, username=CUSTOMER_NAME, role=CUSTOMER_ROLE), None, _AccountManager),
        (1, Customer, _AccountManager)
    ]
)
@patch(f'{MODULE}role_from_class', autospec=True)
def test_make_account_manager(role_from_class, user, cls, manager_type):
    def role_from_class_patch(user_cls):
        if user_cls is Admin:
            return ADMIN_ROLE
        if user_cls is Employee:
            return EMPLOYEE_ROLE
        return CUSTOMER_ROLE

    role_from_class.side_effect = role_from_class_patch

    manager = make_account_manager(user, cls)
    assert type(manager) is manager_type


def test_make_account_manager_exception():
    with pytest.raises(TypeError):
        make_account_manager(ID)


@patch.object(Employee, 'get', autospec=True)
async def test_get_existing_user_from_token(employee_get, session):
    username = EMPLOYEE_NAME
    role = EMPLOYEE_ROLE
    user = UserFromToken(id=ID, username=username, role=role)
    user_db_target = Employee(username, HASH)
    user_db_target.id = ID
    employee_get.return_value = user_db_target

    manager = _AccountManager(Employee, user)
    user_db = await manager.get(session)

    assert user_db == user_db_target


@patch.object(Customer, 'get', autospec=True)
async def test_get_existing_user_by_id(customer_get, session):
    user_db_target = Customer(CUSTOMER_NAME, HASH)
    user_db_target.id = ID
    customer_get.return_value = user_db_target

    manager = _AccountManager(Customer, ID)
    user_db = await manager.get(session)

    assert user_db == user_db_target


@patch.object(Admin, 'get', autospec=True)
async def test_get_non_existing_user(admin_get, session):
    admin_get.return_value = None

    manager = _AccountManager(Admin, 42)
    with pytest.raises(type(not_found())):
        await manager.get(session)


async def test_update_username(base_save, account_manager, session):
    new_username = 'customer0'
    user_db = await account_manager.update_username(session, new_username)

    base_save.assert_awaited_once()
    assert user_db.username == new_username


async def test_update_password(base_save, account_manager, get_password_hash, session):
    new_hash = 'new_fake_hash'
    get_password_hash.return_value = new_hash

    user_db = await account_manager.update_password(session, 'new_fake_password')

    base_save.assert_awaited_once()
    assert user_db.password_hash == new_hash


@patch.object(Customer, 'delete', autospec=True)
async def test_delete_user(user_delete, account_manager, session):
    await account_manager.delete(session)
    user_delete.assert_called_once()


@patch.object(Admin, 'get_all', autospec=True)
async def test_delete_last_admin(admin_get_all, session):
    admin_db = Admin('root', HASH)
    admin_get_all.return_value = (admin_db,)
    manager = _AdminManager(ID)

    with pytest.raises(type(bad_request())):
        await manager.delete(session)
