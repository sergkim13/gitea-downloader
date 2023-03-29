from pathlib import Path

import pytest
from aiohttp import ClientSession

from gitea_downloader.download_utils import (
    check_and_create_directory,
    chunked,
    download_files_from_gitea_repository,
    get_files_list,
)
from tests.constants import FAKE_FILES_LIST


@pytest.mark.asyncio
async def test_download_files_from_gitea_repository(tmp_path, fake_session):
    ClientSession.get = fake_session.get
    path = tmp_path / Path('new_dir')
    await download_files_from_gitea_repository(
        gitea_domain='test',
        repository_owner='test',
        repository_name='test',
        branch_or_commit_sha='test',
        directory=path,
    )
    assert path.exists()
    assert (path / Path(FAKE_FILES_LIST[0]['path'])).exists()
    assert (path / Path(FAKE_FILES_LIST[1]['path'])).exists()
    assert (path / Path(FAKE_FILES_LIST[2]['path'])).exists()
    assert (path / Path(FAKE_FILES_LIST[3]['path'])).exists()


@pytest.mark.asyncio
async def test_check_and_create_directory(tmp_path):
    file1 = {'path': 'file1.py'}
    file2 = {'path': 'dir1/file2.py'}
    file3 = {'path': 'dir2/dir3/file3.py'}
    await check_and_create_directory(file1, tmp_path)
    await check_and_create_directory(file2, tmp_path)
    await check_and_create_directory(file3, tmp_path)
    expected_dir1 = tmp_path / Path('dir1')
    expected_dir2 = tmp_path / Path('dir2') / Path('dir3')
    assert expected_dir1.exists()
    assert expected_dir2.exists()


@pytest.mark.asyncio
async def test_chunked():
    test_list1 = ['file1', 'file2', 'file3']
    test_list2 = ['file1', 'file2', 'file3', 'file4', 'file5']
    assert chunked(test_list1, 3) == [['file1'], ['file2'], ['file3']]
    assert chunked(test_list2, 3) == [['file1', 'file2'], ['file3', 'file4'], ['file5']]


@pytest.mark.asyncio
async def test_get_files_list(fake_session, expected_result_get_files_list):
    result = await get_files_list(fake_session, 'fake_url')
    assert result == expected_result_get_files_list
