from pydantic import BaseModel

from .user import UserIn, UserOut, UserFromToken, UserInternal
from .court import CourtIn, CourtOut
from .timeslot import TimeslotIn, TimeslotOut
from .booking import BookingBase, GuestBookingIn, CustomerBookingIn, BookingOut
from .closing import ClosingIn, ClosingOut


class AccessToken(BaseModel):
    access_token: str
    token_type: str
