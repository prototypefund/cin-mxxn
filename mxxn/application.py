"""The app module."""
from falcon import asgi
from mxxn.settings import Settings, SettingsMiddleware
from mxxn.logging import logger
from mxxn.env import Mxxn, mxns, Mxn, MxnApp
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import capture_errors


class App(object):
    """The App class is the base for creating a Mxxn applications."""

    def __init__(self) -> None:
        self.settings = Settings()
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
        mixxin = Mxxn()

        for resource_dict in mixxin.resources:
            resource = resource_dict['resource']
            routes = resource_dict['routes']

            for route in routes:
                if len(route) > 1:
                    self.asgi.add_route(route[0], resource(), suffix=route[1])

                    continue

                if route[0] == '/.root':
                    self.asgi.add_route('/', resource())

                    continue

                self.asgi.add_route(route[0], resource())

        log.debug(
            'The resources of the mxxn package were registered.'
        )

        for mixin_name in mxns(self.settings):
            mixin = Mxn(mixin_name)

            for resource_dict in mixin.resources:
                resource = resource_dict['resource']
                routes = resource_dict['routes']

                for route in routes:
                    prefix = '/mxns/' + mixin_name
                    if len(route) > 1:
                        self.asgi.add_route(
                            prefix + route[0], resource(),
                            suffix=route[1]
                        )

                        continue

                    self.asgi.add_route(prefix + route[0], resource())

            log.debug(
                'The resources of the mxn "{}" were registered.'
                .format(mixin_name)
            )

        try:
            app = MxnApp()

            for resource_dict in app.resources:
                resource = resource_dict['resource']
                routes = resource_dict['routes']

                for route in routes:
                    if len(route) > 1:
                        self.asgi.add_route(
                            '/app'+route[0],
                            resource(),
                            suffix=route[1]
                        )

                        continue

                    self.asgi.add_route('/app'+route[0], resource())

            log.debug(
                'The resources of the application package {} were registered.'
                .format(app.name)
            )

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
