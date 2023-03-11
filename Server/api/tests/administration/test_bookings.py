import pytest
from unittest.mock import patch
import datetime

from .. import TODAY, NOW, ID, GUEST, TIMESLOT_1, TIMESLOT_PAST_TIME, COURT_1, CUSTOMER_BOOKING, GUEST_BOOKING
from api.db.models import Booking
from api.schemes.booking import GuestBookingIn, CustomerBookingIn
from api.exceptions import bad_request, conflict

from api.administration.bookings import BookingCreator, BookingManager


MODULE = 'api.administration.bookings.'
BOOKING_CREATOR = BookingCreator(CustomerBookingIn(date=TODAY, timeslot_id=TIMESLOT_1.id, court_id=COURT_1.id), ID)


@pytest.fixture
def get_court():
    with patch(f'{MODULE}get_court', autospec=True) as get_court_patch:
        get_court_patch.return_value = COURT_1
        yield get_court_patch


@pytest.fixture
def get_timeslot():
    with patch(f'{MODULE}get_timeslot', autospec=True) as get_timeslot_patch:
        get_timeslot_patch.return_value = TIMESLOT_1
        yield get_timeslot_patch


@pytest.mark.parametrize(
    'booking_in, customer_id',
    [
        (GuestBookingIn(date=TODAY, timeslot_id=TIMESLOT_1.id, court_id=TIMESLOT_1.id, guest_name=GUEST), None),
        (CustomerBookingIn(date=TODAY, timeslot_id=TIMESLOT_1.id, court_id=COURT_1.id), ID)
    ]
)
async def test_create_booking(booking_in, customer_id, base_save, get_timeslot, datetime_datetime, get_court,
                              closing_get_filtered_empty, booking_get_filtered_empty, session):
    booking_target = Booking(
        **booking_in.dict(),
        customer_id=customer_id,
    )
    booking_target.id = ID

    creator = BookingCreator(booking_in, customer_id)
    new_booking = await creator.create(session)

    base_save.assert_awaited_once()
    assert new_booking == booking_target


@pytest.mark.parametrize(
    'booking_in, customer_id',
    [
        (GuestBookingIn(
            date=TODAY - datetime.timedelta(days=1),
            timeslot_id=TIMESLOT_1.id, court_id=COURT_1.id, guest_name=GUEST
        ), None),
        (CustomerBookingIn(
            date=TODAY + BookingCreator.BOOKING_SPAN + datetime.timedelta(days=1),
            timeslot_id=TIMESLOT_1.id, court_id=COURT_1.id
        ), ID),
    ]
)
async def test_create_booking_bad_date(booking_in, customer_id, datetime_datetime, get_timeslot, get_court, session):
    with pytest.raises(type(bad_request())):
        creator = BookingCreator(booking_in, customer_id)
        await creator.create(session)


async def test_create_booking_bad_timeslot(datetime_datetime, get_timeslot, get_court, session):
    get_timeslot.return_value = TIMESLOT_PAST_TIME

    with pytest.raises(type(bad_request())):
        await BOOKING_CREATOR.create(session)


async def test_create_booking_closing_conflict(datetime_datetime, get_timeslot, get_court, closing_get_filtered_single,
                                               booking_get_filtered_empty, session):
    with pytest.raises(type(conflict())):
        await BOOKING_CREATOR.create(session)


async def test_create_booking_booking_conflict(datetime_datetime, get_timeslot, get_court, closing_get_filtered_empty,
                                               booking_get_filtered_single, session):
    with pytest.raises(type(conflict())):
        await BOOKING_CREATOR.create(session)


@pytest.mark.parametrize(
    'booking, truth_value',
    [
        (CUSTOMER_BOOKING, True),
        (GUEST_BOOKING, False)
    ]
)
@patch.object(Booking, 'get', autospec=True)
async def test_is_customer_booking(booking_get, booking, truth_value, session):
    booking_get.return_value = booking
    manager = BookingManager(ID)
    assert (await manager.is_customer_booking(session)) is truth_value


@pytest.mark.parametrize(
    'booking, truth_value',
    [
        (CUSTOMER_BOOKING, False),
        (GUEST_BOOKING, True)
    ]
)
@patch.object(Booking, 'get', autospec=True)
async def test_is_guest_booking(booking_get, booking, truth_value, session):
    booking_get.return_value = booking
    manager = BookingManager(ID)
    assert (await manager.is_guest_booking(session)) is truth_value
