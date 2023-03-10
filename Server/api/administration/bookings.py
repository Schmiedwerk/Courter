from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union
import datetime

from . import get_court, get_timeslot, ManagerBase, check_date, check_time
from ..db.models import Booking, Closing, Timeslot, Court
from ..exceptions import conflict
from ..schemes import GuestBookingIn, CustomerBookingIn


class BookingCreator:
    BOOKING_SPAN = datetime.timedelta(days=60)

    def __init__(self, booking: Union[GuestBookingIn, CustomerBookingIn],
                 customer_id: Union[int, None] = None) -> None:
        self.booking = booking
        self.customer_id = customer_id
        self.timeslot: Union[Timeslot, None] = None
        self.court: Union[Court, None] = None


    async def create(self, session: AsyncSession) -> Booking:
        now = datetime.datetime.now()
        self._check_date(now)
        self.timeslot = await get_timeslot(session, self.booking.timeslot_id)
        self._check_timeslot(now)
        self.court = await get_court(session, self.booking.court_id)

        await self._check_closings(session)
        await self._check_bookings(session)

        self._unify_booking_types()

        new_booking = Booking(**self.booking.dict(), customer_id=self.customer_id)
        await new_booking.save(session)

        return new_booking

    def _unify_booking_types(self) -> None:
        if not hasattr(self.booking, 'guest_name'):
            self.booking.__dict__['guest_name'] = None

    def _check_date(self, now: datetime.datetime):
        check_date(now=now, date_to_check=self.booking.date, date_span=self.BOOKING_SPAN, date_subject='booking')

    def _check_timeslot(self, now: datetime.datetime):
        check_time(now=now, time_to_check=self.timeslot.start,
                   ref_date=self.booking.date, time_subject='booking timeslot')

    async def _check_closings(self, session: AsyncSession) -> None:
        closings = await Closing.get_filtered(session, date=self.booking.date, court_id=self.booking.court_id)
        for closing in closings:
            if closing.start_timeslot.start <= self.timeslot.start <= closing.end_timeslot.start:
                raise conflict(f'booking conflicts with a closing from {closing.start_timeslot.start} '
                               f'to {closing.end_timeslot.end}')

    async def _check_bookings(self, session: AsyncSession) -> None:
        bookings_db = await Booking.get_filtered(
            session, date=self.booking.date, timeslot_id=self.timeslot.id, court_id=self.court.id
        )
        count = sum(1 for _ in bookings_db)  # should be at most 1
        if count > 0:
            raise conflict('booking conflicts with another booking')


class BookingManager(ManagerBase):
    def __init__(self, id_: int) -> None:
        ManagerBase.__init__(self, Booking, id_)

    async def is_guest_booking(self, session: AsyncSession) -> bool:
        return not await self.is_customer_booking(session)

    async def is_customer_booking(self, session: AsyncSession) -> bool:
        booking_db = await self.get(session)
        return booking_db.guest_name is None
