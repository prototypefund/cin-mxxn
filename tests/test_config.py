"""Tests for the config module."""
import pytest
import json
from unittest.mock import Mock
from mxxn.exceptions import filesys as filesys_ex
from mxxn.exceptions import config as config_ex
from mxxn.config import Config, theme, strings


class TestConfigInit():
    """Test for the initialization of Config class instance."""

    def test_path_not_exist(self, mxxn_env):
        """Is PathNotExistError raised if path not exist."""
        with pytest.raises(filesys_ex.PathNotExistError):
            Config(mxxn_env/'mxnone/xxxyyyzzz')

    def test_non_json_extension(self, mxxn_env):
        """Is ExtensionError raised."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()
        (mxnone_config/'fake.txt').touch()

        with pytest.raises(filesys_ex.ExtensionError):
            Config(mxnone_config)

    def test_too_many_defaults(self, mxxn_env):
        """Is TooManyDefaultConfigsError raised."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()
        (mxnone_config/'de-default.json').touch()

        with pytest.raises(config_ex.TooManyDefaultConfigsError):
            Config(mxnone_config)

    def test_no_default(self, mxxn_env):
        """Test if NoDefaultConfigError is raised."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en.json').touch()

        with pytest.raises(config_ex.NoDefaultConfigError):
            Config(mxnone_config)


class TestConfigFiles():
    """Tests for the files method of Config class."""

    def test_files_returned(self, mxxn_env):
        """Are the filenames returned."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        de_file = mxnone_config/'de-DE.json'
        de_file.touch()
        en_file = mxnone_config/'en-default.json'
        en_file.touch()

        config = Config(mxnone_config)

        assert config.files == [en_file, de_file]


class TestConfigNames():
    """Test for the names method of Config class."""

    def test_names_returned(self, mxxn_env):
        """Are the names returned."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()

        config = Config(mxnone_config)

        assert config.names == ['en', 'de-DE']


class TestConfigDefault():
    """Test for the default method of Config class."""

    def test_default_returned(self, mxxn_env):
        """Is the default name returned."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()

        config = Config(mxnone_config)

        assert config.default == 'en'


class TestConfigDict:
    """Test for the dict method of the Config class."""

    def test_not_a_json_file(self, mxxn_env):
        """One file does not contain correct JSON data."""
        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()
        (mxnone_config/'de-DE.json').touch()
        (mxnone_config/'en-default.json').touch()

        config = Config(mxnone_config)

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

        config = Config(mxnone_config)

        with pytest.raises(ValueError):
            config.dict('uk')

    def test_name_is_default(self, mxxn_env):
        """It is the default name."""
        default_config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()

        with open(mxxn_env/'mxnone/config/en-default.json', 'w') as f:
            json.dump(default_config, f)

        config = Config(mxnone_config)

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
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        config = {
            'variables': {
                'primary.color': '#ffffff'
            },
            'data': {
                'navbar.color': '{primary.color}',
              }
        }

        mxnone_config = mxxn_env/'mxnone/config'
        mxnone_config.mkdir()

        with open(mxxn_env/'mxnone/config/light-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxxn_env/'mxnone/config/dark.json', 'w') as f:
            json.dump(config, f)

        merged_config = Config(mxnone_config).dict('dark')

        assert merged_config == {
                'toolbar.color': '#000000',
                'navbar.color': '#ffffff'
                }


class TestConfigValidateVariables():
    """Tests for the _validate_variables function of the Config class."""

    def test_all_variables_correct(self):
        """All variables are in the correct format."""
        config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        Config._validate_variables(config)

    def test_incorrect_format_in_variables(self):
        """A incorrect formated variable in variables section."""
        config = {
            'variables': {
                'primary-color': '#3c0f60'
            },
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        with pytest.raises(config_ex.ConfigsError):
            Config._validate_variables(config)

    def test_incorrect_format_in_data(self):
        """A incorrect formated variable in data section."""
        config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'data': {
                'toolbar-color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        with pytest.raises(config_ex.ConfigsError):
            Config._validate_variables(config)

    def test_not_allows_root_section(self):
        """A key other than variable or data in the root."""
        config = {
            'test': {
            },
            'data': {
              }
        }

        with pytest.raises(config_ex.ConfigsError):
            Config._validate_variables(config)

    def test_no_variables_key(self):
        """No variables key in the root."""
        config = {
            'data': {
              }
        }

        with pytest.raises(config_ex.ConfigsError):
            Config._validate_variables(config)

    def test_no_data_key(self):
        """No data key in the root."""
        config = {
            'varables': {
              }
        }

        with pytest.raises(config_ex.ConfigsError):
            Config._validate_variables(config)


class TestConfigReplaceVariables():
    """Tests for the _replace_variables function of the Config class."""

    def test_variable_replaced(self, mxxn_env):
        """All variables were replaced."""
        config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        replaced_dict = Config._replace_variables(config)

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
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{  primary.color}',
              }
        }

        replaced_dict = Config._replace_variables(config)

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
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color  }',
              }
        }

        replaced_dict = Config._replace_variables(config)

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
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary .color}',
              }
        }

        replaced_dict = Config._replace_variables(config)

        assert replaced_dict == {
                'toolbar.color': '#000000',
                'navbar.color': '{primary .color}'
                }

    def test_multiple_variable(self, mxxn_env):
        """Multiple variables used."""
        config = {
            'variables': {
                'primary.color': '#3c0f60',
                'secondary.color': '#ff00ff'
            },
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color} {secondary.color}',
              }
        }

        replaced_dict = Config._replace_variables(config)

        assert replaced_dict == {
                'toolbar.color': '#000000',
                'navbar.color': '#3c0f60 #ff00ff'
                }


