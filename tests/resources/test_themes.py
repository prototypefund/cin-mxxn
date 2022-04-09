"""Tests for the themes module."""
from falcon import testing
import pytest
from mxxn.application import App


@pytest.fixture()
def client():
    return testing.TestClient(App().asgi)


class TestThemes:
    """Tests for the Themes response."""

    def test_all_themes_returned(self, client):
        """All themes were returned."""
        result = client.get('/app/mxxn/themes')

        themes = result.json

        assert len(themes) == 2
        assert themes[0]['id'] == 'dark'
        assert 'mxxn' in themes[0]['theme']
        assert 'mxns' in themes[0]['theme']
        assert 'mxnapp' in themes[0]['theme']
        assert themes[1]['id'] == 'light'
        assert 'mxxn' in themes[1]['theme']
        assert 'mxns' in themes[1]['theme']
        assert 'mxnapp' in themes[1]['theme']

    def test_theme_of_id_returned(self, client):
        """The theme with given ID returned."""
        result = client.get('/app/mxxn/themes/light')

        theme = result.json

        print(theme)

        assert 'mxxn' in theme
        assert 'mxns' in theme
        assert 'mxnapp' in theme

    def test_only_ids_returned(self, client):
        """Only the IDs were returned."""
        result = client.get('/app/mxxn/themes?fields=id')

        themes = result.json

        print(themes)

        assert themes[0]['id'] == 'dark'
        assert themes[1]['id'] == 'light'
