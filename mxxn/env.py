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
from typing import List, TypedDict, Type
import inspect
from importlib import import_module
import re
from mxxn.exceptions import env as env_ex
from mxxn.utils import modules
from mxxn.settings import Settings


def mixins(settings: Optional[Settings] = None) -> List[str]:
    """
    Get a list of the installed mixins.

    The function considers the enabled_mixins entry in the settings
    file. If it is not included, all installed mixins are returned,
    otherwise only the enabled mixins are given back. If the list
    in the settings file is empty, no installed mixin is returned.

    Args:
        settings: The application settings.

    Returns:
        list: A list of the names of the installed mixins.

    Raises:
        mxxn.exceptions.env.MixinNotExistError: If mixin from enabled_mixins
            section of settings file does not exist.
    """
    installed_mixins = [
        item.name for item in iter_entry_points(group='mxxn_mixin')]

    if settings:
        if isinstance(settings.enabled_mixins, list):
            if all(
                item in installed_mixins for item in settings.enabled_mixins
            ):
                return settings.enabled_mixins

            raise env_ex.MixinNotExistError(
                'The key enabled_mixins in the settings file '
                'contains mixins that are not installed.'
            )

    return installed_mixins


class TypeResourceDict(TypedDict):
    """The type definition of resource dict."""

    resource: Type
    routes: List[List[str]]


TypeListOfResourceDicts = List[TypeResourceDict]
"""The type definition of lsit on resource dicts."""


class PackageBase():
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
    def resources(self) -> TypeListOfResourceDicts:
        """
        Get the resources of the package.

        This method searches the *resources* module or package of the Mixxin
        package, Mixin package or a MixxinApp package for resources and returns
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


class Mixxin(PackageBase):
    """With this class elements of the Mixxin framework can be accessed."""

    def __init__(self) -> None:
        """Initialize the Mixxin object."""
        super().__init__('mxxn')


class Mixin(PackageBase):
    """With this class elements of a Mixin package can be accessed."""

    pass


class MixxinApp(PackageBase):
    """With this class elements of a MixinApp package can be accessed."""

    def __init__(self) -> None:
        """Initialize the MixxinApp class."""
        installed_apps = [
            item.name for item in iter_entry_points(group='mxxn_app')]

        if installed_apps:
            if len(installed_apps) > 1:
                raise env_ex.MultipleMixxinAppsError(
                        'Multiple application packages installed.')

            super().__init__(installed_apps[0])

            return

        raise env_ex.MixxinAppNotExistError('No application package installed')
