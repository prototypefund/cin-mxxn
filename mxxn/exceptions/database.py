"""This module contains several database exceptions."""
from mxxn import exceptions


class DBError(exceptions.Base):
    """The base exception for all database exceptions."""

    pass


class URLError(DBError):
    """Raised if there is an error in the URL."""

    pass
