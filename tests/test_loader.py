"""Loader tests."""

import os
import tempfile

import pytest

from page_loader.loader import download


@pytest.fixture
def assets():
    """Necessary assets, read from files.

    Returns:
        dict
    """
    assets = {
        'page_expected': {
            'path': 'tests/fixtures/ru-hexlet-io-courses_expected.html',
        },
        'page': {
            'path': 'tests/fixtures/ru-hexlet-io-courses.html',
            'url': 'https://ru.hexlet.io/courses',
            'name': 'ru-hexlet-io-courses.html',
        },
        'link_relative': {
            'path': 'tests/fixtures/ru-hexlet-io-courses-reviews.html',
            'url': 'https://ru.hexlet.io/courses/reviews',
            'name': 'ru-hexlet-io-courses-reviews.html',
        },
        'link_absolute': {
            'path': 'tests/fixtures/ru-hexlet-io-tracks.html',
            'url': 'https://ru.hexlet.io/tracks',
            'name': 'ru-hexlet-io-tracks.html',
        },
        'link_full_url': {
            'path': 'tests/fixtures/ru-hexlet-io-about.html',
            'url': 'https://ru.hexlet.io/about',
            'name': 'ru-hexlet-io-about.html',
        },
        'image': {
            'path': 'tests/fixtures/image.png',
            'url': 'https://ru.hexlet.io/assets/professions/nodejs.png',
            'name': 'ru-hexlet-io-assets-professions-nodejs.png',
        },
        'script': {
            'path': 'tests/fixtures/script.js',
            'url': 'https://ru.hexlet.io/packs/js/runtime.js',
            'name': 'ru-hexlet-io-packs-js-runtime.js',
        },
        'style': {
            'path': 'tests/fixtures/style.css',
            'url': 'https://ru.hexlet.io/assets/application.css',
            'name': 'ru-hexlet-io-assets-application.css',
        },
    }

    for attributes in assets.values():
        with open(attributes['path'], 'rb') as file_content:
            attributes['content'] = file_content.read()
    return assets


def test_download(requests_mock, assets):
    """Test 'download' function.

    - webpage is downloaded and processed correctly
    - local sources are downloaded to 'files' directory and saved correctly

    Args:
        requests_mock: external fixture
        assets: dictionary with assets
    """
    page_expected = assets.pop('page_expected')

    for _, asset in assets.items():
        url = asset['url']
        file_content = asset['content']

        requests_mock.get(url, content=file_content)

    page = assets.pop('page')

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Webpage is downloaded and processed correctly
        page_path_expected = os.path.join(tmpdirname, page['name'])
        page_path = download(page['url'], tmpdirname)

        assert page_path == page_path_expected

        with open(page_path, 'rb') as page_object:
            assert page_object.read() == page_expected['content']

        # Assets are downloaded to 'files' directory and saved correctly
        files_name = 'ru-hexlet-io-courses_files'
        files_path = os.path.join(tmpdirname, files_name)

        for attributes in assets.values():
            asset_path = os.path.join(files_path, attributes['name'])

            assert os.path.exists(asset_path)

            with open(asset_path, 'rb') as asset_object:
                assert asset_object.read() == attributes['content']
