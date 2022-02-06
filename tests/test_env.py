"""This module contains tests for the env module."""
import inspect
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from mxxn import env
from mxxn.exceptions import env as env_ex
from mxxn.settings import Settings


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

        assert not pkg.config_path

    def test_config_path_returned(self, mxxn_env):
        """The config path is returned."""
        config_path = mxxn_env/'mxnone/config'
        config_path.mkdir()
        pkg = env.Base('mxnone')

        assert pkg.config_path == config_path


class TestBaseThemesPath():
    """Tests for the themes_path property of the Base class."""

    def test_no_config_path(self, mxxn_env):
        """It is no config path in the package."""
        pkg = env.Base('mxnone')

        pkg.themes_path

        assert not pkg.themes_path

    def test_no_themes_path(self, mxxn_env):
        """It is no themes path is returned."""
        config_path = mxxn_env/'mxnone/config'
        config_path.mkdir()
        pkg = env.Base('mxnone')

        assert not pkg.themes_path

    def test_themes_path_returned(self, mxxn_env):
        """The themes path is returned."""
        themes_path = mxxn_env/'mxnone/config/themes'
        themes_path.mkdir(parents=True)
        pkg = env.Base('mxnone')

        assert pkg.themes_path == themes_path


class TestBaseResources():
    """Tests for the resources property of the Base class."""

    def test_package_has_a_resources_module(self, mxxn_env):
        """Test if the module has a resources module."""
        (mxxn_env/'mxnone/__init__.py').touch()
        (mxxn_env/'mxnone/resources.py').touch()

        pkg = env.Base('mxnone')

        assert pkg.resources == []

    def test_package_has_not_resource_module(self, mxxn_env):
        """Module has a resources module."""
        pkg = env.Base('mxnone')

        assert pkg.resources == []

    def test_has_resources_with_responder(self, mxxn_env):
        """Module has resources with responders."""
        content = """
            class ResourceOne(object):
                def on_get(self, req, resp):
                    pass

            class ResourceTwo(object):
                def on_post(self, req, resp):
                    pass
        """

        (mxxn_env/'mxnone/__init__.py').touch()
        (mxxn_env/'mxnone/resources.py').write_text(
            inspect.cleandoc(content))
        pkg = env.Base('mxnone')
        resources_list = pkg.resources

        assert len(resources_list) == 2
        assert resources_list[0]['routes'] == [['/.resourceone']]
        assert resources_list[1]['routes'] == [['/.resourcetwo']]
        assert resources_list[0]['resource'].__name__ == 'ResourceOne'
        assert resources_list[1]['resource'].__name__ == 'ResourceTwo'
        assert resources_list[0]['resource'].__module__ == 'mxnone.resources'
        assert resources_list[1]['resource'].__module__ == 'mxnone.resources'

    def test_has_responder_and_suffix(self, mxxn_env):
        """Test if the module has resources with responder ans suffix."""
        content = """
            class ResourceOne(object):
                def on_get(self, req, resp):
                    pass

            class ResourceTwo(object):
                def on_post(self, req, resp):
                    pass

                def on_post_list(self, req, resp):
                    pass
        """

        (mxxn_env/'mxnone/__init__.py').touch()
        (mxxn_env/'mxnone/resources.py').write_text(
            inspect.cleandoc(content))

        pkg = env.Base('mxnone')
        resources_list = pkg.resources

        assert len(resources_list) == 2
        assert resources_list[0]['routes'] == [['/.resourceone']]
        assert resources_list[1]['routes'] == [
            ['/.resourcetwo'], ['/.resourcetwo.list', 'list']
        ]
        assert resources_list[0]['resource'].__name__ == 'ResourceOne'
        assert resources_list[1]['resource'].__name__ == 'ResourceTwo'
        assert resources_list[0]['resource'].__module__ == 'mxnone.resources'
        assert resources_list[1]['resource'].__module__ == 'mxnone.resources'

    def test_resource_only_has_suffixed_responder(self, mxxn_env):
        """Test if one resources has only suffixed responder."""
        content = """
            class ResourceOne(object):
                def on_get(self, req, resp):
                    pass

            class ResourceTwo(object):
                def on_post_list(self, req, resp):
                    pass
        """

        (mxxn_env/'mxnone/__init__.py').touch()
        (mxxn_env/'mxnone/resources.py').write_text(
            inspect.cleandoc(content))

        pkg = env.Base('mxnone')
        resources_list = pkg.resources

        assert len(resources_list) == 2
        assert resources_list[0]['routes'] == [['/.resourceone']]
        assert resources_list[1]['routes'] == [['/.resourcetwo.list', 'list']]
        assert resources_list[0]['resource'].__name__ == 'ResourceOne'
        assert resources_list[1]['resource'].__name__ == 'ResourceTwo'
        assert resources_list[0]['resource'].__module__ == 'mxnone.resources'
        assert resources_list[1]['resource'].__module__ == 'mxnone.resources'

    def test_resource_with_subpackage(self, mxxn_env):
        """Test if one resources module has a subpackge."""
        content = """
            class ResourceOne(object):
                def on_get(self, req, resp):
                    pass

            class ResourceTwo(object):
                def on_get(self, req, resp):
                    pass

                def on_post_suffix_one(self, req, resp):
                    pass

                def on_post_suffix_two(self, req, resp):
                    pass
        """

        (mxxn_env/'mxnone/__init__.py').touch()
        (mxxn_env/'mxnone/resources/pkg').mkdir(parents=True)
        (mxxn_env/'mxnone/resources/__init__.py').write_text(
            inspect.cleandoc(content)
        )
        (mxxn_env/'mxnone/resources/pkg/__init__.py').touch()
        (mxxn_env/'mxnone/resources/pkg/resources.py').write_text(
            inspect.cleandoc(content)
        )

        pkg = env.Base('mxnone')
        resources_list = pkg.resources

        assert len(resources_list) == 4
        assert resources_list[0]['routes'] == [['/.resourceone']]
        assert resources_list[1]['routes'] == [
            ['/.resourcetwo'],
            ['/.resourcetwo.suffix_one', 'suffix_one'],
            ['/.resourcetwo.suffix_two', 'suffix_two']
        ]
        assert resources_list[2]['routes'] == [['/pkg/resources/.resourceone']]
        assert resources_list[3]['routes'] == [
            ['/pkg/resources/.resourcetwo'],
            ['/pkg/resources/.resourcetwo.suffix_one', 'suffix_one'],
            ['/pkg/resources/.resourcetwo.suffix_two', 'suffix_two']
        ]
        assert resources_list[0]['resource'].__name__ == 'ResourceOne'
        assert resources_list[1]['resource'].__name__ == 'ResourceTwo'
        assert resources_list[2]['resource'].__name__ == 'ResourceOne'
        assert resources_list[3]['resource'].__name__ == 'ResourceTwo'
        assert resources_list[0]['resource'].__module__ == 'mxnone.resources'
        assert resources_list[1]['resource'].__module__ \
            == 'mxnone.resources'
        assert resources_list[2]['resource'].__module__ \
            == 'mxnone.resources.pkg.resources'
        assert resources_list[3]['resource'].__module__ \
            == 'mxnone.resources.pkg.resources'


