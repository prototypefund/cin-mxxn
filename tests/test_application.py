"""This module contains tests for the app module."""
from inspect import cleandoc
import pytest
from unittest.mock import patch
import falcon
from falcon.testing import TestClient as Client
from mxxn.application import App
from mxxn import env


@pytest.fixture()
def mxxn_resources_env(mxxn_env):
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
            resp.text = 'MxxnRoot'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class MxxnResourceOne():
        async def on_get(self, req, resp):
            resp.text = 'MxxnResourceOne'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    class MxxnResourceTwo():
        async def on_get(self, req, resp):
            resp.text = 'MxxnResourceTwo'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

        async def on_get_suffix(self, req, resp):
            resp.text = 'MxxnResourceTwoSuffix'
            resp.content_type = falcon.MEDIA_HTML
            resp.status = falcon.HTTP_200

    mxxn_routes_mock = [
            {'url': '/', 'resource': MxxnRoot},
            {'url': '/resourceone', 'resource': MxxnResourceOne},
            {'url': '/resourcetwo', 'resource': MxxnResourceTwo},
            {'url': '/resourcetwo/suffix', 'resource': MxxnResourceTwo,
                'suffix': 'suffix'}]

    mxn_resources = """
        import falcon

        class MxnResourceOne(object):
            async def on_get(self, req, resp):
                resp.text = 'MxnResourceOne'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200

        class MxnResourceTwo(object):
            async def on_get(self, req, resp):
                resp.text = 'MxnResourceTwo'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200

            async def on_get_suffix(self, req, resp):
                resp.text = 'MxnResourceTwoSuffix'
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
                resp.text = 'MxnAppResourceOne'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200

        class MxnAppResourceTwo(object):
            async def on_get(self, req, resp):
                resp.text = 'MxnAppResourceTwo'
                resp.content_type = falcon.MEDIA_HTML
                resp.status = falcon.HTTP_200

            async def on_get_suffix(self, req, resp):
                resp.text = 'MxnAppResourceTwoSuffix'
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

    def test_mxxn_routes_added(self, mxxn_resources_env):
        """All routes of the mxxn were added."""
        app = App()
        client = Client(app.asgi)

        response_root = client.simulate_get('/app/mxxn')

        response_one = client.simulate_get('/app/mxxn/resourceone')
        response_two = client.simulate_get('/app/mxxn/resourcetwo')
        response_two_suffix = client.simulate_get('/app/mxxn/resourcetwo/suffix')

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

    def test_mxn_routes_added(self, mxxn_resources_env):
        """All routes of the mxns were added."""
        app = App()
        client = Client(app.asgi)

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

    def test_mxnapp_routes_added(self, mxxn_resources_env):
        """All routes of the mixxin application were added."""
        app = App()
        client = Client(app.asgi)

        response_one = client.simulate_get('/app')
        response_two = client.simulate_get('/app/resourcetwo')
        response_three = client.simulate_get('/app/resourcetwo/suffix')

        assert response_one.text == 'MxnAppResourceOne'
        assert response_one.status == falcon.HTTP_OK
        assert response_one.headers['content-type'] == falcon.MEDIA_HTML

        assert response_two.text == 'MxnAppResourceTwo'
        assert response_two.status == falcon.HTTP_OK
        assert response_two.headers['content-type'] == falcon.MEDIA_HTML

        assert response_three.text == 'MxnAppResourceTwoSuffix'
        assert response_three.status == falcon.HTTP_OK
        assert response_three.headers['content-type'] == falcon.MEDIA_HTML

    def test_mxxn_route_cover(self, mxxn_resources_env):
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

            ROUTES = [{'url': '/resourceone', 'resource': ResourceCover}]

        """
        mxxn_covers = mxxn_resources_env/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = Client(app.asgi)
        response_root = client.simulate_get('/app/mxxn')
        response_one = client.simulate_get('/app/mxxn/resourceone')
        response_two = client.simulate_get('/app/mxxn/resourcetwo')
        response_two_suffix = client.simulate_get('/app/mxxn/resourcetwo/suffix')

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

    def test_mxxn_suffix_route_cover(self, mxxn_resources_env):
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

            ROUTES = [{'url': '/resourcetwo/suffix',
                'resource': ResourceCover, 'suffix':'suffix'}]

        """
        mxxn_covers = mxxn_resources_env/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = Client(app.asgi)
        response_root = client.simulate_get('/app/mxxn')
        response_one = client.simulate_get('/app/mxxn/resourceone')
        response_two = client.simulate_get('/app/mxxn/resourcetwo')
        response_two_suffix = client.simulate_get('/app/mxxn/resourcetwo/suffix')

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

    def test_mxxn_wrong_suffix_route_cover(self, mxxn_resources_env):
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
        mxxn_covers = mxxn_resources_env/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = Client(app.asgi)
        response_root = client.simulate_get('/app/mxxn')
        response_one = client.simulate_get('/app/mxxn/resourceone')
        response_two = client.simulate_get('/app/mxxn/resourcetwo')
        response_two_suffix = client.simulate_get('/app/mxxn/resourcetwo/suffix')

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

    def test_mxxn_root_route_cover(self, mxxn_resources_env):
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
        mxxn_covers = mxxn_resources_env/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = Client(app.asgi)
        response_root = client.simulate_get('/app/mxxn')
        response_one = client.simulate_get('/app/mxxn/resourceone')
        response_two = client.simulate_get('/app/mxxn/resourcetwo')
        response_two_suffix = client.simulate_get('/app/mxxn/resourcetwo/suffix')

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

    def test_mxn_route_cover(self, mxxn_resources_env):
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
        mxnone_covers = mxxn_resources_env/'mxnapp/covers/mxns/mxnone'
        mxnone_covers.mkdir(parents=True)
        (mxnone_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxnone_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = Client(app.asgi)
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

    def test_mxn_suffix_route_cover(self, mxxn_resources_env):
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
        mxnone_covers = mxxn_resources_env/'mxnapp/covers/mxns/mxnone'
        mxnone_covers.mkdir(parents=True)
        (mxnone_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxnone_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = Client(app.asgi)
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

    def test_mxn_wrong_suffix_route_cover(self, mxxn_resources_env):
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
        mxnone_covers = mxxn_resources_env/'mxnapp/covers/mxns/mxnone'
        mxnone_covers.mkdir(parents=True)
        (mxnone_covers/'resources.py').write_text(
            cleandoc(resources_content)
        )
        (mxnone_covers/'routes.py').write_text(
            cleandoc(routes_content)
        )

        app = App()
        client = Client(app.asgi)
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

    def test_mxxn_registration(self, mxxn_static_files_env):
        """The static folder of mxxn has been registered."""
        app = App()

        client = Client(app.asgi)
        result = client.simulate_get(
                '/static/mxxn/js/mxxn.js')

        assert result.status_code == 200

    @pytest.mark.parametrize('mxn_name', ['mxnone', 'mxntwo', 'mxnthree'])
    def test_mxn_registration(self, mxxn_static_files_env, mxn_name):
        """The static folders have been registered."""
        mxn = env.Mxn(mxn_name)
        app = App()

        client = Client(app.asgi)
        result_js = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/js/javascript.js')

        result_html = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/index.html')

        assert result_js.status_code == 200
        assert result_html.status_code == 200

    def test_mxnapp_registration(self, mxxn_static_files_env):
        """The static folder of mxnapp has been registered."""
        app = App()

        client = Client(app.asgi)
        result_js = client.simulate_get(
                '/static/js/javascript.js')

        result_html = client.simulate_get(
                '/static/index.html')

        assert result_js.status_code == 200
        assert result_js.text == 'mxnapp js file'
        assert result_html.status_code == 200
        assert result_html.text == 'mxnapp html file'

    def test_mxxn_covers_added(self, mxxn_static_file_covers_env):
        """The mxxn covers were added."""
        app = App()
        client = Client(app.asgi)
        result = client.simulate_get('/static/covers/mxxn/js/mxxn.js')

        assert result.status_code == 200
        assert result.text == 'mxxn js cover'

    @pytest.mark.parametrize('mxn_name', ['mxnone', 'mxntwo', 'mxnthree'])
    def test_mxn_covers_added(self, mxxn_static_file_covers_env, mxn_name):
        """The mxn covers were added."""
        mxn = env.Mxn(mxn_name)

        app = App()
        client = Client(app.asgi)
        results = client.simulate_get(
                '/static/covers/mxns/'+mxn.unprefixed_name+'/js/javascript.js')

        assert results.status_code == 200
        assert results.text == mxn_name + ' js cover'
