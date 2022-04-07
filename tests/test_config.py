"""Tests for the config module."""
import pytest
from unittest.mock import Mock
import json
from mxxn.exceptions import filesys as filesys_ex
from mxxn.exceptions import config as config_ex
from mxxn.config import Base, Theme
from mxxn import env
from mxxn.settings import Settings


class TestBaseInit():
    """Test for the initialization of Base class instance."""

    def test_path_not_exist(self, mxxn_env):
        """Is PathNotExistError raised if path not exist."""
        with pytest.raises(filesys_ex.PathNotExistError):
            Base(mxxn_env/'mxnone/xxxyyyzzz')

    def test_non_json_extension(self, mxxn_env):
        """Is ExtensionError raised."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()
        (mxnone_config/'fake.txt').touch()

        with pytest.raises(filesys_ex.ExtensionError):
            Base(mxnone_config)

    def test_too_many_defaults(self, mxxn_env):
        """Is TooManyDefaultConfigsError raised."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()
        (mxnone_config/'de-default.json').touch()

        with pytest.raises(config_ex.TooManyDefaultConfigsError):
            Base(mxnone_config)

    def test_no_default(self, mxxn_env):
        """Test if NoDefaultConfigError is raised."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en.json').touch()

        with pytest.raises(config_ex.NoDefaultConfigError):
            Base(mxnone_config)


class TestBaseFiles():
    """Tests for the files method of Base class."""

    def test_files_returned(self, mxxn_env):
        """Are the filenames returned."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        de_file = mxnone_config/'de-DE.json'
        de_file.touch()
        en_file = mxnone_config/'en-default.json'
        en_file.touch()

        config = Base(mxnone_config)

        assert config.files == [en_file, de_file]


class TestBaseNames():
    """Test for the names method of Base class."""

    def test_names_returned(self, mxxn_env):
        """Are the names returned."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()

        config = Base(mxnone_config)

        assert config.names == ['en', 'de-DE']


class TestBaseDefault():
    """Test for the default method of Base class."""

    def test_default_returned(self, mxxn_env):
        """Is the default name returned."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()

        config = Base(mxnone_config)

        assert config.default == 'en'


class TestBaseDict:
    """Test for the dict method of the Base class."""

    def test_not_a_json_file(self, mxxn_env):
        """One file does not contain correct JSON data."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()

        config = Base(mxnone_config)

        with pytest.raises(filesys_ex.FileFormatError):
            config.dict('en')

    def test_name_not_exist(self, mxxn_env):
        """ValueError raised if a file with the name does not exist."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()

        with open(mxxn_env/'mxnone/config/en-default.json', 'w') as f:
            json.dump({}, f)

        with open(mxxn_env/'mxnone/config/de.json', 'w') as f:
            json.dump({}, f)

        config = Base(mxnone_config)

        with pytest.raises(ValueError):
            config.dict('uk')

    def test_name_is_default(self, mxxn_env):
        """It is the default name."""
        default_config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'theme': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()

        with open(mxxn_env/'mxnone/config/en-default.json', 'w') as f:
            json.dump(default_config, f)

        config = Base(mxnone_config)

        assert config.dict('en') == {
                'toolbar.color': '#000000',
                'navbar.color': '#3c0f60'
                }

    def test_not_default_name(self, mxxn_env):
        """It is not the defaul name."""
        default_config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'theme': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        config = {
            'variables': {
                'primary.color': '#ffffff'
            },
            'theme': {
                'navbar.color': '{primary.color}',
              }
        }

        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()

        with open(mxxn_env/'mxnone/config/light-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxxn_env/'mxnone/config/dark.json', 'w') as f:
            json.dump(config, f)

        merged_config = Base(mxnone_config).dict('dark')

        assert merged_config == {
                'toolbar.color': '#000000',
                'navbar.color': '#ffffff'
                }


class TestBaseReplaceVariables():
    """Tests for the _replace_variables function of the Base class."""

    def test_variable_replaced(self, mxxn_env):
        """All variables were replaced."""
        config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'theme': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        replaced_dict = Base._replace_variables(config)

        assert replaced_dict == {
                'toolbar.color': '#000000',
                'navbar.color': '#3c0f60',
                }

    def test_spaces_after_opening_bracket(self, mxxn_env):
        """Spaces after the opening curly bracket."""
        config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'theme': {
                'toolbar.color': '#000000',
                'navbar.color': '{  primary.color}',
              }
        }

        replaced_dict = Base._replace_variables(config)

        assert replaced_dict == {
                'toolbar.color': '#000000',
                'navbar.color': '#3c0f60',
                }

    def test_spaces_before_closing_bracket(self, mxxn_env):
        """Spaces before the closing curly bracket."""
        config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'theme': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color  }',
              }
        }

        replaced_dict = Base._replace_variables(config)

        assert replaced_dict == {
                'toolbar.color': '#000000',
                'navbar.color': '#3c0f60',
                }

    def test_incorrect_variable_name(self, mxxn_env):
        """A incorrect variable name."""
        config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'theme': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary .color}',
              }
        }

        replaced_dict = Base._replace_variables(config)

        assert replaced_dict == {
                'toolbar.color': '#000000',
                'navbar.color': '{primary .color}'
                }


