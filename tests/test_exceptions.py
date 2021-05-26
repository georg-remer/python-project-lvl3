"""Custom exceptions tests."""

import tempfile

import pytest

from page_loader.exceptions import (
    FileSystemError,
    HTTPError,
    NetworkError,
    RequestTimeoutError,
)
from page_loader.loader import download


@pytest.mark.parametrize(
    'exception, dirname',
    (
        (FileSystemError, '/root'),
        (HTTPError, ''),
        (NetworkError, ''),
        (RequestTimeoutError, ''),
    ),
)
def test_error(requests_mock, exception, dirname):
    """Checks custom exceptions.

    Args:
        requests_mock: external fixture
        exception: custom exception to check
        dirname: if specified use this for test
    """
    page_url = 'https://unreachable.com'
    requests_mock.get(page_url, exc=exception)

    with pytest.raises(exception):
        if dirname:
            download(page_url, dirname)
        else:
            with tempfile.TemporaryDirectory() as tmpdirname:
                download(page_url, tmpdirname)
