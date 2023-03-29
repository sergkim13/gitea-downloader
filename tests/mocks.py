"""Mocks for testing."""
import json
from http import HTTPStatus

from tests.constants import (
    FAKE_FILE_1,
    FAKE_FILE_2,
    FAKE_FILE_3,
    FAKE_FILE_4,
    FAKE_FILES_DICT,
)


class FakeSession(object):
    """FakeSession for mocking."""

    def get(self, url: str, params: dict = None):  # noqa: ANN101, WPS110
        """Mock get method."""
        if url == 'fake_url1':
            return MockClientResponse(json.dumps(FAKE_FILE_1), HTTPStatus.OK)
        elif url == 'fake_url2':
            return MockClientResponse(json.dumps(FAKE_FILE_2), HTTPStatus.OK)
        elif url == 'fake_url3':
            return MockClientResponse(json.dumps(FAKE_FILE_3), HTTPStatus.OK)
        elif url == 'fake_url4':
            return MockClientResponse(json.dumps(FAKE_FILE_4), HTTPStatus.OK)
        return MockClientResponse(json.dumps(FAKE_FILES_DICT), HTTPStatus.OK)


class MockClientResponse(object):
    """Mock aiohttp ClientResponse."""

    def __init__(self, text: str, status: HTTPStatus) -> None:  # noqa: ANN101
        """Init MockClientResponse object."""
        self._text = text
        self.status = status

    async def read(self):  # noqa: ANN101
        """Read content."""
        return self._text

    async def __aexit__(
        self, exc_type: str, exc: str, tb: str,  # noqa: ANN101
    ) -> None:
        """Async exit from context manager."""

    async def __aenter__(self) -> None:  # noqa: ANN101
        """Async enter to context manager."""
        return self

    async def json(self):  # noqa: ANN101
        """Convet content to json."""
        return json.loads(self._text)
