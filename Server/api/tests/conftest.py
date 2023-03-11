import pytest
from unittest.mock import patch, create_autospec

from sqlalchemy.ext.asyncio import AsyncSession

from . import ID
from api.db.models import Base


@pytest.fixture(autouse=True)
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def session():
    return create_autospec(AsyncSession)


@pytest.fixture
def base_save():
    def set_id_on_save(self, session):
        self.id = ID

    with patch.object(Base, 'save', autospec=True) as base_save_patch:
        base_save_patch.side_effect = set_id_on_save
        yield base_save_patch
