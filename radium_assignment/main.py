import asyncio
import tempfile

from radium_assignment.download_utils import (
    download_files_from_gitea_repository
)
from radium_assignment.hash_utils import count_hashes


GITEA_DOMAIN = 'radium'
REPOSITORY_OWNER = 'radium'
REPOSITORY_NAME = 'project-configuration'
BRANCH = 'HEAD'
ASYNC_TASKS_COUNT = 3  # В соответствии с условиями задания
TMP_DIRECTORY_NAME = 'tmp'


async def main() -> None:
    '''Script downloads files from gitea repository
    and count hash for each file.'''

    print('Start downloading files..')
    with tempfile.TemporaryDirectory() as temp_dir:
        await download_files_from_gitea_repository(
            gitea_domain=GITEA_DOMAIN,
            repository_owner=REPOSITORY_OWNER,
            repository_name=REPOSITORY_NAME,
            branch_or_commit_sha=BRANCH,
            async_tasks_count=ASYNC_TASKS_COUNT,
            directory=temp_dir,
        )
        print('Downloading is completed..')
        print('Counting hash..')
        await count_hashes(directory=temp_dir)
        print('Finish.')


if __name__ == '__main__':
    asyncio.run(main())
