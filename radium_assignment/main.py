import asyncio
from pathlib import Path
from aiohttp import ClientSession
import base64
import hashlib
from pathlib import PurePath
import math


GITEA_DOMAIN = 'radium'
REPOSITORY_OWNER = 'radium'
REPOSITORY_NAME = 'project-configuration'
BRANCH = 'HEAD'
ASYNC_TASKS_COUNT = 3  # В соответствии с условиями задания
TMP_DIRECTORY_NAME = 'tmp'


async def get_files_list(session: ClientSession, url: str, params: dict = None) -> list[dict]:
    async with session.get(url, params=params) as response:
        files_list = await response.json()
        return files_list['tree']


def chunked(lst: list, chunks_count: int) -> list[list]:
    chunk_size = math.ceil(len(lst) / chunks_count)
    return [lst[chunk:chunk+chunk_size] for chunk in range(0, len(lst), chunk_size)]


async def download_file_and_get_hash(session: ClientSession, path: str | PurePath, url: str):

    async with session.get(url) as response:
        answer = await response.json()
        content = base64.b64decode(answer['content'])
        with open(path, 'wb') as file:
            file.write(content)


async def check_and_create_directory(file, directory):
    file_path = PurePath(file['path'])
    file_path_parts = file_path.parts
    if len(file_path_parts) > 1:
        for part in file_path_parts[:-1]:
            path = directory / Path(part)
            if not path.exists():
                path.mkdir()
            directory = path


async def download_chunk_files(session, chunk, directory):
    for file in chunk:
        file_path = PurePath(file['path'])
        await check_and_create_directory(file, directory)
        path = directory / file_path
        if file['type'] == 'blob':
            await download_file_and_get_hash(session, path, file['url'])


async def async_download(
    session: ClientSession, lst: list[dict], chunks_count: int, directory: PurePath | str = 'tmp'
):
    tasks = []
    for chunk in chunked(lst, chunks_count):
        tasks.append(download_chunk_files(session, chunk, directory))

    await asyncio.gather(*tasks)


async def count_hash(directory):
    items_generator = Path(directory).rglob('*')
    for item in items_generator:
        if Path(item).is_file():
            with open(PurePath(item), 'rb') as f:
                file_hash = hashlib.sha256()
                file_hash.update(f.read())
                print(f'Хэш-сумма файла {item}: {file_hash.hexdigest()}')


async def download_files_from_gitea_repository(
        gitea_domain: str,
        repository_owner: str,
        repository_name: str,
        branch_or_commit_sha: str,
        directory: PurePath | str = 'tmp',
        ) -> None:

    path = Path(directory)
    if not path.exists():
        path.mkdir()

    url = f'https://gitea.{gitea_domain}.group/api/v1/repos/{repository_owner}/{repository_name}/git/trees/{branch_or_commit_sha}'
    params = {'recursive': 'true'}

    async with ClientSession() as session:
        files_list = await get_files_list(session, url, params)
        await async_download(session, files_list, ASYNC_TASKS_COUNT, directory)


async def main():
    print('Начинаю скачивание файлов..')
    await download_files_from_gitea_repository(
        gitea_domain=GITEA_DOMAIN,
        repository_owner=REPOSITORY_OWNER,
        repository_name=REPOSITORY_NAME,
        branch_or_commit_sha=BRANCH,
    )
    print('Скачивание завершено..')
    print('Считаю хэш-суммы..')
    await count_hash(directory=TMP_DIRECTORY_NAME)

if __name__ == '__main__':
    asyncio.run(main())
