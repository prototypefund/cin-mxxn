"""This module provides tools for working with modules."""
import pkgutil
import importlib
import inspect
from typing import List, Type


def submodules(module_name: str, modules: List[str]) -> None:
    """
    Get all submodules of a module.

    The function searches the given module recursively,
    including subpackages.

    Args:
        module_name: The name of the module.
        modules: The list in which the found modules are stored.

    Raises:
        ModuleNotFoundError: If the given module does not exist.
    """
    try:
        module = importlib.import_module(module_name)
        submodules_list = list(
            pkgutil.iter_modules(module.__path__)  # type: ignore
        )

    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            'The module {} for which the submodules are searched does '
            'not exist.'.format(module_name)
        ) from e

    except AttributeError:
        return

    for submodule in submodules_list:
        name = module_name + '.' + submodule.name
        if submodule.ispkg:
            submodules(name, modules)
            modules.append(name)
        else:
            modules.append(name)


def classes(module) -> List[Type]:
    """
    Get all classes of a module.

    Args:
        module_name: The name of the module.

    Return:
        A list of classes.

    Raises:
        ModuleNotFoundError: If the passed module does not exist.
    """
    classes_list = []

    for name, obj in inspect.getmembers(module, inspect.isclass):
        classes_list.append(obj)

    return classes_list


def classes_recursively(module_name: str) -> List[Type]:
    """
    Get all classes of the module and submodules recursively.

    Args:
        module_name: The name of the module.

    Return:
        A List of classes.

    Raises:
        ModuleNotFoundError: If the passed module does not exist.
    """
    submodules_list: List[str] = []
    classes_list = classes(module_name)
    submodules(module_name, submodules_list)

    for submodule in submodules_list:
        classes_list.extend(classes(submodule))

    return classes_list
