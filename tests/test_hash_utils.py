from pathlib import Path

import pytest

from gitea_downloader.hash_utils import count_hashes


@pytest.mark.asyncio
async def test_count_hashes(tmp_path, caplog):
    test_file1 = tmp_path / Path('test1.txt')
    test_file2 = tmp_path / Path('test2.txt')
    test_dir = tmp_path / Path('test_dir')
    Path(test_dir).mkdir()
    with open(test_file1, 'w') as f:
        f.write('test_content1')
    with open(test_file2, 'w') as f:
        f.write('test_content2')

    await count_hashes(tmp_path)
    assert f'Хэш-сумма файла {test_file1}' in caplog.text
    assert f'Хэш-сумма файла {test_file2}' in caplog.text
    assert f'Хэш-сумма файла {test_dir}' not in caplog.text
