from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.access import get_session
from ..db.models import Admin, Employee, Timeslot, Court

from ..administration.accounts import AccountCreator, AccountManager, make_account_manager
from ..security import user_from_token, validate_role
from ..exceptions import conflict, not_found

from ..schemes import (
    UserIn, UserOut, UserFromToken, CourtIn, CourtOut, TimeslotIn, TimeslotOut
)


async def _validate_admin(user: UserFromToken = Depends(user_from_token)) -> UserFromToken:
    return validate_role(Admin, user)


ROUTER = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(_validate_admin)]
)


@ROUTER.get('/admin')
async def get_all_admins(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
    return list(await AccountManager.get_all(Admin, session))


@ROUTER.post('/admin', status_code=status.HTTP_201_CREATED)
async def add_admin(user: UserIn, session: AsyncSession = Depends(get_session)) -> UserOut:
    return await AccountCreator(Admin, user).create(session)


@ROUTER.delete('/admin/{admin_id}')
async def delete_admin(admin_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await make_account_manager(admin_id, Admin).delete(session)


@ROUTER.get('/employee')
async def get_all_employees(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
    return list(await AccountManager.get_all(Employee, session))


@ROUTER.post('/employee', status_code=status.HTTP_201_CREATED)
async def add_employee(user: UserIn, session: AsyncSession = Depends(get_session)) -> UserOut:
    return await AccountCreator(Employee, user).create(session)


@ROUTER.delete('/employee/{employee_id}')
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await make_account_manager(employee_id, Employee).delete(session)


@ROUTER.post('/court', status_code=status.HTTP_201_CREATED)
async def add_court(court: CourtIn, session: AsyncSession = Depends(get_session)) -> CourtOut:
    court_db = await Court.get(session, court.name)
    if court_db is not None:
        raise conflict('duplicate court name')

    new_court = await Court.create(session, court.name, court.surface)
    return CourtOut(id=new_court.id, name=new_court.name, surface=new_court.surface)


@ROUTER.delete('/court/{court_id}')
async def delete_court(court_id: int, session: AsyncSession = Depends(get_session)) -> None:
    court_db = await Court.get(session, court_id)
    if court_db is None:
        raise not_found('court not found')

    await Court.delete(session, court_id)


@ROUTER.post('/timeslot', status_code=status.HTTP_201_CREATED)
async def add_timeslot(timeslot: TimeslotIn, session: AsyncSession = Depends(get_session)) -> TimeslotOut:
    if timeslot.end <= timeslot.start:
        raise conflict('end time before start time')

    # check for overlap
    timeslots_db = await Timeslot.get_all(session)
    for slot_db in timeslots_db:
        if slot_db.start < timeslot.start < slot_db.end or slot_db.start < timeslot.end < slot_db.end:
            raise conflict('overlapping timeslots disallowed')

    new_timeslot = await Timeslot.create(session, timeslot.start, timeslot.end)
    return TimeslotOut(id=new_timeslot.id, start=new_timeslot.start, end=new_timeslot.end)


@ROUTER.delete('/timeslot/{timeslot_id}')
async def delete_timeslot(timeslot_id: int, session: AsyncSession = Depends(get_session)) -> None:
    timeslot_db = await Timeslot.get(session, timeslot_id)
    if timeslot_db is None:
        raise not_found('timeslot not found')

    await Timeslot.delete(session, timeslot_id)
