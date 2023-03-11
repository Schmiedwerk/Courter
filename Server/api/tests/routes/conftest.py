import pytest
from unittest.mock import patch

from .. import CUSTOMER_BOOKING, GUEST_BOOKING
from api.db.models import Booking

@pytest.fixture
def booking_get_filtered():
    with patch.object(Booking, 'get_filtered', autospec=True) as booking_get_filtered:
        booking_get_filtered.return_value = (CUSTOMER_BOOKING, GUEST_BOOKING)
        yield booking_get_filtered
