"""Tests for the config module."""
import pytest
import json
from mxxn.exceptions import filesys as filesys_ex
from mxxn.exceptions import config as config_ex
from mxxn import config


class TestConfigDirInit():
    """Test for the initialization of ConfigDir."""

    def test_path_not_exist(self, mxxn_env):
        """Is PathNotExistError raised if path not exist."""
        with pytest.raises(filesys_ex.PathNotExistError):
            config.ConfigDir(mxxn_env/'mxnone/xxxyyyzzz')

    def test_non_json_extension(self, mxxn_env):
        """Is ExtensionError raised."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()
        (mxnone_config_dir/'fake.txt').touch()

        with pytest.raises(filesys_ex.ExtensionError):
            config.ConfigDir(mxnone_config_dir)

    def test_too_many_defaults(self, mxxn_env):
        """Is TooManyDefaultConfigsError raised."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()
        (mxnone_config_dir/'de-default.json').touch()

        with pytest.raises(config_ex.TooManyDefaultConfigsError):
            config.ConfigDir(mxnone_config_dir)

    def test_no_default(self, mxxn_env):
        """Test if NoDefaultConfigError is raised."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en.json').touch()

        with pytest.raises(config_ex.NoDefaultConfigError):
            config.ConfigDir(mxnone_config_dir)


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

        config_dir = config.ConfigDir(mxnone_config_dir)

        assert config_dir.files == [en_file, de_file]


class TestConfigDirNames():
    """Test for the names method of ConfigDir class."""

    def test_names_returned(self, mxxn_env):
        """Are the names returned."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()

        config_dir = config.ConfigDir(mxnone_config_dir)

        assert config_dir.names == ['en', 'de-DE']


class TestConfigDirDefault():
    """Test for the default method of ConfigDir class."""

    def test_default_returned(self, mxxn_env):
        """Is the default name returned."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()

        config_dir = config.ConfigDir(mxnone_config_dir)

        assert config_dir.default == 'en'


class TestConfigDirDict(object):
    """Test for the dict method of the ConfigDir class."""

    # def test_not_a_json_file(self, mxxn_env):
    def test_tmp(self, mxxn_env):
        """One file does not contain correct JSON data."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()

        config_dir = config.ConfigDir(mxnone_config_dir)

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

        config_dir = config.ConfigDir(mxnone_config_dir)

        assert config_dir.dict('ru') == {'name': 'en'}
