"""
The settings exceptions module.

This module contains exceptions that may occur during the
use of the Settings class.
"""
from mxxn import exceptions


class SettingsError(exceptions.Base):
    """The base exception for all settings exceptions."""

    pass


class SettingsFormatError(SettingsError):
    """Raised if format error in settings file."""

    pass
