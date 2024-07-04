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
import re
from collections import defaultdict
from functools import reduce
from operator import getitem
from typing import Any, Iterable, List, Mapping, Optional, Tuple, Union

import h5py
import lxml.etree as ET
import numpy as np

from pynxtools.dataconverter.helpers import (
    Collector,
    ValidationProblem,
    collector,
    convert_nexus_to_caps,
    is_valid_data_field,
)
from pynxtools.dataconverter.nexus_tree import (
    NexusEntity,
    NexusGroup,
    NexusNode,
    generate_tree_from,
)
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
) -> Mapping[str, Any]:
    """
    Creates a nested mapping from a `/` separated flat mapping.

    Args:
        mapping (Mapping[str, Any]):
            The mapping to nest.

    Returns:
        Mapping[str, Any]: The nested mapping.
    """

    # Based on
    # https://stackoverflow.com/questions/50607128/
    # creating-a-nested-dictionary-from-a-flattened-dictionary
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
        if v is None:
            continue
        _, *keys, final_key = k.split("/")
        # if final_key.startswith("@") and "/" + "/".join(keys) not in mapping:
        # Don't add attributes if the field is not present
        # continue
        data = get_from(data_tree, keys)
        if not isinstance(data, defaultdict):
            # Deal with attributes for fields
            # Store them in a new key with the name `field_name@attribute_name``
            get_from(data_tree, keys[:-1])[f"{keys[-1]}{final_key}"] = v
        else:
            data[final_key] = v

    return default_to_regular_dict(data_tree)


def split_class_and_name_of(name: str) -> Tuple[Optional[str], str]:
    """
    Return the class and the name of a data dict entry of the form
    `get_class_of("ENTRY[entry]")`, which will return `("ENTRY", "entry")`.
    If this is a simple string it will just return this string, i.e.
    `get_class_of("entry")` will return `None, "entry"`.

    Args:
        name (str): The data dict entry

    Returns:
        Tuple[Optional[str], str]:
            First element is the class name of the entry, second element is the name.
            The class name will be None if it is not present.
    """
    name_match = re.search(r"([^\[]+)\[([^\]]+)\](\@.*)?", name)
    if name_match is None:
        return None, name

    prefix = name_match.group(3)
    return name_match.group(
        1
    ), f"{name_match.group(2)}{'' if prefix is None else prefix}"


