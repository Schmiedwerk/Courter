from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union
import datetime

from ..db.models import Booking, Closing, Timeslot, Court
from ..exceptions import not_found, conflict, bad_request
from ..schemes import GuestBookingIn, CustomerBookingIn
from . import get_court, get_timeslot

_BOOKING_SPAN = datetime.timedelta(days=60)


class BookingCreator:
    def __init__(self, booking: Union[GuestBookingIn, CustomerBookingIn],
                 customer_id: Union[int, None] = None) -> None:
        self.booking = booking
        self.customer_id = customer_id
        self.timeslot: Union[Timeslot, None] = None
        self.court: Union[Court, None] = None

        self.today = datetime.datetime.now().date()

    async def create(self, session: AsyncSession) -> Booking:
        self.timeslot = await get_timeslot(session, self.booking.timeslot_id)
        self.court = await get_court(session, self.booking.court_id)

        self._check_date()
        self._check_time()

        await self._check_closings(session)
        await self._check_bookings(session)

        self._unify_booking_types()

        new_booking = Booking(**self.booking.dict(), customer_id=self.customer_id)
        await new_booking.save(session)

        return new_booking

    def _unify_booking_types(self) -> None:
        if not hasattr(self.booking, 'guest_name'):
            self.booking.__dict__['guest_name'] = None

    def _check_date(self):
        if not (self.today <= self.booking.date <= self.today + _BOOKING_SPAN):
            raise bad_request('invalid booking date')

    def _check_time(self):
        if self.today == self.booking.date:
            now = datetime.datetime.now().time()
            if now > self.timeslot.start:
                raise bad_request('invalid booking timeslot')

    async def _check_closings(self, session: AsyncSession) -> None:
        closings = await Closing.get_filtered(session, date=self.booking.date)
        for closing in closings:
            if (self.booking.court_id == closing.court_id and
                    closing.start_timeslot.start <= self.timeslot.start <= closing.end_timeslot.start):
                raise conflict('booking conflicts with a closing')

    async def _check_bookings(self, session: AsyncSession) -> None:
        bookings_db = await Booking.get_filtered(
            session, date=self.booking.date, timeslot_id=self.timeslot.id, court_id=self.court.id
        )
        count = sum(1 for _ in bookings_db)  # should be at most 1
        if count > 0:
            raise conflict('booking conflicts with another booking')


class BookingManager:
    def __init__(self, id_: int) -> None:
        self.id = id_
        self.booking_db: Union[Booking, None] = None

    async def is_guest_booking(self, session: AsyncSession) -> bool:
        return not await self.is_customer_booking(session)

    async def is_customer_booking(self, session: AsyncSession) -> bool:
        await self._ensure_fetched(session)
        return self.booking_db.guest_name is None

    async def get(self, session) -> Booking:
        await self._ensure_fetched(session)
        return self.booking_db

    async def delete(self, session: AsyncSession) -> None:
        await self._ensure_fetched(session)
        await self.booking_db.delete(session)

    async def _ensure_fetched(self, session: AsyncSession) -> None:
        if self.booking_db is None:
            booking_db = await Booking.get(session, self.id)
            if booking_db is None:
                raise not_found('booking not found')

            self.booking_db = booking_db
