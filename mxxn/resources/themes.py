from falcon import Request, Response, HTTP_200
from mxxn import env
from mxxn import config
from typing import Optional


class Themes():
    """The Theme resource of the Mxxn package."""

    async def on_get(
            self,
            req: Request,
            resp: Response,
            id: Optional[str] = None
            ) -> None:
        """
        Get the list of avialable themes.

        Args:
            req: The request object.
            resp: The response object.
            id: The id if the requested theme
        """
        mxxn_pkg = env.Mxxn()
        mxxn_theme = mxxn_pkg.theme
        params = req.params

        if id:
            resp.media = config.theme(id, req.context.settings)
            resp.status = HTTP_200

            return

        themes = []
        theme_names = mxxn_theme.names

        for name in theme_names:
            filtered_theme = {}

            if 'fields' in params:
                if 'id' in params['fields']:
                    filtered_theme['id'] = name

                if 'theme' in params['fields']:
                    filtered_theme['theme'] = config.theme(
                            name, req.context.settings)

                themes.append(filtered_theme)
            else:
                themes.append({
                    'id': name,
                    'theme': config.theme(name, req.context.settings)
                    })

        resp.media = themes
        resp.status = HTTP_200
