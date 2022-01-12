"""This module provides tools for working with modules."""
import pkgutil
from importlib import import_module
import inspect
from typing import List, Type
from types import ModuleType


def submodules(module: ModuleType, modules: List[ModuleType]) -> None:
    """
    Get all submodules of a module.

    The function searches the given module recursively for
    submodules and adds them to the given modules list.

    Args:
        module: The modules to be searched.
        modules: The list into the found modules should be inserted.

    """
    try:
        submodules_list = list(
            pkgutil.iter_modules(module.__path__)
        )

    except AttributeError:
        return

    for submodule in submodules_list:
        name = module.__name__ + '.' + submodule.name
        imported_module = import_module(name)

        if submodule.ispkg:
            submodules(imported_module, modules)
            modules.append(imported_module)
        else:
            modules.append(imported_module)


def classes(module: ModuleType) -> List[Type]:
    """
    Get all classes of a given module.

    Args:
        module: The modules to be searched for classes.

    Return:
        A list of found classes.

    """
    classes_list = []

    for name, obj in inspect.getmembers(module, inspect.isclass):
        classes_list.append(obj)

    return classes_list


def classes_recursively(module: ModuleType) -> List[Type]:
    """
    Get all classes of the module and submodules recursively.

    Args:
        module: The modules to be searched for classes.

    Return:
        A List of found classes.

    """
    submodules_list: List[ModuleType] = []
    classes_list = classes(module)
    submodules(module, submodules_list)

    for submodule in submodules_list:
        classes_list.extend(classes(submodule))

    return classes_list
