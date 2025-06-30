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
import copy
import re
from collections import defaultdict
from collections.abc import Iterable, Mapping, MutableMapping
from functools import reduce
from operator import getitem
from typing import Any, Literal, Optional, Union

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
from pynxtools.units import NXUnitSet, ureg


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


def split_class_and_name_of(name: str) -> tuple[Optional[str], str]:
    """
    Return the class and the name of a data dict entry of the form
    `split_class_and_name_of("ENTRY[entry]")`, which will return `("ENTRY", "entry")`.
    If this is a simple string it will just return this string, i.e.
    `split_class_and_name_of("entry")` will return `None, "entry"`.

    Args:
        name (str): The data dict entry

    Returns:
        tuple[Optional[str], str]:
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


def best_namefit_of(
    name: str,
    nodes: Iterable[NexusNode],
    expected_types: list[str],
    check_types: bool = False,
) -> Optional[NexusNode]:
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
                if node.type not in expected_types and check_types:
                    expected_types_str = " or ".join(expected_types)
                    collector.collect_and_log(
                        name,
                        ValidationProblem.InvalidNexusTypeForNamedConcept,
                        node,
                        expected_types_str,
                    )
                    raise TypeError(
                        f"The type ('{expected_types_str if expected_types else '<unknown>'}') "
                        f"of the given concept {name} conflicts with another existing concept {node.name} (which is of "
                        f"type '{node.type}')."
                    )
                if concept_name and concept_name != node.name:
                    inherited_names = [
                        name
                        if (name := elem.attrib.get("name")) is not None
                        else type_attr[2:].upper()
                        for elem in node.inheritance
                        if (name := elem.attrib.get("name")) is not None
                        or (type_attr := elem.attrib.get("type"))
                        and len(type_attr) > 2
                    ]
                    if concept_name not in inherited_names:
                        if node.type == "group":
                            if concept_name != node.nx_class[2:].upper():
                                collector.collect_and_log(
                                    concept_name,
                                    ValidationProblem.InvalidConceptForNonVariadic,
                                    node,
                                )
                        else:
                            collector.collect_and_log(
                                concept_name,
                                ValidationProblem.InvalidConceptForNonVariadic,
                                node,
                            )
                        return None
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


def is_valid_unit_for_node(
    node: NexusNode, unit: str, unit_path: str, hints: dict[str, Any]
) -> None:
    """
    Validate whether a unit string is compatible with the expected unit category for a given NeXus node.

    This function checks if the provided `unit` string matches the expected unit dimensionality
    defined in the node's `unit` field. Special logic is applied for "NX_TRANSFORMATION", where
    the dimensionality depends on the `transformation_type` hint.

    If the unit does not match the expected dimensionality, a validation problem is logged.

    Args:
        node (NexusNode): The node containing unit metadata to validate against.
        unit (str): The unit string to validate (e.g., "m", "eV", "1", "").
        unit_path (str): The path to the unit in the NeXus template, used for logging.
        hints (dict[str, Any]): Additional metadata used during validation. For example,
            hints["transformation_type"] may be used to determine the expected unit category
            if the node represents a transformation.
    """
    # Need to use a list as `NXtransformation` is a special use case
    if node.unit == "NX_TRANSFORMATION":
        if (transformation_type := hints.get("transformation_type")) is not None:
            category_map: dict[str, str] = {
                "translation": "NX_LENGTH",
                "rotation": "NX_ANGLE",
            }
            node_unit_category = category_map.get(transformation_type, "NX_UNITLESS")
        else:
            node_unit_category = "NX_UNITLESS"
        log_input = node_unit_category
    else:
        node_unit_category = node.unit
        log_input = None

    if NXUnitSet.matches(node_unit_category, unit):
        return

    collector.collect_and_log(
        unit_path, ValidationProblem.InvalidUnit, node, unit, log_input
    )


def validate_dict_against(
    appdef: str, mapping: MutableMapping[str, Any], ignore_undocumented: bool = False
) -> bool:
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
    """

    def get_variations_of(node: NexusNode, keys: Mapping[str, Any]) -> list[str]:
        variations = []

        prefix = f"{'@' if node.type == 'attribute' else ''}"
        if not node.variadic:
            if f"{prefix}{node.name}" in keys:
                variations += [node.name]
            elif (
                hasattr(node, "nx_class")
                and f"{convert_nexus_to_caps(node.nx_class)}[{node.name}]" in keys
            ):
                variations += [f"{convert_nexus_to_caps(node.nx_class)}[{node.name}]"]

            # Also add all variations like CONCEPT[node.name] for inherited concepts
            inherited_names = []
            for elem in node.inheritance:
                inherited_name = elem.attrib.get("name")
                if not inherited_name:
                    inherited_name = elem.attrib.get("type")[2:].upper()
                if inherited_name.startswith("NX"):
                    inherited_name = inherited_name[2:].upper()
                inherited_names += [inherited_name]
            for name in set(inherited_names):
                if f"{prefix}{name}[{prefix}{node.name}]" in keys:
                    variations += [f"{prefix}{name}[{prefix}{node.name}]"]

            return variations

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
        remaining_keys = _follow_link(remaining_keys, prev_path)
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
            variant_path = f"{prev_path}/{variant}"
            if variant in [node.name for node in node.parent_of]:
                # Don't process if this is actually a sub-variant of this group
                continue
            nx_class, _ = split_class_and_name_of(variant)
            if not isinstance(keys[variant], Mapping):
                # Groups should have subelements
                if nx_class is not None:
                    collector.collect_and_log(
                        variant_path,
                        ValidationProblem.ExpectedGroup,
                        None,
                    )
                    # TODO: decide if we want to remove such keys
                    # collector.collect_and_log(
                    #     variant_path,
                    #     ValidationProblem.KeyToBeRemoved,
                    #     node.type,
                    # )
                    # keys_to_remove.append(not_visited_key)
                continue
            if node.nx_class == "NXdata":
                handle_nxdata(node, keys[variant], prev_path=variant_path)
            if node.nx_class == "NXcollection":
                return
            else:
                variant_keys = _follow_link(keys[variant], variant_path)
                recurse_tree(node, variant_keys, prev_path=variant_path)

    def remove_from_not_visited(path: str) -> str:
        if path in not_visited:
            not_visited.remove(path)
        return path

    def _follow_link(
        keys: Optional[Mapping[str, Any]], prev_path: str, p=False
    ) -> Optional[Any]:
        """
        Resolves internal dictionary "links" by replacing any keys containing a
        {"link": "/path/to/target"} structure with the actual referenced content.

        Note that the keys are only replaced in copies of the incoming keys, NOT in
        the gloval mapping. That is, links are resolved for checking, but we still write
        links into the HDF5 file.

        This function traverses the mapping and recursively resolves any keys that
        contain a "link" to another path (relative to the global template).
        If the link cannot be resolved, the issue is logged.

        Args:
            keys (Optional[Mapping[str, Any]]): The dictionary structure to process.
                May be None or a non-dict value, in which case it's returned as-is.
            prev_path (str): The path leading up to the current `keys` context, used
                for logging and error reporting.

        Returns:
            Optional[Any]: A dictionary with resolved links, the original value if
            `keys` is not a dict, or None if `keys` is None.
        """
        if keys is None:
            return None

        if not isinstance(keys, dict):
            return keys

        resolved_keys = copy.deepcopy(keys)
        for key, value in keys.copy().items():
            if isinstance(value, dict) and "link" in value:
                key_path = f"{prev_path}/{key}" if prev_path else key
                current_keys = nested_keys
                link_key = None
                for path_elem in value["link"][1:].split("/"):
                    link_key = None
                    for dict_path_elem in current_keys:
                        _, hdf_name = split_class_and_name_of(dict_path_elem)
                        if hdf_name == path_elem:
                            link_key = hdf_name
                            current_keys = current_keys[dict_path_elem]
                            break

                if link_key is None:
                    collector.collect_and_log(
                        key_path, ValidationProblem.BrokenLink, value["link"]
                    )
                    collector.collect_and_log(
                        key_path,
                        ValidationProblem.KeyToBeRemoved,
                        "key",
                    )
                    keys_to_remove.append(key_path)
                    del resolved_keys[key]
                else:
                    resolved_keys[key] = current_keys
        return resolved_keys

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
            variant_path = f"{prev_path}/{variant}"

            if isinstance(keys[variant], Mapping) and not all(
                k.startswith("@") for k in keys[variant]
            ):
                # A field should not have a dict of keys that are _not_ all attributes,
                # i.e. no sub-fields or sub-groups.
                collector.collect_and_log(
                    variant_path,
                    ValidationProblem.ExpectedField,
                    None,
                )
                # TODO: decide if we want to remove such keys
                # collector.collect_and_log(
                #     variant_path,
                #     ValidationProblem.KeyToBeRemoved,
                #     node.type,
                # )
                # keys_to_remove.append(variant_path)
                continue
            if node.optionality == "required" and isinstance(keys[variant], Mapping):
                # Check if all fields in the dict are actual attributes (startswith @)
                all_attrs = True
                for entry in keys[variant]:
                    if not entry.startswith("@"):
                        all_attrs = False
                        break
                if all_attrs:
                    collector.collect_and_log(
                        variant_path, missing_type_err.get(node.type), None
                    )
                    collector.collect_and_log(
                        variant_path,
                        ValidationProblem.AttributeForNonExistingField,
                        None,
                    )
                    return
            if variant not in keys or mapping.get(variant_path) is None:
                continue

            # Check general validity
            mapping[variant_path] = is_valid_data_field(
                mapping[variant_path],
                node.dtype,
                node.items,
                node.open_enum,
                variant_path,
            )

            _ = check_reserved_suffix(variant_path, mapping)
            _ = check_reserved_prefix(variant_path, mapping, "field")

            # Check unit category
            if node.unit is not None:
                unit_path = f"{variant_path}/@units"
                if node.unit != "NX_UNITLESS":
                    remove_from_not_visited(unit_path)
                    if f"{variant}@units" not in keys and (
                        node.unit != "NX_TRANSFORMATION"
                        or mapping.get(f"{variant_path}/@transformation_type")
                        in ("translation", "rotation")
                    ):
                        collector.collect_and_log(
                            variant_path,
                            ValidationProblem.MissingUnit,
                            node.unit,
                        )
                        break

                unit = keys.get(f"{variant}@units")
                # Special case: NX_TRANSFORMATION unit depends on `@transformation_type` attribute
                if (
                    transformation_type := keys.get(f"{variant}@transformation_type")
                ) is not None:
                    hints = {"transformation_type": transformation_type}
                else:
                    hints = {}
                is_valid_unit_for_node(node, unit, unit_path, hints)

            field_attributes = get_field_attributes(variant, keys)
            field_attributes = _follow_link(field_attributes, variant_path)

            recurse_tree(
                node,
                field_attributes,
                prev_path=variant_path,
            )

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
            variant_path = (
                f"{prev_path}/{variant if variant.startswith('@') else f'@{variant}'}"
            )
            mapping[variant_path] = is_valid_data_field(
                mapping[
                    f"{prev_path}/{variant if variant.startswith('@') else f'@{variant}'}"
                ],
                node.dtype,
                node.items,
                node.open_enum,
                variant_path,
            )
            _ = check_reserved_prefix(variant_path, mapping, "attribute")

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

    def add_best_matches_for(
        key: str, node: NexusNode, check_types: bool = False
    ) -> Optional[NexusNode]:
        key_components = key[1:].split("/")
        is_last_attr = key_components[-1].startswith("@")
        if is_last_attr:
            key_components[-1] = key_components[-1].replace("@", "")

        key_len = len(key_components)

        expected_types = []
        for ind, name in enumerate(key_components):
            index = ind + 1
            children_to_check = [
                node.search_add_child_for(child)
                for child in node.get_all_direct_children_names()
            ]

            if index < key_len - 1:
                expected_types = ["group"]
            elif index == key_len - 1:
                expected_types = ["group"] if not is_last_attr else ["group", "field"]
            elif index == key_len:
                expected_types = ["attribute"] if is_last_attr else ["field"]
                if "link" in str(mapping.get(key, "")):
                    expected_types += ["group"]

            node = best_namefit_of(name, children_to_check, expected_types, check_types)

            if node is None:
                return None

        return node

    def is_documented(key: str, tree: NexusNode) -> bool:
        if mapping.get(key) is None:
            # This value is not really set. Skip checking its documentation.
            return True

        try:
            node = add_best_matches_for(key, tree, check_types=True)
        except TypeError:
            node = None
            nx_type = "attribute" if key.split("/")[-1].startswith("@") else "field"

            collector.collect_and_log(
                key,
                ValidationProblem.KeyToBeRemoved,
                nx_type,
            )
            keys_to_remove.append(key)

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
            resolved_link = _follow_link({key: mapping[key]}, "")

            if key not in resolved_link:
                # Link is broken and key will be removed; no need to check further
                return False

            is_mapping = isinstance(resolved_link[key], Mapping)

            if node.type == "group" and not is_mapping:
                # Groups must have subelements
                collector.collect_and_log(
                    key,
                    ValidationProblem.ExpectedGroup,
                    None,
                )
                # TODO: decide if we want to remove such keys
                # collector.collect_and_log(
                #     key,
                #     ValidationProblem.KeyToBeRemoved,
                #     "group",
                # )
                # keys_to_remove.append(key)
                return False

            elif node.type == "field":
                # A field should not have a dict of keys that are _not_ all attributes,
                # i.e. no sub-fields or sub-groups.
                if is_mapping and not all(
                    k.startswith("@") for k in resolved_link[key]
                ):
                    collector.collect_and_log(
                        key,
                        ValidationProblem.ExpectedField,
                        None,
                    )
                    # TODO: decide if we want to remove such keys
                    # collector.collect_and_log(
                    #     key,
                    #     ValidationProblem.KeyToBeRemoved,
                    #     "field",
                    # )
                    # keys_to_remove.append(key)
                    # return False
                resolved_link[key] = is_valid_data_field(
                    resolved_link[key], node.dtype, node.items, node.open_enum, key
                )

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
            # Workaround for NX_UNITLESS of NX_TRANSFORMATION unit category
            if node.unit != "NX_TRANSFORMATION" or mapping.get(
                f"{key}/@transformation_type"
            ) in ("translation", "rotation"):
                collector.collect_and_log(
                    f"{key}", ValidationProblem.MissingUnit, node.unit
                )

        return True

    def recurse_tree(
        node: NexusNode,
        keys: Mapping[str, Any],
        prev_path: str = "",
        ignore_names: Optional[list[str]] = None,
    ):
        for child in node.children:
            if ignore_names is not None and child.name in ignore_names:
                continue
            if keys is None:
                return

            handling_map.get(child.type, handle_unknown_type)(child, keys, prev_path)

    def find_instance_name_conflicts(mapping: MutableMapping[str, str]) -> None:
        """
        Detect and log conflicts where the same variadic instance name is reused across
        different concept names.

        This function ensures that a given instance name (e.g., 'my_name') is only used
        for a single concept (e.g., SAMPLE or USER, but not both). Reusing the same instance
        name for different concept names (e.g., SAMPLE[my_name] and USER[my_name]) is
        considered a conflict.

        For example, this is a conflict:
            /ENTRY[entry1]/SAMPLE[my_name]/...
            /ENTRY[entry1]/USER[my_name]/...

        But this is NOT a conflict:
            /ENTRY[entry1]/INSTRUMENT[instrument]/FIELD[my_name]/...
            /ENTRY[entry1]/INSTRUMENT[instrument]/DETECTOR[detector]/FIELD[my_name]/...

        When such conflicts are found, an error is logged indicating the instance name
        and the conflicting concept names. Additionally, all keys involved in the conflict
        are logged and added to the `keys_to_remove` list.

        Args:
            mapping (MutableMapping[str, str]):
                The mapping containing the data to validate.
                This should be a dict of `/` separated paths, such as
                "/ENTRY[entry1]/SAMPLE[sample1]/name".
            keys_to_remove (list[str]):
                List of keys that will be removed from the template. This is extended here
                in the case of conflicts.

        """
        pattern = re.compile(r"(?P<concept_name>[^\[\]/]+)\[(?P<instance>[^\]]+)\]")

        # Tracks instance usage with respect to their parent group
        instance_usage: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)

        for key in mapping:
            matches = list(pattern.finditer(key))
            if not matches:
                # The keys contains no concepts with variable name, no need to further check
                continue
            for match in matches:
                concept_name = match.group("concept_name")
                instance_name = match.group("instance")

                # Determine the parent path up to just before this match
                parent_path = key[: match.start()]
                child_path = key[match.start() :].split("/", 1)[-1]

                # Here we check if for this key with a concept name, another valid key
                # with a non-concept name exists.
                non_concept_key = f"{parent_path}{instance_name}/{child_path}"

                if non_concept_key in mapping:
                    try:
                        node = add_best_matches_for(non_concept_key, tree)
                        if node is not None:
                            collector.collect_and_log(
                                key,
                                ValidationProblem.KeysWithAndWithoutConcept,
                                non_concept_key,
                                concept_name,
                            )
                            collector.collect_and_log(
                                key, ValidationProblem.KeyToBeRemoved, "key"
                            )
                            keys_to_remove.append(key)
                            continue
                    except TypeError:
                        pass

                instance_usage[(instance_name, parent_path)].append((concept_name, key))

        for (instance_name, parent_path), entries in sorted(instance_usage.items()):
            concept_names = {c for c, _ in entries}
            if len(concept_names) > 1:
                keys = sorted(k for _, k in entries)
                collector.collect_and_log(
                    instance_name,
                    ValidationProblem.DifferentVariadicNodesWithTheSameName,
                    entries,
                )
                # Now that we have name conflicts, we still need to check that there are
                # at least two valid keys in that conflict. Only then we remove these.
                # This takes care of the example with keys like
                # /ENTRY[my_entry]/USER[some_name]/name and /ENTRY[my_entry]/USERS[some_name]/name,
                #  where we only want to keep the first one.
                valid_keys_with_name_conflicts = []

                for key in keys:
                    try:
                        node = add_best_matches_for(key, tree)
                        if node is not None:
                            valid_keys_with_name_conflicts.append(key)
                            continue
                    except TypeError:
                        pass
                    collector.collect_and_log(
                        key, ValidationProblem.KeyToBeRemoved, "key"
                    )
                    keys_to_remove.append(key)

                if len(valid_keys_with_name_conflicts) >= 1:
                    # At this point, all invalid keys have been removed.
                    # If more than one valid concept still uses the same instance name under the same parent path,
                    # this indicates a semantic ambiguity (e.g., USER[alex] and SAMPLE[alex]).
                    # We remove these keys as well to avoid conflicts in the writer.
                    remaining_concepts = {
                        pattern.findall(k)[-1][0]
                        for k in valid_keys_with_name_conflicts
                        if pattern.findall(k)
                    }
                    # If multiple valid concept names reuse the same instance name, remove them too
                    if len(remaining_concepts) > 1:
                        for valid_key in valid_keys_with_name_conflicts:
                            collector.collect_and_log(
                                valid_key, ValidationProblem.KeyToBeRemoved, "key"
                            )
                            keys_to_remove.append(valid_key)

    def check_attributes_of_nonexisting_field(
        node: NexusNode,
    ):
        """
            This method runs through the mapping dictionary and checks if there are any
            attributes assigned to the fields (not groups!) which are not explicitly
            present in the mapping.
            If there are any found, a warning is logged and the corresponding items are
            added to the list that stores all keys that shall be removed.

        Args:
            node (NexusNode): the tree generated from application definition.

        """

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
                        collector.collect_and_log(
                            key[0:last_index],
                            ValidationProblem.AttributeForNonExistingField,
                            "attribute",
                        )
                        collector.collect_and_log(
                            key,
                            ValidationProblem.KeyToBeRemoved,
                            "attribute",
                        )
                        keys_to_remove.append(key)
                        remove_from_not_visited(key)

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
    ) -> tuple[bool, int]:
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

    def check_reserved_suffix(key: str, mapping: MutableMapping[str, Any]) -> bool:
        """
        Check if an associated field exists for a key with a reserved suffix.

        Reserved suffixes imply the presence of an associated base field (e.g.,
        "temperature_errors" implies "temperature" must exist in the mapping).

        Args:
            key (str):
                The full key path (e.g., "/ENTRY[entry1]/sample/temperature_errors").
            mapping (MutableMapping[str, Any]):
                The mapping containing the data to validate.
                This should be a dict of `/` separated paths.

        Returns:
            bool:
                True if the suffix usage is valid or not applicable.
                False if the suffix is used without the expected associated base field.
        """
        reserved_suffixes = (
            "_end",
            "_increment_set",
            "_errors",
            "_indices",
            "_mask",
            "_set",
            "_weights",
            "_scaling_factor",
            "_offset",
        )

        parent_path, name = key.rsplit("/", 1)
        concept_name, instance_name = split_class_and_name_of(name)

        for suffix in reserved_suffixes:
            if instance_name.endswith(suffix):
                associated_field = instance_name.rsplit(suffix, 1)[0]

                if not any(
                    k.startswith(parent_path + "/")
                    and (
                        k.endswith(associated_field)
                        or k.endswith(f"[{associated_field}]")
                    )
                    for k in mapping
                ):
                    collector.collect_and_log(
                        key,
                        ValidationProblem.ReservedSuffixWithoutField,
                        associated_field,
                        suffix,
                    )
                    return False
                break  # We found the suffix and it passed

        return True

    def check_reserved_prefix(
        key: str,
        mapping: MutableMapping[str, Any],
        nx_type: Literal["group", "field", "attribute"],
    ) -> bool:
        """
        Check if a reserved prefix was used in the correct context.

        Args:
            key (str): The full key path (e.g., "/ENTRY[entry1]/instrument/detector/@DECTRIS_config").
            mapping (MutableMapping[str, Any]):
                The mapping containing the data to validate.
                This should be a dict of `/` separated paths.
                Attributes are denoted with `@` in front of the last element.
            nx_type (Literal["group", "field", "attribute"]):
                The NeXus type the key represents. Determines which reserved prefixes are relevant.


        Returns:
            bool:
                True if the prefix usage is valid or not applicable.
                False if an invalid or misapplied reserved prefix is detected.
        """
        reserved_prefixes = {
            "attribute": {
                "@BLUESKY_": None,  # do not use anywhere
                "@DECTRIS_": "NXmx",
                "@IDF_": None,  # do not use anywhere
                "@NDAttr": None,
                "@NX_": "all",
                "@PDBX_": None,  # do not use anywhere
                "@SAS_": "NXcanSAS",
                "@SILX_": None,  # do not use anywhere
            },
            "field": {
                "DECTRIS_": "NXmx",
            },
        }

        prefixes = reserved_prefixes.get(nx_type)
        if not prefixes:
            return True

        name = key.rsplit("/", 1)[-1]

        if not name.startswith(tuple(prefixes)):
            return False  # Irrelevant prefix, no check needed

        for prefix, allowed_context in prefixes.items():
            if not name.startswith(prefix):
                continue

            if allowed_context is None:
                # This prefix is disallowed entirely
                collector.collect_and_log(
                    prefix,
                    ValidationProblem.ReservedPrefixInWrongContext,
                    None,
                    key,
                )
                return False
            if allowed_context == "all":
                # We can freely use this prefix everywhere.
                return True

            # Check that the prefix is used in the correct context.
            match = re.match(r"(/ENTRY\[[^]]+])", key)
            definition_value = None
            if match:
                definition_key = f"{match.group(1)}/definition"
                definition_value = mapping.get(definition_key)

            if definition_value != allowed_context:
                collector.collect_and_log(
                    prefix,
                    ValidationProblem.ReservedPrefixInWrongContext,
                    allowed_context,
                    key,
                )
                return False

        return True

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

    keys_to_remove: list[str] = []

    tree = generate_tree_from(appdef)
    collector.clear()
    find_instance_name_conflicts(mapping)
    nested_keys = build_nested_dict_from(mapping)
    not_visited = list(mapping)
    keys = _follow_link(nested_keys, "")
    recurse_tree(tree, nested_keys)

    check_attributes_of_nonexisting_field(tree)

    for not_visited_key in not_visited:
        if mapping.get(not_visited_key) is None:
            # This value is not really set. Skip checking its validity.
            continue

        # TODO: remove again if "@target"/"@reference" is sorted out by NIAC
        always_allowed_attributes = ("@target", "@reference")
        if not_visited_key.endswith(always_allowed_attributes):
            # If we want to support this in the future, we could check that the targetted field exists.
            continue
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
                    "attribute",
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

                if node.unit is not None:
                    # Special case: NX_TRANSFORMATION unit depends on `@transformation_type` attribute
                    if (
                        transformation_type := mapping.get(
                            not_visited_key.replace("/@units", "/@transformation_type")
                        )
                    ) is not None:
                        hints = {"transformation_type": transformation_type}
                    else:
                        hints = {}
                    is_valid_unit_for_node(
                        node, mapping[not_visited_key], not_visited_key, hints
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
                        "attribute",
                    )
                    keys_to_remove.append(not_visited_key)
                    continue

        if "@" not in not_visited_key.rsplit("/", 1)[-1]:
            check_reserved_suffix(not_visited_key, mapping)
            check_reserved_prefix(not_visited_key, mapping, "field")

        else:
            associated_field = not_visited_key.rsplit("/", 1)[-2]
            # Check the prefix both for this attribute and the field it belongs to
            check_reserved_prefix(not_visited_key, mapping, "attribute")
            check_reserved_prefix(associated_field, mapping, "field")

        if is_documented(not_visited_key, tree):
            continue

        if not ignore_undocumented and not_visited_key not in keys_to_remove:
            collector.collect_and_log(
                not_visited_key, ValidationProblem.MissingDocumentation, None
            )

    # clear lru_cache
    NexusNode.search_add_child_for.cache_clear()

    # remove keys that are incorrect
    for key in set(keys_to_remove):
        del mapping[key]

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
    _: MutableMapping[str, Any], read_data: MutableMapping[str, Any], root: ET._Element
) -> bool:
    return validate_dict_against(root.attrib["name"], read_data)
