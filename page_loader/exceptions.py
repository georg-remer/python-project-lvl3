"""Known exceptions."""


class NetworkError(Exception):
    """Network problem occured."""

    pass


class HTTPError(Exception):
    """HTTP request returned an unsuccessful status code."""

    pass


class RequestTimeoutError(Exception):
    """Request times out."""

    pass


class FileSystemError(Exception):
    """OS error.

    This exception is raised when a system function returns
    a system-related error, including I/O failures such as
    “file not found” or “disk full”

    https://docs.python.org/3/library/exceptions.html#OSError
    """
