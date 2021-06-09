"""Soup processor."""

import logging
import os
import re
from urllib.parse import urljoin, urlsplit

IMG = 'img'
LINK = 'link'
SCRIPT = 'script'
TAGS = (IMG, LINK, SCRIPT)

tag_attribute_mapping = {
    IMG: 'src',
    LINK: 'href',
    SCRIPT: 'src',
}

logger = logging.getLogger(__name__)


def generate_name(url, name_for='file'):
    """Generate name.

    Args:
        url: asset to generate name for
        name_for: file or directory

    Returns:
        str
    """
    if url.endswith('/'):
        url = url[:-1]

    split_url = urlsplit(url)
    base_name = '{0}{1}'.format(split_url.netloc, split_url.path)
    base_name, extension = os.path.splitext(base_name)
    base_name = re.sub(r'\W', '-', base_name)

    if name_for == 'file':
        name = '{0}{1}'.format(
            base_name,
            extension if extension else '.html',
        )
    elif name_for == 'directory':
        name = '{0}_files'.format(base_name)

    logger.info('Generated name: {0}'.format(name))

    return name


def get_url_from_tag(tag):
    """Get URL and attribute where it's stored from tag.

    Args:
        tag: html-tag to get link from

    Returns:
        (str, str)
    """
    attribute = tag_attribute_mapping[tag.name]
    url = tag.get(attribute)
    return url, attribute


def is_valid_for_downloading(base_url, asset_url):
    """Return True if asset is valid for downloading.

    Args:
        base_url: to check against
        asset_url: url to check

    Returns:
        bool
    """
    if not asset_url:
        return False
    base_netloc = urlsplit(base_url).netloc
    asset_netloc = urlsplit(asset_url).netloc
    return base_netloc == asset_netloc


def replace_tags(base_url, soup, assets_dir_name):
    """Replace asset tags.

    Replace asset tags and return a collection of asset names and URLs
    to download assets from

    Args:
        base_url: to check against
        soup: BeautifulSoup object
        assets_dir_name: name for the assets directory

    Returns:
        dict
    """
    urls = {}
    for tag in soup.find_all(TAGS):
        asset_url, attribute = get_url_from_tag(tag)
        full_asset_url = urljoin('{0}/'.format(base_url), asset_url)

        if is_valid_for_downloading(base_url, full_asset_url):
            asset_name = generate_name(full_asset_url)
            full_asset_name = os.path.join(assets_dir_name, asset_name)
            tag[attribute] = full_asset_name
            urls[full_asset_name] = full_asset_url
    return urls
