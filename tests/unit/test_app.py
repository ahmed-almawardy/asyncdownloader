from unittest import mock
from src.app import App, main


@mock.patch.object(App, 'download_repo_structure')
async def test_main_internals(mocked_download_repo_structure):
    await main()
    mocked_download_repo_structure.assert_called_once()
