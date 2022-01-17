"""The app module."""
from falcon import asgi
from mxxn.settings import Settings
from mxxn.logging import logger
from mxxn.env import Mxxn, mxns, Mxn, MxnApp
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import capture_errors


class App(object):
    """The App class is the base for creating a Mxxn applications."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.asgi = asgi.App()
        self.asgi.add_error_handler(Exception, capture_errors)
        self._register_resources()

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

            if not mixin.resources:
                log.debug(
                    'The mxn "{}" contains no resources.'
                    .format(mixin_name)
                )

                continue

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
