"""This module contains tests for the env module."""
import inspect
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from mxxn import env
from mxxn.exceptions import env as env_ex
from mxxn.exceptions import config as config_ex
from mxxn.settings import Settings
from mxxn import config


class TestIsDevelop():
    """Tests for the is_develop function."""

    def test_develop_requires_installed(self):
        """All develop requirements are installed."""
        with patch('mxxn.env.requires') as mock:
            mock.return_value = ['falcon', 'alembic; extra == "develop"']

            assert env.is_develop()

    def test_not_all_develop_requires_installed(self):
        """Not all develop requirements are installed."""
        with patch('mxxn.env.requires') as mock:
            mock.return_value = [
                'falcon',
                'xxxyyyzzz; extra == "develop"',
                'alembic; extra == "develop"']

            assert not env.is_develop()

    def test_no_develop_extra_requires(self):
        """No develop section in extra_require in setup.cfg."""
        with patch('mxxn.env.requires') as mock:
            mock.return_value = ['falcon', 'alembic']

            assert not env.is_develop()

    def test_package_with_version(self):
        """A develop package has specific version."""
        with patch('mxxn.env.requires') as requires_mock:
            with patch('mxxn.env.metadata') as metadata_mock:
                requires_mock.return_value = [
                    'falcon',
                    'xxx_yyyzzz; extra == "develop"',
                    'xxx_yyyzzz==0.0.1; extra == "develop"',
                    'xxx-yyy-zzz>=0.0.1; extra == "develop"',
                    'alembic; extra == "develop"']

                metadata_mock.return_value = None

                assert env.is_develop()


class TestMixins():
    """Tests for the mxns function."""

    def test_all_enabled_mxis_exist(self, mxxn_env):
        """Return the package names from settings if mixins are installed."""
        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxnthree']

        assert env.mxns(settings) == ['mxnone', 'mxnthree']

    def test_not_in_settings(self, mxxn_env):
        """Return list of installed package names if no entry in settings."""
        settings = Mock()
        settings.enabled_mxns = None

        assert env.mxns(settings) == ['mxnone', 'mxntwo', 'mxnthree']

    def test_mixin_not_exist(self, mxxn_env):
        """Raise MixinNotExistError if mixin from settings not installed."""
        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'xyz']

        with pytest.raises(env_ex.MxnNotExistError):
            env.mxns(settings)

    def test_empty_list_in_settings(self, mxxn_env):
        """Return a empty list if it is a empty list in settings."""
        settings = Mock()
        settings.enabled_mxns = []

        assert env.mxns(settings) == []

    def test_no_settings_file(self, mxxn_env):
        """Return all installed mxns if no settings file given."""
        settings = Mock()
        settings.enabled_mxns = []

        assert env.mxns() == ['mxnone', 'mxntwo', 'mxnthree']


class TestBaseInit():
    """Tests for the initialisation of the Base class."""

    def test_package_not_exist(self):
        """The Package does not exist."""
        with pytest.raises(env_ex.PackageNotExistError):
            env.Base('xyz')

    def test_package_exists(self, mxxn_env):
        """The Package exist."""
        env.Base('mxnone')


class TestBaseName():
    """Tests for the name property of the Base class."""

    def test_name_is_returned(self, mxxn_env):
        """The name is returned."""
        pkg = env.Base('mxnone')
        assert pkg.name == 'mxnone'


class TestBasePath():
    """Tests for the path property of the Base class."""

    def test_path_is_returned(self, mxxn_env):
        """The path is returned."""
        pkg = env.Base('mxnone')

        assert pkg.path == mxxn_env/'mxnone'


class TestBaseConfigPath():
    """Tests for the config_path property of the Base class."""

    def test_no_config_path(self, mxxn_env):
        """It is no config path in the package."""
        pkg = env.Base('mxnone')

        assert not pkg.configs_path

    def test_config_path_returned(self, mxxn_env):
        """The config path is returned."""
        config_path = mxxn_env/'mxnone/configs'
        config_path.mkdir()
        pkg = env.Base('mxnone')

        assert pkg.configs_path == config_path


