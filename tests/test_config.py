"""Tests for the config module."""
import pytest
from unittest.mock import Mock
import json
from mxxn.exceptions import filesys as filesys_ex
from mxxn.exceptions import config as config_ex
from mxxn import config


class TestConfigDirInit():
    """Test for the initialization of ConfigDir."""

    def test_path_not_exist(self, mxxn_env):
        """Is PathNotExistError raised if path not exist."""
        with pytest.raises(filesys_ex.PathNotExistError):
            config.ConfigsDir(mxxn_env/'mxnone/xxxyyyzzz')

    def test_non_json_extension(self, mxxn_env):
        """Is ExtensionError raised."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()
        (mxnone_config_dir/'fake.txt').touch()

        with pytest.raises(filesys_ex.ExtensionError):
            config.ConfigsDir(mxnone_config_dir)

    def test_too_many_defaults(self, mxxn_env):
        """Is TooManyDefaultConfigsError raised."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()
        (mxnone_config_dir/'de-default.json').touch()

        with pytest.raises(config_ex.TooManyDefaultConfigsError):
            config.ConfigsDir(mxnone_config_dir)

    def test_no_default(self, mxxn_env):
        """Test if NoDefaultConfigError is raised."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en.json').touch()

        with pytest.raises(config_ex.NoDefaultConfigError):
            config.ConfigsDir(mxnone_config_dir)


class TestConfigDirFiles():
    """Tests for the files method of ConfigDir class."""

    def test_files_returned(self, mxxn_env):
        """Are the filenames returned."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        de_file = mxnone_config_dir/'de-DE.json'
        de_file.touch()
        en_file = mxnone_config_dir/'en-default.json'
        en_file.touch()

        config_dir = config.ConfigsDir(mxnone_config_dir)

        assert config_dir.files == [en_file, de_file]


class TestConfigDirNames():
    """Test for the names method of ConfigDir class."""

    def test_names_returned(self, mxxn_env):
        """Are the names returned."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()

        config_dir = config.ConfigsDir(mxnone_config_dir)

        assert config_dir.names == ['en', 'de-DE']


class TestConfigDirDefault():
    """Test for the default method of ConfigDir class."""

    def test_default_returned(self, mxxn_env):
        """Is the default name returned."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()

        config_dir = config.ConfigsDir(mxnone_config_dir)

        assert config_dir.default == 'en'


class TestConfigDirDict(object):
    """Test for the dict method of the ConfigDir class."""

    def test_not_a_json_file(self, mxxn_env):
        """One file does not contain correct JSON data."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()

        config_dir = config.ConfigsDir(mxnone_config_dir)

        with pytest.raises(filesys_ex.FileFormatError):
            config_dir.dict('de')

    def test_name_not_exist(self, mxxn_env):
        """The default is returned if a file with the name does not exist."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()

        with open(mxxn_env/'mxnone/config/en-default.json', 'w') as f:
            json.dump({'name': 'en'}, f)

        with open(mxxn_env/'mxnone/config/de.json', 'w') as f:
            json.dump({'name': 'de'}, f)

        config_dir = config.ConfigsDir(mxnone_config_dir)

        assert config_dir.dict('ru') == {'name': 'en'}


class TestThemeInit():
    """Tests for the initialization of the Theme class."""
    def test_all_theme_added(self, mxxn_env):
        """All package themes were added."""
        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        mxnone_themes_dir = mxxn_env/'mxnone/configs/themes'
        mxntwo_themes_dir = mxxn_env/'mxntwo/configs/themes'
        mxnapp_themes_dir = mxxn_env/'mxnapp/configs/themes'
        mxnone_themes_dir.mkdir(parents=True)
        mxntwo_themes_dir.mkdir(parents=True)
        mxnapp_themes_dir.mkdir(parents=True)

        with open(mxnone_themes_dir/'light-default.json', 'w') as f:
            json.dump({'theme_mxnone': 'light'}, f)

        with open(mxnone_themes_dir/'dark.json', 'w') as f:
            json.dump({'theme_mxnone': 'dark'}, f)

        with open(mxntwo_themes_dir/'light-default.json', 'w') as f:
            json.dump({'theme_mxntwo': 'light'}, f)

        with open(mxntwo_themes_dir/'dark.json', 'w') as f:
            json.dump({'theme_mxntwo': 'dark'}, f)

        with open(mxnapp_themes_dir/'light-default.json', 'w') as f:
            json.dump({'theme_mxnapp': 'light'}, f)

        with open(mxnapp_themes_dir/'dark.json', 'w') as f:
            json.dump({'theme_mxnapp': 'dark'}, f)

        theme = config.Theme('dark', settings)

        assert theme['mxns'] == {
                'mxnone': {'theme_mxnone': 'dark'},
                'mxntwo': {'theme_mxntwo': 'dark'}}

        assert theme['mxnapp'] == {'theme_mxnapp': 'dark'}

        assert 'mxxn' in theme

    def test_only_added_if_theme_exists(self, mxxn_env):
        """Only added if the theme exists in the package."""
        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        mxnone_themes_dir = mxxn_env/'mxnone/configs/themes'
        mxnone_themes_dir.mkdir(parents=True)

        with open(mxnone_themes_dir/'light-default.json', 'w') as f:
            json.dump({'theme_mxnone': 'light'}, f)

        with open(mxnone_themes_dir/'dark.json', 'w') as f:
            json.dump({'theme_mxnone': 'dark'}, f)

        theme = config.Theme('dark', settings)

        assert theme['mxns'] == {'mxnone': {'theme_mxnone': 'dark'}}
        assert 'mxxn' in theme
        assert 'mxnapp' not in theme

    def test_1tmp(self, mxxn_env):
        """Only added if the theme exists in the package."""
        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        mxnone_themes_dir = mxxn_env/'mxnone/configs/themes'
        mxnone_themes_dir.mkdir(parents=True)

        with open(mxnone_themes_dir/'light.json', 'w') as f:
            json.dump({'theme_mxnone': 'light'}, f)

        with open(mxnone_themes_dir/'dark-default.json', 'w') as f:
            json.dump({'theme_mxnone': 'dark'}, f)

        with pytest.raises(config_ex.NotSameDefaults):
            config.Theme('dark', settings)

    def test_1tmp(self, mxxn_env):
        """Only added if the theme exists in the package."""
        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        mxnapp_themes_dir = mxxn_env/'mxnapp/configs/themes'
        mxnapp_themes_dir.mkdir(parents=True)

        with open(mxnapp_themes_dir/'light.json', 'w') as f:
            json.dump({'theme_mxnapp': 'light'}, f)

        with open(mxnapp_themes_dir/'dark-default.json', 'w') as f:
            json.dump({'theme_mxnapp': 'dark'}, f)

        with pytest.raises(config_ex.NotSameDefaults):
            config.Theme('dark', settings)
