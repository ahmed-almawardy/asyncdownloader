"""App using Async Http clients as dependencies in order to download a repo.

it is so simple async and written respectively to SOLID/DRY/KISS also it
is tested, and linter friend

"""

import asyncio
import os
import tempfile
from datetime import datetime

import httpx

from a_services import save_file
from services import hash_content, log_ended, log_started, logger
from settings import BASE_DIR, REPO_ROOT_URL


class AsyncHttpClient:
    """HttpClient is a simple wrapper around httpx/aiohttp(Any Async Client).

    to be able to send async requests and download simple raw bytes from
    repo.

    """

    __slots__ = ('internal_client',)

    def __init__(self, http_client=httpx.AsyncClient):
        """
        Store the http-client-detail as Service.

        :param http_client: httpx.AsyncClient
        """
        self.internal_client = http_client()

    async def __aenter__(self):
        """Applicable as ContextManager.

        :return:

        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean resources.

        :return:

        """
        await self.internal_client.aclose()

    async def get(self, url: str = None) -> httpx.Response | None:
        """Request url and return response.

        :param url: str the url to request
        :return: httpx.Response  of the request

        """
        logger.info('{0}: GET {1} HTTP/1.1'.format(logger.name, url))
        return await self.internal_client.get(url)

    async def dispatch_downloader(self, url, path) -> None:
        """Switcher for downloading raw bytes from repo.

        :param url: str the url to request
        :param path: path of the file
        :return: None

        """
        async with asyncio.TaskGroup() as tasks_group:
            response = await self.get(url)
            for row in response.json():
                if row['type'].startswith('file'):
                    tasks_group.create_task(self.download_file(row, path))
                else:
                    tasks_group.create_task(self.download_directory(row, path))

    async def download_file(self, incoming_data: dict, path: str) -> None:
        """Download a single file from url and save it to path.

        :param incoming_data: dict the container to get the url from
        :param path: local path to save the file to
        :return: None

        """
        response = await self.get(incoming_data['download_url'])
        # I could have used CHUNK_SIZE=4096. for simplicity used no chunk
        response_content = await response.aread()
        filename = incoming_data['name']
        await save_file(
            os.path.join(path, filename),
            response_content,
        )
        file_hash = hash_content(response_content)
        logger.info('{0}:{1} Hash {2}'.format(
            logger.name,
            filename,
            file_hash,
        ))

    async def download_directory(self, incoming_data: dict, path=None):
        """Download a nested dirs from url and save it to path.

        :param incoming_data: dict the container to get the url from
        :param path: local path to save the file to
        :return: None

        """
        file_path = os.path.join(path, incoming_data['name'])
        os.makedirs(file_path, exist_ok=True)
        await self.dispatch_downloader(
            incoming_data['_links']['self'],
            file_path,
        )


class App:
    """Entry point for the application."""

    __slots__ = ('async_client', 'temp_dir', 'repo_root_url')

    def __init__(
        self,
        async_client: AsyncHttpClient,
        repo_root_url: str,
        temp_dir: str,
    ):
        """Start app.

        :param async_client: httpx.AsyncClient
        :param repo_root_url: str
        :param temp_dir: str

        """
        self.async_client = async_client
        self.repo_root_url = repo_root_url
        self.temp_dir = temp_dir

    async def download_repo_structure(self):
        """Proxy method to link with the HttpClient."""
        logger.info(
            '{0}: Downloading repo to {1}'.
            format(
                logger.name,
                self.temp_dir,
            ))
        repo_root_path = os.path.join(BASE_DIR, self.temp_dir)
        await self.async_client.dispatch_downloader(
            self.repo_root_url,
            repo_root_path,
        )


async def main():
    """Entry to start the application to download raw bytes from repo."""
    async with AsyncHttpClient() as http_client:
        started_at = datetime.now()
        log_started(started_at)
        app = App(
            http_client,
            repo_root_url=REPO_ROOT_URL,
            temp_dir=tempfile.mkdtemp(),
        )
        await app.download_repo_structure()
        log_ended(started_at)


if __name__ == '__main__':
    asyncio.run(main())
