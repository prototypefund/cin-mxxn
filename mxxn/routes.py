"""
The routes module.

The routes to the resources of the Mxxn package are defined
in the routes module. In addition, routes related middleware
is also defined here.
"""
from typing import TypedDict
from typing_extensions import NotRequired
from jsonschema import validate, ValidationError
from pathlib import Path
from falcon import Request, Response, HTTPBadRequest
from mxxn.resources import Root, App
from mxxn.resources.themes import Themes
from mxxn.resources.strings import Strings
from mxxn.settings import Settings
from mxxn.env import MxnApp, Mxn
from mxxn.exceptions.env import MxnAppNotExistError


class Route(TypedDict):
    """The type definition for the route dictionary."""

    url: str
    resource: object
    suffix: NotRequired[str]


Routes = list[Route]
"""The type definition for the routes list."""


ROUTES: Routes = [
        {'url': 'APP_ROOT', 'resource': Root},
        {'url': '/', 'resource': App},
        {'url': '/themes', 'resource': Themes},
        {'url': '/themes/{id}', 'resource': Themes},
        {'url': '/strings', 'resource': Strings},
        {'url': '/strings/{id}', 'resource': Strings}]
"""The routes definition of the mxxn package."""


class StaticRoutesMiddleware:
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
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
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


class QueryStringValidationMiddleware:
    """The middleware for query string validation."""

    async def process_resource(self, req, resp, resource, params):
        """
        Validate the query string of the URL.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.

        Raises:
            HTTPBadRequest: If the query string is invalid.
        """
        if hasattr(resource, 'QUERY_STRING_DEFINITION') and req.params:
            definition = resource.QUERY_STRING_DEFINITION

            try:
                if not params:
                    schema = definition[req.method]['none']
                    validate(instance=req.params, schema=schema)

                else:
                    if not len(params) == 1:
                        raise HTTPBadRequest(
                            title='Only one parameter allowed.',
                            description='Only one parameter allowed in '
                            'the request URL'
                            )

                    else:
                        param_name = list(params.keys())[0]
                        schema = definition[req.method][param_name]
                        validate(instance=req.params, schema=schema)

            except ValidationError:
                raise HTTPBadRequest(
                        title='Query string error',
                        description='The query string for the '
                        f'{resource.__class__.__name__} resource is not valid'
                        )

            except KeyError:
                raise HTTPBadRequest(
                        title='Query string error',
                        description=f'Query string for {req.method} method of '
                        f'{resource.__class__.__name__} resource not allowed'
                        )
