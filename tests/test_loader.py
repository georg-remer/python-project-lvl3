"""Loader tests."""

import os
import tempfile

import pytest
import requests_mock
from page_loader.loader import download


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
    """Return expected webpage after downloading and processing.

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
    with open('tests/fixtures/image.png', 'rb') as file_object:
        return file_object.read()


@requests_mock.Mocker(kw='mocker')
def test_download(page, page_expected, image, **kwargs):
    """Test 'download' function.

    - webpage is downloaded and processed correctly
    - local sources are downloaded to 'files' directory
    - image contents is downloaded correctly

    Args:
        page: sample webpage for downloading
        page_expected: expected webpage after downloading and processing
        image: sample image for downloading
        kwargs: used for passing mocker
    """
    page_url = 'https://ru.hexlet.io/courses'
    page_name = 'ru-hexlet-io-courses.html'
    files_name = 'ru-hexlet-io-courses_files'
    sources = {
        'css': {
            'url': 'https://ru.hexlet.io/assets/application.css',
            'name': 'ru-hexlet-io-assets-application.css',
        },
        'link': {
            'url': 'https://ru.hexlet.io/courses',
            'name': 'ru-hexlet-io-courses.html',
        },
        'image': {
            'url': 'https://ru.hexlet.io/assets/professions/nodejs.png',
            'name': 'ru-hexlet-io-assets-professions-nodejs.png',
        },
        'script': {
            'url': 'https://ru.hexlet.io/packs/js/runtime.js',
            'name': 'ru-hexlet-io-packs-js-runtime.js',
        },
    }

    mocker = kwargs['mocker']
    mocker.get(page_url, text=page)
    mocker.get(sources['css']['url'], text='')
    mocker.get(sources['link']['url'], text=page)
    mocker.get(sources['image']['url'], content=image)
    mocker.get(sources['script']['url'], text='')

    with tempfile.TemporaryDirectory() as tmpdirname:
        page_path_expected = os.path.join(tmpdirname, page_name)
        page_path = download(page_url, tmpdirname)

        assert page_path == page_path_expected
        with open(page_path, 'r') as page_object:
            assert page_object.read() == page_expected

        files_path = os.path.join(tmpdirname, files_name)
        for _, source in sources.items():
            source_path = os.path.join(files_path, source['name'])
            assert os.path.exists(source_path)

        image_path = os.path.join(files_path, sources['image']['name'])
        with open(image_path, 'rb') as image_object:
            assert image_object.read() == image
