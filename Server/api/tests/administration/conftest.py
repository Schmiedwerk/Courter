import pytest
from unittest.mock import patch

from api.db.models import Base, Closing, Booking
from . import TODAY, ID, COURT, TIMESLOT_1, TIMESLOT_2, CUSTOMER_BOOKING


@pytest.fixture
def base_save():
    def set_id_on_save(self, session):
        self.id = ID

    with patch.object(Base, 'save', autospec=True) as base_save_patch:
        base_save_patch.side_effect = set_id_on_save
        yield base_save_patch


@pytest.fixture
def closing_get_filtered_no_conflict():
    with patch.object(Closing, 'get_filtered', autospec=True) as get_filtered_patch:
        get_filtered_patch.return_value = tuple()
        yield get_filtered_patch


@pytest.fixture
def closing_get_filtered_conflict(closing_get_filtered_no_conflict):
    closing = Closing(
        date=TODAY,
        start_timeslot_id=TIMESLOT_1.id,
        end_timeslot_id=TIMESLOT_2.id,
        court_id=COURT.id
    )
    closing.id = ID
    closing.start_timeslot = TIMESLOT_1
    closing.end_timeslot = TIMESLOT_2
    closing_get_filtered_no_conflict.return_value = (closing,)

    return closing_get_filtered_no_conflict


@pytest.fixture
def booking_get_filtered_no_conflict():
    with patch.object(Booking, 'get_filtered', autospec=True) as get_filtered_patch:
        get_filtered_patch.return_value = tuple()
        yield get_filtered_patch


@pytest.fixture
def booking_get_filtered_conflict(booking_get_filtered_no_conflict):
    booking_get_filtered_no_conflict.return_value = (CUSTOMER_BOOKING,)
    return booking_get_filtered_no_conflict
