"""This module contains exceptions for routing."""
from mxxn import exceptions


class RoutingError(exceptions):
    """Base class for all Routing exceptions."""
    pass


class RootRouteError(RoutingError):
    """Raised if an error occurs in contexts with the '/' route."""

    pass
