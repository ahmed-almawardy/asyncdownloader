"""
Application using  Async Http clients as dependencies in order to download a repo.
it is so simple async and written respectively to SOLID/DRY/KISS
also it is tested, and linter friend
"""

import asyncio
import os
from datetime import datetime

import httpx

from a_services import save_file
from services import logger, log_started, log_ended, hash_content
from settings import BASE_DIR


class AsyncHttpClient:
    """
    HttpClient is a simple wrapper around httpx/aiohttp(Any Async Client)
    to be able to send async requests and download simple raw bytes from repo.
    """
    __slots__ = ("internal_client", )

    def __init__(self, http_client=httpx.AsyncClient):
        """
        Storing the http-client-detail as Service
        :param http_client: httpx.AsyncClient
        """
        self.internal_client = http_client()

    async def __aenter__(self):
        """
        Applicable as ContextManager
        :return:
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Cleaning resources
        :return:
        """
        await self.internal_client.aclose()

    async def get(self, url: str = None) -> httpx.Response | None:
        """
        Request url and return response.
        :param url: str the url to request
        :return: httpx.Response  of the request
        """
        logger.info(f"{logger.name}: GET {url} HTTP/1.1")
        return await self.internal_client.get(url)

    async def dispatch_downloader(self, url, path: str) -> None:
        """
        Switcher for downloading raw bytes from repo.
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

    async def download(self, url: str, filepath: str) -> None:
        """
        Main Entry Point to the downloader
        :param url: str url to repo
        :param filepath: str the path to save the file to
        :return:
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        await self.dispatch_downloader(url, filepath)

    async def download_file(self, data: dict, path: str) -> None:
        """
        Download a single file from url and save it to path.
        :param data: dict the container to get the url from
        :param path: local path to save the file to
        :return: None
        """
        response = await self.get(data['download_url'])
        content = await response.aread()  # I could have used CHUNK_SIZE=4096. for simplicity used no chunk
        await save_file(os.path.join(path, data['name']), content)
        logger.info(f"{logger.name}: {data['name']} Hash {hash_content(content)} ")

    async def download_directory(self, data: dict, path=None):
        """
        Download a nested dirs from url and save it to path.
        :param data: dict the container to get the url from
        :param path: local path to save the file to
        :return: None
        """
        file_path = os.path.join(path, data['name'])
        os.makedirs(file_path, exist_ok=True)
        await self.dispatch_downloader(data['_links']['self'], file_path)


class App:
    """
    Entry point for the application.
    """
    __slots__ = ("async_client",)

    def __init__(self, async_client):
        self.async_client = async_client

    async def download_repo_structure(self):
        repo_structure_url = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents'
        repo_root_path = os.path.join(BASE_DIR, 'download_here/')
        await self.async_client.download(repo_structure_url, repo_root_path)


if __name__ == '__main__':
    async def main():
        async with AsyncHttpClient() as http_client:
            started_at = datetime.now()
            log_started(started_at)
            app = App(http_client)
            await app.download_repo_structure()
            log_ended(started_at)


    asyncio.run(main())


