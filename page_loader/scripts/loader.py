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
    except exceptions.NetworkError as error:
        logging.error(error)
        sys.exit(1)
    except exceptions.HTTPError as error:
        logging.error(error)
        sys.exit(1)
    except exceptions.Timeout as error:
        logging.error(error)
        sys.exit(1)
    except exceptions.FileSystemError as error:
        logging.error(error)
        sys.exit(1)
    else:
        print(file_path)


if __name__ == '__main__':
    main()