class TestTheme():
    """Tests for the theme function."""

    def test_all_pkg_themes_added(self, mxxn_env):
        """The themes of all packages were added."""
        default_config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        config = {
            'variables': {
                'primary.color': '#ffffff'
            },
            'data': {
                'navbar.color': '{primary.color}',
              }
        }

        mxnone_theme_path = mxxn_env/'mxnone/configs/themes'
        mxnone_theme_path.mkdir(parents=True)
        mxntwo_theme_path = mxxn_env/'mxntwo/configs/themes'
        mxntwo_theme_path.mkdir(parents=True)
        mxnapp_theme_path = mxxn_env/'mxnapp/configs/themes'
        mxnapp_theme_path.mkdir(parents=True)

        with open(mxnone_theme_path/'light-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxnone_theme_path/'dark.json', 'w') as f:
            json.dump(config, f)

        with open(mxntwo_theme_path/'light-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxntwo_theme_path/'dark.json', 'w') as f:
            json.dump(config, f)

        with open(mxnapp_theme_path/'light-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxnapp_theme_path/'dark.json', 'w') as f:
            json.dump(config, f)

        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        theme_dict = theme('light', settings)

        assert theme_dict['mxxn']
        assert theme_dict['mxns']['mxnone']
        assert theme_dict['mxns']['mxntwo']
        assert theme_dict['mxnapp']

    def test_only_added_if_theme_exists(self, mxxn_env):
        """Only added if the theme exists in the package."""
        default_config = {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'data': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

        config = {
            'variables': {
                'primary.color': '#ffffff'
            },
            'data': {
                'navbar.color': '{primary.color}',
              }
        }

        mxnone_theme_path = mxxn_env/'mxnone/configs/themes'
        mxnone_theme_path.mkdir(parents=True)

        with open(mxnone_theme_path/'light-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxnone_theme_path/'dark.json', 'w') as f:
            json.dump(config, f)

        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        theme_dict = theme('light', settings)

        assert theme_dict['mxxn']
        assert theme_dict['mxns']['mxnone']
        assert 'mxntwo' not in theme_dict['mxns']
        assert not theme_dict['mxnapp']


class TestStrings():
    """Tests for strings."""

    def test_all_pkg_strings_added(self, mxxn_env):
        """The strings of all packages were added."""
        default_config = {
            'variables': {
                'login': 'login'
            },
            'data': {
                'login.text': 'Hello {login}',
              }
        }

        config = {
            'variables': {
            },
            'data': {
                'some.string': 'some string',
              }
        }

        mxnone_strings_path = mxxn_env/'mxnone/configs/strings'
        mxnone_strings_path.mkdir(parents=True)
        mxntwo_strings_path = mxxn_env/'mxntwo/configs/strings'
        mxntwo_strings_path.mkdir(parents=True)
        mxnapp_strings_path = mxxn_env/'mxnapp/configs/strings'
        mxnapp_strings_path.mkdir(parents=True)

        with open(mxnone_strings_path/'en-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxnone_strings_path/'de.json', 'w') as f:
            json.dump(config, f)

        with open(mxntwo_strings_path/'en-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxntwo_strings_path/'de.json', 'w') as f:
            json.dump(config, f)

        with open(mxnapp_strings_path/'en-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxnapp_strings_path/'de.json', 'w') as f:
            json.dump(config, f)

        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        strings_dict = strings('en', settings)

        assert strings_dict['mxxn']
        assert strings_dict['mxns']['mxnone']
        assert strings_dict['mxns']['mxntwo']
        assert strings_dict['mxnapp']

    def test_only_added_if_strings_exists(self, mxxn_env):
        """Only added if the strings exists in the package."""
        default_config = {
            'variables': {
                'login': 'login'
            },
            'data': {
                'login.text': 'Hello {login}',
              }
        }

        config = {
            'variables': {
            },
            'data': {
                'some.string': 'some string',
              }
        }

        mxnone_strings_path = mxxn_env/'mxnone/configs/strings'
        mxnone_strings_path.mkdir(parents=True)

        with open(mxnone_strings_path/'en-default.json', 'w') as f:
            json.dump(default_config, f)

        with open(mxnone_strings_path/'de.json', 'w') as f:
            json.dump(config, f)

        settings = Mock()
        settings.enabled_mxns = ['mxnone', 'mxntwo']

        strings_dict = strings('en', settings)

        assert strings_dict['mxxn']
        assert strings_dict['mxns']['mxnone']
        assert 'mxntwo' not in strings_dict['mxns']
        assert not strings_dict['mxnapp']