class TestBaseThemesPath():
    """Tests for the themes_path property of the Base class."""

    def test_no_config_path(self, mxxn_env):
        """It is no config path in the package."""
        pkg = env.Base('mxnone')

        assert not pkg.themes_path

    def test_no_themes_path(self, mxxn_env):
        """It is no themes path is returned."""
        config_path = mxxn_env/'mxnone/configs'
        config_path.mkdir()
        pkg = env.Base('mxnone')

        assert not pkg.themes_path

    def test_themes_path_returned(self, mxxn_env):
        """The themes path is returned."""
        themes_path = mxxn_env/'mxnone/configs/themes'
        themes_path.mkdir(parents=True)
        pkg = env.Base('mxnone')

        assert pkg.themes_path == themes_path


class TestBaseTheme():
    """Tests for the theme property of the Base class."""

    def test_config_class_returned(self):
        """A config class is returned."""

        pkg = env.Base('mxxn')

        assert isinstance(pkg.theme, config.Config)


class TestBaseStringsPath():
    """Tests for the strings_path property of the Base class."""

    def test_no_config_path(self, mxxn_env):
        """It is no config path in the package."""
        pkg = env.Base('mxnone')

        pkg.strings_path

        assert not pkg.strings_path

    def test_no_strings_path(self, mxxn_env):
        """It is no strings path is returned."""
        config_path = mxxn_env/'mxnone/configs'
        config_path.mkdir()
        pkg = env.Base('mxnone')

        assert not pkg.strings_path

    def test_strings_path_returned(self, mxxn_env):
        """The strings path is returned."""
        strings_path = mxxn_env/'mxnone/configs/strings'
        strings_path.mkdir(parents=True)
        pkg = env.Base('mxnone')

        assert pkg.strings_path == strings_path


class TestBaseRoutes():
    """Tests for the routes property of the Base class."""

    def test_all_routes_returned(self):
        """All the routes are returnd."""
        pkg = env.Mxxn()
        routes = pkg.routes

        assert len(routes) >= 1

        for route in pkg.routes:
            assert 'url' in route
            assert 'resource' in route

    def test_no_routes_module(self, mxxn_env):
        """No routes module in the package."""
        pkg = env.Mxn('mxnone')

        assert not pkg.routes

    def test_no_routes_list(self, mxxn_env):
        """No routes list in the package."""
        (mxxn_env/'mxnone/routes.py').touch()
        pkg = env.Mxn('mxnone')

        assert not pkg.routes


class TestBaseStaticPath():
    """Tests for the static_path method of the Base class."""

    def test_has_no_static_folder(self, mxxn_env):
        """The package has no static folder."""
        pkg = env.Base('mxnone')

        assert not pkg.static_path

    def test_has_a_static_folder(self, mxxn_static_pathes_env):
        """The static_path function returns the path."""
        mxnone = env.Base('mxnone')
        mxntwo = env.Base('mxntwo')
        mxnthree = env.Base('mxnthree')

        assert mxnone.static_path == \
            mxxn_static_pathes_env/'mxnone/frontend/static'
        assert mxntwo.static_path == \
            mxxn_static_pathes_env/'mxntwo/frontend/static'
        assert mxnthree.static_path == \
            mxxn_static_pathes_env/'mxnthree/frontend/static'


class TestBaseStaticFiles():
    """Tests for the static_files method of the Base class."""

    def test_no_static_dir(self, mxxn_env):
        """It is no in static directory."""
        pkg = env.Base('mxnone')

        assert not pkg.static_files

    def test_no_file_in_static_dir(self, mxxn_static_pathes_env):
        """It is no file in static directory."""
        mxnone = env.Base('mxnone')
        mxntwo = env.Base('mxntwo')
        mxnthree = env.Base('mxnthree')

        assert mxnone.static_files == []
        assert mxntwo.static_files == []
        assert mxnthree.static_files == []

    def test_all_files_found(self, mxxn_static_files_env):
        """All files was found."""
        pkg = env.Base('mxnone')

        assert pkg.static_files == [
                pkg.static_path/'index.html',
                pkg.static_path/'js/javascript.js'
                ]


