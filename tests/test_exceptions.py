"""Tests for the exception module."""
from mxxn import exceptions
from mxxn.exceptions import env as env_ex
import falcon
from falcon import testing


class TestCaptureErrors(object):
    """Tests for the capture_erros function."""

    def test_if_unhandled_error(self, caplog):
        """An unhandled error occurred."""
        class Root(object):
            async def on_get(self, req, resp):
                message = '{}: test'.format('environment')
                raise env_ex.PatchNotExistError(message)

        app = falcon.asgi.App()
        app.add_route('/', Root())
        app.add_error_handler(Exception, exceptions.capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert 'Traceback' in caplog.records[-1].msg
        assert 'PatchNotExistError' in caplog.records[-1].msg
        assert caplog.records[-1].levelname == 'ERROR'
        assert response.status == '500 Internal Server Error'

    def test_no_error(self, caplog):
        """Test if no error has occurred."""
        class Root(object):
            async def on_get(self, req, resp):
                resp.media = {'key': 'value'}

        app = falcon.asgi.App()
        app.add_route('/', Root())
        app.add_error_handler(Exception, exceptions.capture_errors)
        client = testing.TestClient(app)

        response = client.simulate_get('/')

        assert response.status == '200 OK'
        assert response.json == {'key': 'value'}
