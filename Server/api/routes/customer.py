from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union
import datetime

from ..db.access import get_session
from ..db.models import Customer

from ..administration.bookings import BookingCreator, BookingManager
from ..auth import user_from_token, validate_role
from ..schemes import UserFromToken, Booking, CustomerBookingIn, BookingOut
from ..exceptions import ACCESS_DENIED_EXCEPTION


async def _validate_customer(user: UserFromToken = Depends(user_from_token)) -> UserFromToken:
    return validate_role(Customer, user)

ROUTER = APIRouter(prefix='/customer', tags=['customer'])


@ROUTER.get('/bookings/{date}')
async def get_bookings_for_date(date: datetime.date, customer: UserFromToken = Depends(_validate_customer),
                                    session: AsyncSession
                                    = Depends(get_session)) -> list[Union[BookingOut, Booking]]:
    bookings = await BookingManager.all_by_date(session, date)

    return [booking if booking.customer_id == customer.id else Booking(**booking.dict()) for booking in bookings]


@ROUTER.post('/bookings', status_code=status.HTTP_201_CREATED)
async def add_booking(booking: CustomerBookingIn, customer: UserFromToken = Depends(_validate_customer),
                      session: AsyncSession = Depends(get_session)) -> BookingOut:
    return await BookingCreator(booking, customer.id).create(session)


@ROUTER.delete('/bookings/{booking_id}')
async def delete_booking(booking_id: int, customer: UserFromToken = Depends(_validate_customer),
                         session: AsyncSession = Depends(get_session)) -> None:
    manager = BookingManager(booking_id)
    booking = await manager.get(session)
    if booking.customer_id != customer.id:
        raise ACCESS_DENIED_EXCEPTION

    await manager.delete(session)
