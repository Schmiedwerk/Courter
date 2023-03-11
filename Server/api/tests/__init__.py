import datetime
from copy import copy

from api.db.models import Timeslot, Court, Booking, Closing, Admin, Employee, Customer


TODAY = datetime.date.today()
_OPENING_HOUR = 10
NOW = datetime.datetime.combine(TODAY, datetime.time(hour=_OPENING_HOUR, minute=30))

ID = 1
PASSWORD = 'fake_password'
HASH = 'fake_hash'

GUEST = 'guest1'
ADMIN_NAME = 'admin1'
ADMIN_ROLE = 'admin'
EMPLOYEE_NAME = 'employee1'
EMPLOYEE_ROLE = 'employee'
CUSTOMER_NAME = 'customer1'
CUSTOMER_ROLE = 'customer'

ADMIN = Admin(ADMIN_NAME, HASH)
ADMIN.id = ID

EMPLOYEE = Employee(EMPLOYEE_NAME, HASH)
EMPLOYEE.id = ID

CUSTOMER = Customer(CUSTOMER_NAME, HASH)
CUSTOMER.id = ID

TIMESLOT_PAST_TIME = Timeslot(
    start=datetime.time(hour=_OPENING_HOUR),
    end=datetime.time(hour=_OPENING_HOUR + 1)
)
TIMESLOT_PAST_TIME.id = ID

TIMESLOT_1 = Timeslot(
    start=datetime.time(hour=_OPENING_HOUR + 1),
    end=datetime.time(hour=_OPENING_HOUR + 2)
)
TIMESLOT_1.id = TIMESLOT_PAST_TIME.id + 1

TIMESLOT_2 = Timeslot(
    start=datetime.time(hour=_OPENING_HOUR + 2),
    end=datetime.time(hour=_OPENING_HOUR + 3)
)
TIMESLOT_2.id = TIMESLOT_1.id + 1


COURT_1 = Court(name='court1', surface='surface1')
COURT_1.id = ID

COURT_2 = Court(name='court2', surface='surface2')
COURT_2.id = COURT_1.id + 1

CLOSING_1 = Closing(
    date=TODAY,
    start_timeslot_id=TIMESLOT_1.id,
    end_timeslot_id=TIMESLOT_2.id,
    court_id=COURT_1.id
)
CLOSING_1.id = ID
CLOSING_1.start_timeslot = TIMESLOT_1
CLOSING_1.end_timeslot = TIMESLOT_2

CLOSING_2 = Closing(
    date=TODAY,
    start_timeslot_id=TIMESLOT_2.id,
    end_timeslot_id=TIMESLOT_2.id,
    court_id= COURT_2.id
)
CLOSING_2.id = CLOSING_1.id + 1

CUSTOMER_BOOKING = Booking(
        date=TODAY,
        timeslot_id=TIMESLOT_1.id,
        court_id=COURT_1.id,
        guest_name=None,
        customer_id=ID
)
CUSTOMER_BOOKING.id = ID
CUSTOMER_BOOKING.timeslot = TIMESLOT_1

GUEST_BOOKING = copy(CUSTOMER_BOOKING)
GUEST_BOOKING.customer_id = None
GUEST_BOOKING.guest_name = GUEST
