"""This module contains several exceptions for package handling."""
from mxxn import exceptions


class PackageError(exceptions.Base):
    """The base class for all package exceptions."""

    pass


class PackageNotExistError(PackageError):
    """Raised if an Python package does not exist."""

    pass


class MxnNotExistError(PackageError):
    """Raised if an mixxin does not exist."""

    pass


class MixxinAppNotExistError(PackageError):
    """Raised if the mixxin app does not exist."""

    pass


class MultipleMixxinAppsError(PackageError):
    """Raised if the mixxin app does not exist."""

    pass
