from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union

from ..db.models import Booking, Closing, Timeslot, Court

from ..schemes import ClosingIn
from ..exceptions import conflict, bad_request, not_found
from . import get_court, get_timeslot


class ClosingCreator:
    def __init__(self, closing: ClosingIn) -> None:
        self.closing = closing
        self.start_timeslot: Union[Timeslot, None] = None
        self.end_timeslot: Union[Timeslot, None] = None
        self.court: Union[Court, None] = None

    async def create(self, session: AsyncSession) -> Closing:
        self.start_timeslot = await get_timeslot(session, self.closing.start_timeslot_id)
        self.end_timeslot = await get_timeslot(session, self.closing.end_timeslot_id)
        self._check_timeslots()
        self.court = await get_court(session, self.closing.court_id)
        await self._check_bookings(session)
        await self._check_closings(session)

        new_closing = Closing(**self.closing.dict())
        await new_closing.save(session)

        return new_closing

    def _check_timeslots(self):
        if not self.end_timeslot.start >= self.start_timeslot.start:
            raise bad_request('start timeslot after end timeslot')

    async def _check_bookings(self, session: AsyncSession) -> None:
        bookings_db = await Booking.get_filtered(
            session, date=self.closing.date, court_id=self.closing.court_id
        )

        for booking in bookings_db:
            timeslot = booking.timeslot
            if self.start_timeslot.start <= timeslot.start <= self.end_timeslot.start:
                raise conflict('closing conflicts with booking')

    async def _check_closings(self, session: AsyncSession) -> None:
        closings_db = await Closing.get_filtered(
            session, date=self.closing.date, court_id=self.closing.court_id
        )

        for closing in closings_db:
            start = closing.start_timeslot.start
            end = closing.end_timeslot.start

            if start <= self.start_timeslot.start <= end or start <= self.end_timeslot.start <= end:
                raise conflict('closing conflicts with another closing')


class ClosingManager:
    def __init__(self, id_: int) -> None:
        self.id = id_
        self.closing_db: Union[Closing, None] = None

    async def get(self, session: AsyncSession) -> Closing:
        await self._ensure_fetched(session)
        return self.closing_db

    async def delete(self, session: AsyncSession) -> None:
        await self._ensure_fetched(session)
        await self.closing_db.delete(session)

    async def _ensure_fetched(self, session: AsyncSession) -> None:
        if self.closing_db is None:
            closing_db = await Closing.get(session, self.id)
            if closing_db is None:
                raise not_found('closing not found')

            self.closing_db = closing_db
