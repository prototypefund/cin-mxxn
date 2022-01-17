"""The Resource package of the Mixxin package."""
import falcon
from mxxn.hooks import render


class Root(object):
    """The Root resource of the Mxxn package."""

    async def on_get(self, req, resp):
        """Forward the get request to the app resource."""
        raise falcon.HTTPMovedPermanently('.app')


class App(object):
    """The App resource of the Mxxn package."""
    @falcon.after(render, template='app.j2')
    async def on_get(self, req, resp):
        """Get the application front-end."""

        pass
