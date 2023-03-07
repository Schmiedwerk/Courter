from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import datetime

from ..db.access import get_session
from ..db.models import Timeslot, Court, Closing

from ..schemes import CourtOut, TimeslotOut, ClosingOut


ROUTER = APIRouter(prefix='/public', tags=['public'])


@ROUTER.get('/courts', response_model=list[CourtOut])
async def get_courts(session: AsyncSession = Depends(get_session)) -> list[Court]:
    courts = await Court.get_all(session)
    return list(courts)


@ROUTER.get('/timeslots', response_model=list[TimeslotOut])
async def get_timeslots(session: AsyncSession = Depends(get_session)) -> list[Timeslot]:
    timeslots = await Timeslot.get_all(session)
    return list(timeslots)


@ROUTER.get('/closings/{date}')
async def get_closings_for_date(date: datetime.date,
                                session: AsyncSession = Depends(get_session)) -> list[ClosingOut]:
    closings = await Closing.get_filtered(session, date=date)
    return list(ClosingOut.from_orm(closing) for closing in closings)
