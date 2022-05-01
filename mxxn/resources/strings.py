"""The strings module."""
from falcon import Request, Response, HTTP_200, HTTPBadRequest, HTTP_NO_CONTENT
from mxxn import env
from mxxn import config
from typing import Optional, List
from mxxn.exceptions import config as config_ex


class Strings:
    """The Strings resource of the Mxxn package."""
    # QUERY_STRING_DEFINITION = {
    #     'GET': {
    #         'none': {
    #             'type': 'object',
    #             'properties': {
    #                 'fields': {
    #                     'anyOf': [
    #                         {
    #                             'type': 'string',
    #                             'enum': ['id', 'theme']
    #
    #                         },
    #                         {
    #                             'type': 'array',
    #                             'items': {
    #                                 'enum': ['id', 'theme']
    #                                 }
    #                         }]
    #                     }
    #                 },
    #             'additionalProperties': False,
    #             }
    #         }
    #     }

    async def on_get(
            self,
            req: Request,
            resp: Response,
            id: Optional[str] = None
            ) -> None:
        """
        Get the list of avialable string configs.

        Args:
            req: The request object.
            resp: The response object.
            id: The id if the requested theme
        """
        mxxn_pkg = env.Mxxn()
        mxxn_strings = mxxn_pkg.strings

        params = req.params

        if id:
            try:
                resp.media = config.strings(id, req.context.settings)
                resp.status = HTTP_200

            except ValueError:
                resp.status = HTTP_NO_CONTENT
        else:
            strings: List[dict] = []
            strings_names = mxxn_strings.names

            if params:
                for name in strings_names:
                    filtered_strings: dict = {}

                    if 'id' in params['fields']:
                        filtered_strings['id'] = name

                    if 'strings' in params['fields']:
                        filtered_strings['theme'] = config.theme(
                                name, req.context.settings)

                    strings.append(filtered_strings)

                resp.media = strings
                resp.status = HTTP_200
            else:
                for name in strings_names:
                    strings.append({
                        'id': name,
                        'strings': config.strings(name, req.context.settings)
                        })

                resp.media = strings
                resp.status = HTTP_200
