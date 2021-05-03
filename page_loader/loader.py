"""Page loader."""

import logging
import os

import requests
from bs4 import BeautifulSoup
from page_loader import exceptions
from page_loader.processor import generate_name, replace_tags
from progress.bar import Bar

logger = logging.getLogger(__name__)


def make_request(url):
    """Make request.

    Args:
        url: to make request

    Returns:
        Response

    Raises:
        NetworkError: network problem occured
        HTTPError: HTTP request returned an unsuccessful status code
        RequestTimeoutError: Request times out
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exception:
        logger.error('Connection error occured on downloading: {0}'.format(url))
        raise exceptions.NetworkError() from exception
    except requests.exceptions.HTTPError as exception:
        logger.error(
            'Unsuccessful status code returned on downloading: {0}'.format(url),
        )
        raise exceptions.HTTPError() from exception
    except requests.exceptions.Timeout as exception:
        logger.error('Timeout error occured on downloading: {0}'.format(url))
        raise exceptions.RequestTimeoutError() from exception
    return response


def write_to_file(file_path, file_content, mode='w'):
    """Write to file.

    Args:
        file_path: file location
        file_content: to be written to file
        mode: in which the file is opened

    Raises:
        FileSystemError: OS error
    """
    try:
        with open(file_path, mode) as page_object:
            page_object.write(file_content)
    except OSError as exception:
        logger.error('Error writing to: {0}'.format(file_path))
        raise exceptions.FileSystemError() from exception


def download(url, output):
    """Download page.

    Args:
        url: url to download page from
        output: directory to save page to

    Returns:
        str
    """
    logger.info('Downloading: {0}'.format(url))

    progress_bar = Bar('Downloading page', max=1)
    page = make_request(url).text
    progress_bar.next()
    progress_bar.finish()

    soup = BeautifulSoup(page, 'html.parser')

    page_name = generate_name(url)
    files_name = generate_name(url, source_type='directory')

    # Process tags
    sources_urls = replace_tags(url, soup, files_name)

    # Save main page
    page_path = os.path.join(output, '{page_name}'.format(page_name=page_name))
    page_content = soup.prettify(formatter='html5')
    write_to_file(page_path, page_content)

    # Download sources
    progress_bar_length = len(sources_urls)
    progress_bar = Bar('Downloading sources', max=progress_bar_length)
    for source_name, source_url in sources_urls.items():
        if not os.path.isdir(os.path.join(output, files_name)):
            os.mkdir(os.path.join(output, files_name))

        source_path = os.path.join(output, source_name)
        source_content = make_request(source_url).content
        write_to_file(source_path, source_content, mode='wb')

        progress_bar.next()
    progress_bar.finish()

    logger.info('Downloaded to: {0}'.format(page_path))

    return page_path
