"""The Resource package of the mixxin package."""
import falcon


class App(object):
    """The App resource of the mixxin package."""

    async def on_get(self, req, resp):
        """Get the application front-end."""
        resp.text = 'Mixxin'
        resp.content_type = falcon.MEDIA_HTML
