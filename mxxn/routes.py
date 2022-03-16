"""
The routes module.

In the Mxxn framework there are two types of routes, the routes
to resources and the routes to static file. Both are defined
differently, but the way is identical in all framework packages
(Mxxn, Mxn and MxnApp). During the initialization of the
application, routes are searched for in the respective packets
and they are registered automatically.

**Routes to resources**


**Routes to static files**

"""
from pathlib import Path
from falcon import Request, Response
from mxxn.resources import Root, App, Themes
from mxxn.settings import Settings
from mxxn.env import MxnApp, Mxn
from mxxn.exceptions.env import MxnAppNotExistError


ROUTES = [
        {'url': 'ROOT', 'resource': Root},
        {'url': '/', 'resource': App},
        {'url': '/themes', 'resource': Themes},
        {'url': '/themes/{id}', 'resource': Themes}]
"""The routes definition of the mxxn package."""


class StaticRoutesMiddleware():
    """The middleware for static routes."""
    def __init__(self, settings: Settings) -> None:
        """
        Initialize the StaticRoutesMiddleware instance.

        Args:
            settings: The settings of the application.
        """
        self._covers = None

        try:
            mxnapp = MxnApp()
            self._covers = mxnapp.static_file_covers(settings)

            for mxn_name in self._covers['mxns']:
                mxn = Mxn(mxn_name)
                self._covers['mxns'][mxn.unprefixed_name] = \
                    self._covers['mxns'].pop(mxn_name)

        except MxnAppNotExistError:
            pass

    async def process_request(self, req: Request, resp: Response) -> None:
        """
        Change the path to covered static file.

        Args:
            req: The request object.
            resp: The response object.
        """
        if req.path.startswith(('/static/mxxn/', '/static/mxns/')) \
                and self._covers:
            parts = Path(req.path).parts

            if parts[2] == 'mxxn':
                static_file = Path(*parts[3:])

                if static_file in self._covers['mxxn']:
                    req.path = req.path.replace(
                            '/static', '/static/covers', 1)
            else:
                if len(parts) >= 5:
                    static_file = Path(*parts[4:])
                    mxn_name = parts[3]

                    if mxn_name in self._covers['mxns'] \
                            and static_file in self._covers['mxns'][mxn_name]:
                        req.path = req.path.replace(
                                '/static', '/static/covers', 1)
