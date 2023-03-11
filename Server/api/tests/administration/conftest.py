import pytest
from unittest.mock import patch
import datetime

from api.db.models import Closing, Booking
from .. import NOW, CLOSING_1, CUSTOMER_BOOKING


@pytest.fixture
def datetime_datetime():
    with patch.object(datetime, 'datetime', autospec=True) as datetime_patch:
        datetime_patch.now.return_value = NOW
        yield datetime_patch


@pytest.fixture
def closing_get_filtered_empty():
    with patch.object(Closing, 'get_filtered', autospec=True) as get_filtered_patch:
        get_filtered_patch.return_value = tuple()
        yield get_filtered_patch


@pytest.fixture
def closing_get_filtered_single(closing_get_filtered_empty):
    closing_get_filtered_empty.return_value = (CLOSING_1,)
    return closing_get_filtered_empty


@pytest.fixture
def booking_get_filtered_empty():
    with patch.object(Booking, 'get_filtered', autospec=True) as get_filtered_patch:
        get_filtered_patch.return_value = tuple()
        yield get_filtered_patch


@pytest.fixture
def booking_get_filtered_single(booking_get_filtered_empty):
    booking_get_filtered_empty.return_value = (CUSTOMER_BOOKING,)
    return booking_get_filtered_empty
