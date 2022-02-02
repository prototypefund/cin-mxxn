"""Pytest conftest.py file."""
import pytest
from unittest.mock import patch, Mock, PropertyMock
import sys


@pytest.fixture()
def iter_entry_points():
    """Get mocks for the iter_entry_points function."""
    mxnone = Mock()
    mxntwo = Mock()
    mxnthree = Mock()
    mxnapp = Mock()
    mxnone.name = 'mxnone'
    mxntwo.name = 'mxntwo'
    mxnthree.name = 'mxnthree'
    mxnapp.name = 'mxnapp'

    def mock_iter_entry_points(group=''):
        if group == 'mxxn_mxn':
            return [mxnone, mxntwo, mxnthree]

        if group == 'mxxn_app':
            return [mxnapp]

    with patch('mxxn.env.iter_entry_points', new=mock_iter_entry_points):

        yield


@pytest.fixture()
def mxxn_env(tmp_path, iter_entry_points):
    """
    Get mixxin environment.

    This fixture returns a temp directory including three test mixins and a
    app. The names are mxnone, mxntwo, mxnthree and mxnapp. The path will
    be added to the sys.path and deleted after testing.

    Args:
        tmp_path: Pytest temp directory.
        iter_entry_points: The iter_entry_points fixture.

    """
    mixin_one = tmp_path/'mxnone'
    mixin_two = tmp_path/'mxntwo'
    mixin_three = tmp_path/'mxnthree'
    mxnapp = tmp_path/'mxnapp'
    mixin_one.mkdir()
    mixin_two.mkdir()
    mixin_three.mkdir()
    mxnapp.mkdir()
    (mixin_one/'__init__.py').touch()
    (mixin_two/'__init__.py').touch()
    (mixin_three/'__init__.py').touch()
    (mxnapp/'__init__.py').touch()
    sys.path.insert(0, str(tmp_path))

    yield tmp_path

    sys.path.remove(str(tmp_path))
    for mod in list(sys.modules.keys()):
        if mod.startswith('mxn'):
            del sys.modules[mod]


@pytest.fixture
def db(tmp_path):
    """
    Get an initialzed database test environment.

    Args:
        tmp_path: Pytest temp directory.

    """
    with patch(
            'mxxn.cli.Settings.sqlalchemy_url',
            new_callable=PropertyMock) as mock:
        mock.return_value = 'sqlite+aiosqlite:///' + str(tmp_path/'db.sqlite')

        yield
