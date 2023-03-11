from unittest.mock import patch
from fastapi import status

from . import CLIENT
from .. import CUSTOMER, PASSWORD
from api.schemes.user import UserInternal
from api.administration.users import role_from_class


MODULE = 'api.routes.auth.'


@patch(f'{MODULE}create_access_token', autospec=True)
@patch(f'{MODULE}authenticate_user', autospec=True)
def test_login_for_access_token(authenticate_user, create_access_token):
    authenticate_user.return_value = UserInternal(
        id=CUSTOMER.id,
        username=CUSTOMER.username,
        pw_hash=CUSTOMER.password_hash,
        role=role_from_class(type(CUSTOMER))
    )
    access_token = 'fake_token'
    create_access_token.return_value = access_token

    response = CLIENT.post(
        f'/token',
        data={'username': CUSTOMER.username, 'password': PASSWORD},
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@patch(f'{MODULE}create_account', autospec=True)
def test_sign_up(create_account):
    create_account.return_value = CUSTOMER

    response = CLIENT.post(
        '/signup',
        json={
            'username': CUSTOMER.username,
            'password': PASSWORD
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': CUSTOMER.id,
        'username': CUSTOMER.username
    }
