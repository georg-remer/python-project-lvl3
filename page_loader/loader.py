"""Page loader."""

import os
import re
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup


def generate_page_name(netloc, path):
    """Generate page name.

    Args:
        netloc: URI netloc
        path: URI path

    Returns:
        str
    """
    page_name = '{netloc}{path}'.format(netloc=netloc, path=path)
    page_name = re.sub(r'\W', '-', page_name)
    return page_name


def is_valid_for_downloading(page_netloc, url):
    """Return True if image is needed to be downloaded.

    Args:
        page_netloc: URI netloc
        url: image URL

    Returns:
        bool
    """
    if not url:
        return False
    image_netloc = urlsplit(url).netloc
    return page_netloc == image_netloc or not url.startswith('http')


def generate_image_name(page_netloc, image_url):
    """Generate image name for saving file.

    Example: 'ru-hexlet-io-assets-professions-nodejs.png' for
    '/assets/professions/nodejs.png'

    Args:
        page_netloc: URI netloc
        image_url: image URL

    Returns:
        str
    """
    _, image_netloc, image_path, _, _ = urlsplit(image_url)
    if image_netloc:
        image_url = '{netloc}{path}'.format(
            netloc=image_netloc,
            path=image_path,
        )
    else:
        image_url = '{netloc}{path}'.format(netloc=page_netloc, path=image_url)
    name, extension = os.path.splitext(image_url)
    name = re.sub(r'\W', '-', name)
    return '{name}{extension}'.format(name=name, extension=extension)


def generate_image_url(scheme, page_netloc, url):
    """Generate image url for downloading.

    Args:
        scheme: URI scheme
        page_netloc: URI netloc
        url: parsed image URL

    Returns:
        str
    """
    image_netloc = urlsplit(url).netloc
    if image_netloc:
        return url
    return '{0}://{1}{2}'.format(scheme, page_netloc, url)


def process_images(scheme, netloc, soup, files_dir_name):
    """Replace image tags.

    Replace image tags and return a collection of image names and URLs
    to download images from

    Args:
        scheme: URI scheme
        netloc: URI netloc
        soup: BeautifulSoup object
        files_dir_name: name for the files directory

    Returns:
        dict
    """
    urls = {}
    for link in soup.find_all('img'):
        url = link.get('src')

        if is_valid_for_downloading(netloc, url):
            image_name = generate_image_name(netloc, url)
            link['src'] = '{directory}/{file}'.format(
                directory=files_dir_name,
                file=image_name,
            )
            urls[image_name] = generate_image_url(scheme, netloc, url)
    return urls


def download(url, output):
    """Download page.

    Args:
        url: url to download page from
        output: directory to save page to

    Returns:
        str
    """
    scheme, netloc, path, _, _ = urlsplit(url)
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    page_name = generate_page_name(netloc, path)
    files_dir_name = '{0}_files'.format(page_name)

    # Process image tags
    image_urls = process_images(scheme, netloc, soup, files_dir_name)

    # Save main page
    page_path = '{0}.html'.format(os.path.join(output, page_name))
    with open(page_path, 'w') as page_object:
        page_object.write(soup.prettify(formatter='html5'))

    # Download images
    for image_name, image_url in image_urls.items():
        if not os.path.isdir(os.path.join(output, files_dir_name)):
            os.mkdir(os.path.join(output, files_dir_name))

        image = requests.get(image_url).content
        image_path = os.path.join(output, files_dir_name, image_name)
        with open(image_path, 'wb') as image_object:
            image_object.write(image)

    return page_path
