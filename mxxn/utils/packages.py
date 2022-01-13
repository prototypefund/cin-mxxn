"""The packages module of the utils module."""
import inspect
from typing import Optional


def caller_package_name(depth: int = 1) -> Optional[str]:
    """
    Get the package name.

    The function returns the name of the package in
    which the function was called.

    Args:
        depth: The depth of the caller stack.
    """
    stack = inspect.stack()
    frame = stack[depth]
    module = inspect.getmodule(frame[0])

    if module:
        return module.__name__.split('.')[0]

    return None
