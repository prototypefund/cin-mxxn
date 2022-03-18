"""This module contains exceptions for routing."""
from mxxn.exceptions import Base


class RoutingError(Base):
    """Base class for all Routing exceptions."""

    pass


class RootRouteError(RoutingError):
    """Raised if an error occurs in contexts with the '/' route."""

    pass
