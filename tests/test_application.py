
"""This module contains tests for the app module."""
from inspect import cleandoc
import pytest
from unittest.mock import patch, PropertyMock
import falcon
from falcon import testing
from mxxn.application import App


@pytest.fixture()
def resources(mxxn_env):
    """
    Create test resources.

    This fixture creates mock resources for the mixxin package
    and it also mock the ressources() method of the
    mixxin.env.Mixxin class so that it returns the mock resources.
    Also, some resources for mixins and the app are added to the
    mixxin fixture. These are needed to test the registration of
    the resources of the test mixins and the test app.
    """
    class Root(object):
        async def on_get(self, req, resp):
            resp.body = 'Root'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class ResourceOne(object):
        async def on_get(self, req, resp):
            resp.body = 'ResourceOne'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class ResourceTwo(object):
        async def on_get_list(self, req, resp):
            resp.body = 'ResourceTwo'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    mock_mixxin_resources = [
        {
            'resource': Root,
            'routes': [
                ['/.root']
            ]
        },
        {
            'resource': ResourceOne,
            'routes': [
                ['/.resourceone']
            ]
        },
        {
            'resource': ResourceTwo,
            'routes': [
                ['/.resourcetwo.list', 'list']
            ]
        }
    ]

    content_mixins = """
            import falcon

            class MixinResourceOne(object):
                async def on_get(self, req, resp):
                    resp.body = 'MixinResourceOne'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200

            class MixinResourceTwo(object):
                async def on_get(self, req, resp):
                    resp.body = 'MixinResourceTwo'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200

                async def on_get_list(self, req, resp):
                    resp.body = 'MixinResourceTwo list'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

    content_app = """
            import falcon

            class AppResourceOne(object):
                async def on_get(self, req, resp):
                    resp.body = 'AppResourceOne'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200

            class AppResourceTwo(object):
                async def on_get(self, req, resp):
                    resp.body = 'AppResourceTwo'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200

                async def on_get_list(self, req, resp):
                    resp.body = 'AppResourceTwo list'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

    (mxxn_env/'mxnone/__init__.py').touch()
    (mxxn_env/'mxnone/resources.py').write_text(cleandoc(content_mixins))

    (mxxn_env/'mxntwo/__init__.py').touch()
    (mxxn_env/'mxntwo/resources.py').write_text(cleandoc(content_mixins))

    (mxxn_env/'mxxnapp/__init__.py').touch()
    (mxxn_env/'mxxnapp/resources.py').write_text(cleandoc(content_app))

    with patch('mxxn.env.Mxxn.resources', new_callable=PropertyMock) as mock:
        mock.return_value = mock_mixxin_resources

        yield


class TestAppRegisterResources(object):
    """Tests for the _register_resources method of the App class."""

    def test_mixxin_routes_added(self, resources):
        """All routes of the mixxin were added."""
        app = App()
        client = testing.TestClient(app.asgi)

        response_one = client.simulate_get('/.resourceone')
        response_two = client.simulate_get('/.resourcetwo.list')
        #
        assert response_one.text == 'ResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'ResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

    def test_mixin_routes_added(self, resources, tmp_path):
        """All routes of the mixins were added."""
        app = App()
        client = testing.TestClient(app.asgi)

        response_one = client.simulate_get('/mxn/mxnone/.mixinresourceone')
        response_two = client.simulate_get('/mxn/mxnone/.mixinresourcetwo')
        response_three = client.simulate_get(
            '/mxn/mxnone/.mixinresourcetwo.list'
        )

        assert response_one.text == 'MixinResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MixinResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_three.text == 'MixinResourceTwo list'
        assert response_three.status == falcon.HTTP_OK
        assert response_three.headers['content-type'] == falcon.MEDIA_HTML

    def test_root_resource_of_patchwork(self, resources, tmp_path):
        """Test if the "/.root" route was registered under "/"."""
        app = App()
        client = testing.TestClient(app.asgi)

        response = client.simulate_get('/')

        assert response.text == 'Root'
        assert response.status == falcon.HTTP_OK
        assert response.headers['content-type'] == falcon.MEDIA_HTML

    def test_app_routes_added(self, resources, tmp_path):
        """All routes of the mixxin application were added."""
        app = App()
        client = testing.TestClient(app.asgi)

        response_one = client.simulate_get('/app/.appresourceone')
        response_two = client.simulate_get('/app/.appresourcetwo')
        response_three = client.simulate_get(
            '/app/.appresourcetwo.list'
        )

        assert response_one.text == 'AppResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'AppResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_three.text == 'AppResourceTwo list'
        assert response_three.status == falcon.HTTP_OK
        assert response_three.headers['content-type'] == falcon.MEDIA_HTML
