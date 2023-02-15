from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import Engine, select, text
from sqlalchemy.orm import Session

from api.db import access


def test_init_db_access(setup_db):
    check_instances(AsyncEngine, AsyncSession)


async def test_db_access(setup_db):
    async for session in access.get_session():
        result = await session.scalars(select(text('1')))
        assert result.one() == 1


def test_init_db_sync(setup_db_sync):
    check_instances(Engine, Session)


def test_db_access_sync(setup_db_sync):
    with access.get_session_cls()() as session:
        result = session.scalars(select(text('1'))).one()
        assert result == 1


def check_instances(target_engine, target_session):
    engine = access.get_engine()
    session_cls = access.get_session_cls()
    assert isinstance(engine, target_engine)
    assert isinstance(session_cls(), target_session)
