"""Soup processor."""

import logging
import os
import re
from urllib.parse import urljoin, urlsplit

IMG = 'img'
LINK = 'link'
SCRIPT = 'script'
TAGS = (IMG, LINK, SCRIPT)

logger = logging.getLogger(__name__)


def generate_name(url, source_type='page', files_name=None):
    """Generate name.

    Args:
        url: source to generate name for
        source_type: source type to generate name for
        files_name: files directory name

    Returns:
        str

    Raises:
        ValueError: if unknown source type is used
    """
    _, netloc, path, _, _ = urlsplit(url)
    base_name = '{netloc}{path}'.format(netloc=netloc, path=path)
    base_name, extension = os.path.splitext(base_name)
    base_name = re.sub(r'\W', '-', base_name)
    if source_type == 'page':
        name = '{name}.html'.format(name=base_name)

        logger.info('Generated page name: {0}'.format(name))

    elif source_type == 'directory':
        name = '{name}_files'.format(name=base_name)

        logger.info('Generated files folder name: {0}'.format(name))

    elif source_type == 'source':
        name = '{files_name}/{name}{extension}'.format(
            files_name=files_name,
            name=base_name,
            extension=extension if extension else '.html',
        )

        logger.info('Generated source name: {0}'.format(name))

    else:
        raise ValueError('Unknown source type: {0}'.format(source_type))

    return name


def get_url_from_tag(tag):
    """Get URL and attribute where it's stored from tag.

    Args:
        tag: html-tag to get link from

    Returns:
        (str, str)
    """
    if tag.name in {IMG, SCRIPT}:
        attribute = 'src'
    elif tag.name == LINK:
        attribute = 'href'
    url = tag.get(attribute)
    return url, attribute


def is_valid_for_downloading(base_url, tag):
    """Return True if source is valid for downloading.

    Args:
        base_url: to check against
        tag: html-tag to check

    Returns:
        bool
    """
    source_url, _ = get_url_from_tag(tag)
    if not source_url:
        return False
    source_url = urljoin(base_url, source_url)
    base_netloc = urlsplit(base_url).netloc
    source_netloc = urlsplit(source_url).netloc
    return base_netloc == source_netloc


def replace_tags(base_url, soup, files_name):
    """Replace source tags.

    Replace source tags and return a collection of source names and URLs
    to download sources from

    Args:
        base_url: to check against
        soup: BeautifulSoup object
        files_name: name for the files directory

    Returns:
        dict
    """
    urls = {}
    for tag in soup.find_all(TAGS):
        source_url, attribute = get_url_from_tag(tag)
        source_url = urljoin(base_url, source_url)

        if is_valid_for_downloading(base_url, tag):
            source_name = generate_name(
                source_url,
                source_type='source',
                files_name=files_name,
            )
            tag[attribute] = source_name
            urls[source_name] = source_url
    return urls
