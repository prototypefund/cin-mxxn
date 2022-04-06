from falcon import Request, Response, HTTP_200
from mxxn import env


class Themes():
    """The Theme resource of the Mxxn package."""

    async def on_get(self, req: Request, resp: Response, id=None) -> None:
        """
        Get the list of avialable themes.

        Args:
            req: The request object.
            resp: The response object.
        """
        mxxn_pkg = env.Mxxn()
        themes = mxxn_pkg.theme_list

        if id in themes:
            resp.media = mxxn_pkg.theme(id)
            resp.status = HTTP_200

            return

        themes = mxxn_pkg.theme_list
        resp.media = [
                {'id': 0, 'name': themes[0]},
                {'id': 1, 'name': themes[1]}]

        resp.status = HTTP_200
