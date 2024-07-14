import pytest
from unittest.mock import patch
from unittest import mock

from app import AsyncHttpClient
from httpx import AsyncClient


pytestmark = [
    pytest.mark.asyncio
]


async def test_client_get_url():
    dependency_client = mock.AsyncMock(spec=AsyncClient)
    with patch.object(AsyncHttpClient, 'get') as mocked_get:
        http_instance = AsyncHttpClient(dependency_client)

        await http_instance.get("http://example.com")
        mocked_get.assert_called_once_with("http://example.com")


async def test_client_download_url_to_directory():
    dependency_client = mock.AsyncMock(spec=AsyncClient)
    with patch.object(AsyncHttpClient, 'download') as mocked_get:
        http_instance = AsyncHttpClient(dependency_client)

        await http_instance.download("http://example.com", "./download_here")
        mocked_get.assert_called_once_with("http://example.com", "./download_here")



