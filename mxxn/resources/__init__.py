"""The Resource package of the Mixxin package."""
from falcon import after, Request, Response, HTTPMovedPermanently
from mxxn.hooks import render
from mxxn.exceptions import env as env_ex
from mxxn import env


class Root():
    """The Root resource of the Mxxn package."""

    async def on_get(self, req: Request, resp: Response) -> None:
        """
        Forward the get request to the App resource.

        Args:
            req: The request object.
            resp: The response object.
        """
        raise HTTPMovedPermanently('.app')


class App():
    """The App resource of the Mxxn package."""

    @after(render, template='app.j2')
    async def on_get(self, req: Request, resp: Response) -> None:
        """
        Get the application frontend.

        Args:
            req: The request object.
            resp: The response object.

        """
        js_urls = []
        mxxn = env.Mxxn()

        for js_file in mxxn.js_files:
            js_urls.append('static/js'/js_file)

        for mxn_name in env.mxns(req.context.settings):
            mxn = env.Mxn(mxn_name)

            for js_file in mxn.js_files:
                js_urls.append(
                    ('static/mxns/'+mxn.unprefixed_name+'/js')/js_file)

        try:
            mxnapp = env.MxnApp()

            for js_file in mxnapp.js_files:
                js_urls.append('static/app/js'/js_file)

        except env_ex.MxnAppNotExistError:
            pass

        resp.context.render = {
                'auth': True,
                'js_urls': js_urls
            }
