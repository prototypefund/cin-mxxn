"""Tests for the settings module."""
import pytest
from os import chdir, environ
from unittest.mock import patch
from mxxn.settings import Settings
from mxxn.exceptions import settings as settings_ex
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


class TestLoad(object):
    """Test for the static _load() method of the Settings class."""

    def test_validation_error(self, tmp_path):
        """The settings file does not match the JSON Scheme."""
        settings_file = tmp_path/'settings.ini'
        settings_file.write_text(
            """
            [mixxin]
            enabled_mixxins = 1

            [alembic]
            sqlalchemy.url = driver://user:pass@localhost/dbname
            """
        )

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            with pytest.raises(settings_ex.SettingsFormatError):
                Settings()._load(settings_file)

    def test_no_mixxin_section(self, tmp_path):
        """The mixxin section does not exist in the INI file."""
        settings_file = tmp_path/'settings.ini'
        settings_file.write_text(
            """
            [alembic]
            sqlalchemy.url = driver://user:pass@localhost/dbname
            """
        )

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            settings = Settings()
            settings._load(settings_file)

            assert settings._data == {
                'mixxin': {},
                'alembic': {
                    'sqlalchemy.url': 'driver://user:pass@localhost/dbname'
                }
            }

    def test_no_alembic_section(self, tmp_path):
        """The alembic section does not exist in the INI file."""
        settings_file = tmp_path/'settings.ini'
        settings_file.write_text(
            """
            [mixxin]
            """
        )

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            settings = Settings()
            settings._load(settings_file)

            assert settings._data == {'mixxin': {}, 'alembic': {}}

    def test_no_sections_in_settings_file(self, tmp_path):
        """It is no section in the settings file."""
        settings_file = tmp_path/'settings.ini'
        settings_file.write_text(
            """
            ggg
            """
        )

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            with pytest.raises(settings_ex.SettingsFormatError):
                settings = Settings()
                settings._load(settings_file)

    def test_additional_property(self, tmp_path):
        """An addional property in the mixxin section."""
        settings_file = tmp_path/'settings.ini'
        settings_file.write_text(
            """
            [mixxin]
            additional = 123
            """
        )

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            with pytest.raises(settings_ex.SettingsFormatError) as excinfo:
                settings = Settings()
                settings._load(settings_file)

                assert 'additional' in str(excinfo.value)

    def test_not_regular_python_code(self, tmp_path):
        """A value in the mixxin section is not regular Python code."""
        settings_file = tmp_path/'settings.ini'
        settings_file.write_text(
            """
            [mixxin]
            app_path = not_a_type
            """
        )

        with patch.dict(environ, {'MIXXIN_SETTINGS': str(settings_file)}):
            with pytest.raises(settings_ex.SettingsFormatError) as excinfo:
                settings = Settings()
                settings._load(settings_file)

                assert 'literal structure' in str(excinfo.value)