class TestBaseStaticPath():
    """Tests for the static_path method of the Base class."""

    def test_has_no_static_folder(self, mxxn_env):
        """The package has no static folder."""
        pkg = env.Base('mxnone')

        assert not pkg.static_path

    def test_has_a_static_folder(self, mxxn_env):
        """The static_path function returns the path."""
        patch = mxxn_env/'mxnone/frontend/static'
        patch.mkdir(parents=True)
        pkg = env.Base('mxnone')

        assert pkg.static_path == mxxn_env/'mxnone/frontend/static'


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


class TestMixxinInit():
    """Tests for the creation of the Mixxin class."""

    def test_init(self):
        """Test if Mixxin instance has a name "mixxin"."""
        mxxn = env.Mxxn()

        assert mxxn.name == 'mxxn'


class TestMixxinAppInit():
    """Tests for the MxxnApp initialisation."""

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


class TestMixxinAppCoveringResources():
    """Tests for the covering_resources method."""

    def test_cover_for_a_mixxin_resource(self, mxxn_env):
        """Cover for a mxxn resource."""
        content = """
            class Resource(object):
                def on_get(self, req, resp):
                    pass
        """
        covers_mixxin = mxxn_env/'mxnapp/covers/mxxn'
        covers_mixxin.mkdir(parents=True)
        (mxxn_env/'mxnapp/covers/mxxn/resources.py').write_text(
            inspect.cleandoc(content)
        )

        settings = Settings()
        app = env.MxnApp()
        resources = app.covering_resources(settings)

        assert len(resources['mxxn']) == 1
        assert resources['mxxn'][0]['routes'][0] == ['/.resource']

    def test_cover_for_a_mxn_resource(self, mxxn_env):
        """Cover for a mxn resource."""
        content = """
            class Resource(object):
                def on_get(self, req, resp):
                    pass
        """
        covers_mixxin = mxxn_env/'mxnapp/covers/mxns/mxnone'
        covers_mixxin.mkdir(parents=True)
        (mxxn_env/'mxnapp/covers/mxns/mxnone/resources.py').write_text(
            inspect.cleandoc(content)
        )

        settings = Settings()
        app = env.MxnApp()
        resources = app.covering_resources(settings)

        assert len(resources['mxxn']) == 0
        assert len(resources['mxns']['mxnone']) == 1
        assert resources['mxns']['mxnone'][0]['routes'][0] == ['/.resource']

    def test_respects_enabled_mxns(self, mxxn_env):
        """Respects the enabled_mxns from settings file."""
        content = """
            class Resource(object):
                def on_get(self, req, resp):
                    pass
        """
        covers_mxn_one = mxxn_env/'mxnapp/covers/mxns/mxnone'
        covers_mxn_two = mxxn_env/'mxnapp/covers/mxns/mxntwo'
        covers_mxn_one.mkdir(parents=True)
        covers_mxn_two.mkdir(parents=True)
        (mxxn_env/'mxnapp/covers/mxns/mxnone/resources.py').write_text(
            inspect.cleandoc(content)
        )
        (mxxn_env/'mxnapp/covers/mxns/mxntwo/resources.py').write_text(
            inspect.cleandoc(content)
        )

        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxnthree']

        app = env.MxnApp()
        resources = app.covering_resources(settings)

        assert len(resources['mxxn']) == 0
        assert len(resources['mxns']) == 1
        assert resources['mxns']['mxnone'][0]['routes'][0] == ['/.resource']
