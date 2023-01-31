from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.access import get_session
from ..db.models import Timeslot, Court

from ..schemes import CourtOut, TimeslotOut


ROUTER = APIRouter(prefix='/public', tags=['public'])


@ROUTER.get('/courts')
async def get_all_courts(session: AsyncSession = Depends(get_session)) -> list[CourtOut]:
    courts = await Court.get_all(session)
    return [CourtOut(id=court.id, name=court.name, surface=court.surface) for court in courts]


@ROUTER.get('/timeslots')
async def get_all_timeslots(session: AsyncSession = Depends(get_session)) -> list[TimeslotOut]:
    timeslots = await Timeslot.get_all(session)
    return [TimeslotOut(id=timeslot.id, start=timeslot.start, end=timeslot.end) for timeslot in timeslots]
