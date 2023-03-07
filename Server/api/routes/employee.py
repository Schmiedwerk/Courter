from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import datetime

from ..db.access import get_session
from ..db.models import Employee, Booking

from ..administration.bookings import BookingCreator, BookingManager
from ..administration.closings import ClosingCreator, ClosingManager
from ..auth import validate_role
from ..auth.token import user_from_token
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
    bookings = await Booking.get_filtered(session, date=date)
    return list(BookingOut.from_orm(booking) for booking in bookings)


@ROUTER.post('/bookings', status_code=status.HTTP_201_CREATED)
async def add_guest_booking(booking: GuestBookingIn, session: AsyncSession = Depends(get_session)) -> BookingOut:
    new_booking = await BookingCreator(booking).create(session)
    return BookingOut.from_orm(new_booking)


@ROUTER.delete('/bookings/{booking_id}')
async def delete_guest_booking(booking_id: int, session: AsyncSession = Depends(get_session)) -> None:
    manager = BookingManager(booking_id)
    is_guest_booking = await manager.is_guest_booking(session)
    if not is_guest_booking:
        raise bad_request(f'booking with id {booking_id} is not a guest booking')

    await manager.delete(session)


@ROUTER.post('/closings', status_code=status.HTTP_201_CREATED)
async def add_closing(closing: ClosingIn, session: AsyncSession = Depends(get_session)) -> ClosingOut:
    new_closing = await ClosingCreator(closing).create(session)
    return ClosingOut.from_orm(new_closing)


@ROUTER.delete('/closings/{closing_id}')
async def delete_closing(closing_id: int, session: AsyncSession = Depends(get_session)) -> None:
    await ClosingManager(closing_id).delete(session)
