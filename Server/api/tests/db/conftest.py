import pytest

from api.db.access import  init_db_access, cleanup_db_access, get_engine


@pytest.fixture
async def setup_db(anyio_backend):
    init_db_access('sqlite', ':memory:')
    yield
    await cleanup_db_access()


@pytest.fixture
def setup_db_sync():
    init_db_access('sqlite', ':memory:', use_async=False)
    yield
    get_engine().dispose()
