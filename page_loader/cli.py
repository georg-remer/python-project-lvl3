"""CLI parser."""

import argparse
import os


def parse_args():
    """Parse arguments.

    Returns:
        (str, str)
    """
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument(
        '-o',
        '--output',
        default=os.getcwd(),
        help='directory to save result file',
    )
    parser.add_argument('url')

    args = parser.parse_args()

    return args.url, args.output
