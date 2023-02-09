from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from typing import Optional, Union, Type


DB_APIS = {
    'mysql': {
        'sync' : 'pymysql',
        'async': 'aiomysql'
    },
    'postgresql': {
        'sync': 'psycopg',
        'async': 'asyncpg'
    },
    'sqlite': {
        'sync': 'pysqlite',
        'async': 'aiosqlite'
    }
}


_ENGINE: Union[AsyncEngine, Engine, None] = None
_Session: Union[Type[AsyncSession], Type[Session], None] = None


def init_dbms_access(dbms: str, db_name: str, username: str, password: str, host: str, port: int, *,
                     use_async: bool = True, echo: bool = False) -> None:
    global _ENGINE, _Session

    pw = f':{password}' if password is not None else ''
    dbapi = DB_APIS[dbms]['async'] if use_async else DB_APIS[dbms]['sync']

    database_url = f'{dbms}+{dbapi}://{username}{pw}@{host}:{port}/{db_name}'

    _ENGINE = (create_async_engine(database_url, echo=echo) if use_async
               else create_engine(database_url, echo=echo))

    _Session = sessionmaker(
        bind=_ENGINE,
        expire_on_commit=False,
        class_=AsyncSession if use_async else Session
    )


async def cleanup_db_access() -> None:
    if _ENGINE is not None:
        await _ENGINE.dispose()


async def get_session() -> AsyncSession:
    async with _Session() as session:
        yield session


def get_engine() -> Union[AsyncEngine, Engine, None]:
    return _ENGINE


def get_session_cls() -> Union[Type[AsyncSession], Type[Session]]:
    return _Session