# class TestThemeDict():
#     """Tests for the dict method of the Theme class."""
#
#     def test_1tmp(self, mxxn_env):
#         theme = {
#             'variables': {
#                 'primary-color': '#3c0f60'
#             },
#             'theme': {
#                 'toolbar-color': '#000000',
#                 'navbar-color': '{primary-color}',
#               }
#         }
#
#         mxnone_themes_dir = mxxn_env/'mxnone/config'
#         mxnone_themes_dir.mkdir()
#
#         with open(mxxn_env/'mxnone/config/en-default.json', 'w') as f:
#             json.dump(theme, f)
#
#         theme = config.Theme(mxnone_themes_dir)
#
#         assert theme.dict('en') == {
#                 'toolbar-color': '#000000',
#                 'navbar-color': '#3c0f60'
#                 }
#
#     def test_tmp(self, mxxn_env):
#         default_theme = {
#             'variables': {
#                 'primary-color': '#3c0f60'
#             },
#             'theme': {
#                 'toolbar-color': '#000000',
#                 'navbar-color': '{primary-color}',
#               }
#         }
#
#         theme = {
#             'variables': {
#                 'primary-color': '#ffffff'
#             },
#             'theme': {
#                 'navbar-color': '{primary-color}',
#               }
#         }
#
#         mxnone_themes_dir = mxxn_env/'mxnone/config'
#         mxnone_themes_dir.mkdir()
#
#         with open(mxxn_env/'mxnone/config/light-default.json', 'w') as f:
#             json.dump(default_theme, f)
#
#         with open(mxxn_env/'mxnone/config/dark.json', 'w') as f:
#             json.dump(theme, f)
#
#         theme_merged = config.Theme(mxnone_themes_dir).dict('dark')
#
#         assert theme_merged == {
#                 'toolbar-color': '#000000',
#                 'navbar-color': '#ffffff'
#                 }
#

# class TestThemeInit():
#     """Tests for the initialization of the Theme class."""
#
#     def test_only_added_if_theme_exists(self, mxxn_env):
#         """Only added if the theme exists in the package."""
#         settings = Mock()
#         settings.enabled_mxns = ['mxnone', 'mxntwo']
#
#         mxnone_themes_dir = mxxn_env/'mxnone/configs/themes'
#         mxnone_themes_dir.mkdir(parents=True)
#
#         with open(mxnone_themes_dir/'light-default.json', 'w') as f:
#             json.dump({'theme_mxnone': 'light'}, f)
#
#         with open(mxnone_themes_dir/'dark.json', 'w') as f:
#             json.dump({'theme_mxnone': 'dark'}, f)
#
#         theme = config.Theme('dark', settings)
#
#         assert theme['mxns'] == {'mxnone': {'theme_mxnone': 'dark'}}
#         assert 'mxxn' in theme
#         assert 'mxnapp' not in theme
#
#     def test_1tmp(self, mxxn_env):
#         """Only added if the theme exists in the package."""
#         settings = Mock()
#         settings.enabled_mxns = ['mxnone', 'mxntwo']
#
#         mxnone_themes_dir = mxxn_env/'mxnone/configs/themes'
#         mxnone_themes_dir.mkdir(parents=True)
#
#         with open(mxnone_themes_dir/'light.json', 'w') as f:
#             json.dump({'theme_mxnone': 'light'}, f)
#
#         with open(mxnone_themes_dir/'dark-default.json', 'w') as f:
#             json.dump({'theme_mxnone': 'dark'}, f)
#
#         with pytest.raises(config_ex.NotSameDefaults):
#             config.Theme('dark', settings)
#
#     def test_1tmp(self, mxxn_env):
#         """Only added if the theme exists in the package."""
#         settings = Mock()
#         settings.enabled_mxns = ['mxnone', 'mxntwo']
#
#         mxnapp_themes_dir = mxxn_env/'mxnapp/configs/themes'
#         mxnapp_themes_dir.mkdir(parents=True)
#
#         with open(mxnapp_themes_dir/'light.json', 'w') as f:
#             json.dump({'theme_mxnapp': 'light'}, f)
#
#         with open(mxnapp_themes_dir/'dark-default.json', 'w') as f:
#             json.dump({'theme_mxnapp': 'dark'}, f)
#
#         with pytest.raises(config_ex.NotSameDefaults):
#             config.Theme('dark', settings)
#

