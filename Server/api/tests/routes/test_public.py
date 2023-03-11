from unittest.mock import patch
from fastapi import status

from . import CLIENT
from .. import TODAY, COURT_1, COURT_2, TIMESLOT_1, TIMESLOT_2, CLOSING_1, CLOSING_2
from api.db.models import Court, Timeslot, Closing


ROUTE = '/public'


@patch.object(Court, 'get_all', autospec=True)
def test_get_courts(get_all_patch):
    get_all_patch.return_value = (COURT_1, COURT_2)
    response = CLIENT.get(f'{ROUTE}/courts')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': COURT_1.id,
            'name': COURT_1.name,
            'surface': COURT_1.surface
        },
        {
            'id': COURT_2.id,
            'name': COURT_2.name,
            'surface': COURT_2.surface
        }
    ]

@patch.object(Timeslot, 'get_all', autospec=True)
def test_get_timeslots(get_all_patch):
    get_all_patch.return_value = (TIMESLOT_1, TIMESLOT_2)
    response = CLIENT.get(f'{ROUTE}/timeslots')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': TIMESLOT_1.id,
            'start': str(TIMESLOT_1.start),
            'end': str(TIMESLOT_1.end)
        },
        {
            'id': TIMESLOT_2.id,
            'start': str(TIMESLOT_2.start),
            'end': str(TIMESLOT_2.end)
        }
    ]


@patch.object(Closing, 'get_filtered', autospec=True)
def test_get_closings_for_date(get_filtered_patch):
    get_filtered_patch.return_value = (CLOSING_1, CLOSING_2)
    response = CLIENT.get(f'{ROUTE}/closings/{str(TODAY)}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': CLOSING_1.id,
            'date': str(CLOSING_1.date),
            'start_timeslot_id': CLOSING_1.start_timeslot_id,
            'end_timeslot_id': CLOSING_1.end_timeslot_id,
            'court_id': CLOSING_1.court_id
        },
        {
            'id': CLOSING_2.id,
            'date': str(CLOSING_2.date),
            'start_timeslot_id': CLOSING_2.start_timeslot_id,
            'end_timeslot_id': CLOSING_2.end_timeslot_id,
            'court_id': CLOSING_2.court_id
        }
    ]
