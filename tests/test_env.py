"""This module contains tests for the env module."""
import inspect
import pytest
from unittest.mock import MagicMock
from mxxn import env
from mxxn.exceptions import env as env_ex


class TestMixins(object):
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


class TestPackageInit(object):
    """Tests for the initialisation of the Package class."""

    def test_package_not_exist(self):
        """The Package does not exist."""

        with pytest.raises(env_ex.PackageNotExistError):
            env.Package('xyz')

    def test_package_exists(self, mixxin_env):
        """The Package exist."""

        env.Package('mxnone')