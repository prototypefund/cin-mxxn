
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
    class Root():
        async def on_get(self, req, resp):
            resp.body = 'Root'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class ResourceOne():
        async def on_get(self, req, resp):
            resp.body = 'ResourceOne'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class ResourceTwo():
        async def on_get_list(self, req, resp):
            resp.body = 'ResourceTwo'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    mock_mxxn_resources = [
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

    content_mxns = """
            import falcon

            class MxnResourceOne(object):
                async def on_get(self, req, resp):
                    resp.body = 'MxnResourceOne'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200

            class MxnResourceTwo(object):
                async def on_get(self, req, resp):
                    resp.body = 'MxnResourceTwo'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200

                async def on_get_list(self, req, resp):
                    resp.body = 'MxnResourceTwo list'
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
    (mxxn_env/'mxnone/resources.py').write_text(cleandoc(content_mxns))

    (mxxn_env/'mxntwo/__init__.py').touch()
    (mxxn_env/'mxntwo/resources.py').write_text(cleandoc(content_mxns))

    (mxxn_env/'mxnapp/__init__.py').touch()
    (mxxn_env/'mxnapp/resources.py').write_text(cleandoc(content_app))

    with patch('mxxn.env.Mxxn.resources', new_callable=PropertyMock) as mock:
        mock.return_value = mock_mxxn_resources

        yield mxxn_env


class TestAppRegisterResources():
    """Tests for the _register_resources method of the App class."""

    def test_mxxn_routes_added(self, resources):
        """All routes of the mxxn were added."""
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

    def test_mxn_routes_added(self, resources, tmp_path):
        """All routes of the mxns were added."""
        app = App()
        client = testing.TestClient(app.asgi)

        response_one = client.simulate_get('/mxns/one/.mxnresourceone')
        response_two = client.simulate_get('/mxns/one/.mxnresourcetwo')
        response_three = client.simulate_get(
            '/mxns/one/.mxnresourcetwo.list'
        )

        assert response_one.text == 'MxnResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_three.text == 'MxnResourceTwo list'
        assert response_three.status == falcon.HTTP_OK
        assert response_three.headers['content-type'] == falcon.MEDIA_HTML

    def test_root_resource_of_mxxn(self, resources, tmp_path):
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

    # def test_temp(self, resources):
    #     content = """
    #         class MxnResourceTwo(object):
    #             async def on_get(self, req, resp):
    #                 resp.body = 'MxnResourceTwo cover'
    #                 resp.content_type = falcon.MEDIA_HTML
    #                 resp.status = falcon.HTTP_200
    #
    #     """
    #     app = App()
    #     client = testing.TestClient(app.asgi)
    #
    #     covers_mxn_one = resources/'mxnapp/covers/mxns/mxnone'
    #     covers_mxn_two = resources/'mxnapp/covers/mxns/mxntwo'
    #     covers_mxn_one.mkdir(parents=True)
    #     covers_mxn_two.mkdir(parents=True)
    #     (resources/'mxnapp/covers/mxns/mxnone/resources.py').write_text(
    #         cleandoc(content)
    #     )
    #     (resources/'mxnapp/covers/mxns/mxntwo/resources.py').write_text(
    #         cleandoc(content)
    #     )
    #
    #     from mxxn import env
    #     from mxxn.settings import Settings
    #     app = env.MxnApp()
    #     settings = Settings()

        # print(app.covering_resources(settings))

        # response_one = client.simulate_get('/mxns/one/.mxnresourcetwo')
        # response_two = client.simulate_get('/app/.appresourcetwo')

        # print(response_one.text)


class TestStaticPaths(object):
    """Tests for the _register_static_paths method of the App class."""

    def test_mxn_registration(self, mxxn_env):
        """The static folders have been registered."""
        mxnone_static_path = mxxn_env/'mxnone/frontend/static'
        mxntwo_static_path = mxxn_env/'mxntwo/frontend/static'
        mxnone_static_path.mkdir(parents=True)
        mxntwo_static_path.mkdir(parents=True)

        app = App()

        assert len(app.asgi._static_routes) == 3
        assert app.asgi._static_routes[0][0]._prefix == '/static/mxns/two/'
        assert app.asgi._static_routes[1][0]._prefix == '/static/mxns/one/'
        assert app.asgi._static_routes[2][0]._prefix == '/static/'

    def test_mxnapp_registration(self, mxxn_env):
        """The static folder of mxnapp has been registered."""
        mxnapp = mxxn_env/'mxnapp/frontend/static'
        mxnapp.mkdir(parents=True)

        app = App()

        assert len(app.asgi._static_routes) == 2
        assert app.asgi._static_routes[0][0]._prefix == '/static/app/'
        assert app.asgi._static_routes[1][0]._prefix == '/static/'
