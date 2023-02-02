from pydantic import BaseModel, Field, validator
from typing import Optional
import datetime

from ..db.models import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH

_TODAY = datetime.datetime.now().date()
_BOOKING_SPAN = datetime.timedelta(days=60)


class Booking(BaseModel):
    date: datetime.date
    timeslot_id: int
    court_id: int


class CustomerBookingIn(Booking):
    @validator('date')
    def check_date(cls, date: datetime.date) -> datetime.date:
        if not (_TODAY <= date <= _TODAY + _BOOKING_SPAN):
            raise ValueError('invalid booking date')
        return date

    class Config:
        schema_extra = {
            'example': {
                'date': _TODAY + datetime.timedelta(days=5),
                'timeslot_id': 3,
                'court_id': 5,
            }
        }


class GuestBookingIn(CustomerBookingIn):
    guest_name: str = Field(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH)

    class Config:
        schema_extra = {
            'example': {
                'date': _TODAY + datetime.timedelta(days=2),
                'timeslot_id': 5,
                'court_id': 3,
                'guest_name': 'v.Rossum'
            }
        }


class BookingOut(Booking):
    id: int
    customer_id: Optional[int]
    guest_name: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'date': _TODAY + datetime.timedelta(days=10),
                'timeslot_id': 2,
                'court_id': 1,
                'guest_name': 'kThompson',
                'id': 1972,
                'customer_id': None
            }
        }
