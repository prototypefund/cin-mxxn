"""This module provides functionality to work with configuration files."""
from pathlib import Path
from typing import List, Dict, Any
import json
import re
from mxxn.exceptions import config as config_ex
from mxxn.exceptions import env as env_ex
from mxxn import env
from mxxn.exceptions import filesys as filesys_ex
from mxxn.utils import dicts
from mxxn.settings import Settings


class Config:
    """
    This class abstracts a configuration directory.

    A configuration directory is a directory containing JSON files for
    different setups (for example, for themes or strings). The respective
    configuration file can be selected and its content returned as a
    dictionary. Each configuration folder must contain a default
    configuration file. This file will be used as a base and will be
    overwritten with the contents of the selected file. Only JSON files
    are allowed in a configuration directory. In addition, the folder
    must contain a file with the extension "-default.json".

    Configuration files have the following format. The variables are
    replaced by their value when read in.

    .. code:: javascript

        {
            'variables': {
                'primary.color': '#3c0f60'
            },
            'theme': {
                'toolbar.color': '#000000',
                'navbar.color': '{primary.color}',
              }
        }

    """

    def __init__(self, path: Path) -> None:
        """
        Initialize the Config instance.

        The constructor checks whether the path to the configuration files
        exists, if there are only JSON files in it, and if there is a
        default file in it.

        Args:
            path: The relative path to the configuration files.

        Raises:
            mxxn.exceptions.filesys.PathNotExistError:
                If the path does not exist.
            mxxn.exceptions.filesys.ExtensionError:
                If there is a file its extension is not ".json".
            mxxn.exceptions.config.NoDefaultConfigError:
                If there is no default configuration in the folder.
            mxxn.exceptions.config.TooManyDefaultConfigsError:
                If there are too many default configurations in the folder.

        """
        if not path.is_dir():
            raise filesys_ex.PathNotExistError(
                'The config path {} does not exist.'.format(path))

        self._path = path
        self._files = [x for x in self._path.glob('*') if x.is_file()]
        self._names = []

        default_count = 0

        for file in self._files:
            if not file.name.endswith('.json'):
                raise filesys_ex.ExtensionError(
                    'The extension of a config file "{}"'
                    'is not .json'.format(file)
                )

            if file.name.endswith('-default.json'):
                default_count += 1
                self._default = file.name.replace('-default.json', '')
                self._names.append(file.name.replace('-default.json', ''))

                continue

            self._names.append(file.name.replace('.json', ''))

        if default_count == 0:
            raise config_ex.NoDefaultConfigError(
                'There is no default config file in {} path.'
                .format(self._path)
            )

        if default_count > 1:
            raise config_ex.TooManyDefaultConfigsError(
                'There are too many default config files in {} path.'
                .format(self._path)
            )

    @property
    def files(self) -> List[Path]:
        """
        Get the config files of the directory.

        Returns:
            list: A list of files in the directory.

        """
        return self._files

    @property
    def names(self) -> List[str]:
        """
        Get the names of the files in the directory.

        A Name is the file name without extension and
        without "-default" string.

        Returns:
            list: A list of names in the directory.

        """
        return self._names

    @property
    def default(self) -> str:
        """
        Get the names of the default files in the directory.

        A Name is the file name without "-default.json" string.

        Returns:
            string: The name of the default config file.

        """
        return self._default

    def dict(self, name: str) -> dict:
        """
        Read the config file and return the JSON data as dictionary.

        Args:
            name: The name of the config file without extension
                and '-default" string.

        Returns:
            Config data as dictionary.

        Raises:
            ValueError: If config file does not exist.
            mxxn.exceptions.filesys.FileFormatError:
                If the file does not contain correct JSON data.

        """
        try:
            theme = None

            if name in self.names:
                file_name = self._path/f'{self.default}-default.json'

                with open(file_name, 'r') as f:
                    data = json.load(f)

                self._validate_variables(data)
                default_theme = self._replace_variables(data)

                if name != self.default:
                    file_name = self._path/f'{name}.json'

                    with open(file_name, 'r') as f:
                        data = json.load(f)

                    self._validate_variables(data)
                    theme = self._replace_variables(data)
                    dicts.merge(default_theme, theme)

                return default_theme

        except json.decoder.JSONDecodeError:
            message = 'The file "{}" does not contain a ' \
                'regular JSON format.'.format(file_name)

            raise filesys_ex.FileFormatError(message)

        raise ValueError(f'Config name {name} does not exist.')

    @staticmethod
    def _validate_variables(config_dict: Dict[str, Dict[str, dict]]) -> None:
        """
        Validate the variables format.

        Args:
            config_dict: The data dictionary for the config file.
        """
        for section in ['variables', 'data']:
            if section not in config_dict or len(config_dict) != 2:
                raise config_ex.ConfigsError(
                        'Only "variables" and "data" root keys allowed and '
                        'both must exist.')

            for key in config_dict[section].keys():
                result = re.match(r'^[a-zA-Z0-9]+([.]?[a-zA-Z0-9]+)*$', key)

                if not result:
                    raise config_ex.ConfigsError(
                            f'The variable {key} is not in correct format.')

    @staticmethod
    def _replace_variables(config_dict: Dict[str, dict]) -> dict:
        """
        Replace the placeholders with the values of the variables.

        Args:
            theme_dict: The data dictionary for the config file.

        Returns:
            The theme dictionary with replaced variables.
        """
        config_dict_replaced: dict = config_dict['data']
        variables: dict = config_dict['variables']

        for key, value in config_dict_replaced.items():
            matches = list(re.finditer(
                    r'{\s*[a-zA-Z0-9]+([.]?[a-zA-Z0-9]+)*\s*}', value))

            for match in matches:
                variable = match.group()
                variable = variable.replace(' ', '')
                variable = variable[1:-1]

                if variable in variables:
                    value = value.replace(match.group(), variables[variable])

                config_dict_replaced[key] = value

        return config_dict_replaced


