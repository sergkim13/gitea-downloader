"""Tests for hash_utils module."""
from pathlib import Path

import pytest

from gitea_downloader.hash_utils import count_hashes


@pytest.mark.asyncio()
async def test_count_hashes(tmp_path: callable, caplog: callable):
    test_file1 = tmp_path / Path('test1.txt')
    test_file2 = tmp_path / Path('test2.txt')
    test_dir = tmp_path / Path('test_dir')
    Path(test_dir).mkdir()
    with open(test_file1, 'w') as fp1:
        fp1.write('test_content1')
    with open(test_file2, 'w') as fp2:
        fp2.write('test_content2')

    await count_hashes(tmp_path)
    assert 'Хэш-сумма файла {path}'.format(path=test_file1) in caplog.text
    assert 'Хэш-сумма файла {path}'.format(path=test_file2) in caplog.text
    assert 'Хэш-сумма файла {path}'.format(path=test_dir) not in caplog.text
