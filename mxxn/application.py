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
        self._register_resources()
        self._register_static_paths()

    def _register_resources(self) -> None:
        """
        Register all resources.

        This method registers all resources available in the mixxin and
        in installed mxns.

        """
        # TODO add covers!
        log = logger('registration')
        routes_list = []
        mixxin = Mxxn()

        for resource_dict in mixxin.resources:
            resource = resource_dict['resource']
            routes = resource_dict['routes']

            for route in routes:
                if len(route) > 1:
                    routes_list.append([route[0], resource(), route[1]])
                    # self.asgi.add_route(route[0], resource(), suffix=route[1])

                    continue

                if route[0] == '/.root':
                    routes_list.append(['/', resource()])
                    # self.asgi.add_route('/', resource())

                    continue

                routes_list.append([route[0], resource()])
                # self.asgi.add_route(route[0], resource())

        log.debug(
            'The resources of the mxxn package were registered.'
        )

        for mixin_name in mxns(self.settings):
            mixin = Mxn(mixin_name)

            for resource_dict in mixin.resources:
                resource = resource_dict['resource']
                routes = resource_dict['routes']

                for route in routes:
                    prefix = '/mxns/' + mixin.unprefixed_name

                    if len(route) > 1:
                        routes_list.append([prefix + route[0], resource(), route[1]])
                        # self.asgi.add_route(
                        #     prefix + route[0], resource(),
                        #     suffix=route[1]
                        # )

                        continue

                    routes_list.append([prefix + route[0], resource()])
                    # self.asgi.add_route(prefix + route[0], resource())

            log.debug(
                'The resources of the mxn "{}" were registered.'
                .format(mixin_name)
            )

        covering_resources = None

        try:
            app = MxnApp()
            covering_resources = app.covering_resources(self.settings)

            for resource_dict in app.resources:
                resource = resource_dict['resource']
                routes = resource_dict['routes']

                for route in routes:
                    prefix = '/app'

                    if len(route) > 1:
                        routes_list.append([prefix + route[0], resource(), route[1]])
                        # self.asgi.add_route(
                        #     '/app'+route[0],
                        #     resource(),
                        #     suffix=route[1]
                        # )

                        continue

                    routes_list.append([prefix + route[0], resource()])
                    # self.asgi.add_route('/app'+route[0], resource())

            log.debug(
                'The resources of the application package {} were registered.'
                .format(app.name)
            )

        except env_ex.MxnAppNotExistError:
            pass

        # print(covering_resources)

        for route in routes_list:
            if len(route) == 2:
                self.asgi.add_route(route[0], route[1])

                continue

            self.asgi.add_route(route[0], route[1], suffix=route[2])

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
