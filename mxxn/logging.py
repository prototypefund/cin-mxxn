"""Logging module of the application."""
from typing import Optional
from logging import Logger, getLogger
from mxxn.utils.packages import caller_package_name


def logger(context: Optional[str] = None) -> Logger:
    """
    Get a context based application logger.

    Args:
        context: The name of the logging context.

    Return:
        A mixxin application logger.
    """
    caller_package = caller_package_name()

    if context:
        return getLogger(f'mxxn.{caller_package}.{context}')

    return getLogger(f'mxxn.{caller_package}')
