"""The Resource package of the Mixxin package."""
import falcon
from mxxn.hooks import render
from mxxn.exceptions import env as env_ex
from mxxn import env


class Root(object):
    """The Root resource of the Mxxn package."""

    async def on_get(self, req, resp):
        """Forward the get request to the app resource."""
        raise falcon.HTTPMovedPermanently('.app')


class App(object):
    """The App resource of the Mxxn package."""

    @falcon.after(render, template='app.j2')
    async def on_get(self, req, resp):
        """Get the application frontend."""
        # TODO mxnapp js
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
                js_urls.append('static/app/js/'+js_file)

        except env_ex.MxnAppNotExistError:
            pass

        resp.context.render = {
                'auth': True,
                'js_urls': js_urls
            }
