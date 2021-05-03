"""Custom exceptions tests."""

import tempfile

import pytest
import requests_mock
from page_loader import exceptions
from page_loader.loader import download


@requests_mock.Mocker(kw='mocker')
def test_network_error(**kwargs):
    """Test custom NetworkError.

    Args:
        kwargs: used for passing mocker
    """
    page_url = 'https://unreachable.com'
    mocker = kwargs['mocker']
    mocker.get(page_url, exc=exceptions.NetworkError)

    with pytest.raises(exceptions.NetworkError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            download(page_url, tmpdirname)


@requests_mock.Mocker(kw='mocker')
@pytest.mark.parametrize('status_code', (404, 500))
def test_http_error(status_code, **kwargs):
    """Test custom HTTPError.

    Args:
        status_code: for HTTP error
        kwargs: used for passing mocker
    """
    page_url = 'https://unreachable.com'
    mocker = kwargs['mocker']
    mocker.get(page_url, status_code=status_code)

    with pytest.raises(exceptions.HTTPError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            download(page_url, tmpdirname)


@requests_mock.Mocker(kw='mocker')
def test_timeout_error(**kwargs):
    """Test custom TimeoutError.

    Args:
        kwargs: used for passing mocker
    """
    page_url = 'https://unreachable.com'
    mocker = kwargs['mocker']
    mocker.get(page_url, exc=exceptions.RequestTimeoutError)

    with pytest.raises(exceptions.RequestTimeoutError):
        with tempfile.TemporaryDirectory() as tmpdirname:
            download(page_url, tmpdirname)


@requests_mock.Mocker(kw='mocker')
def test_filesystem_error(**kwargs):
    """Test custom TimeoutError.

    Args:
        kwargs: used for passing mocker
    """
    page_url = 'https://unreachable.com'
    tmpdirname = '/root'
    mocker = kwargs['mocker']
    mocker.get(page_url, exc=exceptions.FileSystemError)

    with pytest.raises(exceptions.FileSystemError):
        download(page_url, tmpdirname)
