from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from .login import DB_LOGIN

_ENGINE: AsyncEngine = None
_AsyncSession = None


def init_db_access(dbms: str, db_name: str, echo=False) -> None:
    global _ENGINE, _AsyncSession

    dialects = {
        'mysql': 'aiomysql',
        'postgresql': 'asyncpg',
        'sqlite': 'aiosqlite'
    }
    database_url = f'{dbms}+{dialects[dbms]}://' \
                   f'{DB_LOGIN["user"]}:{DB_LOGIN["pw"]}@localhost:{DB_LOGIN["port"]}' \
                   f'/{db_name}'

    _ENGINE = create_async_engine(database_url, echo=echo)
    _AsyncSession = sessionmaker(bind=_ENGINE, expire_on_commit=False, class_=AsyncSession)


async def cleanup_db_access() -> None:
    if _ENGINE is not None:
        await _ENGINE.dispose()


def get_engine() -> AsyncEngine:
    return _ENGINE


async def get_session() -> AsyncSession:
    async with _AsyncSession() as session:
        yield session
