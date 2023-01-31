from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Timeslot, Court
from ..schemes import TimeslotOut, CourtOut
from ..exceptions import not_found


async def get_timeslot(session: AsyncSession, timeslot_id: int) -> TimeslotOut:
    timeslot = await Timeslot.get(session, timeslot_id)
    if timeslot is None:
        raise not_found('timeslot not found')
    return TimeslotOut(id=timeslot.id, start=timeslot.start, end=timeslot.end)


async def get_court(session: AsyncSession, court_id: int) -> CourtOut:
    court = await Court.get(session, court_id)
    if court is None:
        raise not_found('court not found')
    return CourtOut(id=court.id, name=court.name, surface=court.surface)
