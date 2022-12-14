"""
The filesystem exceptions module.

This module contains exceptions that can be
thrown when accessing files or directories.
"""
from mxxn import exceptions


class FileSysError(exceptions.Base):
    """The base exception for all filesystem exceptions."""

    pass


class FileNotExistError(FileSysError):
    """Raised if the file does not exist."""

    pass


class PathNotExistError(FileSysError):
    """Raised if the path does not exist."""

    pass


class PathNotEmptyError(FileSysError):
    """Raised if the path is not empty."""

    pass


class ExtensionError(FileSysError):
    """Raised if file has a wrong extension."""

    pass


class FileFormatError(FileSysError):
    """Raised if file has a wrong format."""

    pass
