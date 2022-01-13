"""The Resource package of the Mixxin package."""
import falcon


class Root(object):
    """The Root resource of the Mixxin package."""

    async def on_get(self, req, resp):
        """Forward the get request to the app resource."""
        raise falcon.HTTPMovedPermanently('.app')


class App(object):
    """The App resource of the Mixxin package."""

    async def on_get(self, req, resp):
        """Get the application front-end."""
        resp.text = 'Mixxin'
        resp.content_type = falcon.MEDIA_HTML
