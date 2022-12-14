Routing
=======


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

Routes to resources
-------------------

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

Resource route covers
---------------------

It is possible to change the resources of specific routes. For this purpose,
these routes are covered in the MxnApp package. To achieve this, a routes.py
module is created in the respective cover package of the MxnApp package and
the URL to be covered and the corresponding resource are defined in it.
For example, if the Tasks resource of an *mxntodo* package should be covered,
the following folder structure must be created in the MxnApp package.

.. code-block:: bash

    mxnapp
    |-- covers
    |???? |-- __init__.py
    |???? |-- mxns
    |???? |???? |-- __init__.py
    |???? |???? |-- mxntodo
    |???? |???? |   |-- __init__.py
    |   |   |   |-- routes.py
    |   |   |   |-- resources.py
    |-- __init__.py
    setup.cfg

In the routes.py module, the route is then defined as follows.

.. code:: python

    ROUTES: Routes = [{'url': '/tasks', 'resource': Tasks}]

The new Tasks resource should be defined in resource module or in the
respective module of the resource package.


Routes to static files
----------------------

To register static files, the folder *frontend/static* must be created in
the respective framework package (Mxxn, Mxn or MxnApp).

.. code-block:: bash

    mxntodo
    |-- __init__.py
    |-- frontend
    |   |-- static
    |???? |   |-- js
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

Static file covers
------------------

To cover the static file, the new file with the same name must be in the
same location in the *frontend/static* folder of the cover package of the
specific framework package.

.. code-block:: bash

    mxnapp
    |-- covers
    |???? |-- __init__.py
    |???? |-- mxns
    |???? |???? |-- __init__.py
    |???? |???? |-- mxntodo
    |???? |???? |   |-- __init__.py
    |   |   |   |-- frontend
    |   |   |   |   |-- static
    |   |   |   |   |   |-- js
    |   |   |   |   |   |   |-- mxn.js
    |-- __init__.py
    setup.cfg
