import abc
from typing import Self

import httpx


class IAsyncHttpClient(abc.ABC):
    """Interface for providing the main methods for subclasses."""

    @abc.abstractmethod
    async def get(self: Self, url: str) -> httpx.Response | None:
        """
        Request url and return response.

        :param self: Self
        :param url: str the url to request
        :return: httpx.Response  of the request
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def dispatch_downloader(self: Self, url: str, path: str) -> None:
        """
         Switcher for downloading raw bytes from repo.

        :param url: str the url to request
        :param path: path of the file
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def download_file(
        self: Self,
        incoming_data: dict,
        path: str,
    ) -> None:
        """
        Download a single file from url and save it to path.

        :param incoming_data: dict the container to get the url from
        :param path: local path to save the file to
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def download_directory(
        self: Self,
        incoming_data: dict,
        path: str,
    ) -> None:
        """
        Download a nested dirs from url and save it to path.

        :param incoming_data: dict the container to get the url from
        :param path: local path to save the file to
        :return: None
        """
        raise NotImplementedError


class IApp(abc.ABC):
    @abc.abstractmethod
    async def download_repo_structure(self: Self) -> None:
        """Delegate download to async http client"""
        raise NotImplementedError
