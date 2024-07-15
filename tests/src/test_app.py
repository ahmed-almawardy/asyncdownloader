from unittest import mock
from src.app import App, main


@mock.patch('src.app.log_ended', autospec=True)
@mock.patch('src.app.log_started', autospec=True)
@mock.patch('src.app.datetime', autospec=True)
@mock.patch.object(App, 'download_repo_structure')
async def test_main_internals(mocked_download_repo_structure, mocked_datetime, mocked_log_started, mocked_log_ended):
    await main()
    mocked_download_repo_structure.assert_called_once()
    mocked_datetime.now.assert_called()
    mocked_log_started.assert_called_once()
    mocked_log_ended.assert_called_once()


@mock.patch('src.app.AsyncHttpClient', autospec=True)
@mock.patch('src.app.tempfile', autospec=True)
async def test_download_repo_structure(mocked_temp, async_http_client):
    mocked_temp.mkdtemp.return_value = 'temp_directory_path'
    async_http_client.dispatch_downloader.return_value = None
    app = App(
        async_http_client,
        repo_root_url='https://example.com',
        temp_dir=mocked_temp.mkdtemp(),
    )
    await app.download_repo_structure()
    async_http_client.dispatch_downloader.assert_called_once()
