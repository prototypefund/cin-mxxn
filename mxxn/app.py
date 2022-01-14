"""The app module."""
from falcon import asgi
from mxxn.settings import Settings
from mxxn import resources
from mxxn.logging import logger
from mxxn.env import Mixxin


class App(object):
    """The App class is the base for creating a Mixxin applications."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.asgi = asgi.App()
        # self._register_resources()

    def _register_resources(self) -> None:
        """
        Register all resources.

        This method registers all resources available in the mixxin and
        in installed mixins.

        """
        log = logger('registration')
        mixxin = Mixxin()

        for resource in mixxin.resources:
            if resource['route'] == './root':
                for suffix in resource['suffixes']:
                    print(resource['route'])
