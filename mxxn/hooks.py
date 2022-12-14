"""This module contains some before and after hooks."""
from jinja2 import Environment, PackageLoader
from jinja2 import exceptions as jinja2_ex
from pathlib import Path
from typing import Type, Optional
from falcon import Request, Response, MEDIA_HTML, HTTP_200
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import filesys as filesys_ex
from mxxn.utils.packages import caller_package_name


async def render(
            req: Request,
            resp: Response,
            resource: Type,
            template: Path,
            package_name: Optional[str] = None,
            media_type: str = MEDIA_HTML
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

            import falcon import after
            from mxxn import hooks
            from pathlib import Path

            class Resource(object):
                @after(
                    hooks.render, Path('path/to/template.j2'), 'package_name'
                )
                def on_get(self, req, resp):
                    resp.context.render = {'variable': 123}

    Args:
        req: The Falcon request object.
        resp: The Falcon response object containing the context.render
            variable.
        resource: The called Falcon resource.
        template: The name of the template (relative to the template folder
            of the package).
        package_name: The name of the package in which the template is located.
            The default is the package in which the hook was called.
        media_type: The media type of the rendered data. Default type is
            falcon.MEDIA_HTML.

    Raises:
        falcon.HTTPInternalServerError: If the package not exist, if the
            template not exist, if some syntax error in the template.
    """
    try:
        if not package_name:
            package_name = caller_package_name()

        env = Environment(loader=PackageLoader(
            package_name, 'templates'), enable_async=True)

        jinja2_template = env.get_template(str(template))

        if hasattr(resp.context, 'render'):
            resp.text = await jinja2_template.render_async(resp.context.render)
        else:
            resp.text = await jinja2_template.render_async()

        resp.content_type = media_type
        resp.status = HTTP_200

    except ModuleNotFoundError:
        raise env_ex.PackageNotExistError(
            '{}: The framework package "{}" does not exist.'
            .format('environment', package_name)
        )

    except jinja2_ex.TemplateNotFound:
        raise filesys_ex.FileNotExistError(
            '{}: The template "{}" does not exist in the template folder '
            'of the "{}" package.'
            .format('templates', template, package_name)
        )

    except jinja2_ex.TemplateSyntaxError as e:
        message = '{}: There is a syntax error in template "{}" '\
            'of package "{}".'\
            .format('templates', template, package_name)
        e.args = (message,)

        raise
