"""
Hash utils module.

Contains function for counting hash of files in given directory recursively.
"""
import hashlib
from pathlib import Path, PurePath

import aiofiles

from gitea_downloader.logger_utils import logger


async def count_hashes(directory: PurePath) -> None:
    """Count hash for each file in given directory."""
    elements = Path(directory).rglob('*')
    for element in elements:
        if Path(element).is_file():
            async with aiofiles.open(PurePath(element), 'rb') as fp:
                file_hash = hashlib.sha256()
                file_hash.update(await fp.read())
                logging_message = (
                    'Хэш-сумма файла {el}: {hash}'.format(
                        el=element, hash=file_hash.hexdigest(),
                    ),
                )
                logger.info(logging_message)
