"""This module contains tests for the env module."""
import inspect
import pytest
from unittest.mock import MagicMock
from mxxn import env
from mxxn.exceptions import env as env_ex


class TestMixins():
    """Tests for the mixins function."""

    def test_all_enabled_mixins_exist(self, iter_entry_points_mixins):
        """Return the package names from settings if mixins are installed."""
        settings = MagicMock()
        settings.enabled_mixins = ['mxnone', 'mxnthree']

        assert env.mixins(settings) == ['mxnone', 'mxnthree']

    def test_not_in_settings(self, iter_entry_points_mixins):
        """Return list of installed package names if no entry in settings."""
        settings = MagicMock()
        settings.enabled_mixins = None

        assert env.mixins(settings) == ['mxnone', 'mxntwo', 'mxnthree']

    def test_mixin_not_exist(self, iter_entry_points_mixins):
        """Raise MixinNotExistError if mixin from settings not installed."""
        settings = MagicMock()
        settings.enabled_mixins = ['mxnone', 'xyz']

        with pytest.raises(env_ex.MixinNotExistError):
            env.mixins(settings)

    def test_empty_list_in_settings(self, iter_entry_points_mixins):
        """Return a empty list if it is a empty list in settings."""
        settings = MagicMock()
        settings.enabled_mixins = []

        assert env.mixins(settings) == []


class TestPackageInit():
    """Tests for the initialisation of the Package class."""

    def test_package_not_exist(self):
        """The Package does not exist."""
        with pytest.raises(env_ex.PackageNotExistError):
            env.Package('xyz')

    def test_package_exists(self, mixxin_env):
        """The Package exist."""
        env.Package('mxnone')


class TestPackageName():
    """Tests for the name property of the Package class."""

    def test_name_is_returned(self, mixxin_env):
        """The name is returned."""
        pkg = env.Package('mxnone')
        assert pkg.name == 'mxnone'


class TestPackageResources():
    """Tests for the resources property of the Package class."""

    def test_package_has_a_resources_module(self, mixxin_env):
        """Test if the module has a resources module."""
        (mixxin_env/'mxnone/__init__.py').touch()
        (mixxin_env/'mxnone/resources.py').touch()

        pkg = env.Package('mxnone')

        assert pkg.resources == []

    def test_package_has_not_resource_module(self, mixxin_env):
        """Module has a resources module."""
        pkg = env.Package('mxnone')

        assert pkg.resources == []

    def test_has_resources_with_responder(self, mixxin_env):
        """Module has resources with responders."""
        content = """
            class ResourceOne(object):
                def on_get(self, req, resp):
                    pass

            class ResourceTwo(object):
                def on_post(self, req, resp):
                    pass
        """

        (mixxin_env/'mxnone/__init__.py').touch()
        (mixxin_env/'mxnone/resources.py').write_text(
                inspect.cleandoc(content))

        pkg = env.Package('mxnone')
        resources_list = pkg.resources

        assert len(resources_list) == 2
        assert resources_list[0]['routes'] == [['/.resourceone']]
        assert resources_list[1]['routes'] == [['/.resourcetwo']]
        assert resources_list[0]['resource'].__name__ == 'ResourceOne'
        assert resources_list[1]['resource'].__name__ == 'ResourceTwo'
        assert resources_list[0]['resource'].__module__ == 'mxnone.resources'
        assert resources_list[1]['resource'].__module__ == 'mxnone.resources'
