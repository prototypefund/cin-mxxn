"""The app module."""
from falcon import asgi
from typing import Optional
from mxxn.settings import Settings, SettingsMiddleware
from mxxn.routes import StaticRoutesMiddleware
from mxxn.logging import logger
from mxxn.env import Mxxn, mxns, Mxn, MxnApp, TypeRoutes
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import capture_errors
from mxxn.database import Database


class App(object):
    """The App class is the base for creating a Mxxn applications."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.database = Database(self.settings)
        settings_middleware = SettingsMiddleware(self.settings)
        static_routes_middleware = StaticRoutesMiddleware(self.settings)
        self.asgi = asgi.App()
        self.asgi.add_error_handler(Exception, capture_errors)
        self.asgi.add_middleware([
            settings_middleware, static_routes_middleware])
        self._register_routes()
        self._register_static_paths()

    def _register_routes(self) -> None:
        """
        Register all routes of the framwork packages.

        This method registers all routes available in the Mxxn, MxnApp and
        in installed Mxn package.

        """
        log = logger('registration')

        def add_routes(
                routes: Optional[TypeRoutes],
                pkg_name: str, mount: str = ''
                ) -> None:
            if routes:
                for route in routes:
                    url = route['url']

                    if mount and len(url) == 1:
                        url = url[1:]

                    url = mount + url

                    if 'suffix' in route:
                        self.asgi.add_route(
                            url, route['resource'](), suffix=route['suffix'])

                        continue

                    self.asgi.add_route(url, route['resource']())

                log.debug(
                    f'The routes of the {pkg_name} package were registered.'
                )

        def cover(
                routes: Optional[TypeRoutes],
                cover_routes: TypeRoutes
                ) -> Optional[TypeRoutes]:
            if routes:
                for cover_route in cover_routes:
                    for route in routes:
                        if cover_route['url'] == route['url']:
                            if len(cover_route) == 3  \
                                    and len(route) == 3 \
                                    and cover_route['suffix'] != \
                                    route['suffix']:

                                continue

                            route['resource'] = cover_route['resource']

            return routes

        route_covers = None

        try:
            mxnapp_pkg = MxnApp()
            route_covers = mxnapp_pkg.route_covers(self.settings)
            add_routes(mxnapp_pkg.routes, mxnapp_pkg.name, '/app/mxnapp')

        except env_ex.MxnAppNotExistError:
            pass

        mxxn_pkg = Mxxn()
        routes = mxxn_pkg.routes

        if route_covers:
            routes = cover(routes, route_covers['mxxn'])

        add_routes(routes, mxxn_pkg.name)

        for mxn_name in mxns(self.settings):
            mxn_pkg = Mxn(mxn_name)
            routes = mxn_pkg.routes

            if route_covers and mxn_name in route_covers['mxns']:
                routes = cover(routes, route_covers['mxns'][mxn_name])

            add_routes(
                    mxn_pkg.routes, mxn_pkg.name,
                    '/app/mxns/'+mxn_pkg.unprefixed_name)

    def _register_static_paths(self) -> None:
        """
        Register the static folder of the framework packages.

        """
        log = logger('registration')
        mxxn = Mxxn()

        static_path = mxxn.static_path

        if static_path:
            self.asgi.add_static_route('/static/mxxn', static_path)

            log.debug(
                'The static folder of the mxxn package was registered.')

        for mxn_name in mxns(self.settings):
            mxn = Mxn(mxn_name)
            static_path = mxn.static_path

            if static_path:
                self.asgi.add_static_route(
                    '/static/mxns/' + mxn.unprefixed_name, static_path
                )

                log.debug(
                    'The static folder of the {} package was registered.'
                    .format(mxn.name)
                )

        try:
            mxnapp = MxnApp()

            static_path = mxnapp.static_path
            static_file_covers = mxnapp.static_file_covers(self.settings)

            if static_path:
                self.asgi.add_static_route('/static/mxnapp', static_path)

                log.debug(
                    'The static folder of the app package {} was registered.'
                    .format(mxnapp.name)
                )

            if static_file_covers['mxxn']:
                self.asgi.add_static_route(
                        '/static/covers/mxxn',
                        mxnapp.path/'covers/mxxn/frontend/static')

            for mxn_name, pathes in static_file_covers['mxns'].items():
                if pathes:
                    mxn = Mxn(mxn_name)
                    self.asgi.add_static_route(
                        '/static/covers/mxns/' + mxn.unprefixed_name,
                        mxnapp.path/(
                            'covers/mxns/' + mxn_name + '/frontend/static'))

        except env_ex.MxnAppNotExistError:
            pass