class TestBaseJsFiles():
    """Tests for the js_files property of the Base class."""

    def test_no_js_files(self, mxxn_env):
        """The package does not have js files."""
        pkg = env.Base('mxnone')

        assert pkg.js_files == []

    def test_js_files_returned(self, mxxn_env):
        """The package has files."""
        (mxxn_env/'mxnone/frontend/static/js').mkdir(parents=True)
        (mxxn_env/'mxnone/frontend/static/js/mxn.js').touch()
        pkg = env.Base('mxnone')

        assert pkg.js_files == [Path('mxn.js')]

    def test_js_files_from_sub_path_returned(self, mxxn_env):
        """The js files from a sub directory were returned."""
        (mxxn_env/'mxnone/frontend/static/js/sub').mkdir(parents=True)
        (mxxn_env/'mxnone/frontend/static/js/mxn.js').touch()
        (mxxn_env/'mxnone/frontend/static/js/sub/mxn_sub.js').touch()
        pkg = env.Base('mxnone')

        assert pkg.js_files == [Path('mxn.js'), Path('sub/mxn_sub.js')]


class TestMxxnInit():
    """Tests for the creation of the Mxxn class."""

    def test_init(self):
        """Test if Mxxn instance has a name "mxxn"."""
        mxxn = env.Mxxn()

        assert mxxn.name == 'mxxn'


class TestMxxnTheme():
    """Tests for the creation of the Mxxn class."""

    def test_config_instance_returned(self):
        """A config instance is returned."""
        mxxn = env.Mxxn()

        assert isinstance(mxxn.theme, config.Config)

    def test_no_themes_config(self):
        """A NoThemeConfigError exception is raised."""
        mxxn = env.Mxxn()

        with patch('mxxn.config.Config') as mock:
            mock.return_value = None

            with pytest.raises(config_ex.NoThemeConfigError):
                mxxn.theme


class TestMxnUnprefixedName():
    """Tests for the unprefixed_name property of Mxn class."""

    def test_has_prefix(self, mxxn_env):
        """The name has a prefix."""
        mxnone = env.Mxn('mxnone')

        assert mxnone.unprefixed_name == 'one'

    def test_has_no_prefix(self, mxxn_env):
        """The name has a prefix."""
        mxnone = env.Mxn('mxnone')

        assert mxnone.unprefixed_name == 'one'


class TestMxnAppInit():
    """Tests for the MxnApp initialisation."""

    def test_app_not_exist(self):
        """The app does not exist."""
        with pytest.raises(env_ex.MxnAppNotExistError):
            env.MxnApp()

    def test_app_exists(self, mxxn_env):
        """The app exists."""
        app = env.MxnApp()

        assert app.name == 'mxnapp'

    def test_multiple_app(self, mxxn_env):
        """The app exists."""
        mxnapp = Mock()
        mxnapp = Mock()
        mxnapp.name = 'mxnapp'
        mxnapp.name = 'mxnapp'

        with patch('mxxn.env.iter_entry_points') as mock:
            mock.return_value = [mxnapp, mxnapp]

            with pytest.raises(env_ex.MultipleMxnAppsError):
                env.MxnApp()


