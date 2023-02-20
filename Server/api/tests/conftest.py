import pytest
from unittest.mock import create_autospec

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def session():
    return create_autospec(AsyncSession)
