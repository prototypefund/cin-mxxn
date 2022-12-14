
"""The Settings module is used to access the application settings."""
from pathlib import Path
from os import environ
from jsonschema import exceptions as jsonschema_ex
from typing import Optional, List
from jsonschema import validate
import configparser
import ast
from falcon.asgi import Request, Response
from mxxn.exceptions import filesys as filesys_ex
from mxxn.exceptions import settings as settings_ex


_SETTINGS_SCHEMA: dict = {
    'type': 'object',
    'properties': {
        'mxxn': {
            'type': 'object',
            'properties': {
                'enabled_mxns': {
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


class Settings():
    """
    The settings class of the framework.

    This class can be used to access the settings in the
    settings file. For application settings that were not
    set in the settings file, a default value is set so that
    the application can also be started without a settings file.
    """

    __slots__ = [
        '_data'
    ]

    def __init__(self) -> None:
        """
        Initialize the Settings class instance.

        If a settings file exists, it is read in and the default settings are
        set for variables that are not in the file.
        """
        self._data: dict = {'mxxn': {}, 'alembic': {}}
        settings_file = self._file()

        if settings_file:
            self._load(settings_file)

    @property
    def enabled_mxns(self) -> Optional[List[str]]:
        """
        Get a list of enabled mxns.

        It is possible to activate only specific Mxns in the
        settings file. If the *enabled_mxns* variable of the settings
        file is not set, None is returned. To deactivate all installed mxns,
        an empty list can be set in the settings file.
        """
        if 'enabled_mxns' in self._data['mxxn']:
            return self._data['mxxn']['enabled_mxns']

        return None

    @property
    def app_path(self) -> Path:
        """
        Get the application path.

        The application path is the location where the runtime data of the
        application are stored. This is usually where the settings.ini and
        the data folder are located, which contains, for example, the SQLite
        database, if used. If the app_path variable of the settings file is
        not set, the current working directory at the time of the application
        start is returned.
        """
        if 'app_path' in self._data['mxxn']:
            app_path = Path(self._data['mxxn']['app_path'])

            if app_path.is_dir():
                return app_path.resolve()
            else:
                raise filesys_ex.PathNotExistError(
                    'The app_path from the settings file does not exist.'
                )
        else:
            return Path.cwd()

    @property
    def data_path(self) -> Path:
        """
        Get the data path.

        The Data folder is normally located in the application path and
        contains, for example, the SQLite database, if one is used. The files
        folder, in which the uploaded files are stored, is also located there.
        If the data_path variable of the settings file is not set, the
        *app_path/data* is returned.
        """
        if 'data_path' in self._data['mxxn']:
            data_path = Path(self._data['mxxn']['data_path'])

            if data_path.is_dir():
                return data_path.resolve()
            else:
                raise filesys_ex.PathNotExistError(
                    'The data_path from the settings file does not exist.'
                )
        else:
            return self.app_path/'data'

    @property
    def sqlalchemy_url(self) -> str:
        """
        Get the SQLAlchemy database URL.

        The database URL is taken from the *sqlalchemy_url* variable of the
        *alembic* section of the settings file. If this was not set, the
        default URL *sqlite:///<data_path>/mxxn.db* is returned.

        Returns:
            The default database URL.
        """
        if 'sqlalchemy.url' in self._data['alembic']:
            return self._data['alembic']['sqlalchemy.url']
        else:
            return 'sqlite+aiosqlite:///' + str(self.data_path/'mxxn.db')

    def _load(self, settings_file: Path) -> None:
        """
        Load the settings from the settings file.

        The function reads the *mxxn* and the *alembic* section of the
        settings file into the self._data dictionary with the
        respective variables. Only the *sqlalchemy_url* variable is read
        from the `alembic` section, all others are ignored. After reading,
        the self._data dictinary is validated.

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

            if 'mxxn' in sections:
                for option, value in config.items('mxxn'):
                    self._data['mxxn'][option] = ast.literal_eval(value)

            if 'alembic' in sections:
                if 'sqlalchemy.url' in config['alembic']:
                    self._data['alembic']['sqlalchemy.url'] =\
                            config['alembic']['sqlalchemy.url']

            validate(instance=self._data, schema=_SETTINGS_SCHEMA)

        except ValueError:
            raise settings_ex.SettingsFormatError(
                    'One of the values in the mxxn section is not regular '
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

        The function checks if the environment variable *MXXN_SETTINGS* has
        been set and whether the file exists in the file system. If the
        environment variable has not been set, the current working directory
        is searched for a file with the name *settings.ini*. If this file does
        not exist as well, None is returned.

        Raises:
            mixxin.exceptions.filesys.FileNotExistError: If the file in the
                environment variable MXXN_SETTINGS does not exist.

        Returns:
            The absolute path to the settings file or None if it does
            not exist.
        """
        if 'MXXN_SETTINGS' in environ:
            if Path(environ['MXXN_SETTINGS']).is_file():
                return Path(environ['MXXN_SETTINGS']).resolve()
            else:
                raise filesys_ex.FileNotExistError(
                        'The settings file in the environment variable '
                        'MXXN_SETTINGS does not exist.'
                )
        else:
            if (Path.cwd()/'settings.ini').is_file():
                return Path.cwd()/'settings.ini'

            return None


class SettingsMiddleware():
    """The middleware for the Settings class."""

    def __init__(self, settings: Settings):
        """
        Initialize the SettingsMiddleware instance.

        Args:
            settings: The settings of the application.
        """
        self._settings = settings

    async def process_request(self, req: Request, resp: Response) -> None:
        """
        Add the application settings to the request object.

        The settings can be accessed via the context variable
        req.context.settings.

        Args:
            req: The request object.
            resp: The response object.
        """
        req.context.settings = self._settings
