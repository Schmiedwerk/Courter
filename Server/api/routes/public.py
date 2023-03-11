from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from ..db.access import get_session
from ..db.models import Timeslot, Court, Closing
from ..schemes import CourtOut, TimeslotOut, ClosingOut


ROUTER = APIRouter(prefix='/public', tags=['public'])


@ROUTER.get('/courts')
async def get_courts(session: AsyncSession = Depends(get_session)) -> list[CourtOut]:
    courts = await Court.get_all(session)
    return list(CourtOut.from_orm(court) for court in courts)


@ROUTER.get('/timeslots')
async def get_timeslots(session: AsyncSession = Depends(get_session)) -> list[TimeslotOut]:
    timeslots = await Timeslot.get_all(session)
    return list(TimeslotOut.from_orm(timeslot) for timeslot in timeslots)


@ROUTER.get('/closings/{date}')
async def get_closings_for_date(date: datetime.date,
                                session: AsyncSession = Depends(get_session)) -> list[ClosingOut]:
    closings = await Closing.get_filtered(session, date=date)
    return list(ClosingOut.from_orm(closing) for closing in closings)
