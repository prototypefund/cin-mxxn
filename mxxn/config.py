"""This module provides functionality to work with configuration files."""
from pathlib import Path
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

        """
        self._path = path


    @property
    def files(self) -> dict:
        """
        Get the names of the files in the directory.

        Returns:
            list: A list of files in the directory.

        """
        files = [x.name for x in self._path.glob('*') if x.is_file()]

        return files
