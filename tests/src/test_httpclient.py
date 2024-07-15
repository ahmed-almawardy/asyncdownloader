import anyio
import pytest
from unittest.mock import patch
from unittest import mock

from anyio import AsyncFile

from src.app import AsyncHttpClient
from httpx import AsyncClient, Response
from asyncio import TaskGroup


pytestmark = [
    pytest.mark.asyncio
]


async def test_client_get_called_with_url():
    with patch.object(AsyncClient, 'get') as mock_httpx_get:
        async with AsyncHttpClient() as client:
            await client.get("http://example.com")
            mock_httpx_get.assert_called_once_with("http://example.com")


@mock.patch.object(AsyncHttpClient,'get',  return_value=None)
@mock.patch('httpx.Response', autospec=True, return_value=None)
@mock.patch('src.app.logger',  return_value=None)
@mock.patch('src.app.save_file',  autospec=True,return_value=None)
@mock.patch('src.app.hash_content', autospec=True, return_value=None)
async def test_client_download_file(
    mocked_hash_content,
    mocked_save_file,
    mocker_logger,
    mocked_response,
    mocked_get
):
        incoming_data = {'download_url': "https://example.com", "name": "filename"}
        mocked_response.aread.return_value = b'data'
        mocked_get.return_value = mocked_response
        mocked_hash_content.return_value = '12312'
        mocked_save_file.return_value = None

        client = AsyncHttpClient()
        await client.download_file(incoming_data, 'filename_path')
        mocked_hash_content.assert_called_once()
        mocked_save_file.assert_called_once()
        mocked_get.assert_called_once()
        mocked_response.aread.assert_called_once()


@mock.patch.object(AsyncHttpClient,'dispatch_downloader', autospec=True)
@mock.patch('src.app.os.path.join', autospec=True)
@mock.patch('src.app.os.makedirs', autospec=True)
async def test_download_directory(mocked_makedirs,mocked_os_join, mocked_dispatch_downloader):
    mocked_os_join.return_value = 'local_dir'
    client = AsyncHttpClient()
    incoming_data = {'_links': {'self': 'http://example.com'}, "name": "name"}
    await client.download_directory(incoming_data=incoming_data, path="local_dir")
    mocked_dispatch_downloader.assert_called_once()
    mocked_os_join.assert_called_once_with('local_dir', 'name')
    mocked_makedirs.assert_called_once_with('local_dir', exist_ok=True)


@mock.patch.object(Response, 'json', autospec=True, return_value=[{'type': 'file'}])
async def test_dispatch_delegate_to_file_downloader(mocked_response):
    with patch.object(AsyncHttpClient, 'download_file') as mock_download_file:
        async with AsyncHttpClient() as client:
            await client.dispatch_downloader("http://example.com", 'local_path')
            mock_download_file.assert_called_once()


@mock.patch.object(Response, 'json', autospec=True, return_value=[{'type': 'dir'}])
async def test_dispatch_delegate_to_download_directory(mocked_response):
    with patch.object(AsyncHttpClient, 'download_directory') as mock_download_dir:
        async with AsyncHttpClient() as client:
            await client.dispatch_downloader("http://example.com", 'local_path')
            mock_download_dir.assert_called_once()

