"""
Download utils module.

Contains functions for downloading files of given gitea repository.
"""
import base64
import math
from pathlib import Path, PurePath

import aiofiles
from aiohttp import ClientSession
from tqdm import asyncio as tqdm_asyncio


async def download_files_from_gitea_repository(
    gitea_domain: str,
    repository_owner: str,
    repository_name: str,
    branch_or_commit_sha: str,
    directory: PurePath | str = 'tmp',
) -> None:
    """
    Download and save files from gitea repository.

    Downloads all files from given gitea repository in async mode
    and save it to given directory.
    """
    path = Path(directory)
    if not path.exists():
        path.mkdir()

    url = (
        'https://gitea.{dmn}.group/api/v1/repos/{owner}/{name}/git/trees/{sha}'
    ).format(
        dmn=gitea_domain,
        owner=repository_owner,
        name=repository_name,
        sha=branch_or_commit_sha,
    )
    query_params = {'recursive': 'true'}

    async with ClientSession() as session:
        files_list = await get_files_list(session, url, query_params)
        await async_download_files(
            session, files_list, directory,
        )


async def get_files_list(
    session: ClientSession,
    url: str,
    query_params: dict = None,
) -> list[dict]:
    """Send request to gitea API and get list of repository's files."""
    async with session.get(url, params=query_params) as response:
        repo_data = await response.json()
        return repo_data['tree']


async def async_download_files(
    session: ClientSession,
    files_list: list[dict],
    directory: PurePath | str = 'tmp',
) -> None:
    """
    Download all files in async mode.

    Downloads all files in async mode
    in 3 parallel tasks.
    """
    tasks = []
    for chunk in chunked(files_list):
        tasks.append(download_chunk_files(session, chunk, directory))

    for task in tqdm_asyncio.tqdm.as_completed(tasks):
        await task


def chunked(files_list: list, chunks_count: int = 3) -> list[list]:
    """Divide list of all files to `chunks_count` pieces."""
    chunk_size = math.ceil(len(files_list) / chunks_count)
    return [
        files_list[chunk:chunk + chunk_size]
        for chunk in range(0, len(files_list), chunk_size)
    ]


async def download_chunk_files(
    session: ClientSession,
    chunk: list,
    directory: PurePath,
) -> None:
    """Download each file of chunk in async mode."""
    for file_dict in chunk:
        file_path = PurePath(file_dict['path'])
        await check_and_create_directory(file_dict, directory)
        saving_path = directory / file_path
        if file_dict['type'] == 'blob':
            await download_file(session, saving_path, file_dict['url'])


async def check_and_create_directory(
    file_dict: dict,
    directory: PurePath,
) -> None:
    """
    Check and create directory for saving file.

    If file_path is complex (e.g. nitpick/all.toml),
    this function will create `nitpick` dir if it's not exists already.
    """
    file_path = PurePath(file_dict['path'])
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
    url: str,
) -> None:
    """Download one file and save it to `saving_path`."""
    async with session.get(url) as response:
        answer = await response.json()
        file_content = base64.b64decode(answer['content'])
        async with aiofiles.open(saving_path, 'wb') as fp:
            await fp.write(file_content)
