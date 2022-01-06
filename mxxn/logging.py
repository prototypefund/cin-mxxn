"""Logging module of the application."""
from typing import Optional
from logging import Logger, getLogger


def logger(context: Optional[str] = None) -> Logger:
    """
    Get a logger for the application.

    The logger name is in format *mixxin.<context>*.
    In mixxin each log entry should be assigned to a context.
    The respective context should be one of the following:

    +--------------+----------------------------------------+
    | Context      | Description                            |
    +==============+========================================+
    | settings     | Settings specific logging              |
    +--------------+----------------------------------------+
    | filesystem   | Context for filesystem interactions    |
    +--------------+----------------------------------------+
    | database     | Database specific logging              |
    +--------------+----------------------------------------+
    | registration | Context of component registration like |
    |              | resource or static files               |
    +--------------+----------------------------------------+
    | request      | Context for requests                   |
    +--------------+----------------------------------------+
    | template     | Constext for template rendering        |
    +--------------+----------------------------------------+

    If none of these contexts meets your needs, then you can choose your own.

    Usage:

    .. code-block:: python

        from mxxn.logging import logger

        log = logger('some_context')
        log.error('test error')

    Args:
        context: The name of the logging context.

    Return:
        A mixxin application logger.
    """
    if context:
        return getLogger('mixxin.{}'.format(context))

    return getLogger('mixxin')
