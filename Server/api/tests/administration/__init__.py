import datetime
from copy import copy

from api.db.models import Timeslot, Court, Booking


ID = 1
GUEST = 'guest1'
DT_NOW = datetime.datetime.now()
TODAY = DT_NOW.date()
NOW = DT_NOW.time()


TIMESLOT_1 = Timeslot(
    start=(DT_NOW + datetime.timedelta(hours=1)).time(),
    end=(DT_NOW + datetime.timedelta(hours=2)).time()
)
TIMESLOT_1.id = ID

TIMESLOT_2 = Timeslot(
    start=(DT_NOW + datetime.timedelta(hours=2)).time(),
    end=(DT_NOW + datetime.timedelta(hours=3)).time()
)
TIMESLOT_2.id = TIMESLOT_1.id + 1

COURT = Court(
    name='court1',
    surface='surface1'
)
COURT.id = ID

CUSTOMER_BOOKING = Booking(
        date=TODAY,
        timeslot_id=TIMESLOT_1.id,
        court_id=COURT.id,
        guest_name=None,
        customer_id=ID
)
CUSTOMER_BOOKING.id = ID
CUSTOMER_BOOKING.timeslot = TIMESLOT_1

GUEST_BOOKING = copy(CUSTOMER_BOOKING)
GUEST_BOOKING.customer_id = None
GUEST_BOOKING.guest_name = GUEST
