"""The theme module."""
from falcon import Request, Response, HTTP_200, HTTP_NO_CONTENT
from mxxn import env
from mxxn import config
from typing import Optional, List


class Themes():
    """The Theme resource of the Mxxn package."""
    QUERY_STRING_DEFINITION = {
        'GET': {
            'none': {
                'type': 'object',
                'properties': {
                    'fields': {
                        'anyOf': [
                            {
                                'type': 'string',
                                'enum': ['id', 'theme']

                            },
                            {
                                'type': 'array',
                                'items': {
                                    'enum': ['id', 'theme']
                                    }
                            }]
                        }
                    },
                'additionalProperties': False,
                }
            }
        }

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
            try:
                resp.media = config.theme(id, req.context.settings)
                resp.status = HTTP_200

            except ValueError:
                resp.status = HTTP_NO_CONTENT
        else:
            themes: List[dict] = []
            theme_names = mxxn_theme.names

            if params:
                for name in theme_names:
                    filtered_theme: dict = {}

                    if 'id' in params['fields']:
                        filtered_theme['id'] = name

                    if 'theme' in params['fields']:
                        filtered_theme['theme'] = config.theme(
                                name, req.context.settings)

                    themes.append(filtered_theme)

                resp.media = themes
                resp.status = HTTP_200
            else:
                for name in theme_names:
                    themes.append({
                        'id': name,
                        'theme': config.theme(name, req.context.settings)
                        })

                resp.media = themes
                resp.status = HTTP_200
