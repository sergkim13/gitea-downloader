"""
Gitea-downloader script.

Script which downloads files of given gitea repository,
save it into temporary directory
and count hash for each file.
"""


import asyncio
import tempfile

from gitea_downloader.download_utils import (
    download_files_from_gitea_repository,
)
from gitea_downloader.hash_utils import count_hashes
from gitea_downloader.logger_utils import logger

GITEA_DOMAIN = 'radium'
REPOSITORY_OWNER = 'radium'
REPOSITORY_NAME = 'project-configuration'
BRANCH = 'HEAD'


async def main() -> None:
    """Run main script function."""
    logger.info('Start downloading files..')
    with tempfile.TemporaryDirectory() as temp_dir:
        await download_files_from_gitea_repository(
            gitea_domain=GITEA_DOMAIN,
            repository_owner=REPOSITORY_OWNER,
            repository_name=REPOSITORY_NAME,
            branch_or_commit_sha=BRANCH,
            directory=temp_dir,
        )
        logger.info('Downloading is completed..')
        logger.info('Counting hash..')
        await count_hashes(directory=temp_dir)
        logger.info('Finish.')


if __name__ == '__main__':
    asyncio.run(main())
