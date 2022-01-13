"""The app module."""
from falcon import asgi
from mxxn.settings import Settings
from mxxn import resources


class App(object):
    """The App class is the base for creating a Mixxin applications."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.asgi = asgi.App()

        self.asgi.add_route('/', resources.App())
