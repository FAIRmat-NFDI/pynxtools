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
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple, Union

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
    `split_class_and_name_of("ENTRY[entry]")`, which will return `("ENTRY", "entry")`.
    If this is a simple string it will just return this string, i.e.
    `split_class_and_name_of("entry")` will return `None, "entry"`.

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


def best_namefit_of(name: str, nodes: Iterable[NexusNode]) -> Optional[NexusNode]:
    """
    Get the best namefit of `name` in `keys`.

    Args:
        name (str): The name to fit against the keys.
        nodes (Iterable[NexusNode]): The nodes to fit `name` against.

    Returns:
        Optional[NexusNode]: The best fitting node. None if no fit was found.
    """
    if not nodes:
        return None

    concept_name, instance_name = split_class_and_name_of(name)

    best_match = None

    for node in nodes:
        if not node.variadic:
            if instance_name == node.name:
                return node
        else:
            if concept_name and concept_name == node.name:
                if instance_name == node.name:
                    return node

                name_any = node.name_type == "any"
                name_partial = node.name_type == "partial"

                score = get_nx_namefit(instance_name, node.name, name_any, name_partial)
                if score > -1:
                    best_match = node

    return best_match


def validate_dict_against(
    appdef: str, mapping: MutableMapping[str, Any], ignore_undocumented: bool = False
) -> Tuple[bool, List]:
    """
    Validates a mapping against the NeXus tree for application definition `appdef`.

    Args:
        appdef (str): The appdef name to validate against.
        mapping (MutableMapping[str, Any]):
            The mapping containing the data to validate.
            This should be a dict of `/` separated paths.
            Attributes are denoted with `@` in front of the last element.
        ignore_undocumented (bool, optional):
            Ignore all undocumented keys in the verification
            and just check if the required fields are properly set.
            Defaults to False.

    Returns:
        bool: True if the mapping is valid according to `appdef`, False otherwise.
        List: list of keys in mapping that correspond to attributes of non-existing fields
    """

    def get_variations_of(node: NexusNode, keys: Mapping[str, Any]) -> List[str]:
        if not node.variadic:
            if f"{'@' if node.type == 'attribute' else ''}{node.name}" in keys:
                return [node.name]
            elif (
                hasattr(node, "nx_class")
                and f"{convert_nexus_to_caps(node.nx_class)}[{node.name}]" in keys
            ):
                return [f"{convert_nexus_to_caps(node.nx_class)}[{node.name}]"]

        variations = []

        for key in keys:
            concept_name, instance_name = split_class_and_name_of(key)

            if node.type == "attribute":
                # Remove the starting @ from attributes
                if concept_name:
                    concept_name = (
                        concept_name[1:]
                        if concept_name.startswith("@")
                        else concept_name
                    )

                instance_name = (
                    instance_name[1:]
                    if instance_name.startswith("@")
                    else instance_name
                )

            if not concept_name or concept_name != node.name:
                continue

            name_any = node.name_type == "any"
            name_partial = node.name_type == "partial"

            if (
                get_nx_namefit(instance_name, node.name, name_any, name_partial) >= 0
                and key not in node.parent.get_all_direct_children_names()
            ):
                variations.append(key)

            if not variations:
                collector.collect_and_log(
                    concept_name, ValidationProblem.FailedNamefitting, keys
                )
        return variations

    def get_field_attributes(name: str, keys: Mapping[str, Any]) -> Mapping[str, Any]:
        prefix = f"{name}@"
        return {
            # Preserve everything after the field name, keeping '@attr[@attr]' or '@attr'
            k[len(prefix) - 1 :]: v
            for k, v in keys.items()
            if k.startswith(prefix)
        }

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

            # check NXdata attributes
            for attr in ("signal", "auxiliary_signals", "axes"):
                handle_attribute(
                    node.search_add_child_for(attr),
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
                continue
            if node.nx_class == "NXdata":
                handle_nxdata(node, keys[variant], prev_path=f"{prev_path}/{variant}")
            if node.nx_class == "NXcollection":
                return
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
        if (
            not variants
            and node.optionality == "required"
            and node.type in missing_type_err
        ):
            collector.collect_and_log(full_path, missing_type_err.get(node.type), None)
            return

        for variant in variants:
            if node.optionality == "required" and isinstance(keys[variant], Mapping):
                # Check if all fields in the dict are actual attributes (startswith @)
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
            mapping[f"{prev_path}/{variant}"] = is_valid_data_field(
                mapping[f"{prev_path}/{variant}"],
                node.dtype,
                node.items,
                node.open_enum,
                f"{prev_path}/{variant}",
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

        if (
            not variants
            and node.optionality == "required"
            and node.type in missing_type_err
        ):
            collector.collect_and_log(full_path, missing_type_err.get(node.type), None)
            return

        for variant in variants:
            mapping[
                f"{prev_path}/{variant if variant.startswith('@') else f'@{variant}'}"
            ] = is_valid_data_field(
                mapping[
                    f"{prev_path}/{variant if variant.startswith('@') else f'@{variant}'}"
                ],
                node.dtype,
                node.items,
                node.open_enum,
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

    def add_best_matches_for(key: str, node: NexusNode) -> Optional[NexusNode]:
        for name in key[1:].replace("@", "").split("/"):
            children_to_check = [
                node.search_add_child_for(child)
                for child in node.get_all_direct_children_names()
            ]
            node = best_namefit_of(name, children_to_check)

            if node is None:
                return None

        return node

    def is_documented(key: str, tree: NexusNode) -> bool:
        if mapping.get(key) is None:
            # This value is not really set. Skip checking its documentation.
            return True

        node = add_best_matches_for(key, tree)

        if node is None:
            key_path = key.replace("@", "")
            while "/" in key_path:
                key_path = key_path.rsplit("/", 1)[0]  # Remove last segment
                parent_node = add_best_matches_for(key_path, tree)
                if (
                    parent_node
                    and parent_node.type == "group"
                    and parent_node.nx_class == "NXcollection"
                ):
                    # Collection found for parents, mark as documented
                    return True

            return False

        if node.type == "group" and node.nx_class == "NXcollection":
            # Collection found, mark as documented
            return True

        if isinstance(mapping[key], dict) and "link" in mapping[key]:
            # TODO: Follow link and check consistency with current field
            return True

        if "@" not in key and node.type != "field":
            return False
        if "@" in key and node.type != "attribute":
            return False

        # if we arrive here, the key is supposed to be documented.
        # We still do some further checks before returning.

        # Check general validity
        mapping[key] = is_valid_data_field(
            mapping[key], node.dtype, node.items, node.open_enum, key
        )

        # Check main field exists for units
        if (
            isinstance(node, NexusEntity)
            and node.unit is not None
            and f"{key}/@units" not in mapping
        ):
            collector.collect_and_log(
                f"{key}", ValidationProblem.MissingUnit, node.unit
            )

        return True

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

    def check_attributes_of_nonexisting_field(
        node: NexusNode,
    ) -> list:
        """
            This method runs through the mapping dictionary and checks if there are any
            attributes assigned to the fields (not groups!) which are not explicitly
            present in the mapping.
            If there are any found, a warning is logged and the corresponding items are
            added to the list returned by the method.

        Args:
            node (NexusNode): the tree generated from application definition.

        Returns:
            list: list of keys in mapping that correspond to attributes of
            non-existing fields
        """

        keys_to_remove = []

        for key in mapping:
            last_index = key.rfind("/")
            if key[last_index + 1] == "@" and key[last_index + 1 :] != "@units":
                # key is an attribute. Find a corresponding parent, check all the other
                # children of this parent
                # ignore units here, they are checked separately
                attribute_parent_checked = False
                for key_iterating in mapping:
                    # check if key_iterating starts with parent of the key OR any
                    # allowed variation of the parent of the key
                    flag, extra_length = startswith_with_variations(
                        key_iterating, key[0:last_index]
                    )
                    # the variation of the path to the parent might have different length
                    # than the key itself, extra_length is adjusting for that
                    if flag:
                        if len(key_iterating) == last_index + extra_length:
                            # the parent is a field
                            attribute_parent_checked = True
                            break
                        elif (key_iterating[last_index + extra_length] == "/") and (
                            key_iterating[last_index + extra_length + 1] != "@"
                        ):
                            # the parent is a group
                            attribute_parent_checked = True
                            break
                if not attribute_parent_checked:
                    type_of_parent_from_tree = check_type_with_tree(
                        node, key[0:last_index]
                    )
                    # The parent can be a group with only attributes as children; check
                    # in the tree built from app. def. Alternatively, parent can be not
                    # in the tree and then group with only attributes is indistinguishable
                    # from missing field. Continue without warnings or changes.
                    if not (
                        type_of_parent_from_tree == "group"
                        or type_of_parent_from_tree is None
                    ):
                        keys_to_remove.append(key)
                        collector.collect_and_log(
                            key[0:last_index],
                            ValidationProblem.AttributeForNonExistingField,
                            None,
                        )
                        collector.collect_and_log(
                            key,
                            ValidationProblem.KeyToBeRemoved,
                            None,
                        )
        return keys_to_remove

    def check_type_with_tree(
        node: NexusNode,
        path: str,
    ) -> Optional[str]:
        """
            Recursively search for the type of the object from Template
            (described by path) using subtree hanging below the node.
            The path should be relative to the current node.

        Args:
            node (NexusNode): the subtree to search in.
            path (str): the string addressing the object from Mapping (the Template)
            to search the type of.

        Returns:
            Optional str: type of the object as a string, if the object was found
            in the tree, None otherwise.
        """

        # already arrived to the object
        if path == "":
            return node.type
        # searching for object among the children of the node
        next_child_name_index = path[1:].find("/")
        if (
            next_child_name_index == -1
        ):  # the whole path from element #1 is the child name
            next_child_name_index = (
                len(path) - 1
            )  # -1 because we count from element #1, not #0
        next_child_class, next_child_name = split_class_and_name_of(
            path[1 : next_child_name_index + 1]
        )
        if (next_child_class is not None) or (next_child_name is not None):
            output = None
            for child in node.children:
                # regexs to separate the class and the name from full name of the child
                child_class_from_node = re.sub(
                    r"(\@.*)*(\[.*?\])*(\(.*?\))*([a-z]\_)*(\_[a-z])*[a-z]*\s*",
                    "",
                    child.__str__(),
                )
                child_name_from_node = re.sub(
                    r"(\@.*)*(\(.*?\))*(.*\[)*(\].*)*\s*",
                    "",
                    child.__str__(),
                )
                if (child_class_from_node == next_child_class) or (
                    child_name_from_node == next_child_name
                ):
                    output_new = check_type_with_tree(
                        child, path[next_child_name_index + 1 :]
                    )
                    if output_new is not None:
                        output = output_new
            return output
        else:
            return None

    def startswith_with_variations(
        large_str: str, baseline_str: str
    ) -> Tuple[bool, int]:
        """
            Recursively check if the large_str starts with baseline_str or an allowed
            equivalent (i.e. .../AXISNAME[energy]/... matches .../energy/...).

        Args:
            large_str (str): the string to be checked.
            baseline_str (str): the string used as a baseline for comparison.

        Returns:
            bool: True if large_str starts with baseline_str or equivalent, else False.
            int: The combined length difference between baseline_str and the equivalent
            part of the large_str.
        """
        if len(baseline_str.split("/")) == 1:
            # if baseline_str has no separators left, match already found
            return (True, 0)
        first_token_large_str = large_str.split("/")[1]
        first_token_baseline_str = baseline_str.split("/")[1]

        remaining_large_str = large_str[len(first_token_large_str) + 1 :]
        remaining_baseline_str = baseline_str[len(first_token_baseline_str) + 1 :]
        if first_token_large_str == first_token_baseline_str:
            # exact match of n-th token
            return startswith_with_variations(
                remaining_large_str, remaining_baseline_str
            )
        match_check = re.search(r"\[.*?\]", first_token_large_str)
        if match_check is None:
            # tokens are different and do not contain []
            return (False, 0)
        variation_first_token_large = match_check.group(0)[1:-1]
        if variation_first_token_large == first_token_baseline_str:
            # equivalents match
            extra_length_this_step = len(first_token_large_str) - len(
                first_token_baseline_str
            )
            a, b = startswith_with_variations(
                remaining_large_str, remaining_baseline_str
            )
            return (a, b + extra_length_this_step)
        # default
        return (False, 0)

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

    keys_to_remove = check_attributes_of_nonexisting_field(tree)

    for not_visited_key in not_visited:
        if not_visited_key.endswith("/@units"):
            # check that parent exists
            if not_visited_key.rsplit("/", 1)[0] not in mapping.keys():
                collector.collect_and_log(
                    not_visited_key,
                    ValidationProblem.UnitWithoutField,
                    not_visited_key.rsplit("/", 1)[0],
                )
                collector.collect_and_log(
                    not_visited_key,
                    ValidationProblem.KeyToBeRemoved,
                    None,
                )
                keys_to_remove.append(not_visited_key)
            else:
                # check that parent has units
                node = add_best_matches_for(not_visited_key.rsplit("/", 1)[0], tree)

                # Search if unit is somewhere in an NXcollection
                if node is None:
                    key_path = not_visited_key.replace("@", "")
                    while "/" in key_path:
                        key_path = key_path.rsplit("/", 1)[0]  # Remove last segment
                        parent_node = add_best_matches_for(key_path, tree)
                        if (
                            parent_node
                            and parent_node.type == "group"
                            and parent_node.nx_class == "NXcollection"
                        ):
                            # NXcollection found → break while, continue outer loop
                            break
                    continue

                if node is None or node.type != "field" or node.unit is None:
                    if not ignore_undocumented:
                        collector.collect_and_log(
                            not_visited_key,
                            ValidationProblem.UnitWithoutDocumentation,
                            mapping[not_visited_key],
                        )

            # parent key will be checked on its own if it exists, because it is in the list
            continue

        if "@" in not_visited_key.rsplit("/")[-1]:
            # check that parent exists
            if not_visited_key.rsplit("/", 1)[0] not in mapping.keys():
                # check that parent is not a group
                node = add_best_matches_for(not_visited_key.rsplit("/", 1)[0], tree)
                if node is None or node.type != "group":
                    collector.collect_and_log(
                        not_visited_key.rsplit("/", 1)[0],
                        ValidationProblem.AttributeForNonExistingField,
                        None,
                    )
                    collector.collect_and_log(
                        not_visited_key,
                        ValidationProblem.KeyToBeRemoved,
                        None,
                    )
                    keys_to_remove.append(not_visited_key)
                    continue

        if is_documented(not_visited_key, tree):
            continue

        if not ignore_undocumented:
            collector.collect_and_log(
                not_visited_key, ValidationProblem.MissingDocumentation, None
            )

    return (not collector.has_validation_problems(), keys_to_remove)


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
    _: MutableMapping[str, Any], read_data: MutableMapping[str, Any], root: ET._Element
) -> bool:
    return validate_dict_against(root.attrib["name"], read_data)[0]
