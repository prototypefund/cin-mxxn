"""This module provides functionality to work with configuration files."""
from pathlib import Path
from typing import List
import json
import re
from mxxn.exceptions import config as config_ex
from mxxn.exceptions import filesys as filesys_ex
from mxxn.exceptions import env as env_ex
from mxxn.utils import dicts
from mxxn import env
from mxxn.settings import Settings
from mxxn.logging import logger


class ConfigsDir:
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
    """

    def __init__(self, path: Path) -> None:
        """
        Initialize the ConfigDir object.

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
        Get the names of the files in the directory.

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
        if name in self._names:
            if name == self._default:
                file_name = self._path/f'{name}-default.json'
            else:
                file_name = self._path/name

            try:
                with open(file_name, 'r') as f:
                    data = json.load(f)

                    return data

            except json.decoder.JSONDecodeError:
                message = 'The file "{}" does not contain a ' \
                    'regular JSON format.'.format(file_name)

                raise filesys_ex.FileFormatError(message)

        raise ValueError('Config name {name} does not exist.')


class Theme(dict):
    """The Theme dictionary of the framework."""

    def __init__(self, name: str, settings: Settings) -> None:
        """
        Initialize the Themes object.

        Args:
            name: The name of the theme.
            settings: The settings object of the application.
        """
        log = logger('registration')
        mxxn_pkg = env.Mxxn()
        default_theme = mxxn_pkg.default_theme
        self['mxxn'] = mxxn_pkg.theme(name)

        # mxn_names = env.mxns(settings)
        #
        # log.debug('The theme of package mxxn was registered.')
        #
        # if mxn_names:
        #     self['mxns'] = {}
        #
        # for mxn_name in mxn_names:
        #     mxn_pkg = env.Mxn(mxn_name)
        #     theme = mxn_pkg.theme(name)
        #
        #     if theme:
        #         if mxn_pkg.default_theme != default_theme:
        #             raise config_ex.NotSameDefaults(
        #                 'Package {} has not the same default theme a mxxn.'
        #                 .format(mxn_pkg.name))
        #
        #         self['mxns'][mxn_name] = theme
        #
        #     log.debug(
        #         'The theme of package {} was registered.'
        #         .format(mxn_pkg.name)
        #     )
        #
        # try:
        #     mxnapp_pkg = env.MxnApp()
        #     theme = mxnapp_pkg.theme(name)
        #
        #     if theme:
        #         if mxnapp_pkg.default_theme != default_theme:
        #             raise config_ex.NotSameDefaults(
        #                 'Package {} has not the same default theme a mxxn.'
        #                 .format(mxnapp_pkg.name))
        #
        #         self['mxnapp'] = mxnapp_pkg.theme(name)
        #
        #     log.debug(
        #         'The theme of package {} was registered.'
        #         .format(mxnapp_pkg.name)
        #     )
        #
        # except env_ex.MxnAppNotExistError:
        #     pass

    @staticmethod
    def _replace_variables(theme_dict: dict) -> dict:
        """
        Replace the placeholders with the values of the variables.

        Args:
            theme_dict: The data dictionary for the config file.

        Returns:
            The theme dictionary with replaced variables.
        """
        theme_dict_replaced = theme_dict['theme']
        variables = theme_dict['variables']

        for key, value in theme_dict_replaced.items():
            result = re.findall(r'^{\s*[a-zA-Z0-9-]+\s*}$', value)

            if result and len(result) == 1:
                variable = result[0]
                variable = variable.replace(' ', '')
                variable = variable[1:-1]

                if variable in variables:
                    theme_dict_replaced[key] = value.replace(
                            result[0], variables[variable])

        return theme_dict_replaced

    # def dict(self, name: str) -> dict:
    #     """
    #     Get the config dictionary from the directory.
    #
    #     The default JSON configuration file is read in and merged
    #     with the read-in JSON data from the file whose name was
    #     passed as an argument. If a file with the name does not
    #     exist, the default dictionary is returned.
    #
    #     Args:
    #         name: The name of the config file without extension
    #             and '-default" string.
    #
    #     Returns:
    #         A merge of the json files from the directory.
    #
    #     Raises:
    #         mxxn.exceptions.filesys.FileFormatError:
    #             If one of both file does not contain correct JSON data.
    #
    #     """
    #     default_file_name = self._path / (self.default + '-default.json')
    #     file_name = self._path / (name + '.json')
    #
    #     with open(default_file_name, 'r') as f:
    #         try:
    #             default_config_data = json.load(f)
    #         except json.decoder.JSONDecodeError:
    #             message = 'The file "{}" does not contain a ' \
    #                 'regular JSON format.'.format(default_file_name)
    #
    #             raise filesys_ex.FileFormatError(message)
    #
    #     if (not self.default == name) and (name in self.names):
    #         with open(file_name, 'r') as f:
    #             try:
    #                 config_data = json.load(f)
    #             except json.decoder.JSONDecodeError:
    #                 message = 'The file "{}" does not contain a ' \
    #                     'regular JSON format.'.format(file_name)
    #                 raise filesys_ex.FileFormatError(message)
    #
    #         dicts.merge(default_config_data, config_data)
    #
    #     return default_config_data
