import pytest
from unittest.mock import patch, create_autospec
from fastapi import status

from . import CLIENT
from .. import ADMIN, EMPLOYEE, CUSTOMER
from api.administration.accounts import _AccountManager


ROUTE = '/account'


@pytest.fixture
def make_account_manager():
    with patch(f'api.routes.account.make_account_manager', autospec=True) as make_manager_patch:
        make_manager_patch.return_value = create_autospec(_AccountManager)
        yield make_manager_patch


def test_get_info(make_account_manager):
    make_account_manager.return_value.get.return_value = ADMIN
    response = CLIENT.get(ROUTE)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': ADMIN.id,
        'username': ADMIN.username
    }


def test_change_username(make_account_manager):
    new_username = 'new_username'
    update_username = make_account_manager.return_value.update_username
    update_username.return_value = EMPLOYEE

    response = CLIENT.put(f'{ROUTE}/username?new_username={new_username}')

    assert response.status_code == status.HTTP_200_OK
    assert update_username.call_args[0][1] == new_username
    assert response.json() == {
        'id': EMPLOYEE.id,
        'username': EMPLOYEE.username
    }


def test_change_password(make_account_manager):
    new_password = 'new_password'
    update_password = make_account_manager.return_value.update_password
    update_password.return_value = CUSTOMER

    response = CLIENT.put(f'{ROUTE}/password?new_password={new_password}')

    assert response.status_code == status.HTTP_200_OK
    assert update_password.call_args[0][1] == new_password
    assert response.json() == {
        'id': CUSTOMER.id,
        'username': CUSTOMER.username
    }


def test_delete_account(make_account_manager):
    delete = make_account_manager.return_value.delete
    delete.return_value = None

    response = CLIENT.delete(ROUTE)

    assert response.status_code == status.HTTP_200_OK
    delete.assert_called_once()
    assert response.json() is None
