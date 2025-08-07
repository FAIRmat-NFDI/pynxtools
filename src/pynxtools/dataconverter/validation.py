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
DEBUG_VALIDATION = False
import copy
import os
import re
from collections import defaultdict
from collections.abc import Iterable, Mapping, MutableMapping
from functools import reduce
from operator import getitem
from typing import Any, Literal, Optional, Union

if DEBUG_VALIDATION:
    import debugpy  # will connect to debugger if in debug mode
import h5py
import lxml.etree as ET
import numpy as np
from cachetools import LRUCache, cached
from cachetools.keys import hashkey

from pynxtools.dataconverter.helpers import (
    Collector,
    ValidationProblem,
    clean_str_attr,
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

if DEBUG_VALIDATION:
    debugpy.debug_this_thread()
    # set break points like this
    # debugpy.breakpoint()


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


def is_valid_unit_for_node(
    node: NexusEntity, unit: str, unit_path: str, hints: dict[str, Any]
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
        # NX_TRANSFORMATIONS is a pseudo unit
        # and can be either an angle, a length or unitless
        # depending on the transformation type.
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

    unit = clean_str_attr(unit)

    if NXUnitSet.matches(node_unit_category, unit):
        return

    collector.collect_and_log(
        unit_path, ValidationProblem.InvalidUnit, node, unit, log_input
    )


def validate_hdf_group_against(
    appdef: str,
    data: h5py.Group,
    filename: str,
    ignore_undocumented: bool = False,
) -> bool:
    """
    Validate an HDF5 group against the Nexus tree for the application definition `appdef`.

    Args:
        appdef (str): The application definition to validate against.
        data (h5py.Group): The h5py group to validate.
        filename (str): The filename of the h5py group.
        ignore_undocumented (bool, optional):
            Ignore all undocumented items in the verification
            and just check if the required concepts are properly set.
            Defaults to False.

    Returns:
        bool: True if the group is valid according to `appdef`, False otherwise.
    """

    def best_namefit_of(
        name: str,
        nodes: Iterable[NexusNode],
        hint: Optional[Literal["axis", "signal"]] = None,
    ) -> Optional[NexusNode]:
        """
        Get the best namefit of `name` in `nodes`.

        Args:
            name (str): The name to fit against the nodes.
            nodes (Iterable[NexusNode]): The nodes to fit `name` against.
            node_type (str): The type (group, field, attribute) that is expected

        Returns:
            Optional[NexusNode]: The best fitting node. None if no fit was found.
        """
        if not nodes:
            return None

        best_match = None
        best_score = -1

        hint_map: dict[str, str] = {"DATA": "signal", "AXISNAME": "axis"}

        for node in nodes:
            if not node.variadic:
                if name == node.name:
                    return node
            else:
                name_any = node.name_type == "any"
                name_partial = node.name_type == "partial"
                score = get_nx_namefit(name, node.name, name_any, name_partial)
                if score > best_score:
                    if hint and hint_map.get(node.name) != hint:
                        continue
                    best_match = node
                    best_score = score

        return best_match

    # Only cache based on path. That way we retain the nx_class information
    # in the tree
    # Allow for 10000 cache entries. This should be enough for most cases
    @cached(
        cache=LRUCache(maxsize=10000),
        key=lambda path, node_type=None, nx_class=None, hint=None: hashkey(path),
    )
    def find_node_for(
        path: str,
        node_type: Optional[Literal["group", "field", "attribute"]] = None,
        nx_class: Optional[str] = None,
        hint: Optional[Literal["axis", "signal"]] = None,
    ) -> Optional[NexusNode]:
        """
        Find the NexusNode for a given HDF5 path, optionally constrained by node type and NX_class.

        Uses caching for performance.

        Args:
            path (str): The HDF5 path.
            node_type (Optional[str]): Node type filter: 'group', 'field', or 'attribute'.
            nx_class (Optional[str]): NX_class to restrict search for groups.

        Returns:
            Optional[NexusNode]: Matching node, or None if no match found.
        """
        if path == "":
            return tree

        possible_node_types = ["group", "field", "attribute"]

        *prev_path, last_elem = path.rsplit("/", 1)

        node = find_node_for(prev_path[0], hint=hint) if prev_path else tree
        current = copy.copy(node)

        if node is None:
            return None

        children_to_check = [
            node.search_add_child_for(child)
            for child in node.get_all_direct_children_names(
                nx_class=nx_class, node_type=node_type
            )
        ]
        node = best_namefit_of(last_elem, children_to_check, hint)

        if node is None:
            # Check that there is no other node with the same name, but a different type
            other_node_types = [nt for nt in possible_node_types if nt != node_type]

            for other_node_type in other_node_types:
                children_to_check = [
                    current.search_add_child_for(child)
                    for child in current.get_all_direct_children_names(
                        nx_class=nx_class, node_type=other_node_type
                    )
                ]
                other_node = best_namefit_of(last_elem, children_to_check)
                if other_node is not None and not other_node.variadic:
                    collector.collect_and_log(
                        path,
                        ValidationProblem.InvalidNexusTypeForNamedConcept,
                        other_node,
                        node_type,
                    )
                    raise TypeError(
                        f"The type ('{node_type}') of {path} conflicts with another existing concept "
                        f"{other_node.get_path()} (which is of type '{other_node.type}'."
                    )

            return None

        return node

    def update_required_concepts(path: str, node: NexusNode):
        """
        Update the sets of required groups and entities based on the current node.

        Args:
            path (str): Current path in the HDF5 tree.
            node (NexusNode): The node to extract required concepts from.
        """
        prefix = f"{path}/" if path else ""

        required_subgroups = [
            f"{prefix}{grp.lstrip('/')}"
            for grp in node.required_groups(traverse_children=False)
        ]
        required_subentities = [
            f"{prefix}{ent.lstrip('/')}"
            for ent in node.required_fields_and_attrs_names(traverse_children=False)
        ]

        required_groups.update(required_subgroups)
        required_entities.update(required_subentities)

    def _variadic_node_exists_for(
        path: str, variadic_name: str, node_type: Optional[str] = None
    ):
        """
        Check if a variadic node exists that matches a given path and node type.

        Args:
            path (str): Path to check.
            variadic_name (str): Variadic name to compare.
            node_type (Optional[str]): Type of node to restrict search.

        Returns:
            bool: True if a matching variadic node exists.
        """

        def _get_parent_path(path: str) -> str:
            """
            Return the parent path of a given HDF5 path.

            Args:
                path (str): A full HDF5 path (e.g., "/entry/sample/temperature").

            Returns:
                str: The parent path (e.g., "/entry/sample"). If the path has no parent,
                    returns an empty string.

            Example:
                >>> _get_parent_path("/entry/sample/temperature")
                '/entry/sample'

                >>> _get_parent_path("temperature")
                ''

                >>> _get_parent_path("/temperature")
                ''
            """
            if "/" not in path.strip("/"):
                return ""
            return path.rstrip("/").rsplit("/", 1)[0]

        if _get_parent_path(variadic_name) == _get_parent_path(path):
            node = find_node_for(variadic_name, node_type=node_type)
            if node is not None and node.variadic:
                score = get_nx_namefit(
                    path.rsplit("/", 1)[-1],
                    node.name,
                    node.name_type == "any",
                    node.name_type == "partial",
                )
                if score > -1:
                    return True

            return False

    def remove_from_req_groups(path: str):
        """
        Remove a path from the set of required groups, accounting for variadic nodes.

        Args:
            path (str): The path to remove.
        """
        if path in required_groups:
            required_groups.remove(path)
        else:
            # Check if a variadic required group exists
            for grp in list(required_groups):
                if _variadic_node_exists_for(path, grp, node_type="group"):
                    required_groups.remove(grp)

    def remove_from_req_entities(path: str):
        """
        Remove a path from the set of required entities (fields/attributes),
        accounting for variadic nodes.

        Args:
            path (str): The path to remove.
        """
        if path in required_entities:
            required_entities.remove(path)
        else:
            # Check if a variadic required node exists
            for ent in list(required_entities):
                node_type = "attribute" if "@" in ent else "field"

                clean_path = (
                    path.rstrip("/@units")
                    if path.endswith("@units") and ent.endswith("@units")
                    else path
                )
                clean_ent = (
                    ent.rstrip("/@units")
                    if path.endswith("@units") and ent.endswith("@units")
                    else ent
                )

                if _variadic_node_exists_for(
                    clean_path, clean_ent, node_type=node_type
                ):
                    required_entities.remove(ent)

    def _check_for_nxcollection_parent(node: NexusNode):
        """
        Check if the given node has a parent group of type NXcollection.

        Args:
            node (NexusNode): The node to check.

        Returns:
            bool: True if a parent NXcollection group exists.
        """
        parent = node.parent
        while parent:
            if parent.type == "group" and parent.nx_class == "NXcollection":
                # Found a parent collection group
                return True
            parent = parent.parent

        return False

    def check_reserved_suffix(path: str, parent_data: h5py.Group):
        """
        Check if an associated field exists for a key with a reserved suffix.

        Reserved suffixes imply the presence of an associated base field (e.g.,
        "temperature_errors" implies "temperature" must exist in the mapping).

        Args:
            path (str):
                The full path in the HDF5 file (e.g., "/entry1/sample/temperature_errors").
            parent_data (h5py.Group):
                The parent group of the field/attribute path to check.
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

        name = path.strip("/").split("/")[-1]

        for suffix in reserved_suffixes:
            if name.endswith(suffix):
                associated_field = name.rsplit(suffix, 1)[0]

                if associated_field not in parent_data:
                    collector.collect_and_log(
                        path,
                        ValidationProblem.ReservedSuffixWithoutField,
                        associated_field,
                        suffix,
                    )
                    return
                break  # We found the suffix and it passed
        return

    def check_reserved_prefix(
        path: str,
        appdef_name: str,
        nx_type: Literal["group", "field", "attribute"],
    ):
        """
        Check if a reserved prefix was used in the correct context.

        Args:
            path (str):
                The full path in the HDF5 file (e.g., "/entry1/sample/temperature_errors").
            appdef_name (str):
                Name of the application definition (e.g. NXmx, NXmpes, etc.)
            nx_type (Literal["group", "field", "attribute"]):
                The NeXus type the key represents. Determines which reserved prefixes are relevant.

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
            return

        name = path.rsplit("/")[-1]

        if nx_type == "attribute":
            name = f"@{name}"

        if not name.startswith(tuple(prefixes)):
            return  # Irrelevant prefix, no check needed

        for prefix, allowed_context in prefixes.items():
            if not name.startswith(prefix):
                continue

            if allowed_context is None:
                # This prefix is disallowed entirely
                collector.collect_and_log(
                    prefix,
                    ValidationProblem.ReservedPrefixInWrongContext,
                    None,
                    appdef_name,
                )
                return
            if allowed_context == "all":
                # We can freely use this prefix everywhere.
                return

            if allowed_context != appdef_name:
                collector.collect_and_log(
                    prefix,
                    ValidationProblem.ReservedPrefixInWrongContext,
                    allowed_context,
                    appdef_name,
                )
                return

        return

    def handle_group(path: str, group: h5py.Group):
        """
        Handle validation logic for HDF5 groups.

        Args:
            path (str): Relative HDF5 path to the group.
            group (h5py.Group): The group object.
        """
        full_path = f"{entry_name}/{path}"

        check_reserved_prefix(full_path, appdef_node.name, "group")

        if not group.attrs.get("NX_class"):
            # We ignore additional groups that don't have an NX_class
            return

        try:
            node = find_node_for(
                path, node_type="group", nx_class=group.attrs.get("NX_class")
            )
        except TypeError:
            return
        if node is None:
            if not ignore_undocumented:
                collector.collect_and_log(
                    full_path, ValidationProblem.MissingDocumentation, None
                )
            return

        update_required_concepts(path, node)
        remove_from_req_groups(path)

        if _check_for_nxcollection_parent(node):
            # NXcollection found in parents, stop checking
            return

        if node.nx_class == "NXdata":
            handle_nxdata(path, group)
        if node.nx_class == "NXcollection":
            return

    def handle_nxdata(path: str, group: h5py.Group):
        """
        Handle validation of NXdata groups, including signal, axes, and auxiliary signals.

        Args:
            path (str): HDF5 path to the NXdata group.
            group (h5py.Group): The NXdata group object.
        """
        full_path = f"{entry_name}/{path}"

        def check_nxdata():
            data_field = group.get(signal)

            if data_field is None:
                collector.collect_and_log(
                    f"{full_path}/{signal}",
                    ValidationProblem.NXdataMissingSignalData,
                    None,
                )
            else:
                handle_field(f"{path}/{signal}", data_field, hint="signal")

            # check NXdata attributes
            attrs = ("signal", "auxiliary_signals", "axes")
            data_attrs = {k: group.attrs[k] for k in attrs if k in group.attrs}

            handle_attributes(path, data_attrs)

            for i, axis in enumerate(axes):
                if axis == ".":
                    continue
                index = group.get(f"{axis}_indices", i)

                axis_field = group.get(axis)

                if axis_field is None:
                    collector.collect_and_log(
                        f"{full_path}/{axis}",
                        ValidationProblem.NXdataMissingAxisData,
                        None,
                    )
                    break
                else:
                    handle_field(f"{path}/{axis}", axis_field, hint="axis")
                if np.shape(data_field)[index] != len(axis_field):
                    collector.collect_and_log(
                        f"{path}/{axis}",
                        ValidationProblem.NXdataAxisMismatch,
                        f"{full_path}/{signal}",
                        index,
                    )

        signal = group.attrs.get("signal")
        aux_signals = group.attrs.get("auxiliary_signals", [])
        axes = group.attrs.get("axes", [])

        if isinstance(axes, str):
            axes = [axes]

        indices = map(lambda x: f"{x}_indices", axes)
        errors = map(lambda x: f"{x}_errors", [signal, *aux_signals, *axes])

        # TODO: check that the indices match
        # TODO: check that the errors have the same dim as the fields

        if signal is not None:
            check_nxdata()

    def handle_field(
        path: str,
        dataset: h5py.Dataset,
        hint: Optional[Literal["axis", "signal"]] = None,
    ):
        """
        Validate a NeXus field (dataset) within the HDF5 structure.

        Args:
            path (str): Path to the dataset.
            data (h5py.Dataset): Dataset object.
            hint (str):
                If the field is in an NXdata group, this is used to figure out
                if it is an AXISNAME or a DATA.
        """

        full_path = f"{entry_name}/{path}"
        check_reserved_prefix(full_path, appdef_node.name, "field")
        try:
            node = find_node_for(path, node_type="field", hint=hint)
        except TypeError:
            return

        if node is None:
            key_path = path.replace("@", "")
            parent_node = None
            while "/" in key_path:
                key_path = key_path.rsplit("/", 1)[0]  # Remove last segment
                parent_data = data.get(key_path)
                nx_class = (
                    parent_data.attrs.get("NX_class")
                    if parent_data is not None
                    else None
                )
                if nx_class == "NXcollection":
                    # Collection found for parents, mark as documented
                    return

            if not ignore_undocumented:
                collector.collect_and_log(
                    full_path, ValidationProblem.MissingDocumentation, None
                )
            return

        update_required_concepts(path, node)
        remove_from_req_entities(path)

        if _check_for_nxcollection_parent(node):
            # NXcollection found in parents, stop checking
            return

        is_valid_data_field(
            clean_str_attr(dataset[()]),
            node.dtype,
            node.items,
            node.open_enum,
            full_path,
        )

        units = dataset.attrs.get("units")
        units_path = f"{full_path}/@units"
        if node.unit is not None:
            remove_from_req_entities(f"{path}/@units")

            if node.unit != "NX_UNITLESS":
                if units is None:
                    collector.collect_and_log(
                        full_path, ValidationProblem.MissingUnit, node.unit
                    )
                    return
            # Special case: NX_TRANSFORMATION unit depends on `@transformation_type` attribute
            if (
                transformation_type := dataset.attrs.get("transformation_type")
            ) is not None:
                hints = {"transformation_type": transformation_type}
            else:
                hints = {}

            is_valid_unit_for_node(node, units, units_path, hints)

        elif units is not None:
            if not ignore_undocumented:
                collector.collect_and_log(
                    units_path,
                    ValidationProblem.UnitWithoutDocumentation,
                    units,
                )

    def handle_attributes(path: str, attrs: h5py.AttributeManager):
        """
        Validate attributes on a given HDF5 object.

        Args:
            path (str): Path to the object the attributes belong to.
            attrs (h5py.AttributeManager): The attributes collection.
        """
        for attr_name in attrs:
            full_path = f"{entry_name}/{path}/@{attr_name}"
            if attr_name in ("NX_class", "units", "target"):
                # Ignore special attrs
                continue

            check_reserved_prefix(attr_name, appdef_node.name, "attribute")

            try:
                node = find_node_for(f"{path}/{attr_name}", node_type="attribute")
            except TypeError:
                return

            key_path = f"{path}/{attr_name}"
            parent_node = None
            found_collection = False
            while "/" in key_path:
                key_path = key_path.rsplit("/", 1)[0]  # Remove last segment
                parent_data = data.get(key_path)
                nx_class = (
                    parent_data.attrs.get("NX_class")
                    if parent_data is not None
                    else None
                )
                if nx_class == "NXcollection":
                    # Collection found for parents, mark as documented
                    found_collection = True
                    break
            if found_collection:
                continue  # This continues the outer attr_name loop

            if node is None:
                if not ignore_undocumented:
                    collector.collect_and_log(
                        full_path,
                        ValidationProblem.MissingDocumentation,
                        None,
                    )
                continue

            remove_from_req_entities(f"{path}/@{attr_name}")

            if _check_for_nxcollection_parent(node):
                # NXcollection found in parents, stop checking
                return

            attr_data = clean_str_attr(attrs.get(attr_name))

            is_valid_data_field(
                attr_data,
                node.dtype,
                node.items,
                node.open_enum,
                full_path,
            )

    def validate(path: str, h5_obj: Union[h5py.Group, h5py.Dataset]):
        """
        Dispatch validation for either groups or fields based on object type.

        Args:
            path (str): Path to the object.
            h5_obj (Union[h5py.Group, h5py.Dataset]): The HDF5 object to validate.
        """
        if isinstance(h5_obj, h5py.Group):
            handle_group(path, h5_obj)
        elif isinstance(h5_obj, h5py.Dataset):
            handle_field(path, h5_obj)
            parent_path = path.strip("/").rsplit("/", 1)[0]
            check_reserved_suffix(f"{entry_name}/{path}", data[parent_path])
        handle_attributes(path, h5_obj.attrs)

    def visititems(group: h5py.Group, path: str = "", filename: str = ""):
        """
        Recursively visit all items in a group and apply validation.

        Args:
            group (h5py.Group): The group to walk.
            path (str, optional): Current HDF5 path.
            filename (str, optional): Name of the file for resolving links.
        """
        for name in group:
            full_path = f"{path}/{name}".lstrip("/")
            link = group.get(name, getlink=True)

            if isinstance(link, h5py.SoftLink):
                target_path = link.path

                if "target" not in group[name].attrs:
                    collector.collect_and_log(
                        full_path, ValidationProblem.MissingTargetAttribute, None
                    )
                else:
                    attr_target = group[name].attrs["target"]
                    if attr_target != target_path:
                        collector.collect_and_log(
                            full_path,
                            ValidationProblem.TargetAttributeMismatch,
                            attr_target,
                            target_path,
                        )

                # Resolve target relative to the link location
                if target_path.startswith(entry_name):
                    if target_path not in data:
                        collector.collect_and_log(
                            path, ValidationProblem.BrokenLink, target_path
                        )
                        continue
                    resolved_obj = data[target_path]
                    validate(full_path, resolved_obj)
                else:
                    with h5py.File(filename, "r") as h5file:
                        if target_path not in h5file:
                            collector.collect_and_log(
                                path, ValidationProblem.BrokenLink, target_path
                            )
                            continue
                        resolved_obj = h5file[target_path]
                        validate(full_path, resolved_obj)

            elif isinstance(link, h5py.ExternalLink):
                filename = link.filename
                target_path = link.path
                # Open external file and validate
                with h5py.File(filename, "r") as ext_file:
                    if target_path not in ext_file:
                        collector.collect_and_log(
                            path, ValidationProblem.BrokenLink, target_path
                        )
                    resolved_obj = ext_file[target_path]
                    validate(full_path, resolved_obj)

            elif isinstance(link, h5py.HardLink):
                # Validate hard links (normal objects)
                resolved_obj = group.get(name)
                validate(full_path, resolved_obj)
                if isinstance(resolved_obj, h5py.Group):
                    # recurse into subgroups
                    visititems(resolved_obj, full_path, filename)

    collector.clear()

    appdef_node = generate_tree_from(appdef)
    tree = appdef_node.search_add_child_for("ENTRY")
    entry_name = data.name

    required_groups: set[str] = set()
    required_entities: set[str] = set()
    update_required_concepts("", tree)

    visititems(data, filename=filename)

    for req_concept in sorted(required_groups):
        collector.collect_and_log(
            f"{entry_name}/{req_concept}", ValidationProblem.MissingRequiredGroup, None
        )

    for req_concept in sorted(required_entities):
        # Skip if the entire group is missing
        if any(req_concept.startswith(group) for group in required_groups):
            continue
        if "@" in req_concept:
            # Skip if the entire field is missing
            if any(
                req_concept.rsplit("@", -1)[0].startswith(group)
                for group in required_entities
            ):
                continue
            collector.collect_and_log(
                f"{entry_name}/{req_concept}",
                ValidationProblem.MissingRequiredAttribute,
                None,
            )
            continue
        collector.collect_and_log(
            f"{entry_name}/{req_concept}", ValidationProblem.MissingRequiredField, None
        )

    return not collector.has_validation_problems()


def validate_dict_against(
    appdef: str, mapping: MutableMapping[str, Any], ignore_undocumented: bool = False
) -> bool:
    """
    Validates a mapping against the NeXus tree for application definition `appdef`.

    Args:
        appdef (str): The appdef name to validate against.
        mapping (MutableMapping[str, Any]):
            The mapping containing the data to validate.
            This should be a dict of `/` separated paths elements.
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
        keys: Optional[Mapping[str, Any]], prev_path: str
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
                    keys_to_remove.append(f"{key_path}/@target")
                    del resolved_keys[key]
                else:
                    resolved_keys[key] = current_keys

                    if f"{key_path}/@target" not in mapping:
                        collector.collect_and_log(
                            key_path,
                            ValidationProblem.MissingTargetAttribute,
                            value["link"],
                        )
                        mapping[f"{key_path}/@target"] = value["link"]
                    else:
                        attr_target = mapping[f"{key_path}/@target"]
                        remove_from_not_visited(f"{key_path}/@target")
                        target_path = value["link"]
                        if attr_target != target_path:
                            collector.collect_and_log(
                                key_path,
                                ValidationProblem.TargetAttributeMismatch,
                                attr_target,
                                target_path,
                            )

        return resolved_keys

    def handle_field(node: NexusNode, keys: Mapping[str, Any], prev_path: str):
        full_path = f"{prev_path}/{node.name}"
        variants = get_variations_of(node, keys)
        if (
            not variants
            and node.optionality == "required"
            and node.type in missing_type_err
        ):
            collector.collect_and_log(full_path, missing_type_err.get(node.type), None)
            return

        for variant in variants:
            variant_path = remove_from_not_visited(f"{prev_path}/{variant}")

            if (
                isinstance(keys[variant], Mapping)
                and not all(k.startswith("@") for k in keys[variant])
                and not list(keys[variant].keys()) == ["compress", "strength"]
            ):
                # A field should not have a dict of keys that are _not_ all attributes,
                # i.e. there should be no sub-fields or sub-groups.
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
                        ValidationProblem.AttributeForNonExistingConcept,
                        "field",
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

            check_reserved_suffix(variant_path, mapping)
            check_reserved_prefix(variant_path, mapping, "field")

            # Check unit category
            if node.unit is not None:
                unit_path = remove_from_not_visited(f"{variant_path}/@units")
                if f"{variant}@units" not in keys and (
                    node.unit != "NX_TRANSFORMATION"
                    or mapping.get(f"{variant_path}/@transformation_type")
                    in ("translation", "rotation")
                ):
                    if node.unit != "NX_UNITLESS":
                        collector.collect_and_log(
                            variant_path,
                            ValidationProblem.MissingUnit,
                            node.unit,
                        )

                else:
                    unit = keys.get(f"{variant}@units")
                    # Special case: NX_TRANSFORMATION unit depends on `@transformation_type` attribute
                    if (
                        transformation_type := keys.get(
                            f"{variant}@transformation_type"
                        )
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
        full_path = f"{prev_path}/@{node.name}"
        variants = get_variations_of(node, keys)

        if (
            not variants
            and node.optionality == "required"
            and node.type in missing_type_err
        ):
            collector.collect_and_log(full_path, missing_type_err.get(node.type), None)
            return

        for variant in variants:
            variant_path = remove_from_not_visited(
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
            check_reserved_prefix(variant_path, mapping, "attribute")

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

                    score = get_nx_namefit(
                        instance_name, node.name, name_any, name_partial
                    )
                    if score > -1:
                        best_match = node

        return best_match

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

        if isinstance(mapping[key], Mapping) and "link" in mapping[key]:
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
                    return
                break  # We found the suffix and it passed

        return

    def check_reserved_prefix(
        key: str,
        mapping: MutableMapping[str, Any],
        nx_type: Literal["group", "field", "attribute"],
    ):
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
            return

        name = key.rsplit("/", 1)[-1]

        if not name.startswith(tuple(prefixes)):
            return  # Irrelevant prefix, no check needed

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
                return
            if allowed_context == "all":
                # We can freely use this prefix everywhere.
                return

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
                return

        return

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

    for not_visited_key in not_visited:
        if mapping.get(not_visited_key) is None:
            # This value is not really set. Skip checking its validity.
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
            parent_key = not_visited_key.rsplit("/", 1)[0]
            if (parent_key := not_visited_key.rsplit("/", 1)[0]) not in mapping.keys():
                # check that parent is not a group
                node = add_best_matches_for(not_visited_key.rsplit("/", 1)[0], tree)

                remove_attr = False

                if node is None:
                    collector.collect_and_log(
                        parent_key,
                        ValidationProblem.AttributeForNonExistingConcept,
                        "group or field",
                    )
                    remove_attr = True
                elif node.type != "group":
                    collector.collect_and_log(
                        parent_key,
                        ValidationProblem.AttributeForNonExistingConcept,
                        "field",
                    )
                    remove_attr = True

                if remove_attr:
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
        if key in mapping:
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
