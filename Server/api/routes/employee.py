from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import datetime

from ..db.access import get_session
from ..db.models import Employee

from ..administration.bookings import BookingCreator, BookingManager
from ..administration.closings import ClosingCreator, ClosingManager
from ..security import user_from_token, validate_role
from ..exceptions import bad_request
from ..schemes import UserFromToken, GuestBookingIn, BookingOut, ClosingIn, ClosingOut


async def _validate_employee(user: UserFromToken = Depends(user_from_token)) -> UserFromToken:
    return validate_role(Employee, user)

ROUTER = APIRouter(
    prefix='/employee',
    tags=['employee'],
    dependencies=[Depends(_validate_employee)]
)


@ROUTER.get('/bookings/{date}')
async def get_bookings_for_date(date: datetime.date,
                                    session: AsyncSession = Depends(get_session)) -> list[BookingOut]:
    return list(await BookingManager.all_by_date(session, date))


@ROUTER.post('/bookings', status_code=status.HTTP_201_CREATED)
async def add_guest_booking(booking: GuestBookingIn, session: AsyncSession = Depends(get_session)) -> BookingOut:
    return await BookingCreator(booking).create(session)


@ROUTER.delete('/bookings/{booking_id}')
async def delete_guest_booking(booking_id: int, session: AsyncSession = Depends(get_session)) -> None:
    manager = BookingManager(booking_id)
    is_guest_booking = await manager.is_guest_booking(session)
    if not is_guest_booking:
        raise bad_request('booking is not a guest booking')

    await manager.delete(session)


@ROUTER.get('/closings/{date}')
async def get_closings_for_date(date: datetime.date,
                                    session: AsyncSession = Depends(get_session)) -> list[ClosingOut]:
    return list(await ClosingManager.all_by_date(session, date))


@ROUTER.post('/closings', status_code=status.HTTP_201_CREATED)
async def add_closing(closing: ClosingIn, session: AsyncSession = Depends(get_session)) -> ClosingOut:
    return await ClosingCreator(closing).create(session)


@ROUTER.delete('/closings/{closing_id}')
async def delete_closing(closing_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await ClosingManager(closing_id).delete(session)
