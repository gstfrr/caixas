# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
from collections import defaultdict
from typing import Any, Set, Iterable


def get_leaves(struct: Iterable) -> Set[Any]:
    """This is an useful function to flatten dictionaries into a list. It is used to iterate over the values of the
     dictionary without using nested loops in the keys.

    :param struct: Iterable: DictionaryData: The structure to be flattened.

    """
    # Ref: https://stackoverflow.com/a/59832362/
    values = set()
    if isinstance(struct, dict):
        for sub_struct in struct.values():
            values.update(get_leaves(sub_struct))
    elif isinstance(struct, list):
        for sub_struct in struct:
            values.update(get_leaves(sub_struct))
    elif struct is not None:
        values.add(struct)
    return values


def rec_dd() -> defaultdict:
    """Useful function to create a recursive dictionary. This is useful to avoid key errors when accessing."""
    return defaultdict(rec_dd)


class DataDictionary(defaultdict):
    """All the dictionaries in the project are stores in this class. It provides the values() method that
    returns a flatten list of the dictionary. The flatten list can be used to direct iteration
    instead of using nested loops.


    """

    def __init__(self) -> None:
        super().__init__()
        self.default_factory = rec_dd

    def final_values(self) -> Set[Any]:
        """ """
        return get_leaves(self)  # Flattening available to avoid huge nested loops
