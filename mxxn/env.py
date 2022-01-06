"""
Module for using components of the mixxin environment.

The mixxin environment has the three basic package types
mixxin, mixins and app. These packages have essentially
the same structure. On the basis of this structure, when the
application starts, elements are automatically loaded from
the packages and registered in the framework.
"""
from pkg_resources import iter_entry_points
from typing import List
from mxxn.exceptions import env as env_ex
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
