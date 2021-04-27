"""Page loader."""

import logging
import os
import re
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup
from page_loader.processor import process
from progress.bar import Bar

logger = logging.getLogger(__name__)


def generate_page_name(page_netloc, path):
    """Generate page name.

    Args:
        page_netloc: URI netloc
        path: URI path

    Returns:
        str
    """
    page_name = '{netloc}{path}'.format(netloc=page_netloc, path=path)
    page_name = re.sub(r'\W', '-', page_name)

    logger.info('Generated page name: {0}'.format(page_name))

    return page_name


def generate_files_name(page_netloc, path):
    """Generate files name.

    Args:
        page_netloc: URI netloc
        path: URI path

    Returns:
        str
    """
    files_name = '{netloc}{path}_files'.format(netloc=page_netloc, path=path)
    files_name = re.sub(r'\W', '-', files_name)

    logger.info('Generated files folder name: {0}'.format(files_name))

    return files_name


def download(url, output):
    """Download page.

    Args:
        url: url to download page from
        output: directory to save page to

    Returns:
        str
    """
    logger.info('Downloading: {0}'.format(url))

    scheme, netloc, path, _, _ = urlsplit(url)

    progress_bar = Bar('Downloading page', max=1)
    response = requests.get(url)
    response.raise_for_status()

    page = response.text
    progress_bar.next()
    progress_bar.finish()

    soup = BeautifulSoup(page, 'html.parser')

    page_name = generate_page_name(netloc, path)
    files_name = generate_files_name(netloc, path)

    # Process tags
    sources_urls = process(scheme, netloc, soup, files_name)

    # Save main page
    page_path = os.path.join(
        output,
        '{page_name}.html'.format(page_name=page_name),
    )
    page_content = soup.prettify(formatter='html5')
    with open(page_path, 'w') as page_object:
        page_object.write(page_content)

    # Download sources
    progress_bar_length = len(sources_urls)
    progress_bar = Bar('Downloading sources', max=progress_bar_length)
    for source_name, source_url in sources_urls.items():
        if not os.path.isdir(os.path.join(output, files_name)):
            os.mkdir(os.path.join(output, files_name))

        source_path = os.path.join(output, source_name)
        response = requests.get(source_url)
        response.raise_for_status()
        source_content = response.content

        with open(source_path, 'wb') as source_object:
            source_object.write(source_content)

        progress_bar.next()
    progress_bar.finish()

    logger.info('Downloaded to: {0}'.format(page_path))

    return page_path
