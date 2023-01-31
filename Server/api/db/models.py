from __future__ import annotations

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, Date, Time, ForeignKey, CheckConstraint,
    update, delete, select
)
from sqlalchemy.orm import relationship, selectinload, noload
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Any, Type
from collections.abc import Iterable
import datetime

from .access import get_engine


USERNAME_MIN_LENGTH = 2
USERNAME_MAX_LENGTH = 20

_Base = declarative_base()


class _BasicCrud:
    @classmethod
    async def _create(cls: Any, session: AsyncSession, **kwargs) -> Any:
        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)     # get id
        return instance

    @classmethod
    async def get_all_attrs(cls: Any, session: AsyncSession, id_: int) -> Union[Any, None]:
        return await session.get(cls, id_)

    @classmethod
    async def update(cls: Any, session: AsyncSession, id_: int, **kwargs) -> None:
        query = (update(cls)
                 .where(cls.id == id_)
                 .values(**kwargs)
                 .execution_options(synchronize_session='fetch'))

        await session.execute(query)
        await session.commit()

    # TODO: cascading delete on relationships? sqlalchemy doc
    @classmethod
    async def delete(cls: Any, session: AsyncSession, id_: int) -> None:
        query = (delete(cls)
                 .where(cls.id == id_)
                 .execution_options(synchronize_session='fetch'))

        await session.execute(query)
        await session.commit()


class _UserAccess:
    @classmethod
    async def create(cls: Union[Type[Admin], Type[Employee], Type[Customer]], session: AsyncSession,
                     username: str, pw_hash: str) -> Union[Admin, Employee, Customer]:
        return await cls._create(session, username=username, pw_hash=pw_hash)

    @classmethod
    async def get(cls: Union[Type[Admin], Type[Employee], Type[Customer]], session: AsyncSession,
                  id_or_name: Union[str, int]) -> Union[Admin, Employee, Customer, None]:
        query = select(cls.id, cls.username, cls.pw_hash)
        if isinstance(id_or_name, int):
            query = query.filter_by(id=id_or_name)
        elif isinstance(id_or_name, str):
            query = query.filter_by(username=id_or_name)
        else:
            raise TypeError('id or username expected')

        result = await session.execute(query)
        return result.one_or_none()

    @classmethod
    async def get_all(cls: Union[Type[Admin], Type[Employee], Type[Customer]],
                      session: AsyncSession) -> Iterable[Union[Admin, Employee, Customer]]:
        query = select(cls.id, cls.username)
        return await session.execute(query)


def _min_length_constraint(class_name: str) -> CheckConstraint:
    return CheckConstraint(
        f'CHAR_LENGTH(username) >= {USERNAME_MIN_LENGTH}',
        name=f'{class_name}_name_min_length'
    )


class Customer(_Base, _UserAccess, _BasicCrud):
    __tablename__ = 'customers'
    __table_args__ = (_min_length_constraint('customer'), )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(USERNAME_MAX_LENGTH), nullable=False, unique=True, index=True)
    pw_hash = Column(String(256), nullable=False)

    bookings = relationship('Booking', back_populates='customer', lazy='selectin')


class Admin(_Base, _UserAccess, _BasicCrud):
    __tablename__ = 'admins'
    __table_args__ = (_min_length_constraint('admin'), )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(USERNAME_MAX_LENGTH), nullable=False, unique=True, index=True)
    pw_hash = Column(String(256), nullable=False)


class Employee(_Base, _UserAccess, _BasicCrud):
    __tablename__ = 'employees'
    __table_args__ = (_min_length_constraint('employee'), )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(USERNAME_MAX_LENGTH), nullable=False, unique=True, index=True)
    pw_hash = Column(String(256), nullable=False)


class Booking(_Base, _BasicCrud):
    __tablename__ = 'bookings'
    __table_args__ = (
        CheckConstraint(f'guest_name IS NULL '
                        f'OR CHAR_LENGTH(guest_name) >= {USERNAME_MIN_LENGTH}',
                        name='guest_name_min_length'),
        CheckConstraint('(customer_id IS NOT NULL AND guest_name IS NULL) '
                        'OR (customer_id is NULL AND guest_name is NOT NULL)',
                        name='customer_guest_mutually_exclusive')
    )

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    guest_name = Column(String(USERNAME_MAX_LENGTH))

    customer_id = Column(Integer, ForeignKey('customers.id'))
    timeslot_id = Column(Integer, ForeignKey('timeslots.id'), nullable=False)
    court_id = Column(Integer, ForeignKey('courts.id'), nullable=False)

    customer = relationship('Customer', back_populates='bookings', lazy='selectin')
    timeslot = relationship('Timeslot', lazy='selectin')
    court = relationship('Court', back_populates='bookings', lazy='selectin')

    @staticmethod
    async def create(session: AsyncSession, date: datetime.date, guest_name: Union[str, None],
                     customer_id: Union[int, None], timeslot_id: int, court_id: int) -> Booking:
        return await Booking._create(session, date=date, guest_name=guest_name,
                                     customer_id=customer_id, timeslot_id=timeslot_id,
                                     court_id=court_id)

    @staticmethod
    async def get(session: AsyncSession, id_: int) -> Union[Booking, None]:
        query = select(Booking.id, Booking.date, Booking.guest_name, Booking.customer_id,
                       Booking.timeslot_id, Booking.court_id).filter_by(id=id_)
        result = await session.execute(query)
        return result.one_or_none()

    @staticmethod
    async def get_filtered(session: AsyncSession, **kwargs) -> Iterable[Booking]:
        query = select(Booking.id, Booking.date, Booking.guest_name, Booking.customer_id,
                       Booking.timeslot_id, Booking.court_id).filter_by(**kwargs)
        return await session.execute(query)

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Booking]:
        query = select(Booking.id, Booking.date, Booking.guest_name, Booking.customer_id,
                       Booking.timeslot_id, Booking.court_id)
        return await session.execute(query)

    @staticmethod
    async def get_all_attrs_filtered(session: AsyncSession, **kwargs) -> Iterable[Booking]:
        query = select(Booking).filter_by(**kwargs).options(selectinload(Booking.court).noload(Court.closings))
        return await session.scalars(query)


