"""The route module."""
from mxxn.resources import Root, App, Themes

routes = [
        {'url': '/', 'resource': Root},
        {'url': '/app', 'resource': App},
        # {'url': '/app/themes', 'resource': Themes},
        {'url': '/app/themes/{id}', 'resource': Themes}]
