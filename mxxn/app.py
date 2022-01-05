"""The app module."""
from falcon import asgi
from mxxn.settings import Settings


class App(object):
    """The App class is the base for creating a Mixxin applications."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.asgi = asgi.App()