class TestMxnAppRouteCovers():
    """Tests for the route_covers property of the MxnApp class."""

    def test_cover_for_a_mxxn_routes(self, mxxn_env):
        """Cover for a mxxn routes returned."""
        resources_content = """
            class ResourceCover():
                def on_get(self, req, resp):
                    pass
                    resp.body = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        routes_content = """
            from mxnapp.covers.mxxn.resources import ResourceCover

            ROUTES = [{'url': '/', 'resource': ResourceCover}]

        """

        mxxn_covers = mxxn_env/'mxnapp/covers/mxxn'
        mxxn_covers.mkdir(parents=True)
        (mxxn_covers/'resources.py').write_text(
            inspect.cleandoc(resources_content)
        )
        (mxxn_covers/'routes.py').write_text(
            inspect.cleandoc(routes_content)
        )

        settings = Settings()
        app = env.MxnApp()
        route_covers = app.route_covers(settings)

        from mxnapp.covers.mxxn.resources import ResourceCover

        assert len(route_covers['mxxn']) == 1
        assert route_covers['mxxn'][0]['url'] == '/'
        assert route_covers['mxxn'][0]['resource'] == ResourceCover

    def test_cover_for_a_mxns_routes(self, mxxn_env):
        """Cover for a mxns routes returned."""
        resources_content = """
            class ResourceCover():
                def on_get(self, req, resp):
                    pass
                    resp.body = 'ResourceCover'
                    resp.content_type = falcon.MEDIA_HTML
                    resp.status = falcon.HTTP_200
        """

        mxnone_routes_content = """
            from mxnapp.covers.mxns.mxnone.resources import ResourceCover

            ROUTES = [{'url': '/', 'resource': ResourceCover}]

        """

        mxntwo_routes_content = """
            from mxnapp.covers.mxns.mxntwo.resources import ResourceCover

            ROUTES = [{'url': '/', 'resource': ResourceCover}]

        """
        mxnone_covers = mxxn_env/'mxnapp/covers/mxns/mxnone'
        mxntwo_covers = mxxn_env/'mxnapp/covers/mxns/mxntwo'
        mxnone_covers.mkdir(parents=True)
        mxntwo_covers.mkdir(parents=True)
        (mxnone_covers/'resources.py').write_text(
            inspect.cleandoc(resources_content)
        )
        (mxntwo_covers/'resources.py').write_text(
            inspect.cleandoc(resources_content)
        )
        (mxnone_covers/'routes.py').write_text(
            inspect.cleandoc(mxnone_routes_content)
        )
        (mxntwo_covers/'routes.py').write_text(
            inspect.cleandoc(mxntwo_routes_content)
        )

        settings = Settings()
        app = env.MxnApp()
        route_covers = app.route_covers(settings)

        from mxnapp.covers.mxns.mxnone import resources as mxnone_resources
        from mxnapp.covers.mxns.mxntwo import resources as mxntwo_resources

        assert len(route_covers['mxns']['mxnone']) == 1
        assert len(route_covers['mxns']['mxntwo']) == 1
        assert route_covers['mxns']['mxnone'][0]['url'] == '/'
        assert route_covers['mxns']['mxntwo'][0]['url'] == '/'
        assert route_covers['mxns']['mxnone'][0]['resource'] ==\
            mxnone_resources.ResourceCover
        assert route_covers['mxns']['mxntwo'][0]['resource'] ==\
            mxntwo_resources.ResourceCover


class TestStaticRouteCovers():
    """Tests for the static_file_covers property of MxnApp."""
    def test_mxxn_covers(self, mxxn_static_file_covers_env):
        """All covers for Mxxn package found."""
        settings = Settings()
        app = env.MxnApp()

        assert app.static_file_covers(settings)['mxxn'] == [Path('js/mxxn.js')]

    def test_no_mxxn_cover(self, mxxn_env):
        """No cover for Mxxn package found."""
        settings = Settings()
        app = env.MxnApp()

        assert app.static_file_covers(settings)['mxxn'] == []

    def test_mxn_covers(self, mxxn_static_file_covers_env):
        """All covers for Mxn packages found."""
        settings = Settings()
        app = env.MxnApp()

        assert app.static_file_covers(settings)['mxns']['mxnone'] ==\
            [Path('js/javascript.js')]
        assert app.static_file_covers(settings)['mxns']['mxntwo'] ==\
            [Path('js/javascript.js')]
        assert app.static_file_covers(settings)['mxns']['mxnthree'] ==\
            [Path('js/javascript.js')]

    def test_no_mxn_cover(self, mxxn_env):
        """No cover for Mxn packages found."""
        settings = Settings()
        app = env.MxnApp()

        assert app.static_file_covers(settings)['mxns'] == {}

    def test_mxn_has_static_folder(self, mxxn_env):
        """The Mxn has static folder but no files."""
        (mxxn_env/('mxnapp/covers/mxns/mxnone/frontend/static')).mkdir(
                parents=True)

        settings = Settings()
        app = env.MxnApp()

        assert app.static_file_covers(settings)['mxns'] == {}
