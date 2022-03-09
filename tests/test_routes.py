"""Tests for the routes module."""
from falcon.testing import TestClient
import pytest
from mxxn.application import App
from mxxn import env


@pytest.fixture
def static_files(mxxn_env):
    return mxxn_env


class TestStaticRoutesMiddlewareInit():
    """Tests for the StaticRoutesMiddleware."""

    def test_mxxn_file_covered(self, mxxn_static_file_covers_env):
        """The static file form mxxn package was covered."""
        app = App()
        client = TestClient(app.asgi)
        result = client.simulate_get(
                '/static/mxxn/js/mxxn.js')

        assert result.text == 'mxxn js cover'
        assert result.status_code == 200

    @pytest.mark.parametrize('mxn_name', ['mxnone', 'mxntwo', 'mxnthree'])
    def test_mxn_file_covered(self, mxxn_static_file_covers_env, mxn_name):
        """The static files form mxn packages were covered."""
        mxn = env.Mxn(mxn_name)

        app = App()
        client = TestClient(app.asgi)
        result_covered_js = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/js/javascript.js')

        result_covered_html = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/index.html')

        assert result_covered_js.text == mxn_name + ' js cover'
        assert result_covered_js.status_code == 200
        assert result_covered_html.text == mxn_name + ' html file'
        assert result_covered_html.status_code == 200

    @pytest.mark.parametrize('mxn_name', ['mxnone', 'mxntwo', 'mxnthree'])
    def test_no_mxn_covers(self, mxxn_static_files_env, mxn_name):
        """There are no covers for mxns."""
        mxn = env.Mxn(mxn_name)

        app = App()
        client = TestClient(app.asgi)
        result_covered_js = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/js/javascript.js')

        result_covered_html = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/index.html')

        assert result_covered_js.text == mxn_name + ' js file'
        assert result_covered_js.status_code == 200
        assert result_covered_html.text == mxn_name + ' html file'
        assert result_covered_html.status_code == 200
