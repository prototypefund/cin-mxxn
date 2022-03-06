"""The route module."""
from mxxn.resources import Root, App, Themes
from mxxn.env import mxns

ROUTES = [
        {'url': '/', 'resource': Root},
        {'url': '/app', 'resource': App},
        {'url': '/app/themes', 'resource': Themes},
        {'url': '/app/themes/{id}', 'resource': Themes}]


class StaticRoutesMiddleware():
    def __init__(self, settings):
        self._settings = settings

        print(mxns(settings))

    async def process_request(self, req, resp):
        pass
