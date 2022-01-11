"""This module provides tools for working with modules."""
import pkgutil
from importlib import import_module
import inspect
from typing import List, Type


def submodules(module, modules: List[str]) -> None:
    """
    Get all submodules of a module.

    The function searches the given module recursively,
    including subpackages.

    Args:
        module_name: The module.
        modules: The list in which the found modules are stored.

    """
    submodules_list = list(
        pkgutil.iter_modules(module.__path__)  # type: ignore
    )

    for submodule in submodules_list:
        name = module.__name__ + '.' + submodule.name
        imported_module = import_module(name)

        if submodule.ispkg:
            submodules(imported_module, modules)
            modules.append(imported_module)
        else:
            modules.append(imported_module)


def classes(module) -> List[Type]:
    """
    Get all classes of a module.

    Args:
        module: The name of the module.

    Return:
        A list of classes.

    Raises:
        ModuleNotFoundError: If the passed module does not exist.
    """
    classes_list = []

    for name, obj in inspect.getmembers(module, inspect.isclass):
        classes_list.append(obj)

    return classes_list


def classes_recursively(module) -> List[Type]:
    """
    Get all classes of the module and submodules recursively.

    Args:
        module: The name of the module.

    Return:
        A List of classes.

    Raises:
        ModuleNotFoundError: If the passed module does not exist.
    """
    submodules_list: List[str] = []
    classes_list = classes(module)
    submodules(module, submodules_list)

    for submodule in submodules_list:
        classes_list.extend(classes(submodule))

    return classes_list
