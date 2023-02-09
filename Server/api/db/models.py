from __future__ import annotations

from sqlalchemy import (
    Integer, String, Time, ForeignKey, CheckConstraint, select
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, selectinload
)
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Optional, Type
from collections.abc import Iterable
import datetime

from .access import get_engine


USERNAME_MIN_LENGTH = 2
USERNAME_MAX_LENGTH = 16


class Base(DeclarativeBase):
    async def save(self, session: AsyncSession) -> None:
        session.add(self)
        await session.commit()

    async def delete(self, session: AsyncSession) -> None:
        await session.delete(self)
        await session.commit()


def _min_length_constraint(class_name: str) -> CheckConstraint:
    return CheckConstraint(
        f'CHAR_LENGTH(username) >= {USERNAME_MIN_LENGTH}',
        name=f'{class_name}_name_min_length'
    )


class _User:
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(256))

    def __init__(self, username: str, password_hash: str) -> None:
        super().__init__(username=username, password_hash=password_hash)

    @classmethod
    async def _get(cls: Union[Type[Admin], Type[Employee], Type[Customer]], session: AsyncSession,
                   id_or_name: Union[str, int], *, loading_options=None) -> Union[Admin, Employee, Customer, None]:
        query = select(cls) if loading_options is None else select(cls).options(loading_options)

        if isinstance(id_or_name, int):
            query = query.filter_by(id=id_or_name)
        elif isinstance(id_or_name, str):
            query = query.filter_by(username=id_or_name)
        else:
            raise TypeError('int or str expected')

        result = await session.scalars(query)
        return result.one_or_none()

    @classmethod
    async def _get_all(cls: Union[Type[Admin], Type[Employee], Type[Customer]], session: AsyncSession, *,
                       loading_options=None) -> Iterable[Union[Admin, Employee, Customer]]:
        query = select(cls) if loading_options is None else select(cls).options(loading_options)
        return await session.scalars(query)


class Admin(_User, Base):
    __table_args__ = (_min_length_constraint('admin'),)
    __tablename__ = 'admins'

    @staticmethod
    async def get(session: AsyncSession, id_or_name: Union[str, int]) -> Union[Admin, None]:
        return await Admin._get(session, id_or_name)

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Admin]:
        return await Admin._get_all(session)


class Employee(_User, Base):
    __table_args__ = (_min_length_constraint('employee'),)
    __tablename__ = 'employees'

    @staticmethod
    async def get(session: AsyncSession, id_or_name: Union[str, int]) -> Union[Employee, None]:
        return await Employee._get(session, id_or_name)

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Employee]:
        return await Employee._get_all(session)


class Customer(_User, Base):
    __tablename__ = 'customers'
    __table_args__ = (_min_length_constraint('customer'),)

    bookings: Mapped[list[Booking]] = relationship(
        back_populates='customer',
        lazy='raise',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        passive_deletes=True
    )

    @staticmethod
    async def get(session: AsyncSession, id_or_name: Union[str, int],
                  load_bookings: bool = False) -> Union[Customer, None]:
        return await Customer._get(
            session,
            id_or_name,
            loading_options=selectinload(Customer.bookings) if load_bookings else None
        )

    @staticmethod
    async def get_all(session: AsyncSession, load_bookings: bool = False) -> Iterable[Customer]:
        return await Customer._get_all(
            session,
            loading_options=selectinload(Customer.bookings) if load_bookings else None
        )


