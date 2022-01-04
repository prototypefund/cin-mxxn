"""The app module."""
from falcon import asgi


class App(object):
    """The App class is the base for creating a Mixxin applications."""

    def __init__(self) -> None:
        self.asgi = asgi.App()
