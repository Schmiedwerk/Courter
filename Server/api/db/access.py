from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from typing import Union, Type, Optional
from collections.abc import AsyncGenerator


DB_DRIVERS = {
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


def init_db_access(dbms: str, database: str, username: Optional[str] = None, password: Optional[str] = None,
                   host: Optional[str] = None, port: Optional[int] = None, *,
                   use_async: bool = True, echo: bool = False) -> None:
    global _ENGINE, _Session

    driver = DB_DRIVERS[dbms]['async'] if use_async else DB_DRIVERS[dbms]['sync']
    database_url = f'{dbms}+{driver}://'

    options = {'echo': echo}

    if dbms == 'sqlite':
        database_url += f'/{database}'
        options['connect_args'] = {'check_same_thread': False}
    else:
        pw = f':{password}' if password is not None else ''
        database_url += f'{username}{pw}@{host}:{port}/{database}'
        if dbms == 'mysql':
            options['pool_recycle'] = 3600

    _ENGINE = (create_async_engine(database_url, **options) if use_async
               else create_engine(database_url, **options))

    _Session = (async_sessionmaker(bind=_ENGINE, expire_on_commit=False) if use_async else
                sessionmaker(bind=_ENGINE))


async def cleanup_db_access() -> None:
    if _ENGINE is not None:
        await _ENGINE.dispose()


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with _Session() as session:
        yield session


def get_engine() -> Union[AsyncEngine, Engine, None]:
    return _ENGINE


def get_session_cls() -> Union[Type[AsyncSession], Type[Session]]:
    return _Session
