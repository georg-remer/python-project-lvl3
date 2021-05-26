"""Main module."""
import logging
import sys

from page_loader.cli import parse_args
from page_loader.exceptions import (
    FileSystemError,
    HTTPError,
    NetworkError,
    RequestTimeoutError,
)
from page_loader.loader import download


def main():
    """Download page."""
    logging.basicConfig(level=logging.INFO)
    url, output = parse_args()

    try:
        file_path = download(url, output)
    except (
        FileSystemError,
        HTTPError,
        NetworkError,
        RequestTimeoutError,
    ) as error:
        logging.error(error)
        sys.exit(1)
    except Exception:
        print('Unexpected error:', sys.exc_info()[0])
        raise
    else:
        print(file_path)


if __name__ == '__main__':
    main()