class Timeslot(_Base, _BasicCrud):
    __tablename__ = 'timeslots'
    __table_args__ = (
        CheckConstraint('TIMEDIFF(end, start) > 0',
                        name='duration_positive'),
    )

    id = Column(Integer, primary_key=True, index=True)
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)

    @staticmethod
    async def create(session: AsyncSession, start: datetime.time, end: datetime.time) -> Timeslot:
        return await Timeslot._create(session, start=start, end=end)

    @staticmethod
    async def get(session: AsyncSession, id_: int) -> Union[Timeslot, None]:
        query = select(Timeslot.id, Timeslot.start, Timeslot.end).filter_by(id=id_)
        result = await session.execute(query)
        return result.one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Timeslot]:
        query = select(Timeslot.id, Timeslot.start, Timeslot.end)
        return await session.execute(query)


class Court(_Base, _BasicCrud):
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 25
    SURFACE_MIN_LENGTH = 1
    SURFACE_MAX_LENGTH = 20

    __tablename__ = 'courts'
    __table_args__ = (
        CheckConstraint(f'CHAR_LENGTH(name) >= {NAME_MIN_LENGTH}',
                        name='name_min_length'),
        CheckConstraint(f'surface IS NULL OR '
                        f'CHAR_LENGTH(surface) >= {SURFACE_MIN_LENGTH}',
                        name='surface_min_length')
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(NAME_MAX_LENGTH), nullable=False)
    surface = Column(String(SURFACE_MAX_LENGTH))

    bookings = relationship('Booking', back_populates='court', lazy='selectin')
    closings = relationship('Closing', back_populates='court', lazy='selectin')

    @staticmethod
    async def create(session: AsyncSession, name: str, surface: str) -> Court:
        return await Court._create(session, name=name, surface=surface)

    @staticmethod
    async def get(session: AsyncSession, id_or_name: Union[int, str]) -> Union[Court, None]:
        query = select(Court.id, Court.name, Court.surface)
        if isinstance(id_or_name, int):
            query = query.filter_by(id=id_or_name)
        elif isinstance(id_or_name, str):
            query = query.filter_by(name=id_or_name)
        else:
            raise TypeError('id or name expected')

        result = await session.execute(query)
        return result.one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> Iterable[Court]:
        query = select(Court.id, Court.name, Court.surface)
        return await session.execute(query)


class Closing(_Base, _BasicCrud):
    __tablename__ = 'closings'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)

    start_timeslot_id = Column(Integer, ForeignKey('timeslots.id'), nullable=False)
    end_timeslot_id = Column(Integer, ForeignKey('timeslots.id'), nullable=False)
    court_id = Column(Integer, ForeignKey('courts.id'), nullable=False)

    court = relationship('Court', back_populates='closings', lazy='selectin')
    start_timeslot = relationship('Timeslot', foreign_keys=[start_timeslot_id], lazy='selectin')
    end_timeslot = relationship('Timeslot', foreign_keys=[end_timeslot_id], lazy='selectin')

    @staticmethod
    async def get(session: AsyncSession, id_: int) -> Union[Closing, None]:
        query = select(Closing.id, Closing.date, Closing.start_timeslot_id,
                       Closing.end_timeslot_id, Closing.court_id).filter_by(id=id_)
        result = await session.execute(query)
        return result.one_or_none()

    @staticmethod
    async def create(session: AsyncSession, date: datetime.date, start_timeslot_id: int,
                     end_timeslot_id: int, court_id: int) -> Closing:
        return await Closing._create(session, date=date, start_timeslot_id=start_timeslot_id,
                                     end_timeslot_id=end_timeslot_id, court_id=court_id)

    @staticmethod
    async def get_filtered(session: AsyncSession, **kwargs) -> Iterable[Closing]:
        query = (select(Closing.id, Closing.date, Closing.start_timeslot_id,
                        Closing.end_timeslot_id, Closing.court_id).filter_by(**kwargs))
        return await session.execute(query)

    @staticmethod
    async def get_all_attrs_filtered(session: AsyncSession, **kwargs) -> Iterable[Closing]:
        query = select(Closing).filter_by(**kwargs)
        return await session.scalars(query)


async def create_tables():
    async with get_engine().begin() as conn:
        await conn.run_sync(_Base.metadata.create_all)
