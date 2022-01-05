
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
from jsonschema import exceptions as jsonschema_ex
from typing import Optional, List
from jsonschema import validate
import configparser
import ast
from mxxn.exceptions import filesys as filesys_ex
from mxxn.exceptions import settings as settings_ex


_settings_schema: dict = {
    'type': 'object',
    'properties': {
        'mixxin': {
            'type': 'object',
            'properties': {
                'enabled_mixins': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                },
                'app_path': {
                    'type': 'string',
                },
                'data_path': {
                    'type': 'string',
                }
            },
            'additionalProperties': False
        },
        'alembic': {
            'type': 'object',
            'properties': {
                'sqlalchemy.url': {
                    'type': 'string'
                }
            },
            'additionalProperties': False
        }
    },
    'additionalProperties': False
}
"""Schema dictionary for settings file validation."""


class Settings(object):
    """The Setting class."""

    __slots__ = [
        '_data'
    ]

    def __init__(self) -> None:
        """
        Initialize the Settings class.

        If a settings file exists, it is read in and the default settings are
        set for variables that are not in the file.
        """
        self._data = {'mixxin': {}, 'alembic': {}}
        settings_file = self._file()

        if settings_file:
            self._load(settings_file)

    def _load(self, settings_file: Path) -> None:
        """
        Load the settings from the settings file.

        The function reads the `mixxin` and the `alembic` section of the
        settings file and extends the passed data dictionary with the
        respective variables. Only the `sqlalchemy_url` variable is read
        from the `alembic` section, all others are ignored. After reading,
        the data-dictinary is validated. The `_settings_schema` is used
        for this.

        Args:
            settings_file: The settings file.

        Raises:
            mixxin.exceptions.settings.SettingsFormatError: If the settings
                file has an invalid format.
        """
        try:
            config = configparser.ConfigParser()
            config.read(settings_file)
            sections = config.sections()

            if 'mixxin' in sections:
                for option, value in config.items('mixxin'):
                    self._data['mixxin'][option] = ast.literal_eval(value)

            if 'alembic' in sections:
                if 'sqlalchemy.url' in config['alembic']:
                    self._data['alembic']['sqlalchemy.url'] =\
                            config['alembic']['sqlalchemy.url']

            validate(instance=self._data, schema=_settings_schema)

        except ValueError:
            raise settings_ex.SettingsFormatError(
                    'One of the values in the mixxin section is not regular '
                    'Python code. It must be a Python literal structure: '
                    'strings, numbers, tuples, lists, dicts, booleans, '
                    'and None.'
            )

        except configparser.Error:
            raise settings_ex.SettingsFormatError(
                    'The settings file is not in the required format. For '
                    'example, the file must have at least one section.'
            )

        except jsonschema_ex.ValidationError as e:
            if e.validator == 'additionalProperties':
                message = 'Additional variable "{}" is not allowed in the '\
                    'section of the settings file.'\
                    .format(next(iter(e.instance)))

            elif e.validator == 'type':
                message = 'The format of variable "{}" in the "{}" section '\
                    'must be "{}".'.format(
                        e.absolute_path[1],
                        e.absolute_path[0],
                        e.validator_value
                    )
            else:
                message = "The settings file is not in the required format."

            raise settings_ex.SettingsFormatError(message)

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
