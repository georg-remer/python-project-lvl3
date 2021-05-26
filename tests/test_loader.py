"""Loader tests."""

import os
import tempfile

import pytest

from page_loader.loader import _normalize, download

PAGE_EXPECTED = 'page_expected'
PAGE = 'page'
IMAGE = 'image'
SCRIPT = 'script'
STYLE = 'style'


@pytest.fixture
def assets():
    """Necessary assets, read from files.

    Returns:
        dict
    """
    assets = {
        PAGE_EXPECTED: {
            'path': 'tests/fixtures/ru-hexlet-io-courses_expected.html',
            'mode': 'r',
        },
        PAGE: {
            'path': 'tests/fixtures/ru-hexlet-io-courses.html',
            'mode': 'r',
            'url': 'https://ru.hexlet.io/courses',
            'name': 'ru-hexlet-io-courses.html',
        },
        IMAGE: {
            'path': 'tests/fixtures/image.png',
            'mode': 'rb',
            'url': 'https://ru.hexlet.io/assets/professions/nodejs.png',
            'name': 'ru-hexlet-io-assets-professions-nodejs.png',
        },
        SCRIPT: {
            'path': 'tests/fixtures/script.js',
            'mode': 'r',
            'url': 'https://ru.hexlet.io/packs/js/runtime.js',
            'name': 'ru-hexlet-io-packs-js-runtime.js',
        },
        STYLE: {
            'path': 'tests/fixtures/style.css',
            'mode': 'r',
            'url': 'https://ru.hexlet.io/assets/application.css',
            'name': 'ru-hexlet-io-assets-application.css',
        },
    }

    for attributes in assets.values():
        with open(attributes['path'], attributes['mode']) as file_object:
            attributes['file_object'] = file_object.read()
    return assets


def test_download(requests_mock, assets):
    """Test 'download' function.

    - webpage is downloaded and processed correctly
    - local sources are downloaded to 'files' directory and saved correctly

    Args:
        requests_mock: external fixture
        assets: dictionary with assets
    """
    page_expected_attributes = assets.pop(PAGE_EXPECTED)
    page_expected = page_expected_attributes['file_object']

    for key, asset in assets.items():
        url = asset['url']
        file_object = asset['file_object']

        if key == IMAGE:
            requests_mock.get(url, content=file_object)
        else:
            requests_mock.get(url, text=file_object)

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Webpage is downloaded and processed correctly
        page_path_expected = os.path.join(tmpdirname, assets[PAGE]['name'])
        page_path = download(assets[PAGE]['url'], tmpdirname)

        assert page_path == page_path_expected

        with open(page_path, 'r') as page_object:
            assert page_object.read() == page_expected

        # Assets are downloaded to 'files' directory and saved correctly
        files_name = 'ru-hexlet-io-courses_files'
        files_path = os.path.join(tmpdirname, files_name)

        for attributes in assets.values():
            asset_path = os.path.join(files_path, attributes['name'])

            assert os.path.exists(asset_path)

            with open(asset_path, attributes['mode']) as asset_object:
                assert asset_object.read() == attributes['file_object']


@pytest.mark.parametrize(
    'url, expected',
    (
        (
            'https://ru.hexlet.io/courses',
            'https://ru.hexlet.io/courses/',
        ),
        (
            'https://ru.hexlet.io/courses/',
            'https://ru.hexlet.io/courses/',
        ),
        (
            'https://ru.hexlet.io/courses?key=value',
            'https://ru.hexlet.io/courses/',
        ),
    ),
)
def test_normalize(url, expected):
    """Test _normalize function."""
    normalized_url = _normalize(url)

    assert normalized_url == expected
