
"""
The Settings module is used to access the application settings.

Like most Python packages, the Mixxin framework uses a settings file in INI
format. This has the advantage that there is the possibility of using only
one settings file for Mixxin, Alembic, Supervisor, Uvicorn etc.

Mixxin itself reads the `mixxin` section and the `sqlalchemy_url` variable of
the `alembic` section of the settings file.

.. note::
    If an extra settings file is used for alembic, then the alembic section
    with the sqlalchemy_url variable must still be present in the Mixxin
    settings file.

The Mixxin settings file can be passed to the framework via the environment
variable `MIXXIN_SETTINGS`. If the variable is not used, the settings.ini file
is searched for in the current working environment. If no settings file is
applied, the default settings of the Mixxin framework are used.
"""
from pathlib import Path
from os import environ
from typing import Optional
from mxxn.exceptions import filesys as filesys_ex


class Settings(object):
    """The Setting class."""

    @staticmethod
    def _file() -> Optional[Path]:
        """
        Get the path of the settings file.

        The function checks if the environment variable `MIXXIN_SETTINGS` has
        been set and whether the file exists in the file system. If the
        environment variable has not been set, the current working directory
        is searched for a file with the name `settings.ini`. If this file does
        not exist as well, None is returned.

        Raises:
            mixxin.exceptions.filesys.FileNotExistError: If the file in the
                environment variable MIXXIN_SETTINGS does not exist.

        Returns:
            The absolute path to the settings file or None if it does
            not exist.
        """
        if 'MIXXIN_SETTINGS' in environ:
            if Path(environ['MIXXIN_SETTINGS']).is_file():
                return Path(environ['MIXXIN_SETTINGS']).resolve()
            else:
                raise filesys_ex.FileNotExistError(
                        'The settings file in the environment variable '
                        'MIXXIN_SETTINGS does not exist.'
                )
        else:
            if (Path.cwd()/'settings.ini').is_file():
                return Path.cwd()/'settings.ini'

            return
