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
            '<title>\n Курсы по программированию Хекслет\n</title>',
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


@pytest.fixture
def page():
    """Return sample webpage for downloading.

    Returns:
        str
    """
    with open('tests/fixtures/ru-hexlet-io-courses.html', 'r') as file_object:
        return file_object.read()


@pytest.fixture
def page_expected():
    """Return expected webpage after downloading.

    Returns:
        str
    """
    with open(
        'tests/fixtures/ru-hexlet-io-courses_expected.html', 'r',
    ) as file_object:
        return file_object.read()


@pytest.fixture
def image():
    """Return sample image for downloading.

    Returns:
        bytes
    """
    with open('tests/fixtures/python.png', 'rb') as file_object:
        return file_object.read()


@pytest.mark.parametrize(
    'page_url, files_dir_name_expected, image_url1, image_url2, image_name_expected',   # noqa: E501
    [
        (
            'https://ru.hexlet.io/courses',
            'ru-hexlet-io-courses_files',
            'https://ru.hexlet.io/assets/professions/nodejs.png',
            'https://ru.hexlet.io/assets/professions/ruby.png',
            'ru-hexlet-io-assets-professions-nodejs.png',
        ),
    ],
)
def test_download_images(
    page,
    page_expected,
    page_url,
    files_dir_name_expected,
    image_url1,
    image_url2,
    image_name_expected,
    image,
):
    """Test 'download' function.

    Test that:
        - webpage is downloaded and processed correctly
        - image is downloaded to 'files' directory
        - image contents is downloaded correctly

    Args:
        page: sample webpage for downloading
        page_expected: expected webpage after downloading
        page_url: URL to download page from
        files_dir_name_expected: expected 'files' directory name
        image_url1: image URL for downloading
        image_url2: image URL for downloading
        image_name_expected: expected image name after downloading
        image: sample image for downloading
    """
    with requests_mock.Mocker() as adapter:
        adapter.get(page_url, text=page)
        adapter.get(image_url1, content=image)
        adapter.get(image_url2, content=b'')

        with tempfile.TemporaryDirectory() as tmpdirname:
            page_path = download(page_url, tmpdirname)
            with open(page_path, 'r') as page_object:
                assert page_object.read() == page_expected

            files_dir_path = os.path.join(tmpdirname, files_dir_name_expected)
            image_path = os.path.join(files_dir_path, image_name_expected)
            assert os.path.exists(image_path)

            with open(image_path, 'rb') as image_object:
                assert image_object.read() == image
