"""
Module for using components of the mixxin environment.

Mixxin applications are always based on a Python virtual environment.
A separate environment must be used for each application, because
only one MixxinApp package is accepted per environment.

The mixxin environment has the three basic package types
Mixxin, Mixin and MixxinApp. The Mixxin package it self is the
framework package containing the framework functionality.
Mixins are plugins that can be installed in the environment and
automatically detected by the framework. These plugins extend
the functionality of the application. The MixxinApp brings together
all the required Mixins and the Mixxin framework and packages it.
In addition, overloads for components of the Mixins and for the
framework can be defined in the MixxinApp.
For package management the setuptools are used. Each Mixxin package
is standalone Python package and can be installed into the environment
using pip. However, it is recommended to manage the dependence on
other Mixxin packages in the setup file of the MixxinApp package.

All three package types have essentially the same structure. On the
basis of this structure, when the application starts, elements are
automatically loaded from the packages and registered in the framework.

.. warning::
    To avoid conflicts with other Python packages installed in the virtual
    environment, the following naming should be used.

    * The name of the Mixin packages should always start with *mxn*. For
      example, *mxntodo* or *mxnchat*.

    * The name of the Mixxin framework package is *mxxn*.

    * All MixxinApp packages should always start with *mxxn* (e.g. *mxxnapp*).
"""
from pkg_resources import iter_entry_points
from typing import List, TypedDict, Type, Dict,Optional
import inspect
from importlib import import_module
import re
from pathlib import Path
from mxxn.exceptions import env as env_ex
from mxxn.utils import modules
from mxxn.settings import Settings


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
        item.name for item in iter_entry_points(group='mxxn_mixin')]

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


class TypeResourceDict(TypedDict):
    """The type definition of resource dict."""

    resource: Type
    routes: List[List[str]]


TypeListOfResourceDicts = List[TypeResourceDict]
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
                    'The environment Package {} does not exist'
                    .format(name))

    @property
    def name(self) -> str:
        """Get the package name."""
        return self._package.__name__

    @property
    def path(self) -> str:
        """Get the package path."""
        return Path(self._package.__path__[0])

    @property
    def resources(self) -> TypeListOfResourceDicts:
        """
        Get the resources of the package.

        This method searches the *resources* module or package of the Mxxn
        package, Mxn package or a MxnApp package for resources and returns
        a list of the resources found. If no resource exists or there is no
        resources module or package, then an empty list is returned. A
        resource is a class that implements at least one responder method of
        the form *on_*()*, where * is any one of the standard HTTP methods
        (get, post, put, delete, patch, websocket). Classes that exclusively or
        additionally implement methods with a suffix in the form
        *on_*_<suffix>* are also identified as a resource and the
        suffixes are returned with it. The returned list contains resource
        dictionaries. A dictionary has the following format:

        .. code-block:: python

            {
                'resource': <resource class>,
                'routes': [
                    [<route 1>, <optional suffix>],
                    [<route n>, <optional suffix>],
                ]
            }

        .. note::

            Only resources with get, post, put, patch, delete or/and websocket
            responder are considered.
        """
        try:
            resources_list: TypeListOfResourceDicts = []

            resources_module = import_module(
                    self._package.__name__ + '.resources')

            classes = modules.classes_recursively(resources_module)

            for resource in classes:
                members = inspect.getmembers(
                    resource, predicate=inspect.isfunction
                )
                member_names = [member[0] for member in members]
                r = 'on_(get|post|put|delete|patch|websocket)'

                has_responder = any(
                    i for i in member_names if re.match(r+'$', i)
                )

                suffixes: List[str] = []

                for i in member_names:
                    if re.match(r + '_[a-z0-9_]+', i):
                        suffixes.append(re.sub(r+'_', '', i))

                import_name = resource.__module__+'.'+resource.__name__

                if has_responder or suffixes:
                    route = re.sub(
                            '^'+resources_module.__name__, '', import_name)\
                            .replace('.', '/').lower()

                    route = route[::-1].replace('/', './', 1)[::-1]

                    resource_dict: TypeResourceDict = {
                        'resource': resource,
                        'routes': []
                    }

                    if has_responder:
                        resource_dict['routes'].append([route])

                    if suffixes:
                        for suffix in suffixes:
                            resource_dict['routes'].append(
                                [route+'.'+suffix, suffix]
                            )

                    resources_list.append(resource_dict)

        except ModuleNotFoundError:
            pass

        return resources_list

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
    def js_files(self) -> List[Path]:
        """
        Get the static JavaScript files, if they exist in the package.

        Return:
            A list of absolute paths starting in, if it exists,
            otherwise a empty list.

        """
        static_path = self.static_path

        if static_path:
            js_files = list(static_path.rglob('**/*.js'))

            for i in range(len(js_files)):
                js_files[i] = js_files[i].relative_to(static_path)

            return js_files

        return []