def best_namefit_of(name: str, keys: Iterable[str]) -> Optional[str]:
    """
    Get the best namefit of `name` in `keys`.

    Args:
        name (str): The name to fit against the keys.
        keys (Iterable[str]): The keys to fit `name` against.

    Returns:
        Optional[str]: The best fitting key. None if no fit was found.
    """
    if not keys:
        return None

    nx_name, name2fit = split_class_and_name_of(name)

    if name2fit in keys:
        return name2fit
    if nx_name is not None and nx_name in keys:
        return nx_name

    best_match, score = max(
        map(lambda x: (x, get_nx_namefit(name2fit, x)), keys), key=lambda x: x[1]
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
        if not node.variadic:
            if node.name in keys:
                return [node.name]
            elif (
                hasattr(node, "nx_class")
                and f"{convert_nexus_to_caps(node.nx_class)}[{node.name}]" in keys
            ):
                return [f"{convert_nexus_to_caps(node.nx_class)}[{node.name}]"]

        variations = []
        for key in keys:
            nx_name, name2fit = split_class_and_name_of(key)
            if node.type == "attribute":
                # Remove the starting @ from attributes
                name2fit = name2fit[1:] if name2fit.startswith("@") else name2fit
            if nx_name is not None and nx_name != node.name:
                continue
            if (
                get_nx_namefit(name2fit, node.name) >= 0
                and key not in node.parent.get_all_direct_children_names()
            ):
                variations.append(key)
            if nx_name is not None and not variations:
                collector.collect_and_log(
                    nx_name, ValidationProblem.FailedNamefitting, keys
                )
        return variations

    def get_field_attributes(name: str, keys: Mapping[str, Any]) -> Mapping[str, Any]:
        return {k.split("@")[1]: keys[k] for k in keys if k.startswith(f"{name}@")}

    def handle_nxdata(node: NexusGroup, keys: Mapping[str, Any], prev_path: str):
        def check_nxdata():
            data = (
                keys.get(f"DATA[{signal}]")
                if f"DATA[{signal}]" in keys
                else keys.get(signal)
            )
            if data is None:
                collector.collect_and_log(
                    f"{prev_path}/{signal}",
                    ValidationProblem.NXdataMissingSignalData,
                    None,
                )
            else:
                # Attach the base class to the inheritance chain
                # if the concept for signal is already defined in the appdef
                # TODO: This appends the base class multiple times
                # it should be done only once
                data_node = node.search_add_child_for_multiple((signal, "DATA"))
                data_bc_node = node.search_add_child_for("DATA")
                data_node.inheritance.append(data_bc_node.inheritance[0])
                for child in data_node.get_all_direct_children_names():
                    data_node.search_add_child_for(child)

                handle_field(
                    node.search_add_child_for_multiple((signal, "DATA")),
                    keys,
                    prev_path=prev_path,
                )

            for i, axis in enumerate(axes):
                if axis == ".":
                    continue
                index = keys.get(f"{axis}_indices", i)

                if f"AXISNAME[{axis}]" in keys:
                    axis = f"AXISNAME[{axis}]"
                axis_data = _follow_link(keys.get(axis), prev_path)
                if axis_data is None:
                    collector.collect_and_log(
                        f"{prev_path}/{axis}",
                        ValidationProblem.NXdataMissingAxisData,
                        None,
                    )
                    break
                else:
                    # Attach the base class to the inheritance chain
                    # if the concept for the axis is already defined in the appdef
                    # TODO: This appends the base class multiple times
                    # it should be done only once
                    axis_node = node.search_add_child_for_multiple((axis, "AXISNAME"))
                    axis_bc_node = node.search_add_child_for("AXISNAME")
                    axis_node.inheritance.append(axis_bc_node.inheritance[0])
                    for child in axis_node.get_all_direct_children_names():
                        axis_node.search_add_child_for(child)

                    handle_field(
                        node.search_add_child_for_multiple((axis, "AXISNAME")),
                        keys,
                        prev_path=prev_path,
                    )
                if isinstance(data, np.ndarray) and data.shape[index] != len(axis_data):
                    collector.collect_and_log(
                        f"{prev_path}/{axis}",
                        ValidationProblem.NXdataAxisMismatch,
                        f"{prev_path}/{signal}",
                        index,
                    )

        keys = _follow_link(keys, prev_path)
        signal = keys.get("@signal")
        aux_signals = keys.get("@auxiliary_signals", [])
        axes = keys.get("@axes", [])
        if isinstance(axes, str):
            axes = [axes]

        if signal is not None:
            check_nxdata()

        indices = map(lambda x: f"{x}_indices", axes)
        errors = map(lambda x: f"{x}_errors", [signal, *aux_signals, *axes])

        # Handle all remaining keys which are not part of NXdata
        remaining_keys = {
            x: keys[x]
            for x in keys
            if x not in [signal, *axes, *indices, *errors, *aux_signals]
        }
        recurse_tree(
            node,
            remaining_keys,
            prev_path=prev_path,
            ignore_names=[
                "DATA",
                "AXISNAME",
                "AXISNAME_indices",
                "FIELDNAME_errors",
                "signal",
                "auxiliary_signals",
                "axes",
                signal,
                *axes,
                *indices,
                *errors,
                *aux_signals,
            ],
        )

    def handle_group(node: NexusGroup, keys: Mapping[str, Any], prev_path: str):
        variants = get_variations_of(node, keys)
        if node.parent_of:
            for child in node.parent_of:
                variants += get_variations_of(child, keys)
        if (
            not variants
            and node.optionality == "required"
            and node.type in missing_type_err
        ):
            collector.collect_and_log(
                f"{prev_path}/{node.name}",
                missing_type_err.get(node.type),
                None,
            )
            return
        for variant in variants:
            if variant in [node.name for node in node.parent_of]:
                # Don't process if this is actually a sub-variant of this group
                continue
            nx_class, _ = split_class_and_name_of(variant)
            if not isinstance(keys[variant], Mapping):
                if nx_class is not None:
                    collector.collect_and_log(
                        f"{prev_path}/{variant}",
                        ValidationProblem.ExpectedGroup,
                        None,
                    )
                return
            if node.nx_class == "NXdata":
                handle_nxdata(node, keys[variant], prev_path=f"{prev_path}/{variant}")
            else:
                recurse_tree(node, keys[variant], prev_path=f"{prev_path}/{variant}")

    def remove_from_not_visited(path: str) -> str:
        if path in not_visited:
            not_visited.remove(path)
        return path

    def _follow_link(
        keys: Optional[Mapping[str, Any]], prev_path: str
    ) -> Optional[Any]:
        if keys is None:
            return None
        if len(keys) == 1 and "link" in keys:
            current_keys = nested_keys
            link_key = None
            for path_elem in keys["link"][1:].split("/"):
                link_key = None
                for dict_path_elem in current_keys:
                    _, hdf_name = split_class_and_name_of(dict_path_elem)
                    if hdf_name == path_elem:
                        link_key = hdf_name
                        break
                if link_key is None:
                    collector.collect_and_log(
                        prev_path, ValidationProblem.BrokenLink, keys["link"]
                    )
                    return None
                current_keys = current_keys[dict_path_elem]
            return current_keys
        return keys

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
            if node.optionality == "required" and isinstance(keys[variant], Mapping):
                # Check if all fields in the dict are actual attributes (startwith @)
                all_attrs = True
                for entry in keys[variant]:
                    if not entry.startswith("@"):
                        all_attrs = False
                        break
                if all_attrs:
                    collector.collect_and_log(
                        f"{prev_path}/{variant}", missing_type_err.get(node.type), None
                    )
                    collector.collect_and_log(
                        f"{prev_path}/{variant}",
                        ValidationProblem.AttributeForNonExistingField,
                        None,
                    )
                    return
            if variant not in keys or mapping.get(f"{prev_path}/{variant}") is None:
                continue

            # Check general validity
            is_valid_data_field(
                mapping[f"{prev_path}/{variant}"], node.dtype, f"{prev_path}/{variant}"
            )

            # Check enumeration
            if (
                node.items is not None
                and mapping[f"{prev_path}/{variant}"] not in node.items
            ):
                collector.collect_and_log(
                    f"{prev_path}/{variant}",
                    ValidationProblem.InvalidEnum,
                    node.items,
                )

            # Check unit category
            if node.unit is not None:
                remove_from_not_visited(f"{prev_path}/{variant}/@units")
                if f"{variant}@units" not in keys:
                    collector.collect_and_log(
                        f"{prev_path}/{variant}",
                        ValidationProblem.MissingUnit,
                        node.unit,
                    )
                # TODO: Check unit with pint

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
                mapping[
                    f"{prev_path}/{variant if variant.startswith('@') else f'@{variant}'}"
                ],
                node.dtype,
                f"{prev_path}/{variant if variant.startswith('@') else f'@{variant}'}",
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
            f"{prev_path}/{node.name}",
            ValidationProblem.ChoiceValidationError,
            None,
        )

    def handle_unknown_type(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        # This should normally not happen if
        # the handling map includes all types allowed in NexusNode.type
        # Still, it's good to have a fallback
        # TODO: Raise error or log the issue?
        pass

    def is_documented(key: str, node: NexusNode) -> bool:
        if mapping.get(key) is None:
            # This value is not really set. Skip checking it's documentation.
            return True

        for name in key[1:].replace("@", "").split("/"):
            children = node.get_all_direct_children_names()
            best_name = best_namefit_of(name, children)
            if best_name is None:
                return False

            node = node.search_add_child_for(best_name)

        if isinstance(mapping[key], dict) and "link" in mapping[key]:
            # TODO: Follow link and check consistency with current field
            return True

        if "@" not in key and node.type != "field":
            return False
        if "@" in key and node.type != "attribute":
            return False

        if (
            isinstance(node, NexusEntity)
            and node.unit is not None
            and f"{key}/@units" not in mapping
        ):
            collector.collect_and_log(
                f"{key}", ValidationProblem.MissingUnit, node.unit
            )

        return is_valid_data_field(mapping[key], node.dtype, key)

    def recurse_tree(
        node: NexusNode,
        keys: Mapping[str, Any],
        prev_path: str = "",
        ignore_names: Optional[List[str]] = None,
    ):
        for child in node.children:
            if ignore_names is not None and child.name in ignore_names:
                continue
            keys = _follow_link(keys, prev_path)
            if keys is None:
                return
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
    nested_keys = build_nested_dict_from(mapping)
    not_visited = list(mapping)
    recurse_tree(tree, nested_keys)

    for not_visited_key in not_visited:
        if not_visited_key.endswith("/@units"):
            if is_documented(not_visited_key.rsplit("/", 1)[0], tree):
                continue
            if not_visited_key.rsplit("/", 1)[0] not in not_visited:
                collector.collect_and_log(
                    not_visited_key,
                    ValidationProblem.UnitWithoutField,
                    not_visited_key.rsplit("/", 1)[0],
                )
            if not ignore_undocumented:
                collector.collect_and_log(
                    not_visited_key,
                    ValidationProblem.UnitWithoutDocumentation,
                    mapping[not_visited_key],
                )
        if is_documented(not_visited_key, tree):
            continue

        if not ignore_undocumented:
            collector.collect_and_log(
                not_visited_key, ValidationProblem.MissingDocumentation, None
            )

    return not collector.has_validation_problems()


def populate_full_tree(node: NexusNode, max_depth: Optional[int] = 5, depth: int = 0):
    """
    Recursively populate the full tree.

    Args:
        node (NexusNode):
            The current node from which to populate the full tree.
        max_depth (Optional[int], optional):
            The maximum depth to populate the tree. Defaults to 5.
        depth (int, optional):
            The current depth.
            This is used as a recursive parameter and should be
            kept at the default value when calling this function.
            Defaults to 0.
    """
    if max_depth is not None and depth >= max_depth:
        return
    if node is None:
        # TODO: node is None should actually not happen
        # but it does while recursing the tree and it should
        # be fixed.
        return
    for child in node.get_all_direct_children_names():
        child_node = node.search_add_child_for(child)
        populate_full_tree(child_node, max_depth=max_depth, depth=depth + 1)


# Backwards compatibility
def validate_data_dict(
    _: Mapping[str, Any], read_data: Mapping[str, Any], root: ET._Element
) -> bool:
    return validate_dict_against(root.attrib["name"], read_data)
