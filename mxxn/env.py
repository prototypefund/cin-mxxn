"""
Module for using components of the mxxn environment.

Mxxn applications are always based on a Python virtual environment.
A separate environment must be used for each application, because
only one MxnApp package is accepted per environment.

The mxxn environment has the three basic package types
Mxxn, Mxn and MxnApp. The Mxxn package it self is the
framework package containing the framework functionality.
Mxns are plugins that can be installed in the environment and
automatically detected by the framework. These plugins extend
the functionality of the application. The MxnApp brings together
all the required Mixins and the Mxxn framework and packages it.
In addition, overloads for components of the Mixins and for the
framework can be defined in the MxnApp.
For package management the setuptools are used. Each Mxxn package
is standalone Python package and can be installed into the environment
using pip. However, it is recommended to manage the dependence on
other Mxxn packages in the setup file of the MxnApp package.

All three package types have essentially the same structure. On the
basis of this structure, when the application starts, elements are
automatically loaded from the packages and registered in the framework.

    .. warning::
        To avoid conflicts with other Python packages installed in the virtual
        environment, the following naming should be used.

        * The name of the Mxn packages should always start with *mxn*. For
          example, *mxntodo* or *mxnchat*.

        * The name of the Mxxn framework package is *mxxn*.
"""
from pkg_resources import iter_entry_points
from typing import List, TypedDict, Type, Optional
from importlib import import_module
from importlib.metadata import metadata, requires, PackageNotFoundError
import re
from pathlib import Path
from mxxn.exceptions import env as env_ex
from mxxn.settings import Settings
from mxxn import config


def is_develop() -> bool:
    """
    Is the extra_require develop installed in environment.

    Returns:
        Returns True if installed, otherwise returns False.
    """
    requirenments = requires('mxxn')

    if not requirenments:
        return False

    requirenments_develop = [
        x.split(';')[0] for x in requirenments if 'extra == "develop"' in x]

    if not requirenments_develop:
        return False

    try:
        for package in requirenments_develop:
            matches = re.split(r'[^a-zA-Z0-9_-]+', package)

            if not matches:
                return False

            metadata(matches[0])

    except PackageNotFoundError:
        return False

    return True


def mxns(settings: Optional[Settings] = None) -> List[str]:
    """
    Get a list of the installed mixins.

    The function considers the enabled_mxns entry in the settings
    file. If it is not included, all installed mixins are returned,
    otherwise only the enabled mxns are given back. If the list
    in the settings file is empty, no installed mxn is returned.

    Args:
        settings: The application settings.

    Returns:
        list: A list of the names of the installed mxns.

    Raises:
        mxxn.exceptions.env.MxnNotExistError: If mixin from enabled_mxns
            section of settings file does not exist.
    """
    installed_mxns = [
        item.name for item in iter_entry_points(group='mxxn_mxn')]

    if settings:
        if isinstance(settings.enabled_mxns, list):
            if all(
                item in installed_mxns for item in settings.enabled_mxns
            ):
                return settings.enabled_mxns

            raise env_ex.MxnNotExistError(
                'The key enabled_mxns in the settings file '
                'contains mixins that are not installed.'
            )

    return installed_mxns


class TypeRoute(TypedDict):
    """The type definition of routes dict."""

    url: str
    resource: Type
    suffix: str


TypeRoutes = List[TypeRoute]
"""The type definition of list of route dicts."""


class TypeResource(TypedDict):
    """The type definition of resource dict."""

    resource: Type
    routes: list[list[str]]


TypeResources = List[TypeResource]
"""The type definition of lsit on resource dicts."""


