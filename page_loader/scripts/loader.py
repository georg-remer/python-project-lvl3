"""Main module."""
import logging
import sys

from page_loader.cli import parse_args
from page_loader.loader import download


def main():
    """Download page."""
    logging.basicConfig(level=logging.INFO)
    url, output = parse_args()

    try:
        file_path = download(url, output)
    except Exception as exception:
        logging.error(exception)
        sys.exit(1)
    else:
        print(file_path)


if __name__ == '__main__':
    main()
