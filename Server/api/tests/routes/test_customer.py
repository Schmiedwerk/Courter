import pytest
from unittest.mock import patch, create_autospec
from fastapi import status

from . import CLIENT
from .. import TODAY, CUSTOMER_BOOKING, GUEST_BOOKING
from api.administration.bookings import BookingCreator, BookingManager


ROUTE = '/customer'
MODULE = 'api.routes.customer.'


@pytest.fixture
def booking_manager():
    with patch(f'{MODULE}BookingManager', autospec=True) as booking_manager:
        booking_manager.return_value = create_autospec(BookingManager)
        yield booking_manager


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
            'date': str(GUEST_BOOKING.date),
            'timeslot_id': GUEST_BOOKING.timeslot_id,
            'court_id': GUEST_BOOKING.court_id
        }
    ]


@patch(f'{MODULE}BookingCreator', autospec=True)
def test_add_booking(booking_creator):
    booking_creator.return_value = create_autospec(BookingCreator)
    creator_create = booking_creator.return_value.create
    creator_create.return_value = CUSTOMER_BOOKING
    booking_json_in = {
        'date': str(CUSTOMER_BOOKING.date),
        'timeslot_id': CUSTOMER_BOOKING.timeslot_id,
        'court_id': CUSTOMER_BOOKING.court_id
    }

    response = CLIENT.post(f'{ROUTE}/bookings', json=booking_json_in)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': CUSTOMER_BOOKING.id,
        'guest_name': CUSTOMER_BOOKING.guest_name,
        'customer_id': CUSTOMER_BOOKING.customer_id,
        **booking_json_in
    }


def test_delete_own_booking(booking_manager):
    manager_get = booking_manager.return_value.get
    manager_get.return_value = CUSTOMER_BOOKING

    response = CLIENT.delete(f'{ROUTE}/bookings/{CUSTOMER_BOOKING.id}')

    assert response.status_code == status.HTTP_200_OK
    booking_manager.return_value.delete.assert_awaited_once()


def test_delete_someone_elses_booking(booking_manager):
    manager_get = booking_manager.return_value.get
    manager_get.return_value = GUEST_BOOKING

    response = CLIENT.delete(f'{ROUTE}/bookings/{GUEST_BOOKING.id}')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    booking_manager.return_value.delete.assert_not_awaited()
