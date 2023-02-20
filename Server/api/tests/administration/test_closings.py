import datetime

import pytest
from unittest.mock import patch

from . import TODAY, ID, TIMESLOT_1, TIMESLOT_2, COURT
from api.schemes.closing import ClosingIn
from api.db.models import Closing
from api.exceptions import bad_request, conflict

from api.administration.closings import ClosingCreator, CLOSING_SPAN


MODULE = 'api.administration.closings.'


@pytest.fixture
def get_court():
    with patch(f'{MODULE}get_court', autospec=True) as get_court_patch:
        get_court_patch.return_value = COURT
        yield get_court_patch


@pytest.fixture
def get_timeslot():
    with patch(f'{MODULE}get_timeslot', autospec=True) as get_timeslot_patch:
        get_timeslot_patch.side_effect = (TIMESLOT_1, TIMESLOT_2)
        yield get_timeslot_patch


async def test_create_closing(base_save, get_court, get_timeslot, closing_get_filtered_no_conflict,
                              booking_get_filtered_no_conflict, session):
    closing_in = ClosingIn(
        date=TODAY, start_timeslot_id=TIMESLOT_1.id, end_timeslot_id=TIMESLOT_2.id, court_id=COURT.id
    )

    closing_target = Closing(**closing_in.dict())
    closing_target.id = ID

    creator = ClosingCreator(closing_in)
    new_closing = await creator.create(session)

    base_save.assert_called_once()
    assert new_closing == closing_target


@pytest.mark.parametrize(
    'closing_in',
    [
        ClosingIn(
            date=TODAY - datetime.timedelta(days=1),
            start_timeslot_id=TIMESLOT_1.id, end_timeslot_id=TIMESLOT_2.id, court_id=COURT.id
        ),
        ClosingIn(
            date=TODAY + CLOSING_SPAN + datetime.timedelta(days=1),
            start_timeslot_id=TIMESLOT_1.id, end_timeslot_id=TIMESLOT_2.id, court_id=COURT.id
        )
    ]
)
async def test_create_closing_bad_date(closing_in, get_timeslot, get_court, session):
    with pytest.raises(type(bad_request())):
        creator = ClosingCreator(closing_in)
        await creator.create(session)


async def test_create_closing_bad_timeslots(get_timeslot, get_court, session):
    # TIMESLOT_2 starts after TIMESLOT_1
    get_timeslot.side_effect = [TIMESLOT_2, TIMESLOT_1]
    closing_in = ClosingIn(
        date=TODAY, start_timeslot_id=TIMESLOT_2.id, end_timeslot_id=TIMESLOT_1.id, court_id=COURT.id
    )

    with pytest.raises(type(bad_request())):
        creator = ClosingCreator(closing_in)
        await creator.create(session)


@pytest.mark.parametrize(
    'closing_in, timeslots',
    [
        (ClosingIn(date=TODAY, start_timeslot_id=TIMESLOT_1.id, end_timeslot_id=TIMESLOT_1.id, court_id=COURT.id),
         [TIMESLOT_1, TIMESLOT_1]),
        (ClosingIn(date=TODAY, start_timeslot_id=TIMESLOT_2.id, end_timeslot_id=TIMESLOT_2.id, court_id=COURT.id),
         [TIMESLOT_2, TIMESLOT_2])
    ]
)
async def test_create_closing_closing_conflict(
        closing_in, timeslots, get_timeslot, get_court, closing_get_filtered_conflict,
        booking_get_filtered_no_conflict, session):
    # closing_get_filtered_conflict returns a closing from TIMESLOT_1 to TIMESLOT_2
    get_timeslot.side_effect = timeslots

    with pytest.raises(type(conflict())):
        creator = ClosingCreator(closing_in)
        await creator.create(session)


async def test_create_closing_booking_conflict(
        get_timeslot, get_court, closing_get_filtered_no_conflict, booking_get_filtered_conflict, session):
    closing_in = ClosingIn(
        date=TODAY, start_timeslot_id=TIMESLOT_1.id, end_timeslot_id=TIMESLOT_2.id, court_id=COURT.id
    )

    with pytest.raises(type(conflict())):
        creator = ClosingCreator(closing_in)
        await creator.create(session)
