from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from typing import Union

from ..db.models import Booking, Closing, Timeslot, Court

from ..schemes import ClosingIn
from ..exceptions import conflict, bad_request
from . import get_court, get_timeslot, ManagerBase, check_date, check_time


class ClosingCreator:
    CLOSING_SPAN = datetime.timedelta(days=365)

    def __init__(self, closing: ClosingIn) -> None:
        self.closing = closing
        self.start_timeslot: Union[Timeslot, None] = None
        self.end_timeslot: Union[Timeslot, None] = None
        self.court: Union[Court, None] = None

    async def create(self, session: AsyncSession) -> Closing:
        now = datetime.datetime.now()
        self._check_date(now)
        self.start_timeslot = await get_timeslot(session, self.closing.start_timeslot_id)
        self.end_timeslot = await get_timeslot(session, self.closing.end_timeslot_id)
        self._check_timeslots(now)
        self.court = await get_court(session, self.closing.court_id)
        await self._check_bookings(session)
        await self._check_closings(session)

        new_closing = Closing(**self.closing.dict())
        await new_closing.save(session)

        return new_closing

    def _check_date(self, now: datetime.datetime):
        check_date(now=now, date_to_check=self.closing.date, date_span=self.CLOSING_SPAN, date_subject='closing')

    def _check_timeslots(self, now: datetime.datetime):
        check_time(now=now, time_to_check=self.start_timeslot.start,
                   ref_date=self.closing.date, time_subject='closing start timeslot')

        if not self.end_timeslot.start >= self.start_timeslot.start:
            raise bad_request(f'start timeslot with id {self.start_timeslot.id} after end '
                              f'timeslot with id {self.end_timeslot.id}')

    async def _check_bookings(self, session: AsyncSession) -> None:
        bookings_db = await Booking.get_filtered(
            session, date=self.closing.date, court_id=self.closing.court_id
        )

        for booking in bookings_db:
            timeslot = booking.timeslot
            if self.start_timeslot.start <= timeslot.start <= self.end_timeslot.start:
                raise conflict(f'closing conflicts with booking with id {booking.id} '
                               f'at timeslot with id {timeslot.id}')

    async def _check_closings(self, session: AsyncSession) -> None:
        closings_db = await Closing.get_filtered(
            session, date=self.closing.date, court_id=self.closing.court_id
        )

        for closing in closings_db:
            start = closing.start_timeslot.start
            end = closing.end_timeslot.start

            if start <= self.start_timeslot.start <= end or start <= self.end_timeslot.start <= end:
                raise conflict(f'closing conflicts with another closing with id {closing.id}')


class ClosingManager(ManagerBase):
    def __init__(self, id_: int) -> None:
        ManagerBase.__init__(self, Closing, id_)
