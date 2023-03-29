import json
from http import HTTPStatus
from aiohttp import ClientSession
from tests.constants import (
    FAKE_FILES_DICT,
    FAKE_FILE_1,
    FAKE_FILE_2,
    FAKE_FILE_3,
    FAKE_FILE_4,
)


class FakeSession():

    def get(self, url: str, params: dict = None):

        if url == 'fake_url1':
            return MockClientResponse(json.dumps(FAKE_FILE_1), HTTPStatus.OK)
        elif url == 'fake_url2':
            return MockClientResponse(json.dumps(FAKE_FILE_2), HTTPStatus.OK)
        elif url == 'fake_url3':
            return MockClientResponse(json.dumps(FAKE_FILE_3), HTTPStatus.OK)
        elif url == 'fake_url4':
            return MockClientResponse(json.dumps(FAKE_FILE_4), HTTPStatus.OK)
        else:
            return MockClientResponse(json.dumps(FAKE_FILES_DICT), HTTPStatus.OK)



class MockClientResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status

    async def read(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    async def json(self):
        return json.loads(self._text)
