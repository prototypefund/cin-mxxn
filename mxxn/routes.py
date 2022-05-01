"""
The routes module.

In the Mxxn framework there are two types of routes, the routes
to resources and the routes to static file. Both are defined
differently, but the way is identical in all framework packages
(Mxxn, Mxn and MxnApp). During the initialization of the
application, routes are searched for in the respective packets
and they are registered automatically. The defined routes of the
framework packages are mounted in the URL at specific locations.
The following table shows the respective mount points.

.. list-table::
   :header-rows: 1

   * - Mount point
     - Framework package
   * - /app
     - The routes of the MxnApp package
   * - /app/mxxn
     - The routes of the Mxxn Framework
   * - /app/mxns/<unprefixed name of Mxn package>
     - The routes of the respective Mxn packages

**Routes to resources**

To register routes for resources there must be a routes.py module
in the package. This module must contain a variable named ROUTES.
The ROUTES variable is a dictionary in the following form.

.. code:: python

    ROUTES: Routes = [
            {'url': 'APP_ROOT', 'resource': AppRoot},
            {'url': '/', 'resource': App},
            {'url': '/themes', 'resource': Themes},
            {'url': '/themes/{id}', 'resource': Themes, 'suffix': 'list'}]

The url is the URL that is hooked to the mount point of the particular
package and resource is the associated resource. If the resource uses
a suffix, then this must also be specified.
The route is a normal route of the Falcon framework with all its features.
More information can be found in the Falcon documentation at `Falcon routing`_.

.. _Falcon routing: https://falcon.readthedocs.io/en/stable/api/routing.html

    .. note::

        In this project the agreement is that all URLs to resources end
        without backslash! Please keep this in mind. This is very important
        for a consistent API.

There are two special cases when defining routes. The first relates to the
root URL */* of the package. The root resource is always mounted directly
to the mount point. The reason for this was described in the note above.
For example, if a root resource is defined in the mxntodo package as follows,
then it will be accessible under the URL */app/mxns/todo*, without backslash.

.. code:: python

    ROUTES: Routes = [{'url': '/', 'resource': Root}]

The second special case is the *APP_ROOT* route. This is the real root URL of
the entire application. By default, a call to this URL is forwarded to the
*/app/mxxn* URL. This URL is an exact entry point of the application. However,
if the application is to be used as a backend that displays a frontend page
under the root URL, such as in a CMS system, then this route can be overloaded
using the URL APP_ROOT like this:

.. code:: python

    ROUTES: Routes = [{'url': 'APP_ROOT', 'resource': Frontend}]


But please notice the warning below.

    .. warning::

        The original *APP_ROOT* is defined in the Mxxn package and can only
        be overloaded in route covers of this package. If it is done in
        other packages, the *RootRouteError* exception is raised.

**Resource route covers**

It is possible to change the resources of specific routes. For this purpose,
these routes are covered in the MxnApp package. To achieve this, a routes.py
module is created in the respective cover package of the MxnApp package and
the URL to be covered and the corresponding resource are defined in it.
For example, if the Tasks resource of an *mxntodo* package should be covered,
the following folder structure must be created in the MxnApp package.

.. code-block:: bash

    mxnapp
    |-- covers
    |   |-- __init__.py
    |   |-- mxns
    |   |   |-- __init__.py
    |   |   |-- mxntodo
    |   |   |   |-- __init__.py
    |   |   |   |-- routes.py
    |   |   |   |-- resources.py
    |-- __init__.py
    setup.cfg

In the routes.py module, the route is then defined as follows.

.. code:: python

    ROUTES: Routes = [{'url': '/tasks', 'resource': Tasks}]

The new Tasks resource should be defined in resource module or in the
respective module of the resource package.


**Routes to static files**
To register static files, the folder *frontend/static* must be created in
the respective framework package (Mxxn, Mxn or MxnApp).

.. code-block:: bash

    mxntodo
    |-- __init__.py
    |-- frontend
    |   |-- static
    |   |   |-- js
    |   |   |   |-- mxn.js
    setup.cfg

All files of the folder and its subfolders are then accessible via the
following URLs.

.. list-table::
   :header-rows: 1

   * - Mount point
     - Framework package
   * - /static/app
     - The static folder of the MxnApp package
   * - /staic/app/mxxn
     - The static folder of the Mxxn Framework
   * - /static/app/mxns/<unprefixed name of Mxn package>
     - The static of the respective Mxn packages

**Static file covers**

To cover the static file, the new file with the same name must be in the
same location in the *frontend/static* folder of the cover package of the
specific framework package.

.. code-block:: bash

    mxnapp
    |-- covers
    |   |-- __init__.py
    |   |-- mxns
    |   |   |-- __init__.py
    |   |   |-- mxntodo
    |   |   |   |-- __init__.py
    |   |   |   |-- frontend
    |   |   |   |   |-- static
    |   |   |   |   |   |-- js
    |   |   |   |   |   |   |-- mxn.js
    |-- __init__.py
    setup.cfg
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
