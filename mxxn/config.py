"""This module provides functionality to work with configuration files."""
from pathlib import Path
from typing import List
from mxxn.exceptions import config as config_ex
from mxxn.exceptions import filesys as filesys_ex


class ConfigDir(object):
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

        default_count = 0

        for file in self.files:
            if not file.name.endswith('.json'):
                raise filesys_ex.ExtensionError(
                    'The extension of a config file "{}"'
                    'is not .json'.format(file)
                )

            if file.name.endswith('-default.json'):
                default_count += 1

        if default_count == 0:
            raise config_ex.NoDefaultConfigError(
                'There is no default config file.'
            )

        if default_count > 1:
            raise config_ex.TooManyDefaultConfigsError(
                'There are too many default config files.'
            )

    @property
    def files(self) -> List[Path]:
        """
        Get the names of the files in the directory.

        Returns:
            list: A list of files in the directory.

        """
        files = [x for x in self._path.glob('*') if x.is_file()]

        return files

    @property
    def names(self) -> List[str]:
        """
        Get the names of the files in the directory.

        A Name is the file name without extension and
        without "-default" string.

        Returns:
            list: A list of names in the directory.

        """
        names = []

        for file in self.files:
            if file.name.endswith('-default.json'):
                names.append(file.name.replace('-default.json', ''))
            else:
                names.append(file.name.replace('.json', ''))

        return names

    @property
    def default(self) -> str:
        """
        Get the names of the default files in the directory.

        A Name is the file name without "-default.json" string.

        Returns:
            string: The name of the default config file.

        """
        for file in self.files:
            if file.name.endswith('-default.json'):
                return file.name.replace('-default.json', '')
