from pydantic import BaseModel, Field
from typing import Optional
import datetime

from .user import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH

_STARTUP_DAY = datetime.datetime.now().date()


class BookingBase(BaseModel):
    date: datetime.date
    timeslot_id: int
    court_id: int

    class Config:
        orm_mode = True


class CustomerBookingIn(BookingBase):
    class Config:
        schema_extra = {
            'example': {
                'date': _STARTUP_DAY + datetime.timedelta(days=5),
                'timeslot_id': 3,
                'court_id': 5,
            }
        }


class GuestBookingIn(CustomerBookingIn):
    guest_name: str = Field(min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH)

    class Config:
        schema_extra = {
            'example': {
                'date': _STARTUP_DAY + datetime.timedelta(days=2),
                'timeslot_id': 5,
                'court_id': 3,
                'guest_name': 'v.Rossum'
            }
        }


class BookingOut(BookingBase):
    id: int
    customer_id: Optional[int]
    guest_name: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                'date': _STARTUP_DAY + datetime.timedelta(days=10),
                'timeslot_id': 2,
                'court_id': 1,
                'guest_name': 'kThompson',
                'id': 1972,
                'customer_id': None
            }
        }
