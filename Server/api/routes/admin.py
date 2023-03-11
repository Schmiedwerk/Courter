from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..administration.accounts import make_account_manager, create_account
from ..db.access import get_session
from ..db.models import Admin, Employee, Timeslot, Court
from ..exceptions import conflict, not_found, bad_request
from ..schemes import (
    UserIn, UserOut, UserFromToken, CourtIn, CourtOut, TimeslotIn, TimeslotOut
)
from ..auth import validate_role
from ..auth.token import user_from_token


async def _validate_admin(user: UserFromToken = Depends(user_from_token)) -> UserFromToken:
    return validate_role(Admin, user)


ROUTER = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(_validate_admin)]
)


@ROUTER.get('/admins')
async def get_admins(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
    admins = await Admin.get_all(session)
    return list(UserOut.from_orm(admin) for admin in admins)


@ROUTER.post('/admins', status_code=status.HTTP_201_CREATED)
async def add_admin(user: UserIn, session: AsyncSession = Depends(get_session)) -> UserOut:
    admin = await create_account(session, Admin, user)
    return UserOut.from_orm(admin)


@ROUTER.delete('/admins/{admin_id}')
async def delete_admin(admin_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await make_account_manager(admin_id, Admin).delete(session)


@ROUTER.get('/employees')
async def get_employees(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
    employees = await Employee.get_all(session)
    return list(UserOut.from_orm(employee) for employee in employees)


@ROUTER.post('/employees', status_code=status.HTTP_201_CREATED)
async def add_employee(user: UserIn, session: AsyncSession = Depends(get_session)) -> UserOut:
    employee = await create_account(session, Employee, user)
    return UserOut.from_orm(employee)


@ROUTER.delete('/employees/{employee_id}')
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await make_account_manager(employee_id, Employee).delete(session)


@ROUTER.post('/courts', status_code=status.HTTP_201_CREATED)
async def add_court(court: CourtIn, session: AsyncSession = Depends(get_session)) -> CourtOut:
    court_db = await Court.get(session, court.name)
    if court_db is not None:
        raise conflict(f"duplicate court name '{court.name}'")

    new_court = Court(court.name, court.surface)
    await new_court.save(session)

    return CourtOut.from_orm(new_court)


@ROUTER.delete('/courts/{court_id}')
async def delete_court(court_id: int, session: AsyncSession = Depends(get_session)) -> None:
    court_db = await Court.get(session, court_id)
    if court_db is None:
        raise not_found(f'court with id {court_id} not found')

    await court_db.delete(session)


@ROUTER.post('/timeslots', status_code=status.HTTP_201_CREATED, response_model=TimeslotOut)
async def add_timeslot(timeslot: TimeslotIn, session: AsyncSession = Depends(get_session)) -> Timeslot:
    if timeslot.end <= timeslot.start:
        raise bad_request('end time before start time')

    # check for conflicting timeslots
    timeslots_db = await Timeslot.get_all(session)
    for slot_db in timeslots_db:
        if not (slot_db.end <= timeslot.start or timeslot.end <= slot_db.start):
            raise conflict(
                f'timeslot conflicts with existing timeslot with id {slot_db.id} ({slot_db.start} - {slot_db.end})'
            )

    new_timeslot = Timeslot(timeslot.start, timeslot.end)
    await new_timeslot.save(session)

    return new_timeslot


@ROUTER.delete('/timeslots/{timeslot_id}')
async def delete_timeslot(timeslot_id: int, session: AsyncSession = Depends(get_session)) -> None:
    timeslot_db = await Timeslot.get(session, timeslot_id)
    if timeslot_db is None:
        raise not_found(f'timeslot with id {timeslot_id} not found')

    await timeslot_db.delete(session)
