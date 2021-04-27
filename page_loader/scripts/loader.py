"""Main module."""
import logging
import sys

from page_loader import exceptions
from page_loader.cli import parse_args
from page_loader.loader import download


def main():
    """Download page."""
    logging.basicConfig(level=logging.INFO)
    url, output = parse_args()

    try:
        file_path = download(url, output)
    except exceptions.NetworkError:
        sys.exit(1)
    except exceptions.HTTPError:
        sys.exit(1)
    except exceptions.Timeout:
        sys.exit(1)
    except exceptions.FileSystemError:
        sys.exit(1)
    else:
        print(file_path)


if __name__ == '__main__':
    main()
