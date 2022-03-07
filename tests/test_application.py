
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
    class MxxnRoot():
        async def on_get(self, req, resp):
            resp.body = 'MxxnRoot'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class MxxnResourceOne():
        async def on_get(self, req, resp):
            resp.body = 'MxxnResourceOne'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class MxxnResourceTwo():
        async def on_get(self, req, resp):
            resp.body = 'MxxnResourceTwo'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

        async def on_get_suffix(self, req, resp):
            resp.body = 'MxxnResourceTwoSuffix'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    mxxn_routes_mock = [
            {'url': '/', 'resource': MxxnRoot},
            {'url': '/app/resourceone', 'resource': MxxnResourceOne},
            {'url': '/app/resourcetwo', 'resource': MxxnResourceTwo},
            {'url': '/app/resourcetwo/suffix', 'resource': MxxnResourceTwo,
                'suffix': 'suffix'}]

    mxn_resources = """
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

            async def on_get_suffix(self, req, resp):
                resp.body = 'MxnResourceTwoSuffix'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200
        """

    mxnone_routes = """
        from mxnone.resources import MxnResourceOne, MxnResourceTwo

        ROUTES = [
                {'url': '/', 'resource': MxnResourceOne},
                {'url': '/resourcetwo', 'resource': MxnResourceTwo},
                {
                    'url': '/resourcetwo/suffix',
                    'resource': MxnResourceTwo,
                    'suffix': 'suffix'}]
            """

    mxntwo_routes = """
        from mxntwo.resources import MxnResourceOne, MxnResourceTwo

        ROUTES = [
                {'url': '/', 'resource': MxnResourceOne},
                {'url': '/resourcetwo', 'resource': MxnResourceTwo},
                {
                    'url': '/resourcetwo/suffix',
                    'resource': MxnResourceTwo,
                    'suffix': 'suffix'}]
            """

    mxnapp_resource = """
        import falcon

        class MxnAppResourceOne(object):
            async def on_get(self, req, resp):
                resp.body = 'MxnAppResourceOne'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200

        class MxnAppResourceTwo(object):
            async def on_get(self, req, resp):
                resp.body = 'MxnAppResourceTwo'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200

            async def on_get_suffix(self, req, resp):
                resp.body = 'MxnAppResourceTwoSuffix'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200
        """

    mxnapp_routes = """
        from mxnapp.resources import MxnAppResourceOne, MxnAppResourceTwo

        ROUTES = [
                {'url': '/', 'resource': MxnAppResourceOne},
                {'url': '/resourcetwo', 'resource': MxnAppResourceTwo},
                {
                    'url': '/resourcetwo/suffix',
                    'resource': MxnAppResourceTwo,
                    'suffix': 'suffix'}]
            """

    (mxxn_env/'mxnone/resources.py').write_text(cleandoc(mxn_resources))
    (mxxn_env/'mxntwo/resources.py').write_text(cleandoc(mxn_resources))
    (mxxn_env/'mxnapp/resources.py').write_text(cleandoc(mxnapp_resource))
    (mxxn_env/'mxnone/routes.py').write_text(cleandoc(mxnone_routes))
    (mxxn_env/'mxntwo/routes.py').write_text(cleandoc(mxntwo_routes))
    (mxxn_env/'mxnapp/routes.py').write_text(cleandoc(mxnapp_routes))

    with patch('mxxn.routes.ROUTES', mxxn_routes_mock):
        yield mxxn_env


