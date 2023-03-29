import json
import sys
from contextlib import contextmanager
from http import HTTPStatus

import pytest
import pytest_asyncio
from aiohttp import ClientSession
from pytest import MonkeyPatch

from tests.constants import (
    FAKE_FILE_1,
    FAKE_FILE_2,
    FAKE_FILE_3,
    FAKE_FILE_4,
    FAKE_FILES_DICT,
    FAKE_FILES_LIST,
)
from tests.mocks import FakeSession, MockClientResponse


@pytest_asyncio.fixture()
async def fake_session():
    return FakeSession()
    # yield patched_session


@pytest_asyncio.fixture
async def expected_result_get_files_list():
    return FAKE_FILES_LIST


