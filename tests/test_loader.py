"""Loader tests."""

import os
import tempfile

import pytest
import requests_mock
from page_loader.loader import download


@pytest.mark.parametrize(
    'url, mocked_data, file_name',
    [
        (
            'https://ru.hexlet.io/courses',
            'mocked_data',
            'ru-hexlet-io-courses.html',
        ),
    ],
)
def test_download(url, mocked_data, file_name):
    """Test 'download' function.

    Args:
        url: to download page from
        mocked_data: to stub response
        file_name: of the page saved to directory
    """
    with requests_mock.Mocker() as adapter:
        adapter.get(url, text=mocked_data)

        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = os.path.join(tmpdirname, file_name)
            assert download(url, tmpdirname) == file_path

            with open(file_path, 'r') as file_object:
                assert file_object.read() == mocked_data
