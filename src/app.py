"""App using Async Http clients as dependencies in order to download a repo.

it is so simple async and written respectively to SOLID/DRY/KISS also it
is tested, and linter friend

"""
import asyncio
import os
import tempfile
from datetime import datetime
from typing import Callable, Self

import httpx

from src.a_services import save_file
from src.app_interfaces import IApp, IAsyncHttpClient
from src.logger import logger
from src.services import hash_content, log_ended, log_started
from src.settings import BASE_DIR, REPO_ROOT_URL


class AsyncHttpClient(IAsyncHttpClient):
    """HttpClient is a simple wrapper around httpx/aiohttp(Any Async Client).

    to be able to send async requests and download simple raw bytes from
    repo.
    """

    __slots__ = ('internal_client',)

    def __init__(
        self: Self,
        http_client: Callable[[], httpx.AsyncClient] = httpx.AsyncClient,
    ) -> None:
        """
        Store the http-client-detail as Service.

        :param http_client: httpx.AsyncClient
        """
        self.internal_client = http_client()

    async def __aenter__(self: Self) -> Self:
        """Applicable as ContextManager.

        :return: Self
        """
        return self

    async def __aexit__(self: Self, *exc: tuple) -> None:
        """Clean resources.

        :return: None
        """
        await self.internal_client.aclose()

    async def get(self: Self, url: str) -> httpx.Response:
        """Request url and return response from HTTP resource."""
        message = 'GET {0} HTTP/1.1'.format(url)
        logger.info(message)
        return await self.internal_client.get(url)

    async def dispatch_downloader(self: Self, url: str, path: str) -> None:
        """Switcher for downloading bytes from repo, delegating downloading."""
        async with asyncio.TaskGroup() as tasks_group:
            response = await self.get(url)
            for row in response.json():
                if row['type'].startswith('file'):
                    tasks_group.create_task(self.download_file(row, path))
                else:
                    tasks_group.create_task(self.download_directory(row, path))

    async def download_file(
        self: Self,
        incoming_data: dict,
        path: str,
    ) -> None:
        """Download a single file from url and save it to the disk."""
        response = await self.get(incoming_data['download_url'])
        # I could have used CHUNK_SIZE=4096. for simplicity used no chunk
        response_content = await response.aread()
        filename = incoming_data['name']
        await save_file(
            os.path.join(path, filename),
            response_content,
        )
        file_hash = hash_content(response_content)
        message = '{0} Hash {1}'.format(filename, file_hash)
        logger.info(message)

    async def download_directory(
        self: Self,
        incoming_data: dict,
        path: str,
    ) -> None:
        """Recursive download directory and subdirectories."""
        file_path = os.path.join(path, incoming_data['name'])
        os.makedirs(file_path, exist_ok=True)
        await self.dispatch_downloader(
            incoming_data['_links']['self'],
            file_path,
        )


class App(IApp):
    """Entry point for the application."""

    __slots__ = ('async_client', 'temp_dir', 'repo_root_url')

    def __init__(
        self: Self,
        async_client: AsyncHttpClient,
        repo_root_url: str,
        temp_dir: str,
    ) -> None:
        """Start app.

        :param async_client: httpx.AsyncClient
        :param repo_root_url: str
        :param temp_dir: str

        """
        self.async_client = async_client
        self.repo_root_url = repo_root_url
        self.temp_dir = temp_dir

    async def download_repo_structure(self: Self) -> None:
        """Proxy method to link with the HttpClient."""
        message = 'Downloading to repo {0}'.format(self.temp_dir)
        logger.info(message)
        repo_root_path = os.path.join(BASE_DIR, self.temp_dir)
        await self.async_client.dispatch_downloader(
            self.repo_root_url,
            repo_root_path,
        )


async def main() -> None:
    """Entry to start the application to download raw bytes from repo."""
    async with AsyncHttpClient() as http_client:
        started_at = datetime.now()
        log_started()
        app = App(
            http_client,
            repo_root_url=REPO_ROOT_URL,
            temp_dir=tempfile.mkdtemp(),
        )
        await app.download_repo_structure()
        log_ended(started_at)


if __name__ == '__main__':
    asyncio.run(main())
