"""Tests for the routes module."""
from falcon.testing import TestClient as Client
from falcon import asgi
import pytest
from mxxn.application import App
from mxxn import env
from mxxn.routes import QueryStringValidationMiddleware


@pytest.fixture
def static_files(mxxn_env):
    return mxxn_env


class TestStaticRoutesMiddlewareInit:
    """Tests for the StaticRoutesMiddleware."""

    def test_mxxn_file_covered(self, mxxn_static_file_covers_env):
        """The static file form mxxn package was covered."""
        app = App()
        client = Client(app.asgi)
        result = client.simulate_get(
                '/static/mxxn/js/mxxn.js')

        assert result.text == 'mxxn js cover'
        assert result.status_code == 200

    @pytest.mark.parametrize('mxn_name', ['mxnone', 'mxntwo', 'mxnthree'])
    def test_mxn_file_covered(self, mxxn_static_file_covers_env, mxn_name):
        """The static files form mxn packages were covered."""
        mxn = env.Mxn(mxn_name)

        app = App()
        client = Client(app.asgi)
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
        client = Client(app.asgi)
        result_covered_js = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/js/javascript.js')

        result_covered_html = client.simulate_get(
                '/static/mxns/' + mxn.unprefixed_name + '/index.html')

        assert result_covered_js.text == mxn_name + ' js file'
        assert result_covered_js.status_code == 200
        assert result_covered_html.text == mxn_name + ' html file'
        assert result_covered_html.status_code == 200


class TestQueryStingValidationMiddleware:
    """Tests for the QueryStringValidationMiddleware."""

    def test_invalid_query_string(self):
        """It is an invalid query string."""
        class Root:
            query_string_definition = {
                'GET': {
                    'none': {
                        'type': 'object',
                        'properties': {
                            'fields': {
                                'anyOf': [
                                    {
                                        'type': 'string',
                                        'enum': ['one', 'two']

                                    },
                                    {
                                        'type': 'array',
                                        'items': {
                                            'enum': ['one', 'two']
                                            }
                                    }]
                                }
                            },
                        'additionalProperties': False,
                        },
                    'id': 123
                    }
                }

            async def on_get(self, req, resp, id=None):
                pass

        app = asgi.App(middleware=[QueryStringValidationMiddleware()])
        app.req_options.auto_parse_qs_csv = True
        app.add_route('/', Root())
        client = Client(app)

        result = client.get('/?fields=xyz')

        assert result.status_code == 400
        assert 'Query string' in result.json['title']

    def test_no_query_string_definition(self):
        """No query_string_definition class property in the resource."""
        class Root:
            async def on_get(self, req, resp, id=None):
                pass

        app = asgi.App(middleware=[QueryStringValidationMiddleware()])
        app.req_options.auto_parse_qs_csv = True
        app.add_route('/', Root())
        client = Client(app)

        result = client.get('/')

        assert result.status_code == 200

    def test_to_many_parameter(self):
        """To many parameters in reguest URL."""
        class Root:
            query_string_definition = {
                'GET': {
                    'none': {
                        'type': 'object',
                        'properties': {
                            'fields': {
                                'anyOf': [
                                    {
                                        'type': 'string',
                                        'enum': ['one', 'two']

                                    },
                                    {
                                        'type': 'array',
                                        'items': {
                                            'enum': ['one', 'two']
                                            }
                                    }]
                                }
                            },
                        'additionalProperties': False,
                        },
                    'id': 123
                    }
                }

            async def on_get(self, req, resp, id, name):
                pass

        app = asgi.App(middleware=[QueryStringValidationMiddleware()])
        app.req_options.auto_parse_qs_csv = True
        app.add_route('/{id}/{name}', Root())
        client = Client(app)

        result = client.get('/test/ggg?ddd=123')

        assert result.status_code == 400
        assert 'one parameter allowed' in result.json['title']

    def test_no_definition_for_method(self):
        """It is no definition for the request method."""
        class Root:
            query_string_definition = {
                'DELETE': {
                    'none': {
                        'type': 'object',
                        'properties': {
                            'fields': {
                                'anyOf': [
                                    {
                                        'type': 'string',
                                        'enum': ['one', 'two']

                                    },
                                    {
                                        'type': 'array',
                                        'items': {
                                            'enum': ['one', 'two']
                                            }
                                    }]
                                }
                            },
                        'additionalProperties': False,
                        },
                    }
                }

            async def on_get(self, req, resp):
                pass

        app = asgi.App(middleware=[QueryStringValidationMiddleware()])
        app.req_options.auto_parse_qs_csv = True
        app.add_route('/', Root())
        client = Client(app)

        result = client.get('/?ggg=123')

        assert result.status_code == 400
        assert 'Query string for GET' in result.json['description']

    def test_wrong_query_parameter(self):
        """The query parameter not allowed."""
        class Root:
            query_string_definition = {
                'GET': {
                    'none': {
                        'type': 'object',
                        'properties': {
                            'fields': {
                                'anyOf': [
                                    {
                                        'type': 'string',
                                        'enum': ['one', 'two']

                                    },
                                    {
                                        'type': 'array',
                                        'items': {
                                            'enum': ['one', 'two']
                                            }
                                    }]
                                }
                            },
                        'additionalProperties': False,
                        },
                    }
                }

            async def on_get(self, req, resp):
                pass

        app = asgi.App(middleware=[QueryStringValidationMiddleware()])
        app.req_options.auto_parse_qs_csv = True
        app.add_route('/', Root())
        client = Client(app)

        result = client.get('/?ggg=123')

        assert result.status_code == 400
        assert 'is not valid' in result.json['description']

    def test_correct_query_string(self):
        """Correct query string."""
        class Root:
            query_string_definition = {
                'GET': {
                    'none': {
                        'type': 'object',
                        'properties': {
                            'fields': {
                                'anyOf': [
                                    {
                                        'type': 'string',
                                        'enum': ['one', 'two']

                                    },
                                    {
                                        'type': 'array',
                                        'items': {
                                            'enum': ['one', 'two']
                                            }
                                    }]
                                }
                            },
                        'additionalProperties': False,
                        },
                    }
                }

            async def on_get(self, req, resp):
                pass

        app = asgi.App(middleware=[QueryStringValidationMiddleware()])
        app.req_options.auto_parse_qs_csv = True
        app.add_route('/', Root())
        client = Client(app)

        result = client.get('/?fields=one,two')

        assert result.status_code == 200

    def test_parameter_with_correct_query_string(self):
        """Correct query string for URL with parameter."""
        class Root:
            query_string_definition = {
                'GET': {
                    'id': {
                        'type': 'object',
                        'properties': {
                            'fields': {
                                'anyOf': [
                                    {
                                        'type': 'string',
                                        'enum': ['one', 'two']

                                    },
                                    {
                                        'type': 'array',
                                        'items': {
                                            'enum': ['one', 'two']
                                            }
                                    }]
                                }
                            },
                        'additionalProperties': False,
                        },
                    }
                }

            async def on_get(self, req, resp, id):
                pass

        app = asgi.App(middleware=[QueryStringValidationMiddleware()])
        app.req_options.auto_parse_qs_csv = True
        app.add_route('/{id}', Root())
        client = Client(app)

        result = client.get('/id?fields=one,two')

        assert result.status_code == 200
