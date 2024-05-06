from collections import defaultdict
from functools import reduce
from operator import getitem
from typing import Any, Dict, List, Mapping, Union

import h5py
import lxml.etree as ET

from pynxtools.dataconverter.helpers import Collector
from pynxtools.dataconverter.nexus_tree import NexusNode, generate_tree_from
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nx_namefit

collector = Collector()


def validate_hdf_group_against(appdef: str, data: h5py.Group):
    """Checks whether all the required paths from the template are returned in data dict."""

    def validate(name: str, data: Union[h5py.Group, h5py.Dataset]):
        # Namefit name against tree (use recursive caching)
        pass

    tree = generate_tree_from(appdef)
    data.visitems(validate)


def build_tree_from(mapping: Mapping[str, Any]) -> Mapping[str, Any]:
    def get_from(data_tree, map_list):
        """Iterate nested dictionary"""
        return reduce(getitem, map_list, data_tree)

    # instantiate nested defaultdict of defaultdicts
    def tree():
        return defaultdict(tree)

    def default_to_regular_dict(d):
        """Convert nested defaultdict to regular dict of dicts."""
        if isinstance(d, defaultdict):
            d = {k: default_to_regular_dict(v) for k, v in d.items()}
        return d

    data_tree = tree()

    # iterate input dictionary
    for k, v in mapping.items():
        _, *keys, final_key = k.split("/")
        get_from(data_tree, keys)[final_key] = v

    return default_to_regular_dict(data_tree)


def validate_dict_against(appdef: str, mapping: Mapping[str, Any]) -> bool:
    tree = generate_tree_from(appdef)
    collector.clear()
    nested_keys = build_tree_from(mapping)

    def recurse_tree(node: NexusNode, keys: Dict[str, Any]):
        for key in keys:
            namefit = None
            for child in node.children:
                if child.name == key:
                    pass
                if child.variadic and get_nx_namefit(key, child.name) >= 0:
                    namefit = child
                    break
            if namefit is not None and isinstance(keys[key], dict):
                recurse_tree(namefit, keys[key])

    print(nested_keys)
    for key in nested_keys:
        for child in tree.children:
            if get_nx_namefit(key, child.name) >= 0:
                print("We fit!")
                pass
            print(key)
            print(child)

    return not collector.has_validation_problems()