class Booking(Base):
    __tablename__ = 'bookings'
    __table_args__ = (
        CheckConstraint(f'guest_name IS NULL '
                        f'OR CHAR_LENGTH(guest_name) >= {USERNAME_MIN_LENGTH}',
                        name='guest_name_min_length'),
        CheckConstraint('(customer_id IS NOT NULL AND guest_name IS NULL) '
                        'OR (customer_id is NULL AND guest_name is NOT NULL)',
                        name='customer_guest_mutually_exclusive')
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime.date] = mapped_column(index=True)
    guest_name: Mapped[Optional[str]] = mapped_column(String(USERNAME_MAX_LENGTH))

    customer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('customers.id', ondelete='cascade'))
    timeslot_id: Mapped[int] = mapped_column(ForeignKey('timeslots.id', ondelete='cascade'))
    court_id: Mapped[int] = mapped_column(ForeignKey('courts.id', ondelete='cascade'))

    customer: Mapped[Customer] = relationship(back_populates='bookings', lazy='joined', innerjoin=True)
    timeslot: Mapped[Timeslot] = relationship(lazy='joined', innerjoin=True)
    court: Mapped[Court] = relationship(lazy='joined', innerjoin=True)

    def __init__(self, date: datetime.date, timeslot_id: int, court_id: int,
                 guest_name: Optional[str] = None, customer_id: Optional[str] = None) -> None:
        Base.__init__(
            self, date=date, guest_name=guest_name, customer_id=customer_id,
            timeslot_id=timeslot_id, court_id=court_id
        )

    @staticmethod
    async def get(session: AsyncSession, id_: int) -> Union[Booking, None]:
        return await session.get(Booking, id_)

    @staticmethod
    async def get_filtered(session: AsyncSession, **filters) -> Iterable[Booking]:
        query = select(Booking).filter_by(**filters)
        return await session.scalars(query)

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Booking]:
        query = select(Booking)
        return await session.scalars(query)


class Timeslot(Base):
    __tablename__ = 'timeslots'
    __table_args__ = (
        CheckConstraint('TIMEDIFF(end, start) > 0',
                        name='duration_positive'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    start: Mapped[datetime.time]
    end: Mapped[datetime.time]

    def __init__(self, start: datetime.time, end: datetime.time) -> None:
        Base.__init__(self, start=start, end=end)

    @staticmethod
    async def get(session: AsyncSession, id_: int) -> Union[Timeslot, None]:
        return await session.get(Timeslot, id_)

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Timeslot]:
        query = select(Timeslot)
        return await session.scalars(query)


class Court(Base):
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 16
    SURFACE_MIN_LENGTH = 1
    SURFACE_MAX_LENGTH = 16

    __tablename__ = 'courts'
    __table_args__ = (
        CheckConstraint(f'CHAR_LENGTH(name) >= {NAME_MIN_LENGTH}',
                        name='name_min_length'),
        CheckConstraint(f'surface IS NULL OR '
                        f'CHAR_LENGTH(surface) >= {SURFACE_MIN_LENGTH}',
                        name='surface_min_length')
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), unique=True)
    surface: Mapped[Optional[str]] = mapped_column(String(SURFACE_MAX_LENGTH))

    def __init__(self, name: str, surface: Optional[str] = None) -> None:
        Base.__init__(self, name=name, surface=surface)

    @staticmethod
    async def get(session: AsyncSession, id_or_name: Union[int, str]) -> Union[Court, None]:
        if isinstance(id_or_name, int):
            return await session.get(Court, id_or_name)

        if isinstance(id_or_name, str):
            result = await session.scalars(select(Court))
            return result.one_or_none()

        raise TypeError('int or str expected')

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Court]:
        query = select(Court)
        return await session.scalars(query)


class Closing(Base):
    __tablename__ = 'closings'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime.date] = mapped_column(index=True)

    start_timeslot_id: Mapped[int] = mapped_column(ForeignKey('timeslots.id'))
    end_timeslot_id: Mapped[int] = mapped_column(ForeignKey('timeslots.id'))
    court_id: Mapped[int] = mapped_column(ForeignKey('courts.id'))

    court: Mapped[Court] = relationship('Court', lazy='joined', innerjoin=True)
    start_timeslot: Mapped[Timeslot] = relationship(
        foreign_keys=[start_timeslot_id],
        lazy='joined',
        innerjoin=True
    )
    end_timeslot: Mapped[Timeslot] = relationship(
        foreign_keys=[end_timeslot_id],
        lazy='joined',
        innerjoin=True
    )

    def __init__(self, date: datetime.date, start_timeslot_id: int, end_timeslot_id: int, court_id: int) -> None:
        Base.__init__(
            self, date=date, start_timeslot_id=start_timeslot_id,
            end_timeslot_id=end_timeslot_id, court_id=court_id
        )

    @staticmethod
    async def get(session: AsyncSession, id_: int) -> Union[Closing, None]:
        return await session.get(Closing, id_)

    @staticmethod
    async def get_filtered(session: AsyncSession, **filters) -> Iterable[Closing]:
        query = select(Closing).filter_by(**filters)
        return await session.scalars(query)

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Closing]:
        query = select(Closing)
        return await session.scalars(query)


async def create_tables():
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
