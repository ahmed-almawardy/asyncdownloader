from unittest import mock


@mock.patch('app.App.run', return_value=None)
def test_app_runs(stub_run):
    assert stub_run() is None