def theme(name: str, settings: Settings) -> dict:
    """
    Get the theme dict of the application.

    The application's theme dictionary has the following format.

    .. code:: javascript
        {
            'mxxn': {
                <Mxxn package theme variables>
            },
            'mxns': {
                'one': {
                    <Mxn two package theme variables>
                },
                'two': {
                    <Mxn two package theme variables>
                }
            },
            'mxnapp': {
                <MxnApp package theme variables>
            }

    Args:
        name: The name of the theme.
        settings: The settings object of the application.
    """
    theme_dict = {}
    mxxn_pkg = env.Mxxn()
    mxxn_theme = mxxn_pkg.theme

    if mxxn_theme:
        theme_dict['mxxn'] = mxxn_theme.dict(name)
    else:
        theme_dict['mxxn'] = {}

    mxn_names = env.mxns(settings)

    if mxn_names:
        theme_dict['mxns'] = {}

        for mxn_name in mxn_names:
            mxn_pkg = env.Mxn(mxn_name)
            mxn_theme = mxn_pkg.theme

            if mxn_theme:
                if mxn_theme.default != mxxn_theme.default:
                    raise config_ex.NotSameDefaults(
                        'Package {} has not the same default theme a mxxn.'
                        .format(mxn_pkg.name))

                theme_dict['mxns'][mxn_name] = mxn_theme.dict(name)

    try:
        theme_dict['mxnapp'] = {}
        mxnapp_pkg = env.MxnApp()
        mxnapp_theme = mxnapp_pkg.theme

        if mxnapp_theme:
            if mxnapp_theme.default != mxnapp_theme.default:
                raise config_ex.NotSameDefaults(
                    'Package {} has not the same default theme a mxxn.'
                    .format(mxnapp_pkg.name))

            theme_dict['mxnapp'] = mxnapp_theme.dict(name)

    except env_ex.MxnAppNotExistError:
        pass

    return theme_dict
