import sys
from contextlib import contextmanager



import pytest_asyncio
from pytest import MonkeyPatch
from tests.mocks import FakeSession, MockClientResponse
from http import HTTPStatus
import json
from aiohttp import ClientSession
from tests.constants import (
    FAKE_FILES_DICT,
    FAKE_FILES_LIST,
    FAKE_FILE_1,
    FAKE_FILE_2,
    FAKE_FILE_3,
    FAKE_FILE_4,
)
import pytest


@pytest_asyncio.fixture()
async def fake_session():
    return FakeSession()
    # yield patched_session


@pytest_asyncio.fixture
async def expected_result_get_files_list():
    return FAKE_FILES_LIST


