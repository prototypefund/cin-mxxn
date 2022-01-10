"""
Module for using components of the mixxin environment.

The mixxin environment has the three basic package types
mixxin, mixins and app. These packages have essentially
the same structure. On the basis of this structure, when the
application starts, elements are automatically loaded from
the packages and registered in the framework.
"""
from pkg_resources import iter_entry_points
from typing import List, TypedDict, Type, Dict
import inspect
from importlib.util import find_spec
from importlib import import_module
import re
from mxxn.exceptions import env as env_ex
from mxxn.utils import modules
from mxxn.settings import Settings


def mixins(settings: Settings) -> List[str]:
    """
    Get a list of the installed mixins.

    The function considers the enabled_mixins entry in the settings
    file. If it is not included, all installed mixins are returned,
    otherwise only the enabled mixins are given back. If the list
    in the settings file is empty, no installed mixin is returned.

    Returns:
        list: A list of the names of the installed mixins.

    """
    installed_mixins = [
        item.name for item in iter_entry_points(group='mixxin_mixins')]

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


class Package(object):
    """
    The base class of all framework packages.

    This class offers methods with which elements of the framework
    packages can be accessed.
    """

    __slots__ = ['_package']

    def __init__(self, name: str) -> None:
        """
        Initialize an object of the Package class.

        Args:
            name (string): The name of the package.

        """
        try:
            self._package = import_module(name)
        except ModuleNotFoundError:
            raise env_ex.PackageNotExistError(
                    'The environment Package {} does not exist'
                    .format(name))

    @property
    def name(self):
        return self._package.__name__
