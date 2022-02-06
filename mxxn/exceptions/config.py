"""This module contains several exceptions for config file handling."""
from mxxn.exceptions import Base


class ConfigsError(Base):
    """The base class for all locale errors."""

    pass


class NoDefaultConfigError(ConfigsError):
    """Raised when no default config was found."""

    pass


class TooManyDefaultConfigsError(ConfigsError):
    """Raised when more than one default config was found."""

    pass
