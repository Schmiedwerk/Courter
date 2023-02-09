from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import datetime

from ..db.access import get_session
from ..db.models import Employee, Booking, Closing

from ..administration.bookings import BookingCreator, BookingManager
from ..administration.closings import ClosingCreator, ClosingManager
from ..auth import user_from_token, validate_role
from ..exceptions import bad_request
from ..schemes import UserFromToken, GuestBookingIn, BookingOut, ClosingIn, ClosingOut


async def _validate_employee(user: UserFromToken = Depends(user_from_token)) -> UserFromToken:
    return validate_role(Employee, user)

ROUTER = APIRouter(
    prefix='/employee',
    tags=['employee'],
    dependencies=[Depends(_validate_employee)]
)


@ROUTER.get('/bookings/{date}', response_model=list[BookingOut])
async def get_bookings_for_date(date: datetime.date,
                                session: AsyncSession = Depends(get_session)) -> list[Booking]:
    bookings = await Booking.get_filtered(session, date=date)
    return  list(bookings)


@ROUTER.post('/bookings', status_code=status.HTTP_201_CREATED, response_model=BookingOut)
async def add_guest_booking(booking: GuestBookingIn, session: AsyncSession = Depends(get_session)) -> Booking:
    return await BookingCreator(booking).create(session)


@ROUTER.delete('/bookings/{booking_id}')
async def delete_guest_booking(booking_id: int, session: AsyncSession = Depends(get_session)) -> None:
    manager = BookingManager(booking_id)
    is_guest_booking = await manager.is_guest_booking(session)
    if not is_guest_booking:
        raise bad_request('booking is not a guest booking')

    await manager.delete(session)


@ROUTER.get('/closings/{date}', response_model=list[ClosingOut])
async def get_closings_for_date(date: datetime.date,
                                session: AsyncSession = Depends(get_session)) -> list[Closing]:
    closings = await Closing.get_filtered(session, date=date)
    return list(closings)


@ROUTER.post('/closings', status_code=status.HTTP_201_CREATED, response_model=ClosingOut)
async def add_closing(closing: ClosingIn, session: AsyncSession = Depends(get_session)) -> Closing:
    return await ClosingCreator(closing).create(session)


@ROUTER.delete('/closings/{closing_id}')
async def delete_closing(closing_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await ClosingManager(closing_id).delete(session)
