"""Tests for the settings module."""
import pytest
from os import chdir, environ
from unittest.mock import patch
from mxxn.settings import Settings
from mxxn.exceptions import filesys as filesys_ex


class TestFile(object):
    """Test for the static _file() method of the Settings class."""

    def test_no_environment_variable(self):
        """The environment variable does not exist."""
        assert not Settings._file()

    def test_settings_in_current_dir(self, tmp_path):
        """The settings from current dir used."""
        settings_file = tmp_path/'settings.ini'
        settings_file.touch()
        chdir(tmp_path)

        assert Settings._file() == tmp_path/'settings.ini'

    def test_settings_in_env_variable(self, tmp_path):
        """The settings file is in the environment variable."""
        settings_file = tmp_path/'settings.ini'
        settings_file.touch()

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            assert Settings._file() == tmp_path/'settings.ini'

    def test_settings_file_is_not_a_file(self, tmp_path):
        """The settings file is in the environment variable is not a file."""
        settings_file = tmp_path

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            with pytest.raises(filesys_ex.FileNotExistError):
                Settings._file()

    def test_with_relative_path(self, tmp_path):
        """The settings file path is ralative."""
        path_1 = tmp_path/'path_1'
        path_2 = tmp_path/'path_2'
        path_1.mkdir()
        path_2.mkdir()
        settings_file = path_1/'settings.ini'
        settings_file.touch()
        chdir(path_2)

        with patch.dict(
                environ, {'MIXXIN_SETTINGS': '../path_1/settings.ini'}):
            assert Settings._file() == settings_file
