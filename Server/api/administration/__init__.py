from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional
import datetime

from ..db.models import Timeslot, Court
from ..exceptions import not_found, bad_request


async def get_timeslot(session: AsyncSession, timeslot_id: int) -> Timeslot:
    timeslot = await Timeslot.get(session, timeslot_id)
    if timeslot is None:
        raise not_found(f'timeslot with id {timeslot_id} not found')
    return timeslot


async def get_court(session: AsyncSession, court_id: int) -> Court:
    court = await Court.get(session, court_id)
    if court is None:
        raise not_found(f'court with id {court_id} not found')
    return court


class ManagerBase:
    def __init__(self, cls: Any, id_: int) -> None:
        self.cls = cls
        self.id = id_
        self.resource_db = None

    async def get(self, session: AsyncSession) -> Any:
        await self._ensure_fetched(session)
        return self.resource_db

    async def delete(self, session: AsyncSession) -> None:
        await self._ensure_fetched(session)
        await self.resource_db.delete(session)

    async def _ensure_fetched(self, session: AsyncSession) -> None:
        if self.resource_db is None:
            resource_db = await self.cls.get(session, self.id)
            if resource_db is None:
                raise not_found(f'{self.cls.__name__.lower()} with id {self.id} not found')

            self.resource_db = resource_db


def check_date(now: datetime.datetime, date_to_check: datetime.date,
               date_span: datetime.timedelta, date_subject: str) -> None:
    today = now.date()
    if not (today <= date_to_check <= today + date_span):
        raise bad_request(
            f"invalid {date_subject} date '{date_to_check}' ({date_subject} span: {date_span.days} days)"
        )


def check_time(now: datetime.datetime, time_to_check: datetime.time,
               ref_date: datetime.date, time_subject: str) -> None:
    today = now.date()
    curr_time = now.time()
    if today == ref_date and curr_time > time_to_check:
        raise bad_request(f"invalid {time_subject} with start time '{time_to_check}'")
