import pytest
from unittest.mock import patch, create_autospec
from fastapi import status

from . import CLIENT
from .. import TODAY, CUSTOMER_BOOKING, GUEST_BOOKING, CLOSING_1
from api.administration.bookings import BookingCreator, BookingManager
from api.administration.closings import ClosingCreator, ClosingManager


ROUTE = '/employee'
MODULE = 'api.routes.employee.'


@pytest.fixture
def booking_manager():
    with patch(f'{MODULE}BookingManager', autospec=True) as manager_patch:
        manager_patch.return_value = create_autospec(BookingManager)
        yield manager_patch


def test_get_bookings_for_date(booking_get_filtered):
    response = CLIENT.get(f'{ROUTE}/bookings/{str(TODAY)}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': CUSTOMER_BOOKING.id,
            'date': str(CUSTOMER_BOOKING.date),
            'timeslot_id': CUSTOMER_BOOKING.timeslot_id,
            'court_id': CUSTOMER_BOOKING.court_id,
            'guest_name': CUSTOMER_BOOKING.guest_name,
            'customer_id': CUSTOMER_BOOKING.customer_id
        },
        {
            'id': GUEST_BOOKING.id,
            'date': str(GUEST_BOOKING.date),
            'timeslot_id': GUEST_BOOKING.timeslot_id,
            'court_id': GUEST_BOOKING.court_id,
            'guest_name': GUEST_BOOKING.guest_name,
            'customer_id': GUEST_BOOKING.customer_id
        }
    ]


@patch(f'{MODULE}BookingCreator', autospec=True)
def test_add_guest_booking(booking_creator):
    booking_creator.return_value = create_autospec(BookingCreator)
    creator_create = booking_creator.return_value.create
    creator_create.return_value = GUEST_BOOKING

    guest_booking_json_in = {
        'date': str(GUEST_BOOKING.date),
        'timeslot_id': GUEST_BOOKING.timeslot_id,
        'court_id': GUEST_BOOKING.court_id,
        'guest_name': GUEST_BOOKING.guest_name
    }

    response = CLIENT.post(f'{ROUTE}/bookings', json=guest_booking_json_in)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        **guest_booking_json_in,
        'id': GUEST_BOOKING.id,
        'customer_id': GUEST_BOOKING.customer_id
    }


def test_delete_guest_booking(booking_manager):
    manager_is_guest = booking_manager.return_value.is_guest_booking
    manager_is_guest.return_value = True

    response = CLIENT.delete(f'{ROUTE}/bookings/{GUEST_BOOKING.id}')

    assert response.status_code == status.HTTP_200_OK
    booking_manager.return_value.delete.assert_awaited_once()
    assert response.json() is None


def test_delete_guest_booking_with_customer_booking(booking_manager):
    manager_is_guest = booking_manager.return_value.is_guest_booking
    manager_is_guest.return_value = False

    response = CLIENT.delete(f'{ROUTE}/bookings/{CUSTOMER_BOOKING.id}')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    booking_manager.return_value.delete.assert_not_awaited()



@patch(f'{MODULE}ClosingCreator', autospec=True)
def test_add_closing(closing_creator):
    closing_creator.return_value = create_autospec(ClosingCreator)
    creator_create = closing_creator.return_value.create
    creator_create.return_value = CLOSING_1

    closing_in_json = {
        'date': str(CLOSING_1.date),
        'start_timeslot_id': CLOSING_1.start_timeslot_id,
        'end_timeslot_id': CLOSING_1.end_timeslot_id,
        'court_id': CLOSING_1.court_id
    }

    response = CLIENT.post(f'{ROUTE}/closings/',json=closing_in_json)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        **closing_in_json,
        'id': CLOSING_1.id
    }


@patch(f'{MODULE}ClosingManager', autospec=True)
def test_delete_closing(closing_manager):
    closing_manager.return_value = create_autospec(ClosingManager)
    manager_delete = closing_manager.return_value.delete

    response = CLIENT.delete(f'{ROUTE}/closings/{CLOSING_1.id}')

    assert response.status_code == status.HTTP_200_OK
    manager_delete.assert_awaited_once()
