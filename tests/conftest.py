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
    mxn_one = tmp_path/'mxnone'
    mxn_two = tmp_path/'mxntwo'
    mxn_three = tmp_path/'mxnthree'
    mxnapp = tmp_path/'mxnapp'
    mxn_one.mkdir()
    mxn_two.mkdir()
    mxn_three.mkdir()
    mxnapp.mkdir()
    (mxn_one/'__init__.py').touch()
    (mxn_two/'__init__.py').touch()
    (mxn_three/'__init__.py').touch()
    (mxnapp/'__init__.py').touch()
    sys.path.insert(0, str(tmp_path))

    yield tmp_path

    sys.path.remove(str(tmp_path))
    for mod in list(sys.modules.keys()):
        if mod.startswith('mxn'):
            del sys.modules[mod]


@pytest.fixture
def static_pathes(mxxn_env):
    mxns = ['mxnone', 'mxntwo', 'mxnthree']

    for mxn in mxns:
        static_path = mxxn_env/(mxn + '/frontend/static')
        static_path.mkdir(parents=True)

    return mxxn_env


@pytest.fixture
def static_files(static_pathes):
    mxns = ['mxnone', 'mxntwo', 'mxnthree']

    for mxn in mxns:
        js_path = static_pathes/(mxn + '/frontend/static/js')
        js_path.mkdir()
        js_file = js_path/'mxn.js'
        js_file.touch()
        index_file = static_pathes/(mxn + '/frontend/static/index.html')
        index_file.touch()

    return static_pathes


@pytest.fixture
def static_file_covers(static_files):
    static_cover_path = \
        static_files/('mxnapp/covers/mxxn/frontend/static')
    static_cover_path.mkdir(parents=True)

    js_cover_path = static_cover_path/'js'
    js_cover_path.mkdir()

    (js_cover_path/'mxxn.js').touch()

    mxns = ['mxnone', 'mxntwo', 'mxnthree']

    for mxn in mxns:
        static_cover_path = \
            static_files/('mxnapp/covers/mxns/' + mxn + '/frontend/static')
        static_cover_path.mkdir(parents=True)

        js_cover_path = static_cover_path/'js'
        js_cover_path.mkdir()

        (js_cover_path/'mxn.js').touch()

    return static_files


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
