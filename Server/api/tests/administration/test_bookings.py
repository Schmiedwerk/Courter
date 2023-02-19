import pytest
from unittest.mock import patch
import datetime

from . import TODAY, DT_NOW, NOW, ID, GUEST, TIMESLOT_1, COURT, CUSTOMER_BOOKING, GUEST_BOOKING
from api.db.models import Court, Booking
from api.schemes.booking import GuestBookingIn, CustomerBookingIn
from api.exceptions import bad_request, conflict

from api.administration.bookings import BookingCreator, BookingManager, BOOKING_SPAN


MODULE = 'api.administration.bookings.'
BOOKING_CREATOR = BookingCreator(CustomerBookingIn(date=TODAY, timeslot_id=TIMESLOT_1.id, court_id=COURT.id), ID)


@pytest.fixture
def get_court():
    with patch(f'{MODULE}get_court', autospec=True) as get_court_patch:
        get_court_patch.return_value = COURT
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
        (CustomerBookingIn(date=TODAY, timeslot_id=TIMESLOT_1.id, court_id=COURT.id), ID)
    ]
)
async def test_create_booking(booking_in, customer_id, base_save, get_timeslot, get_court,
                              closing_get_filtered_no_conflict, booking_get_filtered_no_conflict, session):
    booking_target = Booking(
        **booking_in.dict(),
        customer_id=customer_id,
    )
    booking_target.id = ID

    creator = BookingCreator(booking_in, customer_id)
    new_booking = await creator.create(session)

    base_save.assert_called_once()
    assert new_booking == booking_target


@pytest.mark.parametrize(
    'booking_in, customer_id',
    [
        (GuestBookingIn(
            date=TODAY - datetime.timedelta(days=1),
            timeslot_id=TIMESLOT_1.id, court_id=COURT.id, guest_name=GUEST
        ), None),
        (CustomerBookingIn(
            date=TODAY + BOOKING_SPAN + datetime.timedelta(days=1),
            timeslot_id=TIMESLOT_1.id, court_id=COURT.id
        ), ID),
    ]
)
async def test_create_booking_bad_date(booking_in, customer_id, get_timeslot, get_court, session):
    with pytest.raises(type(bad_request())):
        creator = BookingCreator(booking_in, customer_id)
        await creator.create(session)


async def test_create_booking_bad_timeslot(get_timeslot, get_court, session):
    timeslot = get_timeslot.return_value
    timeslot.start = (DT_NOW - datetime.timedelta(hours=1)).time()
    timeslot.end = NOW

    with pytest.raises(type(bad_request())):
        await BOOKING_CREATOR.create(session)


async def test_create_booking_closing_conflict(get_timeslot, get_court, closing_get_filtered_conflict,
                                               booking_get_filtered_no_conflict, session):
    with pytest.raises(type(conflict())):
        await BOOKING_CREATOR.create(session)


async def test_create_booking_booking_conflict(get_timeslot, get_court, closing_get_filtered_no_conflict,
                                               booking_get_filtered_conflict, session):
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
