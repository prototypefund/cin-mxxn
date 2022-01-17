"""This module contains some before and after hooks."""
from jinja2 import Environment, PackageLoader
from jinja2 import exceptions as jinja2_ex
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import filesys as filesys_ex
from pathlib import Path
import falcon
from typing import Type


async def render(
            req: falcon.Request,
            resp: falcon.Response,
            resource: Type,
            package: str,
            template: Path,
            media_type: str = falcon.MEDIA_HTML
        ) -> None:
    """
    Render the given Jinja2 template.

    This is an after-responder hook that renders a passed Jinja2
    template. The template must be located in the template folder
    of the passed package. The template name must be relative to
    the template folder in the given package. The variables to
    render are passed to the render hook via the resp.context.render
    attribute of the response variable.

    Examples:
        .. code-block:: python

            import falcon
            from mxxn import hooks
            from pathlib import Path

            class Resource(object):
                @falcon.after(
                    hooks.render, 'package_name', Path('path/to/template.j2')
                )
                def on_get(self, req, resp):
                    resp.context.render = {'variable': 123}

    Args:
        req: The Falcon request object.
        resp: The Falcon response object containing the variables in
            the media attribute.
        resource: The called Falcon resource.
        package: The name of the package in which the template is located.
        template: The name of the template (relative to the template folder
            of the package).
        media_type: The media type of the rendered data. Default type is
            falcon.MEDIA_HTML.

    Raises:
        falcon.HTTPInternalServerError: If the package not exist, if the
            template not exist, if some syntax error in the template.
    """
    try:
        env = Environment(loader=PackageLoader(package, 'templates'))
        jinja2_template = env.get_template(str(template))

        if hasattr(resp.context, 'render'):
            resp.text = jinja2_template.render(resp.context.render)
        else:
            resp.text = jinja2_template.render()

        resp.content_type = media_type
        resp.status = falcon.HTTP_200

    except ModuleNotFoundError:
        raise env_ex.PackageNotExistError(
            '{}: The framework package "{}" does not exist.'
            .format('environment', package)
        )

    except jinja2_ex.TemplateNotFound:
        raise filesys_ex.FileNotExistError(
            '{}: The template "{}" does not exist in the template folder '
            'of the "{}" package.'
            .format('templates', template, package)
        )

    except jinja2_ex.TemplateSyntaxError as e:
        message = '{}: There is a syntax error in template "{}" '\
            'of package "{}".'\
            .format('templates', template, package)
        e.args = (message,)

        raise
