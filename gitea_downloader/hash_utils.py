from pathlib import Path
import hashlib
from pathlib import PurePath
import aiofiles


async def count_hashes(directory: PurePath) -> None:
    '''Count hash for each file in given directory.'''
    items_generator = Path(directory).rglob('*')
    for item in items_generator:
        if Path(item).is_file():
            async with aiofiles.open(PurePath(item), 'rb') as f:
                file_hash = hashlib.sha256()
                file_hash.update(await f.read())
                print(f'Хэш-сумма файла {item}: {file_hash.hexdigest()}')
