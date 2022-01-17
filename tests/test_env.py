"""This module contains tests for the env module."""
import inspect
import pytest
from unittest.mock import Mock, MagicMock, patch
from mxxn import env
from mxxn.exceptions import env as env_ex
from mxxn.settings import Settings


class TestMixins():
    """Tests for the mixins function."""

    def test_all_enabled_mixins_exist(self, mxxn_env):
        """Return the package names from settings if mixins are installed."""
        settings = MagicMock()
        settings.enabled_mixins = ['mxnone', 'mxnthree']

        assert env.mxns(settings) == ['mxnone', 'mxnthree']

    def test_not_in_settings(self, mxxn_env):
        """Return list of installed package names if no entry in settings."""
        settings = MagicMock()
        settings.enabled_mixins = None

        assert env.mxns(settings) == ['mxnone', 'mxntwo', 'mxnthree']

    def test_mixin_not_exist(self, mxxn_env):
        """Raise MixinNotExistError if mixin from settings not installed."""
        settings = MagicMock()
        settings.enabled_mixins = ['mxnone', 'xyz']

        with pytest.raises(env_ex.MxnNotExistError):
            env.mxns(settings)

    def test_empty_list_in_settings(self, mxxn_env):
        """Return a empty list if it is a empty list in settings."""
        settings = MagicMock()
        settings.enabled_mixins = []

        assert env.mxns(settings) == []

    def test_no_settings_file(self, mxxn_env):
        """Return all installed mxns if no settings file given."""
        settings = MagicMock()
        settings.enabled_mixins = []

        assert env.mxns() == ['mxnone', 'mxntwo', 'mxnthree']


class TestPackageBaseInit():
    """Tests for the initialisation of the PackageBase class."""

    def test_package_not_exist(self):
        """The Package does not exist."""
        with pytest.raises(env_ex.PackageNotExistError):
            env.Base('xyz')

    def test_package_exists(self, mxxn_env):
        """The Package exist."""
        env.Base('mxnone')


class TestPackageBaseName():
    """Tests for the name property of the PackageBase class."""

    def test_name_is_returned(self, mxxn_env):
        """The name is returned."""
        pkg = env.Base('mxnone')
        assert pkg.name == 'mxnone'


class TestPackageBasePath():
    """Tests for the path property of the PackageBase class."""

    def test_path_is_returned(self, mxxn_env):
        """The path is returned."""
        pkg = env.Base('mxnone')

        assert pkg.path == mxxn_env/'mxnone'


class TestPackageBaseResources():
    """Tests for the resources property of the PackageBase class."""

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


class TestMixxinInit():
    """Tests for the creation of the Mixxin class."""

    def test_init(self):
        """Test if Mixxin instance has a name "mixxin"."""
        mixxin = env.Mxxn()

        assert mixxin.name == 'mxxn'


class TestMixxinAppInit():
    """Tests for the MixxinApp initialisation."""

    def test_app_not_exist(self):
        """The app does not exist."""

        with pytest.raises(env_ex.MxnAppNotExistError):
            env.MxnApp()

    def test_app_exists(self, mxxn_env):
        """The app exists."""
        app = env.MxnApp()

        assert app.name == 'mxxnapp'

    def test_multiple_app(self, mxxn_env):
        """The app exists."""
        mxxnapp_one = MagicMock()
        mxxnapp_two = MagicMock()
        mxxnapp_one.name = 'mxxnappone'
        mxxnapp_two.name = 'mxxnapptwo'

        with patch('mxxn.env.iter_entry_points') as mock:
            mock.return_value = [mxxnapp_one, mxxnapp_two]

            with pytest.raises(env_ex.MultipleMxnAppsError):
                env.MxnApp()


class TestMixxinAppCoveringResources(object):
    """Tests for the covering_resources method."""

    def test_cover_for_a_mixxin_resource(self, mxxn_env):
        """Cover for a mixxin resource."""
        content = """
            class Resource(object):
                def on_get(self, req, resp):
                    pass
        """
        covers_mixxin = mxxn_env/'mxxnapp/covers/mixxin'
        covers_mixxin.mkdir(parents=True)
        (mxxn_env/'mxxnapp/covers/mixxin/resources.py').write_text(
            inspect.cleandoc(content)
        )

        settings = Settings()
        app = env.MxnApp()
        resources = app.covering_resources(settings)

        assert len(resources['mixxin']) == 1
        assert resources['mixxin'][0]['routes'][0] == ['/.resource']

    def test_cover_for_a_mixin_resource(self, mxxn_env):
        """Cover for a mixin resource."""
        content = """
            class Resource(object):
                def on_get(self, req, resp):
                    pass
        """
        covers_mixxin = mxxn_env/'mxxnapp/covers/mixins/mxnone'
        covers_mixxin.mkdir(parents=True)
        (mxxn_env/'mxxnapp/covers/mixins/mxnone/resources.py').write_text(
            inspect.cleandoc(content)
        )

        settings = Settings()
        app = env.MxnApp()
        resources = app.covering_resources(settings)

        assert len(resources['mixxin']) == 0
        assert len(resources['mixins']['mxnone']) == 1
        assert resources['mixins']['mxnone'][0]['routes'][0] == ['/.resource']

    def test_respects_enabled_mixins(self, mxxn_env):
        """Respects the enabled_mixins from settings file."""
        content = """
            class Resource(object):
                def on_get(self, req, resp):
                    pass
        """
        covers_mixxin_one = mxxn_env/'mxxnapp/covers/mixins/mxnone'
        covers_mixxin_two = mxxn_env/'mxxnapp/covers/mixins/mxntwo'
        covers_mixxin_one.mkdir(parents=True)
        covers_mixxin_two.mkdir(parents=True)
        (mxxn_env/'mxxnapp/covers/mixins/mxnone/resources.py').write_text(
            inspect.cleandoc(content)
        )
        (mxxn_env/'mxxnapp/covers/mixins/mxntwo/resources.py').write_text(
            inspect.cleandoc(content)
        )

        settings = Mock()
        settings.enabled_mixins = ['mxnone', 'mxnthree']

        app = env.MxnApp()
        resources = app.covering_resources(settings)

        assert len(resources['mixxin']) == 0
        assert len(resources['mixins']) == 1
        assert resources['mixins']['mxnone'][0]['routes'][0] == ['/.resource']
