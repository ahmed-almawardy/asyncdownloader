import pytest
from unittest import mock


@pytest.fixture
@mock.patch("app.App",  spec=True)
def app(mocked_app):
    return mocked_app


