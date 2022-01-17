"""The app module."""
from falcon import asgi
from mxxn.settings import Settings
from mxxn.logging import logger
from mxxn.env import Mixxin, mxns, Mixin, MixxinApp
from mxxn.exceptions import env as env_ex


class App(object):
    """The App class is the base for creating a Mixxin applications."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.asgi = asgi.App()
        self._register_resources()

    def _register_resources(self) -> None:
        """
        Register all resources.

        This method registers all resources available in the mixxin and
        in installed mixins.

        """
        log = logger('registration')
        mixxin = Mixxin()

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
            'The resources of the mixxin package were registered.'
        )

        for mixin_name in mxns(self.settings):
            mixin = Mixin(mixin_name)

            if not mixin.resources:
                log.debug(
                    'The mixin "{}" contains no resources.'
                    .format(mixin_name)
                )

                continue

            for resource_dict in mixin.resources:
                resource = resource_dict['resource']
                routes = resource_dict['routes']

                for route in routes:
                    prefix = '/mxn/' + mixin_name
                    if len(route) > 1:
                        self.asgi.add_route(
                            prefix + route[0], resource(),
                            suffix=route[1]
                        )

                        continue

                    self.asgi.add_route(prefix + route[0], resource())

            log.debug(
                'The resources of the mixin "{}" were registered.'
                .format(mixin_name)
            )

        try:
            app = MixxinApp()

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

        except env_ex.MixxinAppNotExistError:
            pass