class TestAppRegisterResources():
    """Tests for the _register_resources method of the App class."""

    def test_mxxn_routes_added(self, resources):
        """All routes of the mxxn were added."""
        app = App()
        client = testing.TestClient(app.asgi)

        response_root = client.simulate_get('/')

        response_one = client.simulate_get('/app/resourceone')
        response_two = client.simulate_get('/app/resourcetwo')
        response_two_suffix = client.simulate_get('/app/resourcetwo/suffix')

        assert response_root.text == 'MxxnRoot'
        assert response_root.status == falcon.HTTP_OK
        assert response_root.headers['content-type'] == falcon.MEDIA_HTML

        assert response_one.text == 'MxxnResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'MxxnResourceTwoSuffix'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxn_routes_added(self, resources):
        """All routes of the mxns were added."""
        app = App()
        client = testing.TestClient(app.asgi)

        mxnone_response_one = client.simulate_get('/app/mxns/one')
        mxnone_response_two = client.simulate_get('/app/mxns/one/resourcetwo')
        mxnone_response_three = client.simulate_get(
                '/app/mxns/one/resourcetwo/suffix')

        mxntwo_response_one = client.simulate_get('/app/mxns/two')
        mxntwo_response_two = client.simulate_get('/app/mxns/two/resourcetwo')
        mxntwo_response_three = client.simulate_get(
                '/app/mxns/two/resourcetwo/suffix')

        assert mxnone_response_one.text == 'MxnResourceOne'
        assert mxnone_response_one.status == falcon.HTTP_OK
        assert mxnone_response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert mxnone_response_two.text == 'MxnResourceTwo'
        assert mxnone_response_two.status == falcon.HTTP_OK
        assert mxnone_response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert mxnone_response_three.text == 'MxnResourceTwoSuffix'
        assert mxnone_response_three.status == falcon.HTTP_OK
        assert mxnone_response_three.headers['content-type'] == \
            falcon.MEDIA_HTML

        assert mxntwo_response_one.text == 'MxnResourceOne'
        assert mxntwo_response_one.status == falcon.HTTP_OK
        assert mxntwo_response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert mxntwo_response_two.text == 'MxnResourceTwo'
        assert mxntwo_response_two.status == falcon.HTTP_OK
        assert mxntwo_response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert mxntwo_response_three.text == 'MxnResourceTwoSuffix'
        assert mxntwo_response_three.status == falcon.HTTP_OK
        assert mxntwo_response_three.headers['content-type'] == \
            falcon.MEDIA_HTML

    def test_mxnapp_routes_added(self, resources):
        """All routes of the mixxin application were added."""
        app = App()
        client = testing.TestClient(app.asgi)

        response_one = client.simulate_get('/app/mxnapp')
        response_two = client.simulate_get('/app/mxnapp/resourcetwo')
        response_three = client.simulate_get('/app/mxnapp/resourcetwo/suffix')

        assert response_one.text == 'MxnAppResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxnAppResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_three.text == 'MxnAppResourceTwoSuffix'
        assert response_three.status == falcon.HTTP_OK
        assert response_three.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxxn_route_cover(self, resources):
        """A mxxn route was covered."""
        resources_content = """
            import falcon

            class ResourceCover():
                async def on_get(self, req, resp):
                    resp.text = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxxn.resources import ResourceCover

            ROUTES = [{'url': '/app/resourceone', 'resource': ResourceCover}]

        """
        mxxn_covers = resources/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = testing.TestClient(app.asgi)
        response_root = client.simulate_get('/')
        response_one = client.simulate_get('/app/resourceone')
        response_two = client.simulate_get('/app/resourcetwo')
        response_two_suffix = client.simulate_get('/app/resourcetwo/suffix')

        assert response_root.text == 'MxxnRoot'
        assert response_root.status == falcon.HTTP_OK
        assert response_root.headers['content-type'] == falcon.MEDIA_HTML

        assert response_one.text == 'ResourceCover'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'MxxnResourceTwoSuffix'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxxn_suffix_route_cover(self, resources):
        """A mxxn route with suffix was covered."""
        resources_content = """
            import falcon

            class ResourceCover():
                async def on_get_suffix(self, req, resp):
                    resp.text = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxxn.resources import ResourceCover

            ROUTES = [{'url': '/app/resourcetwo/suffix',
                'resource': ResourceCover, 'suffix':'suffix'}]

        """
        mxxn_covers = resources/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = testing.TestClient(app.asgi)
        response_root = client.simulate_get('/')
        response_one = client.simulate_get('/app/resourceone')
        response_two = client.simulate_get('/app/resourcetwo')
        response_two_suffix = client.simulate_get('/app/resourcetwo/suffix')

        assert response_root.text == 'MxxnRoot'
        assert response_root.status == falcon.HTTP_OK
        assert response_root.headers['content-type'] == falcon.MEDIA_HTML

        assert response_one.text == 'MxxnResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'ResourceCover'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxxn_wrong_suffix_route_cover(self, resources):
        """The cover resource has wrong suffix."""
        resources_content = """
            import falcon

            class ResourceCover():
                async def on_get_suffix(self, req, resp):
                    resp.text = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxxn.resources import ResourceCover

            ROUTES = [{'url': '/app/resourcetwo/suffix',
                'resource': ResourceCover, 'suffix':'wrong_suffix'}]

        """
        mxxn_covers = resources/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = testing.TestClient(app.asgi)
        response_root = client.simulate_get('/')
        response_one = client.simulate_get('/app/resourceone')
        response_two = client.simulate_get('/app/resourcetwo')
        response_two_suffix = client.simulate_get('/app/resourcetwo/suffix')

        assert response_root.text == 'MxxnRoot'
        assert response_root.status == falcon.HTTP_OK
        assert response_root.headers['content-type'] == falcon.MEDIA_HTML

        assert response_one.text == 'MxxnResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'MxxnResourceTwoSuffix'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxxn_root_route_cover(self, resources):
        """A mxxn root route was covered."""
        resources_content = """
            import falcon

            class ResourceCover():
                async def on_get(self, req, resp):
                    resp.text = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxxn.resources import ResourceCover

            ROUTES = [{'url': '/', 'resource': ResourceCover}]

        """
        mxxn_covers = resources/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = testing.TestClient(app.asgi)
        response_root = client.simulate_get('/')
        response_one = client.simulate_get('/app/resourceone')
        response_two = client.simulate_get('/app/resourcetwo')
        response_two_suffix = client.simulate_get('/app/resourcetwo/suffix')

        assert response_root.text == 'ResourceCover'
        assert response_root.status == falcon.HTTP_OK
        assert response_root.headers['content-type'] == falcon.MEDIA_HTML

        assert response_one.text == 'MxxnResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'MxxnResourceTwoSuffix'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxn_route_cover(self, resources):
        """A mxn route was covered."""
        resources_content = """
            import falcon

            class ResourceCover():
                async def on_get(self, req, resp):
                    resp.text = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxns.mxnone.resources import ResourceCover

            ROUTES = [{'url': '/', 'resource': ResourceCover}]

        """
        mxnone_covers = resources/'mxnapp/covers/mxns/mxnone'
        mxnone_covers.mkdir(parents=True)
        (mxnone_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxnone_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = testing.TestClient(app.asgi)
        response_one = client.simulate_get('/app/mxns/one')
        response_two = client.simulate_get('/app/mxns/one/resourcetwo')
        response_two_suffix = client.simulate_get(
                '/app/mxns/one/resourcetwo/suffix')

        assert response_one.text == 'ResourceCover'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'MxnResourceTwoSuffix'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxn_suffix_route_cover(self, resources):
        """A mxn route with suffix was covered."""
        resources_content = """
            import falcon

            class ResourceCover():
                async def on_get_suffix(self, req, resp):
                    resp.text = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxns.mxnone.resources import ResourceCover

            ROUTES = [{'url': '/resourcetwo/suffix',
                'resource': ResourceCover,
                'suffix': 'suffix'}]

        """
        mxnone_covers = resources/'mxnapp/covers/mxns/mxnone'
        mxnone_covers.mkdir(parents=True)
        (mxnone_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxnone_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = testing.TestClient(app.asgi)
        response_one = client.simulate_get('/app/mxns/one')
        response_two = client.simulate_get('/app/mxns/one/resourcetwo')
        response_two_suffix = client.simulate_get(
                '/app/mxns/one/resourcetwo/suffix')

        assert response_one.text == 'MxnResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'ResourceCover'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxn_wrong_suffix_route_cover(self, resources):
        """The Mxn cover resource has wrong suffix."""
        resources_content = """
            import falcon

            class ResourceCover():
                async def on_get_suffix(self, req, resp):
                    resp.text = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxns.mxnone.resources import ResourceCover

            ROUTES = [{'url': '/resourcetwo/suffix',
                'resource': ResourceCover,
                'suffix': 'wrong_suffix'}]

        """
        mxnone_covers = resources/'mxnapp/covers/mxns/mxnone'
        mxnone_covers.mkdir(parents=True)
        (mxnone_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxnone_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = testing.TestClient(app.asgi)
        response_one = client.simulate_get('/app/mxns/one')
        response_two = client.simulate_get('/app/mxns/one/resourcetwo')
        response_two_suffix = client.simulate_get(
                '/app/mxns/one/resourcetwo/suffix')

        assert response_one.text == 'MxnResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxnResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two_suffix.text == 'MxnResourceTwoSuffix'
        assert response_two_suffix.status == falcon.HTTP_OK
        assert response_two_suffix.headers['content-type'] == falcon.MEDIA_HTML


class TestRegisterStaticPaths():
    """Tests for the _register_static_paths method of the App class."""

    def test_mxn_registration(self, mxxn_env):
        """The static folders have been registered."""
        mxnone_static_path = mxxn_env/'mxnone/frontend/static'
        mxntwo_static_path = mxxn_env/'mxntwo/frontend/static'
        mxnone_static_path.mkdir(parents=True)
        mxntwo_static_path.mkdir(parents=True)

        app = App()

        print(app.asgi._static_routes[2][0]._prefix)

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
        assert app.asgi._static_routes[0][0]._prefix == '/static/mxnapp/'
        assert app.asgi._static_routes[1][0]._prefix == '/static/'

    def test_mxxn_covers_added(self, mxxn_env):
        """The mxxn covers were added."""
        (mxxn_env/'mxnapp/covers/mxxn/frontend/static/js').mkdir(parents=True)
        (mxxn_env/'mxnapp/covers/mxxn/frontend/static/js/mxxn.js').touch()
        (mxxn_env/'mxnapp/covers/mxxn/frontend/static/index.html').touch()

        app = App()
        client = testing.TestClient(app.asgi)
        result = client.simulate_get('/static/covers/mxxn/index.html')

        assert result.status_code == 200

    def test_tmp(self, mxxn_env):
        mxns_cover_path = mxxn_env/'mxnapp/covers/mxns/'

        (mxns_cover_path/'mxnone/frontend/static/js').mkdir(parents=True)
        (mxns_cover_path/'mxntwo/frontend/static/js').mkdir(parents=True)
        (mxns_cover_path/'mxnone/frontend/static/js/mxn.js').touch()
        (mxns_cover_path/'mxnone/frontend/static/index.html').touch()
        (mxns_cover_path/'mxntwo/frontend/static/js/mxn.js').touch()
        (mxns_cover_path/'mxntwo/frontend/static/index.html').touch()

        app = App()
        client = testing.TestClient(app.asgi)
        mxnone_result_index = client.simulate_get(
                '/static/covers/mxns/one/index.html')
        mxnone_result_js = client.simulate_get(
                '/static/covers/mxns/one/js/mxn.js')
        mxntwo_result_index = client.simulate_get(
                '/static/covers/mxns/two/index.html')
        mxntwo_result_js = client.simulate_get(
                '/static/covers/mxns/two/js/mxn.js')

        assert mxnone_result_index.status_code == 200
        assert mxnone_result_js.status_code == 200
        assert mxntwo_result_index.status_code == 200
        assert mxntwo_result_js.status_code == 200
