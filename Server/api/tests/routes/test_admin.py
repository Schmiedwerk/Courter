import pytest
from unittest.mock import patch, create_autospec
from fastapi import status

from . import CLIENT
from .. import ID, ADMIN, EMPLOYEE, PASSWORD, COURT_1, TIMESLOT_1, TIMESLOT_2
from api.db.models import Base, Admin, Employee, Court, Timeslot
from api.administration.accounts import _AccountManager


ROUTE = '/admin'
MODULE = 'api.routes.admin.'


@pytest.fixture
def make_account_manager():
    with patch(f'{MODULE}make_account_manager', autospec=True) as make_manager_patch:
        make_manager_patch.return_value = create_autospec(_AccountManager)
        yield make_manager_patch


@pytest.fixture
def account_manager_delete(make_account_manager):
    manager_delete = make_account_manager.return_value.delete
    manager_delete.return_value = None
    return make_account_manager



@pytest.fixture
def court_get():
    with patch.object(Court, 'get', autospec=True) as court_get:
        yield court_get


@pytest.fixture
def timeslot_get_all():
    with patch.object(Timeslot, 'get_all', autospec=True) as timeslot_get_all:
        yield timeslot_get_all


@pytest.fixture
def timeslot_get():
    with patch.object(Timeslot, 'get', autospec=True) as timeslot_get:
        yield timeslot_get


@pytest.fixture
def base_delete():
    with patch.object(Base, 'delete', autospec=True) as base_delete:
        yield base_delete


@patch.object(Admin, 'get_all', autospec=True)
def test_get_admins(admin_get_all):
    admin_get_all.return_value = (ADMIN,)

    response = CLIENT.get(f'{ROUTE}/admins')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': ADMIN.id,
            'username': ADMIN.username
        }
    ]

@patch(f'{MODULE}create_account', autospec=True)
def test_add_admin(create_account):
    create_account.return_value = ADMIN

    response = CLIENT.post(
        f'{ROUTE}/admins',
        json={
            'username': ADMIN.username,
            'password': PASSWORD
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': ADMIN.id,
        'username': ADMIN.username
    }


def test_delete_admin(account_manager_delete):
    response = CLIENT.delete(f'{ROUTE}/admins/{ADMIN.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None


@patch.object(Employee, 'get_all', autospec=True)
def test_get_employees(employee_get_all):
    employee_get_all.return_value = (EMPLOYEE,)

    response = CLIENT.get(f'{ROUTE}/employees')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': EMPLOYEE.id,
            'username': EMPLOYEE.username
        }
    ]


@patch(f'{MODULE}create_account', autospec=True)
def test_add_employee(create_account):
    create_account.return_value = EMPLOYEE

    response = CLIENT.post(
        f'{ROUTE}/employees',
        json={
            'username': EMPLOYEE.username,
            'password': PASSWORD
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': EMPLOYEE.id,
        'username': EMPLOYEE.username
    }


def test_delete_employee(account_manager_delete):
    response = CLIENT.delete(f'{ROUTE}/employees/{EMPLOYEE.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None


def test_add_court_no_conflict(court_get, base_save):
    court_get.return_value = None
    court_json_in = {
        'name': COURT_1.name,
        'surface': COURT_1.surface
    }

    response = CLIENT.post(f'{ROUTE}/courts', json=court_json_in)

    assert response.status_code == status.HTTP_201_CREATED
    base_save.assert_awaited_once()
    assert response.json() == {
        'id': ID,
        **court_json_in
    }


def test_add_court_conflict(court_get, base_save):
    court_get.return_value = COURT_1

    response = CLIENT.post(
        f'{ROUTE}/courts',
        json={
            'name': COURT_1.name,
            'surface': COURT_1.surface
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    base_save.assert_not_awaited()


def test_delete_existing_court(court_get, base_delete):
    court_get.return_value = COURT_1

    response = CLIENT.delete(f'{ROUTE}/courts/{COURT_1.id}')

    assert response.status_code == status.HTTP_200_OK
    base_delete.assert_awaited_once()


def test_delete_non_existing_court(court_get, base_delete):
    court_get.return_value = None

    response = CLIENT.delete(f'{ROUTE}/courts/{COURT_1.id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    base_delete.assert_not_awaited()


def test_add_valid_timeslot_no_conflict(timeslot_get_all, base_save):
    timeslot_get_all.return_value = (TIMESLOT_1,)
    timeslot_json_in = {
        'start': str(TIMESLOT_2.start),
        'end': str(TIMESLOT_2.end)
    }

    response = CLIENT.post(f'{ROUTE}/timeslots', json=timeslot_json_in)

    assert response.status_code == status.HTTP_201_CREATED
    base_save.assert_awaited_once()
    assert response.json() == {
        'id': ID,
        **timeslot_json_in
    }


def test_add_valid_timeslot_conflict(timeslot_get_all, base_save):
    timeslot_get_all.return_value = (TIMESLOT_1,)

    response = CLIENT.post(
        f'{ROUTE}/timeslots',
        json={
            'start': str(TIMESLOT_1.start),
            'end': str(TIMESLOT_1.end)
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    base_save.assert_not_awaited()


def test_add_invalid_timeslot(timeslot_get_all, base_save):
    timeslot_get_all.return_value = tuple()

    response = CLIENT.post(
        f'{ROUTE}/timeslots',
        json={
            'start': str(TIMESLOT_1.end),
            'end': str(TIMESLOT_1.start)
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    base_save.assert_not_awaited()


def test_delete_existing_timeslot(timeslot_get, base_delete):
    timeslot_get.return_value = TIMESLOT_1

    response = CLIENT.delete(f'{ROUTE}/timeslots/{TIMESLOT_1.id}')

    assert response.status_code == status.HTTP_200_OK
    base_delete.assert_awaited_once()


def test_delete_non_existing_timeslot(timeslot_get, base_delete):
    timeslot_get.return_value = None

    response = CLIENT.delete(f'{ROUTE}/timeslots/{TIMESLOT_1.id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    base_delete.assert_not_awaited()
