"""Main module."""

from page_loader.cli import parse_args
from page_loader.loader import download


def main():
    """Download page."""
    url, output = parse_args()
    file_path = download(url, output)
    print(file_path)


if __name__ == '__main__':
    main()