class Base():
    """
    The base class of all framework packages.

    This class offers methods with which elements of the framework
    packages can be accessed.
    """

    __slots__ = ['_package']

    def __init__(self, name: str) -> None:
        """
        Initialize an object of the PackageBase class.

        Args:
            name: The name of the Python package.

        """
        try:
            self._package = import_module(name)
        except ModuleNotFoundError:
            raise env_ex.PackageNotExistError(
                    f'The environment Package {name} does not exist')

    @property
    def name(self) -> str:
        """Get the package name."""
        return self._package.__name__

    @property
    def path(self) -> Path:
        """Get the package path."""
        return Path(self._package.__path__[0])

    @property
    def configs_path(self) -> Optional[Path]:
        """
        Get the configs path of the package.

        The config path is always the config folder in the root of
        the package.

        Returns:
            Returns the config path if it exists, otherwise returns None.

        """
        path = self.path/'configs'

        if path.is_dir():
            return path

        return None

    @property
    def themes_path(self) -> Optional[Path]:
        """
        Get the themes path of the package.

        The themes path is always the themes folder in the config path of
        the package.

        Returns:
            Returns the themes path if it exists, otherwise returns None.

        """
        if self.configs_path:
            path = self.configs_path/'themes'

            if path.is_dir():
                return path

        return None

    @property
    def strings_path(self) -> Optional[Path]:
        """
        Get the strings path of the package.

        The strings path is always the strings folder in the config path of
        the package.

        Returns:
            Returns the strings path if it exists, otherwise returns None.

        """
        if self.configs_path:
            path = self.configs_path/'strings'

            if path.is_dir():
                return path

        return None

    @property
    def routes(self) -> Optional[TypeRoutes]:
        """
        Get the routes of the package.

        The routes of the package must be defined in the *routes* variable
        of the *routes* modules. They must be defined as a list of
        dictionaries. Each dictionary corresponds to a route and contains
        the URL, the resource and, if available, the respective suffix of
        the resource.

        .. code:: python

            from mxxn.resources import Root, SomeResource

            routes = [
                    {'url': '/', 'resource': Root},
                    {'url': '/some_route', 'resource': SomeResource},
                    {'url': '/some_route/{id}', 'resource': SomeResource},
                    {
                        'url': '/some_route/suffix',
                        'resource': SomeResource},
                        'suffix': 'suffix'
                    }]
        """
        try:
            routes_module = import_module(self.name + '.routes')

            return routes_module.ROUTES

        except (ModuleNotFoundError, AttributeError):
            return None

    @property
    def static_path(self) -> Optional[Path]:
        """
        Get the path to the static folder of the package.

        If a framework package contains the folder *frontend/static*,
        the path to this folder is returned. If the folder does not
        exist, the function returns None.

        Return:
            The the absolute path, if it exists,
            otherwise None.

        """
        static_path = Path(self.path/'frontend/static')

        if static_path.is_dir():
            return static_path

        return None

    @property
    def static_files(self) -> Optional[list[Path]]:
        """
        Get a list of all files in the static folder recursively.

        If a framework package contains the folder *frontend/static*,
        all contained files and those of the subfolders are returned.
        If the static folder does not exist, the function returns None.

        Return:
            The the absolute path, if it exists,
            otherwise None.

        """
        static_path = self.static_path

        if static_path:
            return [f for f in static_path.glob('**/*') if f.is_file()]

        return None

    @property
    def js_files(self) -> List[Path]:
        """
        Get the static JavaScript files, if they exist in the package.

        Return:
            A list of absolute paths starting in, if it exists,
            otherwise a empty list.

        """
        static_path = self.static_path

        if static_path:
            js_path = static_path/'js'

            if js_path.is_dir():
                js_files = list(js_path.rglob('**/*.js'))

                for i in range(len(js_files)):
                    js_files[i] = js_files[i].relative_to(js_path)

                return js_files

        return []

    @property
    def theme(self) -> Optional[config.Config]:
        """
        Get an instance of the Theme config for this package.

        Returns:
            Returns instance of Theme config class if it exists,
                otherwise returns None.
        """
        if self.themes_path:
            return config.Config(self.themes_path)

        return None


class Mxxn(Base):
    """With this class elements of the Mxxn framework can be accessed."""

    def __init__(self, name: str = 'mxxn') -> None:
        """
        Initialize the Package class.

        Args:
            name: A optional name of the Mxxn package.
        """
        super().__init__(name)

    @property
    def theme_list(self) -> Optional[List[str]]:
        """Get a list of available themes."""
        if self.themes_path:
            themes_dir = config.Config(self.themes_path)
            return themes_dir.names

        return None


class Mxn(Base):
    """With this class elements of a Mxn package can be accessed."""

    @property
    def unprefixed_name(self) -> str:
        """Get the name without prefix *mxn*."""
        name = self.name
        prefix = 'mxn'

        if name.startswith(prefix):
            return name.replace(prefix, '', 1)

        return self.name


class TypeRouteCovers(TypedDict):
    """Type definition for the route covers dict."""

    mxxn: list[TypeRoute]
    mxns: dict[str, list[TypeRoute]]


class TypeStaticFileCovers(TypedDict):
    """Type definition for the static file covers dict."""

    mxxn: list[Path]
    mxns: dict[str, list[Path]]


