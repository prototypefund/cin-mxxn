"""
The the exception package.

In this module the base class of all framework exceptions
and the capture_errors function is defined.
"""
import traceback
import falcon
from mxxn.logging import logger
from falcon import Request, Response
from typing import Dict


async def capture_errors(
            req: Request, resp: Response, ex: Exception, params: Dict
        ) -> None:
    """
    Capture the unhandled errors.

    This error handler logs all unhandled server-side errors into the
    error log and even throws the HTTPInternalServerError exception.
    For security reasons, no information about the occurred error is
    sent to the client. It only receives the information that a
    server-side error has occurred and that it has been logged into
    the error log.

    Args:
        req: The Falcon request object.
        resp: The Falcon response object.
        ex: A class that inherited from Exception.
        params: A dictionary of parameters.

    Raises:
        falcon.HTTPInternalServerError: If an error occurred.
    """
    log = logger('request')
    log.error('\n' + traceback.format_exc())

    message = 'An error occurred while executing server-side program code. '\
        'The necessary information has been logged and is available to the '\
        'administrator.'

    raise falcon.HTTPInternalServerError(description=message)


class Base(Exception):
    """The base class for all framework exceptions."""

    pass
