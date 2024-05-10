#
# Copyright The pynxtools Authors.
#
# This file is part of pynxtools.
# See https://github.com/FAIRmat-NFDI/pynxtools for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import defaultdict
from functools import reduce
from operator import getitem
from typing import Any, Iterable, List, Mapping, Optional, Tuple, Union

import h5py
from anytree import Resolver

from pynxtools.dataconverter.helpers import (
    Collector,
    ValidationProblem,
    collector,
    convert_data_dict_path_to_hdf5_path,
    is_valid_data_field,
)
from pynxtools.dataconverter.nexus_tree import NexusNode, generate_tree_from
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nx_namefit


def validate_hdf_group_against(appdef: str, data: h5py.Group):
    """
    Checks whether all the required paths from the template are returned in data dict.

    THIS IS JUST A FUNCTION SKELETON AND IS NOT WORKING YET!
    """

    def validate(name: str, data: Union[h5py.Group, h5py.Dataset]):
        # Namefit name against tree (use recursive caching)
        pass

    tree = generate_tree_from(appdef)
    data.visitems(validate)


def build_nested_dict_from(
    mapping: Mapping[str, Any],
) -> Tuple[Mapping[str, Any], Mapping[str, Any]]:
    """
    Creates a nested mapping from a `/` separated flat mapping.
    It also converts data dict paths to HDF5 paths, i.e.,
    it converts the path `/ENTRY[my_entry]/TEST[test]` to `/my_entry/test`.

    Args:
        mapping (Mapping[str, Any]):
            The mapping to nest.

    Returns:
        Tuple[Mapping[str, Any], Mapping[str, Any]]:
            First element is the nested mapping.
            Second element is the original dict in hdf5 path notation.
    """

    # Based on
    # https://stackoverflow.com/questions/50607128/creating-a-nested-dictionary-from-a-flattened-dictionary
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
    hdf_path_mapping = {}
    for k, v in mapping.items():
        hdf_path_mapping[convert_data_dict_path_to_hdf5_path(k)] = v
        _, *keys, final_key = (
            convert_data_dict_path_to_hdf5_path(k).replace("/@", "@").split("/")
            if not k.startswith("/@")
            else k.split("/")
        )
        get_from(data_tree, keys)[final_key] = v

    return default_to_regular_dict(data_tree), hdf_path_mapping


def best_namefit_of(name: str, keys: Iterable[str]) -> Optional[str]:
    """
    Get the best namefit of `name` in `keys`.

    Args:
        name (str): The name to fit against the keys.
        keys (Iterable[str]): The keys to fit `name` against.

    Returns:
        Optional[str]: The best fitting key. None if no fit was found.
    """
    if name in keys:
        return name

    best_match, score = max(
        map(lambda x: (x, get_nx_namefit(name, x)), keys), key=lambda x: x[1]
    )
    if score < 0:
        return None

    return best_match


def validate_dict_against(
    appdef: str, mapping: Mapping[str, Any], ignore_undocumented: bool = False
) -> bool:
    """
    Validates a mapping against the NeXus tree for applicationd definition `appdef`.

    Args:
        appdef (str): The appdef name to validate against.
        mapping (Mapping[str, Any]):
            The mapping containing the data to validate.
            This should be a dict of `/` separated paths.
            Attributes are denoted with `@` in front of the last element.
        ignore_undocumented (bool, optional):
            Ignore all undocumented keys in the verification
            and just check if the required fields are properly set.
            Defaults to False.

    Returns:
        bool: True if the mapping is valid according to `appdef`, False otherwise.
    """

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

    def get_field_attributes(name: str, keys: Mapping[str, Any]) -> Mapping[str, Any]:
        return {k.split("@")[1]: keys[k] for k in keys if k.startswith(f"{name}@")}

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
            if (
                node.items is not None
                and mapping[f"{prev_path}/{variant}"] not in node.items
            ):
                collector.collect_and_log(
                    f"{prev_path}/{variant}",
                    ValidationProblem.InvalidEnum,
                    node.items,
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

            recurse_tree(
                node,
                get_field_attributes(variant, keys),
                prev_path=f"{prev_path}/{variant}",
            )

        # TODO: Build variadic map for fields and attributes
        # Introduce variadic siblings in NexusNode?

    def handle_attribute(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        full_path = remove_from_not_visited(f"{prev_path}/@{node.name}")
        variants = get_variations_of(node, keys)
        if not variants:
            if node.optionality == "required" and node.type in missing_type_err:
                collector.collect_and_log(
                    full_path, missing_type_err.get(node.type), None
                )
            return

        for variant in variants:
            is_valid_data_field(
                mapping[f"{prev_path}/@{variant}"],
                node.dtype,
                f"{prev_path}/@{variant}",
            )

    def handle_choice(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        global collector
        old_collector = collector
        collector = Collector()
        collector.logging = False
        for child in node.children:
            collector.clear()
            child.name = node.name
            handle_group(child, keys, prev_path)

            if not collector.has_validation_problems():
                collector = old_collector
                return

        collector = old_collector
        collector.collect_and_log(
            f"{prev_path}/{node.name}", ValidationProblem.ChoiceValidationError, None
        )

    def handle_unknown_type(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        # This should normally not happen if
        # the handling map includes all types allowed in NexusNode.type
        # Still, it's good to have a fallback
        # TODO: Raise error or log the issue?
        pass

    def is_documented(key: str, node: NexusNode) -> bool:
        for name in key[1:].replace("@", "").split("/"):
            children = node.get_all_children_names()
            best_name = best_namefit_of(name, children)
            if best_name is None:
                return False
            if best_name not in node.get_all_children_names(depth=1):
                node = node.add_inherited_node(best_name)
            else:
                resolver = Resolver("name")
                node = resolver.get(node, best_name)

        if "@" not in key and node.type != "field":
            return False
        if "@" in key and node.type != "attribute":
            return False

        return is_valid_data_field(mapping[key], node.dtype, key)

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
    nested_keys, mapping = build_nested_dict_from(mapping)
    not_visited = list(mapping)
    recurse_tree(tree, nested_keys)

    if ignore_undocumented:
        return not collector.has_validation_problems()

    for not_visited_key in not_visited:
        if is_documented(not_visited_key, tree):
            continue
        if not_visited_key.endswith("/@units"):
            if not_visited_key.rsplit("/", 1)[0] not in not_visited:
                collector.collect_and_log(
                    not_visited_key,
                    ValidationProblem.UnitWithoutField,
                    not_visited_key.rsplit("/", 1)[0],
                )
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
