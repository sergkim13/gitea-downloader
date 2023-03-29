"""Pytest fixtures."""
import pytest_asyncio

from tests.constants import FAKE_FILES_LIST
from tests.mocks import FakeSession


@pytest_asyncio.fixture()
async def fake_session():
    return FakeSession()


@pytest_asyncio.fixture
async def expected_result_get_files_list():
    return FAKE_FILES_LIST