class Mxxn(Base):
    """With this class elements of the Mxxn framework can be accessed."""

    def __init__(self, name: str = 'mxxn') -> None:
        """
        Initialize the Package class.

        Args:
            name: A optional name of the Mxxn package.
        """
        super().__init__(name)


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


class TypeCoveringResources(TypedDict):
    mixxin: TypeListOfResourceDicts
    mixins: Dict[str, TypeListOfResourceDicts]


class MxnApp(Base):
    """
    With this class elements of a MxnApp package can be accessed.

    Application developers can overwrite almost all elements of the Mxns or
    the Mxxn framework. This can include resources, static files, etc. For
    this purpose, the covers package must be created in the application
    package. All overloads of the Mxxn framework are in the sub-package
    mxxn, those of the mxns are in the sub-folder mxns. A sub-package
    must exist for each mxn for which elements will be overloaded.
    The folder structure of the overloads is exactly the same as in the
    package that is to be overloaded.

    Here is the folder structure of an exemplary application that overloads
    the resources of the framework and a Mxn:

    . code-block:: bash
        mxxnapp
        |-- covers
        |   |-- __init__.py
        |   |-- mxns
        |   |   |-- __init__.py
        |   |   |-- mxntest
        |   |       |-- __init__.py
        |   |       |-- resources.py
        |   |
        |   |-- mxxn
        |   |   |-- __init__.py
        |   |   |-- resources.py
        |-- __init__.py
        setup.cfg
    """
    def __init__(self) -> None:
        """Initialize the MixxinApp class."""
        installed_apps = [
            item.name for item in iter_entry_points(group='mxxn_app')]

        if installed_apps:
            if len(installed_apps) > 1:
                raise env_ex.MultipleMxnAppsError(
                        'Multiple application packages installed.')

            super().__init__(installed_apps[0])

            return

        raise env_ex.MxnAppNotExistError('No application package installed')

    def covering_resources(self, settings: Settings) -> TypeCoveringResources:
        """
        Get the resource covers.

        To overload a resource, the respective resource module must be created
        in the package to be overloaded and the corresponding resource class
        must be created in it. If only one or a few responders are to be
        overloaded, then the resource class can be derived from the original
        resource and the particular responder or responders can be overloaded.

        Returns:
            A dictionary containing the covering resources.

        """
        resource_covers: TypeCoveringResources = {
            'mxxn': [],
            'mxns': {}
        }

        try:
            mxxn_covers = Mxxn(self.name + '.covers.mxxn')
            resource_covers['mxxn'] = mxxn_covers.resources

        except env_ex.PackageNotExistError:
            pass

        for mxn_name in mxns(settings):
            try:
                mxn = Mxn(self.name + '.covers.mxns.' + mxn_name)
                resource_covers['mxns'][mxn_name] = mxn.resources

            except env_ex.PackageNotExistError:
                pass

        return resource_covers