class MxnApp(Base):
    """
    With this class elements of a MxnApp package can be accessed.

    Application developers can overwrite almost all elements of the Mxns or
    the Mxxn framework. This can include resources, static files, etc. For
    this purpose, the covers package must be created in the application
    package. All overloads of the Mxxn framework are in the sub-package
    mxxn, those of the Mxns are in the sub-folder mxns. A sub-package
    must exist for each Mxn for which elements will be overloaded.
    The folder structure of the overloads is exactly the same as in the
    package that is to be overloaded.

    Here is the folder structure of an exemplary application that overloads
    the resources of the framework and a Mxn:

    .. code-block:: bash

        mxnapp
        |-- covers
        |   |-- __init__.py
        |   |-- mxns
        |   |   |-- __init__.py
        |   |   |-- mxntest
        |   |   |   |-- __init__.py
        |   |   |   |-- routes.py
        |   |   |   |-- resources.py
        |   |-- mxxn
        |   |   |-- __init__.py
        |   |   |-- routes.py
        |   |   |-- resources.py
        |-- __init__.py
        setup.cfg
    """

    def __init__(self) -> None:
        """Initialize the MixxinApp class."""
        installed_apps = [
            item.name for item in iter_entry_points(group='mxxn_mxnapp')]

        if installed_apps:
            if len(installed_apps) > 1:
                raise env_ex.MultipleMxnAppsError(
                        'Multiple application packages installed.')

            super().__init__(installed_apps[0])

            return

        raise env_ex.MxnAppNotExistError('No application package installed')

    def route_covers(self, settings: Settings) -> TypeRouteCovers:
        """
        Get the route covers.

        It is possible to overload the routes of a package with new resources.
        To do this, there must be a routes.py module with the routes to the
        new resources in the covers folder of the respective package. These
        routes then overload the original routes of the package with the new
        resources.

        The following listing shows the format of the returned dictionary.

        .. code:: python

            {
                'mxxn': [
                    {'url': '<url_to_cover>', 'resource': '<new_resource>'}
                ],
                'mxns': {
                    'mxnone': [
                        {'url': '<url_to_cover>', 'resource': '<new_resource>'}
                    ],
                    'mxntwo': [
                        {
                            'url': '<url_to_cover>',
                            'resource': '<new_resource>',
                            'suffix': 'some_suffix'}
                    ]
                }
            }


        Returns:
            A dictionary containing the routes covers.

        """
        resource_covers: TypeRouteCovers = {
            'mxxn': [],
            'mxns': {}
            }

        try:
            mxxn_covers = Mxxn(self.name + '.covers.mxxn')

            if mxxn_covers.routes:
                resource_covers['mxxn'] = mxxn_covers.routes

        except env_ex.PackageNotExistError:
            pass

        for mxn_name in mxns(settings):
            try:
                mxn = Mxn(self.name + '.covers.mxns.' + mxn_name)

                if mxn.routes:
                    resource_covers['mxns'][mxn_name] = mxn.routes

            except env_ex.PackageNotExistError:
                pass

        return resource_covers

    def static_file_covers(self, settings: Settings) -> TypeStaticFileCovers:
        """
        Get the static file covers.

        It is possible to overload the static files of a package with new
        static files. This function returns a list of overloaded files for
        each package. The files are passed as a path relative to the
        package's static folder.

        The following listing shows the format of the returned dictionary.

        .. code:: python

            {
                'mxxn': [<list of pathes>],
                'mxns': {
                    'mxnone': [<list of pathes>],
                    'mxntwo': [<list of pathes>]
                }
            }


        Returns:
            A dictionary containing the lists of static file covers.

        """
        covers: TypeStaticFileCovers = {
            'mxxn': [],
            'mxns': {}
            }

        try:
            mxxn_covers = Mxxn(self.name + '.covers.mxxn')
            static_files = mxxn_covers.static_files
            static_path = mxxn_covers.static_path

            if static_files and static_path:
                for i, file in enumerate(static_files):
                    static_files[i] = file.relative_to(static_path)

                covers['mxxn'] = static_files

        except env_ex.PackageNotExistError:
            pass

        for mxn_name in mxns(settings):
            try:
                mxn_covers = Mxn(self.name + '.covers.mxns.' + mxn_name)
                static_files = mxn_covers.static_files
                static_path = mxn_covers.static_path

                if static_files and static_path:
                    for i, file in enumerate(static_files):
                        static_files[i] = file.relative_to(static_path)

                    covers['mxns'][mxn_name] = static_files

            except env_ex.PackageNotExistError:
                pass

        return covers
