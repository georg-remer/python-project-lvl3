"""Page loader."""

import os
import re

import requests


def generate_name(url):
    """Generate file name based on URL.

    Rules:
        1. remove URL schema
        2. symbols except for letters and digits are replaced with '-'
        3. add '.html'

    Args:
        url: url to base upon

    Returns:
        str
    """
    temp_file_name = re.sub('http[s]?://', '', url)
    temp_file_name = re.sub(r'\W', '-', temp_file_name)
    return '{0}.html'.format(temp_file_name)


def download(url, output):
    """Download page.

    Args:
        url: url to download page from
        output: directory to save page to

    Returns:
        str
    """
    response = requests.get(url)
    file_name = generate_name(url)
    file_path = os.path.join(output, file_name)

    with open(file_path, 'w') as file_object:
        file_object.write(response.text)

    return file_path
