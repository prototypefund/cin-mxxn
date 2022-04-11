"""Tests for the hooks module."""
from falcon import testing
import falcon
import falcon.asgi
from mxxn import hooks
from mxxn.exceptions import capture_errors
import inspect
from pathlib import Path


class TestRender:
    """Tests for render hook."""

    def test_file_was_rendered(self):
        """Test if the file was rendered."""
        class Root:
            @falcon.after(hooks.render, Path('app.j2'), 'mxxn')
            async def on_get(self, req, resp):
                resp.context.render = {}

        app = falcon.asgi.App()
        app.add_route('/', Root())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.text.find('<!DOCTYPE html>') != -1
        assert response.text.find('</html>') != -1
        assert response.text.find('<head>') != -1
        assert response.text.find('</head>') != -1
        assert response.text.find('<body>') != -1
        assert response.text.find('</body>') != -1

    def test_package_not_exist(self, caplog):
        """The package does not exist."""
        class Root:
            @falcon.after(hooks.render, Path('app.j2'), 'mxnxxyyzz')
            async def on_get(self, req, resp):
                resp.context.render = {}

        app = falcon.asgi.App()
        app.add_route('/', Root())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.status_code == 500
        assert response.status == '500 Internal Server Error'
        assert 'PackageNotExistError' in str(caplog.records[-1])

    def test_default_content_type(self):
        """Default content-type is HTML."""
        class Root:
            @falcon.after(hooks.render, Path('app.j2'), 'mxxn')
            async def on_get(self, req, resp):
                resp.context.render = {}

        app = falcon.asgi.App()
        app.add_route('/', Root())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.headers['content-type'] == falcon.MEDIA_HTML

    def test_given_media_type_used(self):
        """The given media type was used."""
        class Root:
            @falcon.after(
                hooks.render, Path('app.j2'), 'mxxn', falcon.MEDIA_TEXT
            )
            async def on_get(self, req, resp):
                resp.context.render = {}

        app = falcon.asgi.App()
        app.add_route('/', Root())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.headers['content-type'] == falcon.MEDIA_TEXT

    def test_if_template_not_found(self, caplog):
        """The template was not found."""
        class Root:
            @falcon.after(hooks.render, Path('non-existing.j2'), 'mxxn')
            async def on_get(self, req, resp):
                resp.context.render = {}

        app = falcon.asgi.App()
        app.add_route('/', Root())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.status_code == 500
        assert response.status == '500 Internal Server Error'
        assert 'FileNotExistError' in str(caplog.records[-1])

    def test_a_template_from_other_package(self, mxxn_env):
        """Template is in other package."""
        content = '''
        import falcon
        from mxxn import hooks
        from pathlib import Path

        class Resource:
            @falcon.after(
                hooks.render, Path('template.j2'), 'mxnone', falcon.MEDIA_TEXT
            )
            async def on_get(self, req, resp):
                resp.context.render = {}
        '''
        (mxxn_env/'mxnone/resources.py').write_text(inspect.cleandoc(content))
        (mxxn_env/'mxnone/templates').mkdir()
        (mxxn_env/'mxnone/templates/template.j2')\
            .write_text('test template')

        app = falcon.asgi.App()

        from mxnone import resources

        app.add_route('/', resources.Resource())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.text == 'test template'
        assert response.headers['content-type'] == falcon.MEDIA_TEXT

    def test_no_resp_context_render(self, mxxn_env):
        """The resp.context.render does not exist."""
        content = '''
        import falcon
        from mxxn import hooks
        from pathlib import Path

        class Resource:
            @falcon.after(
                hooks.render, Path('template.j2'), 'mxnone', falcon.MEDIA_TEXT
            )
            async def on_get(self, req, resp):
                pass
        '''
        (mxxn_env/'mxnone/resources.py').write_text(inspect.cleandoc(content))
        (mxxn_env/'mxnone/templates').mkdir()
        (mxxn_env/'mxnone/templates/template.j2')\
            .write_text('test template')

        app = falcon.asgi.App()

        from mxnone import resources

        app.add_route('/', resources.Resource())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.text == 'test template'
        assert response.headers['content-type'] == falcon.MEDIA_TEXT

    def test_with_variable(self, mxxn_env):
        """A variable was passed to the template."""
        content = '''
        import falcon
        from mxxn import hooks
        from pathlib import Path

        class Resource:
            @falcon.after(
                hooks.render, Path('template.j2'), 'mxnone', falcon.MEDIA_TEXT
            )
            async def on_get(self, req, resp):
                resp.context.render = {'content': '123'}
        '''
        (mxxn_env/'mxnone/resources.py').write_text(inspect.cleandoc(content))
        (mxxn_env/'mxnone/templates').mkdir()
        (mxxn_env/'mxnone/templates/template.j2')\
            .write_text('test {{ content }} template')

        app = falcon.asgi.App()

        from mxnone import resources

        app.add_route('/', resources.Resource())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.text == 'test 123 template'
        assert response.headers['content-type'] == falcon.MEDIA_TEXT

    def test_a_template_syntax_error(self, mxxn_env, caplog):
        """There is a syntax error in the template."""
        content = '''
        import falcon
        from mxxn import hooks
        from pathlib import Path

        class Resource:
            @falcon.after(
                hooks.render, Path('template.j2'), 'mxnone', falcon.MEDIA_TEXT
            )
            async def on_get(self, req, resp):
                resp.context.render = {'content': 123}
        '''
        (mxxn_env/'mxnone/resources.py').write_text(inspect.cleandoc(content))
        (mxxn_env/'mxnone/templates').mkdir()
        (mxxn_env/'mxnone/templates/template.j2')\
            .write_text('test {{ }} template')

        app = falcon.asgi.App()

        from mxnone import resources

        app.add_route('/', resources.Resource())
        app.add_error_handler(Exception, capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.status_code == 500
        assert response.status == '500 Internal Server Error'
        assert 'TemplateSyntaxError' in str(caplog.records[-1])

    def test_caller_package_used(self):
        """Caller package is used."""
        class Root:
            @falcon.after(hooks.render, Path('app.j2'))
            async def on_get(self, req, resp):
                resp.context.render = {}

        app = falcon.asgi.App()
        app.add_route('/', Root())
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.text.find('<!DOCTYPE html>') != -1
        assert response.text.find('</html>') != -1
        assert response.text.find('<head>') != -1
        assert response.text.find('</head>') != -1
        assert response.text.find('<body>') != -1
        assert response.text.find('</body>') != -1
