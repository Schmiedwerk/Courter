from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.access import get_session
from ..db.models import Timeslot, Court

from ..schemes import CourtOut, TimeslotOut


ROUTER = APIRouter(prefix='/public', tags=['public'])


@ROUTER.get('/courts', response_model=list[CourtOut])
async def get_courts(session: AsyncSession = Depends(get_session)) -> list[Court]:
    courts = await Court.get_all(session)
    return list(courts)


@ROUTER.get('/timeslots', response_model=list[TimeslotOut])
async def get_timeslots(session: AsyncSession = Depends(get_session)) -> list[Timeslot]:
    timeslots = await Timeslot.get_all(session)
    return list(timeslots)
