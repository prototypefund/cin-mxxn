"""This module contains helper functions for dictionary handling."""


def merge(base_dict: dict, merge_dict: dict) -> None:
    """
    Merge the a dictionary into the base dictionary.

    The values are only updated if they are in the
    base dictionary.

    Args:
        base_dict: The Basic Dictionary to be merged into.
        merge_dict: The dictionary to be merged.

    """
    for key, value in merge_dict.items():
        if key in base_dict:
            if not isinstance(base_dict[key], dict):
                base_dict[key] = merge_dict[key]
            else:
                merge(base_dict[key], merge_dict[key])
