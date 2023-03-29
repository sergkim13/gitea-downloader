from pathlib import Path, PurePath
from aiohttp import ClientSession
import base64
import math
import aiofiles
import tqdm.asyncio

async def download_files_from_gitea_repository(
        gitea_domain: str,
        repository_owner: str,
        repository_name: str,
        branch_or_commit_sha: str,
        async_tasks_count: int,
        directory: PurePath | str = 'tmp',
) -> None:
    '''
    Downloads all files from given gitea repository in async mode
    and save it to given directory.
    '''
    path = Path(directory)
    if not path.exists():
        path.mkdir()

    url = (
        f'https://gitea.{gitea_domain}.group/api/v1/repos/{repository_owner}/'
        f'{repository_name}/git/trees/{branch_or_commit_sha}'
    )
    params = {'recursive': 'true'}

    async with ClientSession() as session:
        files_list = await get_files_list(session, url, params)
        await async_download_files(
            session, files_list, async_tasks_count, directory
        )


async def get_files_list(
        session: ClientSession,
        url: str, params:
        dict = None
) -> list[dict]:
    '''
    Send request to gitea API and get list of repository's files.
    '''
    async with session.get(url, params=params) as response:
        repo_data = await response.json()
        files_list = repo_data['tree']
        return files_list


async def async_download_files(
    session: ClientSession,
    files_list: list[dict],
    async_tasks_count: int,
    directory: PurePath | str = 'tmp',
) -> None:
    '''
    Downloads all files in async mode
    in given number (`async_tasks_count`) parallel tasks.
    '''
    tasks = []
    for chunk in chunked(files_list, async_tasks_count):
        tasks.append(download_chunk_files(session, chunk, directory))

    for f in tqdm.asyncio.tqdm.as_completed(tasks):
        await f


def chunked(files_list: list, chunks_count: int) -> list[list]:
    '''Divide list of all files to `chunks_count` pieces.'''
    chunk_size = math.ceil(len(files_list) / chunks_count)
    return [
        files_list[chunk:chunk + chunk_size] for chunk
        in range(0, len(files_list), chunk_size)
    ]


async def download_chunk_files(
        session: ClientSession,
        chunk: list,
        directory: PurePath
) -> None:
    '''
    Downloads each file in chunk in async mode.
    '''
    for file in chunk:
        file_path = PurePath(file['path'])
        await check_and_create_directory(file, directory)
        saving_path = directory / file_path
        if file['type'] == 'blob':
            await download_file(session, saving_path, file['url'])


async def check_and_create_directory(file: dict, directory: PurePath) -> None:
    '''
    If file_path is complex (e.g. nitpick/all.toml),
    this function will create `nitpick` dir if it's not exists already.
    '''
    file_path = PurePath(file['path'])
    file_path_parts = file_path.parts
    if len(file_path_parts) > 1:
        for part in file_path_parts[:-1]:
            path = directory / Path(part)
            if not path.exists():
                path.mkdir()
            directory = path


async def download_file(
        session: ClientSession,
        saving_path: str | PurePath,
        url: str
) -> None:
    '''Download one file and save it to `saving_path`.'''
    async with session.get(url) as response:
        answer = await response.json()
        content = base64.b64decode(answer['content'])
        async with aiofiles.open(saving_path, 'wb') as file:
            await file.write(content)
