"""Soup processor."""

import os
import re
from urllib.parse import urlsplit, urlunsplit

IMG = 'img'
LINK = 'link'
SCRIPT = 'script'
TAGS = (IMG, LINK, SCRIPT)


def is_valid_for_downloading(page_netloc, tag):
    """Return True if source is valid for downloading.

    Args:
        page_netloc: URI netloc
        tag: html-tag to check

    Returns:
        bool
    """
    if tag.name in {IMG, SCRIPT}:
        url = tag.get('src')
    elif tag.name == LINK:
        url = tag.get('href')
    if not url:
        return False
    source_netloc = urlsplit(url).netloc
    return page_netloc == source_netloc or not url.startswith('http')


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


def generate_source_name(page_netloc, source_url, files_name):
    """Generate source name for saving file.

    Example: 'ru-hexlet-io-assets-professions-nodejs.png' for
    '/assets/professions/nodejs.png'

    Args:
        page_netloc: URI netloc
        source_url: source URL
        files_name: files directory name

    Returns:
        str
    """
    _, source_netloc, source_path, _, _ = urlsplit(source_url)
    if source_netloc:
        source_url = '{netloc}{path}'.format(
            netloc=source_netloc,
            path=source_path,
        )
    else:
        source_url = '{netloc}{path}'.format(
            netloc=page_netloc,
            path=source_url,
        )
    name, extension = os.path.splitext(source_url)
    name = re.sub(r'\W', '-', name)
    return '{files_name}/{name}{extension}'.format(
        files_name=files_name,
        name=name,
        extension=extension if extension else '.html',
    )


def generate_source_url(scheme, page_netloc, source_url):
    """Generate source url for downloading.

    Args:
        scheme: URI scheme
        page_netloc: URI netloc
        source_url: source URL

    Returns:
        str
    """
    source_netloc = urlsplit(source_url).netloc
    if source_netloc:
        return source_url
    return urlunsplit((scheme, page_netloc, source_url, None, None))


def process(scheme, netloc, soup, files_name):
    """Replace source tags.

    Replace source tags and return a collection of source names and URLs
    to download sources from

    Args:
        scheme: URI scheme
        netloc: URI netloc
        soup: BeautifulSoup object
        files_name: name for the files directory

    Returns:
        dict
    """
    urls = {}
    for tag in soup.find_all(TAGS):
        url, attribute = get_url_from_tag(tag)

        if is_valid_for_downloading(netloc, tag):
            source_name = generate_source_name(netloc, url, files_name)
            tag[attribute] = source_name
            urls[source_name] = generate_source_url(scheme, netloc, url)
    return urls
