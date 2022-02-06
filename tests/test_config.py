"""Tests for the config module."""
import pytest
from mxxn.exceptions import filesys as filesys_ex
from mxxn import config



class TestConfigDirFiles():
    """Tests for the files method of ConfigDir class."""

    def test_files_returned(self, mxxn_env):
        """Are the filenames returned."""
        mxnone_config_dir = mxxn_env/'mxnone/config'
        mxnone_config_dir.mkdir()
        (mxnone_config_dir/'de-DE.json').touch()
        (mxnone_config_dir/'en-default.json').touch()

        config_dir = config.ConfigDir(mxnone_config_dir)

        assert config_dir.files == ['en-default.json', 'de-DE.json']
