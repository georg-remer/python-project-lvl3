"""Page loader."""

import logging
import os
import re
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup
from page_loader.processor import process


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

    logging.info('Generated page name: %s', page_name)

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

    logging.info('Generated files folder name: %s', files_name)

    return files_name


def download(url, output):
    """Download page.

    Args:
        url: url to download page from
        output: directory to save page to

    Returns:
        str
    """
    logging.info('Downloading: %s', url)

    scheme, netloc, path, _, _ = urlsplit(url)
    page = requests.get(url).text
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
    with open(page_path, 'w') as page_object:
        page_object.write(soup.prettify(formatter='html5'))

    # Download sources
    for source_name, source_url in sources_urls.items():
        if not os.path.isdir(os.path.join(output, files_name)):
            os.mkdir(os.path.join(output, files_name))

        source = requests.get(source_url).content
        source_path = os.path.join(output, source_name)
        with open(source_path, 'wb') as source_object:
            source_object.write(source)

    logging.info('Downloaded to: %s', page_path)

    return page_path
