from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import getitem
from typing import Any, Dict, List, Mapping, Optional, Union

import h5py
import lxml.etree as ET
import numpy as np

from pynxtools.dataconverter.helpers import (
    Collector,
    ValidationProblem,
    is_valid_data_field,
)
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
    # Based on https://stackoverflow.com/questions/50607128/creating-a-nested-dictionary-from-a-flattened-dictionary
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
        _, *keys, final_key = k.replace("/@", "@").split("/")
        get_from(data_tree, keys)[final_key] = v

    return default_to_regular_dict(data_tree)


def validate_dict_against(appdef: str, mapping: Mapping[str, Any]) -> bool:
    def get_variations_of(node: NexusNode, keys: Mapping[str, Any]) -> List[str]:
        if not node.variadic and node.name in keys:
            return [node.name]

        variations = []
        for key in keys:
            if get_nx_namefit(key, node.name) >= 0 and key not in [
                x.name for x in node.parent.children
            ]:
                variations.append(key)
        return variations

    def handle_group(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        variants = get_variations_of(node, keys)
        if not variants:
            if node.optionality == "required" and node.type in missing_type_err:
                collector.collect_and_log(
                    f"{prev_path}/{node.name}", missing_type_err.get(node.type), None
                )
            return
        for variant in variants:
            if not isinstance(keys[variant], Mapping):
                collector.collect_and_log(
                    f"{prev_path}/{variant}", ValidationProblem.ExpectedGroup, None
                )
                return
            recurse_tree(node, keys[variant], prev_path=f"{prev_path}/{variant}")

    def remove_from_not_visited(path: str) -> str:
        if path in not_visited:
            not_visited.remove(path)
        return path

    def handle_field(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        full_path = remove_from_not_visited(f"{prev_path}/{node.name}")
        variants = get_variations_of(node, keys)
        if not variants:
            if node.optionality == "required" and node.type in missing_type_err:
                collector.collect_and_log(
                    full_path, missing_type_err.get(node.type), None
                )
            return

        for variant in variants:
            is_valid_data_field(
                mapping[f"{prev_path}/{variant}"], node.dtype, f"{prev_path}/{variant}"
            )
            if node.unit is not None:
                remove_from_not_visited(f"{prev_path}/{variant}/@units")
                if f"{variant}@units" not in keys:
                    collector.collect_and_log(
                        f"{prev_path}/{variant}",
                        ValidationProblem.MissingUnit,
                        node.unit,
                    )
                # TODO: Check unit

        # TODO: Build variadic map for fields and attributes
        # Introduce variadic siblings in NexusNode?

    def handle_attribute(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        full_path = f"{prev_path}/@{node.name}"
        if full_path in not_visited:
            not_visited.remove(full_path)
        if node.name not in keys:
            collector.collect_and_log(full_path, missing_type_err.get(node.type), None)

        # TODO: Check variants

    def handle_choice(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        # TODO: Implement this
        pass

    def handle_unknown_type(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        # This should normally not happen if
        # the handling map includes all types allowed in NexusNode.type
        # Still, it's good to have a fallback
        # TODO: Raise error or log the issue?
        pass

    def recurse_tree(node: NexusNode, keys: Mapping[str, Any], prev_path: str = ""):
        for child in node.children:
            handling_map.get(child.type, handle_unknown_type)(child, keys, prev_path)

    missing_type_err = {
        "field": ValidationProblem.MissingRequiredField,
        "group": ValidationProblem.MissingRequiredGroup,
        "attribute": ValidationProblem.MissingRequiredAttribute,
    }

    handling_map = {
        "group": handle_group,
        "field": handle_field,
        "attribute": handle_attribute,
        "choice": handle_choice,
    }

    tree = generate_tree_from(appdef)
    collector.clear()
    not_visited = list(mapping)
    nested_keys = build_tree_from(mapping)
    recurse_tree(tree, nested_keys)

    for not_visited_key in not_visited:
        if not_visited_key.endswith("/@units"):
            collector.collect_and_log(
                not_visited_key,
                ValidationProblem.UnitWithoutDocumentation,
                mapping[not_visited_key],
            )
        else:
            collector.collect_and_log(
                not_visited_key, ValidationProblem.MissingDocumentation, None
            )

    return not collector.has_validation_problems()
