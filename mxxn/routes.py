"""The route module."""
from mxxn.resources import Root, App, Themes

routes = [
        {'url': '/', 'resource': Root},
        {'url': '/app', 'resource': App},
        # {'url': '/app/theme/', 'resource': Themes},
        {'url': '/app/theme/{id}', 'resource': Themes}]
