import pytest

from api.db import access


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def setup_db(anyio_backend):
    access.init_db_access('sqlite', ':memory:')
    yield
    await access.cleanup_db_access()


@pytest.fixture
def setup_db_sync():
    access.init_db_access('sqlite', ':memory:', use_async=False)
    yield
    access.get_engine().dispose()
