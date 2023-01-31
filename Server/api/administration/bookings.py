from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union
from collections.abc import Iterable
import datetime

from ..db.models import Booking, Closing
from ..exceptions import not_found, conflict
from ..schemes import GuestBookingIn, CustomerBookingIn, BookingOut, TimeslotOut, CourtOut
from . import get_court, get_timeslot


class BookingCreator:
    def __init__(self, booking: Union[GuestBookingIn, CustomerBookingIn], customer_id: Union[int, None] = None) -> None:
        self.booking = booking
        self.customer_id = customer_id
        self.timeslot: Union[TimeslotOut, None] = None
        self.court: Union[CourtOut, None] = None

    async def create(self, session: AsyncSession):
        self.timeslot = await get_timeslot(session, self.booking.timeslot_id)
        self.court = await get_court(session, self.booking.court_id)
        await self._check_closings(session)
        await self._check_bookings(session)

        self._unify_booking_types()
        new_booking = await Booking.create(
            session, self.booking.date, self.booking.guest_name, self.customer_id,
            self.booking.timeslot_id, self.booking.court_id
        )

        return _booking_out_from_booking(new_booking)

    def _unify_booking_types(self) -> None:
        if not hasattr(self.booking, 'guest_name'):
            self.booking.__dict__['guest_name'] = None

    async def _check_closings(self, session: AsyncSession) -> None:
        closings = await Closing.get_all_attrs_filtered(session, date=self.booking.date)
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

    async def get(self, session) -> BookingOut:
        await self._ensure_fetched(session)
        return _booking_out_from_booking(self.booking_db)

    async def delete(self, session: AsyncSession) -> None:
        await self._ensure_fetched(session)
        await Booking.delete(session, self.id)

    async def _ensure_fetched(self, session: AsyncSession) -> None:
        if self.booking_db is None:
            booking_db = await Booking.get(session, self.id)
            if booking_db is None:
                raise not_found('booking not found')

            self.booking_db = booking_db

    @staticmethod
    async def all_by_date(session: AsyncSession, date: datetime.date) -> Iterable[BookingOut]:
        bookings = await Booking.get_filtered(session, date=date)
        return (BookingOut(
            id=booking.id, date=booking.date, guest_name=booking.guest_name, customer_id=booking.customer_id,
            timeslot_id=booking.timeslot_id, court_id=booking.court_id
        ) for booking in bookings)


def _booking_out_from_booking(booking: Booking) -> BookingOut:
    return BookingOut(
        id=booking.id, date=booking.date, guest_name=booking.guest_name, customer_id=booking.customer_id,
        timeslot_id=booking.timeslot_id, court_id=booking.court_id
    )