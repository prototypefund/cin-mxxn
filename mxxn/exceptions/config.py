"""This module contains several exceptions for config file handling."""
from mxxn.exceptions import Base


class ConfigsError(Base):
    """The base class for all locale errors."""

    pass


class NoDefaultConfigError(ConfigsError):
    """Raised if no default config was found."""

    pass


class TooManyDefaultConfigsError(ConfigsError):
    """Raised if more than one default config was found."""

    pass


class NotSameDefaults(ConfigsError):
    """Raised if the defaults are not the same."""

    pass


class NoThemeConfigError(ConfigsError):
    """Raised ff there are no theme configuration files."""

    pass
