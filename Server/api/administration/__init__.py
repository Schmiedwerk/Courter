from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Timeslot, Court
from ..exceptions import not_found


async def get_timeslot(session: AsyncSession, timeslot_id: int) -> Timeslot:
    timeslot = await Timeslot.get(session, timeslot_id)
    if timeslot is None:
        raise not_found('timeslot not found')
    return timeslot


async def get_court(session: AsyncSession, court_id: int) -> Court:
    court = await Court.get(session, court_id)
    if court is None:
        raise not_found('court not found')
    return court
