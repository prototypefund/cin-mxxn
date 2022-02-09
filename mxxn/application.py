"""The app module."""
from falcon import asgi
from mxxn.settings import Settings, SettingsMiddleware
from mxxn.logging import logger
from mxxn.env import Mxxn, mxns, Mxn, MxnApp
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import capture_errors
from mxxn.database import Database


class App(object):
    """The App class is the base for creating a Mxxn applications."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.database = Database(self.settings)
        settings_middleware = SettingsMiddleware(self.settings)
        self.asgi = asgi.App()
        self.asgi.add_error_handler(Exception, capture_errors)
        self.asgi.add_middleware([settings_middleware])
        self._register_routes()
        self._register_static_paths()

    def _register_routes(self) -> None:
        """
        Register all routes of the framwork packages.

        This method registers all routes available in the Mxxn, MxnApp and
        in installed Mxn package.

        """
        # TODO add covers!
        log = logger('registration')

        def add_routes(pkg, mount=''):
            routes = pkg.routes

            if routes:
                for route in pkg.routes:
                    url = route['url']

                    if url[0] != '/':
                        url = '/' + url

                    url = mount + url

                    if 'suffix' in route:
                        self.asgi.add_route(
                            url, route['resource'](), suffix=route['suffix'])

                        continue

                    self.asgi.add_route(url, route['resource']())

                log.debug(
                    f'The routes of the {pkg.name} package were registered.'
                )

        mxxn_pkg = Mxxn()
        add_routes(mxxn_pkg)

        for mxn_name in mxns(self.settings):
            mxn_pkg = Mxn(mxn_name)
            add_routes(mxn_pkg, '/app/mxns/'+mxn_pkg.unprefixed_name)

        try:
            mxnapp_pkg = MxnApp()
            add_routes(mxnapp_pkg, '/app/mxnapp')

        except env_ex.MxnAppNotExistError:
            pass

    def _register_static_paths(self) -> None:
        """
        Register the static folder of the framework packages.

        If the folder ``/frontend/static`` exists in the package,
        it will be accessible under the URL
        ``<domain>/static/<package_name>``.

        """
        log = logger('registration')
        mxxn = Mxxn()

        static_path = mxxn.static_path

        if static_path:
            self.asgi.add_static_route('/static', static_path)

            log.debug(
                'The static folder of the mxxn package was registered.')

        for mxn_name in mxns(self.settings):
            mxn = Mxn(mxn_name)
            static_path = mxn.static_path

            if static_path:
                self.asgi.add_static_route(
                    '/static/mxns/'+mxn.unprefixed_name, static_path
                )

                log.debug(
                    'The static folder of the {} package was registered.'
                    .format(mxn.name)
                )

        try:
            mxnapp = MxnApp()

            static_path = mxnapp.static_path

            if static_path:
                self.asgi.add_static_route('/static/app', static_path)

                log.debug(
                    'The static folder of the app package {} was registered.'
                    .format(mxnapp.name)
                )

        except env_ex.MxnAppNotExistError:
            pass
