#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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
"""Helper functions commonly used by the convert routine."""

import json
import logging
import os
import re
from collections.abc import Mapping, MutableMapping, Sequence
from datetime import datetime, timezone
from enum import Enum, auto
from functools import cache
from typing import Any, Literal, Optional, Union, cast

import h5py
import lxml.etree as ET
import numpy as np
from ase.data import chemical_symbols

from pynxtools import get_nexus_version, get_nexus_version_hash
from pynxtools.dataconverter.chunk import COMPRESSION_FILTERS

# TODO: nxdl_utils is legacy XML-walking infrastructure. These imports should be
# removed as helpers.py XML-walking functions are replaced by NexusNode-based equivalents.
from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    get_enums,  # TODO: remove, only used by deprecated is_value_valid_element_of_enum
    get_inherited_nodes,  # TODO: remove, only used by deprecated get_all_defined_required_children
    get_node_at_nxdl_path,  # TODO: remove, only used by deprecated check_for_optional_parent, is_node_required
)
from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    get_required_string as nexus_get_required_string,  # TODO: remove, only used by deprecated functions
)
from pynxtools.nexus.nexus_tree import (
    NexusAttribute,
    NexusChoice,
    NexusField,
    NexusGroup,
    NexusLink,
    NexusNode,
    generate_tree_from,
)
from pynxtools.nexus.utils import (
    # moved to pynxtools.nexus.utils, backwards compatibility
    # TODO: remove backwards-compatibility shim in future releases
    ISO8601,
    NEXUS_TO_PYTHON_DATA_TYPES,
    RESERVED_PREFIXES,
    RESERVED_SUFFIXES,
    get_all_parents_for,
    get_appdef_root,
    get_nxdl_root_and_path,
    is_appdef,
    is_variadic,
    nx_bool,
    nx_char,
    nx_float,
    nx_int,
    nx_number,
    remove_namespace_from_tag,
    strip_nx_prefix,
)

logger = logging.getLogger("pynxtools")

import importlib.metadata

from pynxtools.dataconverter.chunk import CHUNK_CONFIG_DEFAULT


def get_pynxtools_version() -> str:
    """Attempt getting the version of pynxtools at runtime with fallback."""
    # for a discussion whether to collect at build or runtime see
    # https://discuss.python.org/t/please-make-package-version-go-away/58501
    try:
        return f"{importlib.metadata.version('pynxtools')}"
    except importlib.metadata.PackageNotFoundError:
        return f"unknown_version"


class ValidationProblem(Enum):
    DifferentVariadicNodesWithTheSameName = auto()
    UnitWithoutDocumentation = auto()
    InvalidUnit = auto()
    InvalidEnum = auto()
    OpenEnumWithCustom = auto()
    OpenEnumWithCustomFalse = auto()
    OpenEnumWithMissingCustom = auto()
    MissingRequiredGroup = auto()
    MissingRequiredField = auto()
    MissingRequiredAttribute = auto()
    InvalidType = auto()
    InvalidDatetime = auto()
    IsNotPosInt = auto()
    ExpectedGroup = auto()
    ExpectedField = auto()
    MissingDocumentation = auto()
    MissingUnit = auto()
    ChoiceValidationError = auto()
    UnitWithoutField = auto()
    AttributeForNonExistingConcept = auto()
    BrokenLink = auto()
    MissingTargetAttribute = auto()
    TargetAttributeMismatch = auto()
    FailedNamefitting = auto()
    NXdataMissingSignalData = auto()
    NXdataMissingAxisData = auto()
    NXdataOutdatedConvention = auto()
    NXdataNoConvention = auto()
    NXdataAxisMismatch = auto()
    KeyToBeRemoved = auto()
    InvalidConceptForNonVariadic = auto()
    ReservedSuffixWithoutField = auto()
    ReservedPrefixInWrongContext = auto()
    InvalidNexusTypeForNamedConcept = auto()
    KeysWithAndWithoutConcept = auto()
    InvalidCompressionFilter = auto()
    InvalidCompressionStrength = auto()
    CompressionStrengthZero = auto()
    MissingNXclass = auto()
    ExternalLinkedFileNotFound = auto()
    SymbolSizeMismatch = auto()


class Collector:
    """A class to collect data and return it in a dictionary format."""

    def __init__(self):
        self.data: dict[str, set] = {
            "warning_and_error": set(),
            "info": set(),
        }

        self.logging = True

    def _log(self, path: str, log_type: ValidationProblem, value: Any | None, *args):
        if value is None:
            value = "<unknown>"

        if log_type == ValidationProblem.DifferentVariadicNodesWithTheSameName:
            value = cast(Any, value)
            logger.warning(
                f"Instance name '{path}' used for multiple different concepts: "
                f"{', '.join(sorted({c for c, _ in value}))}. "
                f"The following keys are affected: {', '.join(sorted({k for _, k in value}))}."
            )
        if log_type == ValidationProblem.UnitWithoutDocumentation:
            logger.info(f"The unit {path} = {value} has no documentation.")
        if log_type == ValidationProblem.InvalidUnit:
            value = cast(Any, value)
            log_text = f"The unit '{args[0]}' at {path} does not match with the unit category {value.unit} of '{value.name}'."
            if len(args) == 2 and args[1] is not None:
                log_text += f" Based on the 'transformation_type' of the field {path.replace('/@units', '')}, it should match with '{args[1]}'."
            logger.warning(log_text)

        elif log_type == ValidationProblem.InvalidEnum:
            logger.warning(
                f"The value '{args[0]}' at {path} should be one of the following: {value}."
            )
        elif log_type == ValidationProblem.OpenEnumWithCustom:
            logger.info(
                f"The value '{args[0]}' at {path} does not match with the enumerated items from the open enumeration: {value}."
            )
        elif log_type == ValidationProblem.OpenEnumWithCustomFalse:
            logger.warning(
                f"The value '{args[0]}' at {path} does not match with the enumerated items from the open enumeration: {value}. "
                "When a different value is used, the boolean 'custom' attribute cannot be False."
            )
        elif log_type == ValidationProblem.OpenEnumWithMissingCustom:
            log_text = (
                f"The value '{args[0]}' at {path} does not match with the enumerated items from the open enumeration: {value}. "
                "When a different value is used, a boolean 'custom=True' attribute must be added."
            )
            if args[1] is True:
                log_text += " It was added here automatically."
                logger.info(log_text)
            else:
                logger.warning(log_text)
        elif log_type == ValidationProblem.MissingRequiredGroup:
            logger.warning(f"The required group {path} hasn't been supplied.")
        elif log_type == ValidationProblem.MissingRequiredField:
            logger.warning(f"The required field {path} hasn't been supplied.")
        elif log_type == ValidationProblem.MissingRequiredAttribute:
            logger.warning(f"The required attribute {path} hasn't been supplied.")
        elif log_type == ValidationProblem.InvalidType:
            logger.warning(
                f"The value at {path} should be one of the following Python types: {value}"
                f", as defined in the NXDL as {args[0] if args else '<unknown>'}."
            )
        elif log_type == ValidationProblem.InvalidDatetime:
            logger.warning(
                f"The value at {path} = {value} should be a timezone aware ISO8601 "
                "formatted str. For example, 2022-01-22T12:14:12.05018Z"
                " or 2022-01-22T12:14:12.05018+00:00."
            )
        elif log_type == ValidationProblem.IsNotPosInt:
            logger.warning(
                f"The value at {path} should be a positive int, but is {value}."
            )
        elif log_type == ValidationProblem.ExpectedGroup:
            logger.error(f"Expected a group at {path}, but found a field or attribute.")
        elif log_type == ValidationProblem.ExpectedField:
            logger.error(f"Expected a field at {path}, but found a group.")
        elif log_type == ValidationProblem.MissingDocumentation:
            if "@" in path.rsplit("/", maxsplit=1)[-1]:
                logger.warning(f"Attribute {path} has no documentation.")
            else:
                logger.warning(f"Field {path} has no documentation.")
        elif log_type == ValidationProblem.MissingUnit:
            logger.warning(
                f"Field {path} requires a unit in the unit category {value}."
            )
        elif log_type == ValidationProblem.UnitWithoutField:
            logger.warning(f"Unit {path} in dataset without its field {value}.")
        elif log_type == ValidationProblem.AttributeForNonExistingConcept:
            logger.warning(
                f"There were attributes set for the {value} {path}, "
                f"but the {value} does not exist."
            )
        elif log_type == ValidationProblem.BrokenLink:
            logger.warning(f"Broken link at {path} to {value}.")
        elif log_type == ValidationProblem.MissingTargetAttribute:
            log_text = (
                f"A link was used for {path}, but no '@target' attribute was found."
            )
            logger.warning(log_text)
        elif log_type == ValidationProblem.TargetAttributeMismatch:
            logger.warning(
                f"A link was used for {path}, but its @target attribute '{value}' "
                f"does not match with the link's target '{args[0]}'."
            )
        elif log_type == ValidationProblem.FailedNamefitting:
            logger.warning(f"Found no namefit of {path} in {value}.")
        elif log_type == ValidationProblem.NXdataMissingSignalData:
            logger.warning(f"Missing data for signal in {path}.")
        elif log_type == ValidationProblem.NXdataMissingAxisData:
            logger.warning(f"Missing data for @axes in {path}.")
        elif log_type == ValidationProblem.NXdataAxisMismatch:
            logger.warning(
                f"Length of axis {path} does not match to {value} in dimension {args[0]}"
            )
        elif log_type == ValidationProblem.NXdataOutdatedConvention:
            logger.warning(
                f"NXdata group {path} uses version {value} for defining the plottable data. "
                "This is discouraged; consider updating to v3."
            )
        elif log_type == ValidationProblem.NXdataNoConvention:
            logger.warning(
                f"NXdata group {path} does not use any of the existing versions (v3/v2/v1) for "
                "defining the plottable data."
            )

        elif log_type == ValidationProblem.KeyToBeRemoved:
            logger.warning(f"The {value} {path} will not be written.")
        elif log_type == ValidationProblem.InvalidConceptForNonVariadic:
            value = cast(Any, value)
            log_text = f"Given {value.nx_type} name '{path}' conflicts with the non-variadic name '{value}'"
            if value.nx_type == "group":
                log_text += f", which should be of type {value.nx_class}."
            logger.warning(log_text)
        elif log_type == ValidationProblem.ReservedSuffixWithoutField:
            logger.warning(
                f"Reserved suffix '{args[0]}' was used in {path}, but there is no associated field {value}."
            )
        elif log_type == ValidationProblem.ReservedPrefixInWrongContext:
            log_text = f"Reserved prefix {path} was used in {args[0] if args else '<unknown>'}, but is not valid in {value}."
            # Note that value=None" gets converted to "<unknown>"
            if args[1]:
                log_text += f" It is only valid in the context of {args[1] if args else '<unknown>'}."
            logger.error(log_text)
        elif log_type == ValidationProblem.InvalidNexusTypeForNamedConcept:
            value = cast(Any, value)
            logger.error(
                f"The type ('{args[0] if args else '<unknown>'}') of '{path}' "
                f"conflicts with the concept {value.get_path()}, which "
                f"is of type '{value.nx_type}'."
            )
        elif log_type == ValidationProblem.KeysWithAndWithoutConcept:
            value = cast(Any, value)
            logger.warning(
                f"The key '{path}' uses the valid concept name '{args[0]}', but there is another valid key {value} that uses the non-variadic name of the node.'"
            )
        elif log_type == ValidationProblem.CompressionStrengthZero:
            value = cast(dict, value)
            logger.info(
                f"Compression strength for {path} is 0. The value '{value['compress']}' will be written effectively uncompressed."
            )
        elif log_type == ValidationProblem.InvalidCompressionFilter:
            value = cast(dict, value)
            logger.warning(
                f"Compression filter for {path} is not any of {COMPRESSION_FILTERS}."
            )
        elif log_type == ValidationProblem.InvalidCompressionStrength:
            value = cast(dict, value)
            logger.warning(
                f"Compression strength for {path} = {value} should be between 0 and 9."
            )
        elif log_type == ValidationProblem.MissingNXclass:
            logger.info(
                f"Group '{path}' does not have an NX_class attribute and will therefore not be validated."
            )
        elif log_type == ValidationProblem.ExternalLinkedFileNotFound:
            logger.warning(f"Linked external file '{value}' for {path} was not found.")
        elif log_type == ValidationProblem.SymbolSizeMismatch:
            field_to_size: dict[str, int] = args[0]
            details = ", ".join(
                f"'{field}': size {size}"
                for field, size in sorted(field_to_size.items())
            )
            logger.warning(
                f"Inconsistent dimensions for NXDL symbol '{value}' in group '{path}': {details}."
            )

    def collect_and_log(
        self,
        path: str,
        log_type: ValidationProblem,
        value: Any | None,
        *args,
        **kwargs,
    ):
        """Inserts a path into the data dictionary and logs the action."""
        if log_type == ValidationProblem.MissingUnit and value in (
            "NX_UNITLESS",
            "NX_DIMENSIONLESS",
            "NX_ANY",
        ):
            return

        message: str = path + str(log_type) + str(value)

        # info messages should not fail validation
        if log_type in (
            ValidationProblem.UnitWithoutDocumentation,
            ValidationProblem.CompressionStrengthZero,
            ValidationProblem.MissingNXclass,
            ValidationProblem.OpenEnumWithCustom,
            ValidationProblem.OpenEnumWithMissingCustom,
        ):
            if self.logging and message not in self.data["info"]:
                self._log(path, log_type, value, *args, **kwargs)
            self.data["info"].add(message)
        else:
            if self.logging and message not in self.data["warning_and_error"]:
                self._log(path, log_type, value, *args, **kwargs)
            self.data["warning_and_error"].add(message)

    def has_validation_problems(self) -> bool:
        """Returns True if there were any validation problems."""
        return len(self.data["warning_and_error"]) > 0

    def get(self):
        """Returns the set of problematic paths."""
        return self.data["warning_and_error"]

    def clear(self):
        """Clears the collected data."""
        self.data: dict[str, set] = {
            "warning_and_error": set(),
            "info": set(),
        }


collector = Collector()


def is_a_lone_group(xml_element) -> bool:
    """Checks whether a given group XML element has no field or attributes mentioned.

    .. deprecated::
        TODO: not used anymore, remove in future release.
    """
    if xml_element.get("type") == "NXentry":
        return False
    for child in xml_element.findall(".//"):
        if remove_namespace_from_tag(child.tag) in ("field", "attribute"):
            return False
    return True


def get_nxdl_name_from_elem(xml_element) -> str:
    """Extracts the name or uses the type to remove the NX bit and use as name.

    .. deprecated::
        Use ``NexusNode.name`` directly.
        TODO: removed, only called in deprecated get_all_defined_required_children_for_elem.
    """
    name_to_add = ""
    if "name" in xml_element.attrib:
        name_to_add = xml_element.attrib["name"]
    elif "type" in xml_element.attrib:
        name_to_add = (
            f"{convert_nexus_to_caps(xml_element.attrib['type'])}"
            f"[{convert_nexus_to_suggested_name(xml_element.attrib['type'])}]"
        )
    return name_to_add


def get_nxdl_name_for(xml_elem: ET._Element) -> str | None:
    """Get the name of the element from the NXDL element.

    For an entity having a name this is just the name.
    For groups it is the uppercase type without NX, e.g. "ENTRY" for "NXentry".

    .. deprecated::
        Use ``NexusNode.name`` directly.
        TODO: remove, not used anymore.

    Args:
        xml_elem (ET._Element): The xml element to get the name for.

    Returns:
        Optional[str]:
            The name of the element.
            None if the xml element has no name or type attribute.
    """
    if "name" in xml_elem.attrib:
        return xml_elem.attrib["name"]
    if "type" in xml_elem.attrib:
        return convert_nexus_to_caps(xml_elem.attrib["type"])
    return None


def get_all_defined_required_children_for_elem(xml_element):
    """Gets all possible inherited required children for a given NXDL element.

    .. deprecated::
        Use ``NexusNode`` children filtered by ``optionality == "required"`` instead.
        TODO: remove when removed deprecated callers.
    """
    list_of_children_to_add = set()
    for child in xml_element:
        tag = remove_namespace_from_tag(child.tag)
        if tag not in ("group", "field", "attribute"):
            continue
        child.set("nxdlbase_class", xml_element.get("nxdlbase_class"))
        if child.attrib and get_required_string(child) == "required":
            tag = remove_namespace_from_tag(child.tag)

            name_to_add = get_nxdl_name_from_elem(child)

            if tag in ("field", "attribute"):
                name_to_add = f"@{name_to_add}" if tag == "attribute" else name_to_add
                list_of_children_to_add.add(name_to_add)
                if tag == "field" and (
                    "units" in child.attrib.keys()
                    and child.attrib["units"] != "NX_UNITLESS"
                ):
                    list_of_children_to_add.add(f"{name_to_add}/@units")
            elif tag == "group":
                nxdlpath = (
                    f"{xml_element.get('nxdlpath')}/{get_nxdl_name_from_elem(child)}"
                )
                nxdlbase = xml_element.get("nxdlbase")
                nx_name = nxdlbase[nxdlbase.rfind("/") + 1 : nxdlbase.rfind(".nxdl")]
                if nxdlpath not in visited_paths:
                    visited_paths.append(nxdlpath)
                    children = get_all_defined_required_children(nxdlpath, nx_name)
                    further_children = set()
                    for further_child in children:
                        further_children.add(f"{name_to_add}/{further_child}")
                    list_of_children_to_add.update(further_children)
    return list_of_children_to_add


visited_paths: list[str] = []


def get_all_defined_required_children(nxdl_path, nxdl_name):
    """Helper function to find all possible inherited required children for an NXDL path.

    .. deprecated::
        Use ``NexusNode`` tree traversal with ``optionality == "required"`` instead.
        TODO: remove, not used anymore
    """
    if nxdl_name == "NXtest":
        return []

    elem_list = get_inherited_nodes(nxdl_path, nx_name=nxdl_name)[2]
    list_of_children_to_add = set()
    for elem in elem_list:
        list_of_children_to_add.update(get_all_defined_required_children_for_elem(elem))

    return list_of_children_to_add


def add_inherited_children(list_of_children_to_add, path, nxdl_root, template):
    """Takes a list of child names and appends them to template for a given path.

    .. deprecated::
        TODO: remove, not used anymore.
    """
    for child in list_of_children_to_add:
        child_path = f"{path}/{child}"
        if child_path not in template.keys():
            optional_parent = check_for_optional_parent(child_path, nxdl_root)
            optionality = (
                "required" if optional_parent == "<<NOT_FOUND>>" else "optional"
            )
            template[optionality][f"{path}/{child}"] = None
    return template


def _node_template_segment(node: NexusNode) -> str:
    """Return the template path segment string for a single NexusNode."""
    if isinstance(node, NexusAttribute) or node.nx_type == "attribute":
        return f"@{node.name}"
    # NexusGroup or NexusField
    if node.variadic:
        return f"{node.name}[{node.name.lower()}]"
    return node.name


def _walk_nexus_tree_for_template(
    node: NexusNode,
    template,
    parent_path: str,
    opt_parent_path: str | None = None,
) -> None:
    """Recursively populate *template* by walking a NexusNode tree.

    *opt_parent_path* is the template path of the nearest optional/recommended
    ancestor, propagated downward so that required children under optional parents
    are correctly marked optional in the template.
    """
    for child in node.children:
        if isinstance(child, NexusChoice):
            _walk_nexus_tree_for_template(child, template, parent_path, opt_parent_path)
            continue

        segment = _node_template_segment(child)
        path = f"{parent_path}/{segment}"

        if isinstance(child, (NexusField, NexusAttribute)):
            optionality = child.optionality or "optional"
            if optionality == "required" and opt_parent_path is not None:
                optionality = "optional"
                template.optional_parents.append(opt_parent_path)
            template[optionality][path] = None
            if (
                isinstance(child, NexusField)
                and getattr(child, "unit", None)
                and child.unit != "NX_UNITLESS"
            ):
                template[optionality][f"{path}/@units"] = None
            _walk_nexus_tree_for_template(child, template, path, opt_parent_path)

        elif isinstance(child, NexusGroup):
            has_descendants = any(
                isinstance(desc, (NexusField, NexusAttribute))
                for desc in child.descendants
            )
            is_lone = not has_descendants and child.nx_class != "NXentry"
            if is_lone:
                optionality = child.optionality or "optional"
                if optionality == "required" and opt_parent_path is not None:
                    optionality = "optional"
                    template.optional_parents.append(opt_parent_path)
                template[optionality][path] = None
                template["lone_groups"].append(path)

            child_opt_parent = opt_parent_path
            if child.optionality in ("optional", "recommended"):
                child_opt_parent = path
            _walk_nexus_tree_for_template(child, template, path, child_opt_parent)

        elif isinstance(child, NexusLink):
            template["optional"][path] = {"link": child.target}


def generate_template_from_nxdl(
    root, template, path="", nxdl_root=None, nxdl_name=None
):
    """Generate a template dictionary for the given NXDL definition using NexusNode.

    The first positional argument *root* must be the XML root element of the NXDL
    definition (as returned by ``get_nxdl_root_and_path``).  The remaining arguments
    are accepted for backward compatibility but are ignored.
    """
    nxdl_name = root.attrib["name"]
    tree = generate_tree_from(nxdl_name)
    _walk_nexus_tree_for_template(tree, template, path)


def get_required_string(elem):
    """Return nicely formatted optionality string for an NXDL XML element.

    .. deprecated::
        Use ``NexusNode.optionality`` instead.
        TODO: remove once all callers (including nexus.py HandleNexus) are migrated.
    """
    return nexus_get_required_string(elem)[2:-2].lower()


def convert_nexus_to_caps(nexus_name: str) -> str:
    """Convert a NeXus class name like ``"NXentry"`` to its uppercase concept ``"ENTRY"``.

    Thin wrapper around :func:`~pynxtools.nexus.utils.strip_nx_prefix`.

    TODO: use strip_nx_prefix consistently throughout
    """
    return strip_nx_prefix(nexus_name)


def _contains_uppercase(field_name: str | None) -> bool:
    """Return True if *field_name* contains any uppercase character."""
    if field_name is None:
        return False
    return any(char.isupper() for char in field_name)


def convert_nexus_to_suggested_name(nexus_name: str) -> str:
    """Suggest an HDF5 instance name from a NeXus class name.

    .. deprecated::
        TODO: remove together with get_nxdl_name_from_elem.
    """
    if _contains_uppercase(nexus_name):
        return nexus_name
    return nexus_name[2:]


def _convert_data_converter_entry_to_nxdl_path_entry(entry) -> str | None:
    """
    Helper function to convert data converter style entry to NXDL style entry:
    ENTRY[entry] -> ENTRY
    """
    regex = re.compile(r"(.*?)(?=\[)")
    results = regex.search(entry)
    return entry if results is None else results.group(1)


def _convert_nxdl_path_entry_to_data_converter_entry(entry) -> str:
    """
    Helper function to convert NXDL style entry to data converter style entry:
    ENTRY -> ENTRY[entry]
    """
    return f"{entry}[{entry.lower()}]"


def convert_nxdl_path_dict_to_data_converter_dict(path) -> str:
    """
    Helper function to convert NXDL style path to data converter style path:
    /ENTRY/entry -> /ENTRY[entry]/entry
    """
    data_converter_path = ""
    for entry in path.split("/")[1:]:
        if not _contains_uppercase(entry) or entry.startswith("@"):
            data_converter_path += f"/{entry}"
            continue
        data_converter_path += "/" + _convert_nxdl_path_entry_to_data_converter_entry(
            entry
        )
    return data_converter_path


def convert_data_converter_dict_to_nxdl_path(path) -> str:
    """
    Helper function to convert data converter style path to NXDL style path:
    /ENTRY[entry]/sample -> /ENTRY/sample
    """
    nxdl_path = ""
    for entry in path.split("/")[1:]:
        nxdl_path += "/" + _convert_data_converter_entry_to_nxdl_path_entry(entry)
    return nxdl_path


def get_name_from_data_dict_entry(entry: str) -> str:
    """Helper function to get entry name from data converter style entry

    ENTRY[entry] -> entry
    """

    @cache
    def get_regex():
        return re.compile(r"(?<=\[)(.*?)(?=\])")

    results = get_regex().search(entry)
    if results is None:
        return entry

    if entry[0] == "@":
        name = results.group(1)
        return name if name.startswith("@") else "@" + name
    return results.group(1)


def convert_data_dict_path_to_hdf5_path(path) -> str:
    """Helper function to convert data converter style path to HDF5 style path

    /ENTRY[entry]/sample -> /entry/sample
    """
    hdf5path = ""
    for entry in path.split("/")[1:]:
        hdf5path += "/" + get_name_from_data_dict_entry(entry)
    return hdf5path


def is_value_valid_element_of_enum(value, elem_list) -> tuple[bool, list]:
    """Checks whether a value has to be specific from the NXDL enumeration and returns options.

    .. deprecated::
        Use ``NexusNode.items`` and ``NexusNode.open_enum`` directly.
        TODO: remove, not used anymore
    """
    for elem in elem_list:
        enums = get_enums(elem)
        if enums is not None:
            return value in enums, enums
    return True, []


def is_valid_data_type(value: Any, accepted_types: Sequence) -> bool:
    """Checks whether the given value or its children are of an accepted type."""

    if not isinstance(value, np.ndarray):
        value = np.array(value)
    # Handle 'object' dtype separately (for lists from HDF5 files)
    if value.dtype == np.dtype("O"):
        return all(
            isinstance(v.decode() if isinstance(v, bytes) else v, tuple(accepted_types))
            for v in value.flat
        )

    return any(np.issubdtype(value.dtype, dtype) for dtype in accepted_types)


def is_valid_data_type_hdf(hdf_node: h5py.Dataset, accepted_types: Sequence) -> bool:
    """Checks whether the given value or its children are of an accepted type."""
    if hdf_node.dtype != np.dtype("O"):
        # standard numeric / fixed dtypes
        return any(np.issubdtype(hdf_node.dtype, t) for t in accepted_types)

    # handle 'object' dtype separately (for lists from HDF5 files)
    return all(
        isinstance(v.decode() if isinstance(v, bytes) else v, tuple(accepted_types))
        for v in np.asarray(hdf_node[...].flat)
    )


def is_positive_int(value: Any) -> bool:
    """Checks whether the given value or its children are positive."""

    if not isinstance(value, np.ndarray):
        value = np.array(value)
    return bool(np.all(value > 0))


def is_positive_int_hdf(hdf_node: h5py.Dataset) -> bool:
    """Checks whether values in hdf_node are all positive."""
    if hdf_node.dtype.kind in "iu":
        if hdf_node.chunks is not None:
            # chunked storage irrespective if compressed or not
            for chunk in hdf_node.iter_chunks():
                if (hdf_node[chunk] > 0).all():
                    continue
                else:
                    return False
            return True
        else:
            # contiguous storage can never be compressed
            # typically fastest but reading all data at once
            return bool(np.all(hdf_node[...] > 0))
    return False


def convert_str_to_bool_safe(value: str) -> bool | None:
    """Only returns True or False if someone mistakenly adds quotation marks but mean a bool.

    For everything else it raises a ValueError.
    """
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise ValueError(f"Could not interpret string '{value}' as boolean.")


def convert_int_to_float(value):
    """
    Converts int-like values to float, including values in arrays, and lists

    Args:
        value: The input value, which can be a single value, list, or numpy array.

    Returns:
        The input value with all int-like values converted to float.
    """
    if isinstance(value, int):
        return float(value)
    elif isinstance(value, list):
        return [convert_int_to_float(v) for v in value]
    elif isinstance(value, tuple):
        return tuple(convert_int_to_float(v) for v in value)
    elif isinstance(value, set):
        return {convert_int_to_float(v) for v in value}
    elif isinstance(value, np.ndarray) and np.issubdtype(value.dtype, np.integer):
        return value.astype(float)
    elif isinstance(value, np.generic) and np.issubdtype(type(value), np.integer):
        return float(value)
    else:
        return value


def is_valid_data_field(value: Any, nxdl_type: str, path: str) -> Any:
    """Checks whether a given value is valid according to the type defined in the NXDL."""

    def validate_data_value(value: Any, nxdl_type: str, path: str) -> Any:
        """Validate and possibly convert a primitive value according to NXDL type rules."""
        accepted_types = NEXUS_TO_PYTHON_DATA_TYPES[nxdl_type]
        original_value = value

        # Do not count other dicts as they represent a link value
        if not isinstance(value, dict):
            # Attempt type conversion
            if accepted_types[0] is bool and isinstance(value, str):
                try:
                    value = convert_str_to_bool_safe(value)
                except (ValueError, TypeError):
                    value = original_value
            elif accepted_types[0] is float:
                value = convert_int_to_float(value)

            if not is_valid_data_type(value, accepted_types):
                collector.collect_and_log(
                    path, ValidationProblem.InvalidType, accepted_types, nxdl_type
                )

        # Type-specific validation
        if nxdl_type == "NX_POSINT" and not is_positive_int(value):
            collector.collect_and_log(path, ValidationProblem.IsNotPosInt, value)

        if nxdl_type in ("ISO8601", "NX_DATE_TIME"):
            results = ISO8601.search(decode_if_bytes(value))
            if results is None:
                collector.collect_and_log(
                    path, ValidationProblem.InvalidDatetime, value
                )

        return value

    if isinstance(value, dict) and "compress" in value:
        compressed_value = value["compress"]
        if "filter" in value:
            if value["filter"] not in COMPRESSION_FILTERS:
                collector.collect_and_log(
                    path, ValidationProblem.InvalidCompressionFilter, value
                )
        if "strength" in value:
            if not (1 <= value["strength"] <= 9):
                if value["strength"] == 0:
                    collector.collect_and_log(
                        path, ValidationProblem.CompressionStrengthZero, value
                    )
                else:
                    collector.collect_and_log(
                        path, ValidationProblem.InvalidCompressionStrength, value
                    )

        # Apply standard validation to compressed value
        value["compress"] = validate_data_value(compressed_value, nxdl_type, path)

        return value

    return validate_data_value(value, nxdl_type, path)


def is_valid_data_field_hdf(hdf_node: h5py.Dataset, nxdl_type: str, path: str):
    """Checks whether value of hdf_node is valid according to the type defined in the NXDL."""
    # validating i.e. reading only not converting !
    accepted_types = NEXUS_TO_PYTHON_DATA_TYPES[nxdl_type]

    if not is_valid_data_type_hdf(hdf_node, accepted_types):
        collector.collect_and_log(
            path, ValidationProblem.InvalidType, accepted_types, nxdl_type
        )

    # type-specific validation
    if nxdl_type == "NX_POSINT" and not is_positive_int_hdf(hdf_node):
        collector.collect_and_log(
            path, ValidationProblem.IsNotPosInt, hdf_node[(0,) * hdf_node.ndim]
        )

    if nxdl_type in ("ISO8601", "NX_DATE_TIME"):
        if h5py.check_string_dtype(hdf_node.dtype) is not None and hdf_node.shape == ():
            value = decode_if_bytes(hdf_node[()])
            results = ISO8601.search(value)
            if results is None:
                collector.collect_and_log(
                    path, ValidationProblem.InvalidDatetime, value
                )


def get_custom_attr_path(path: str) -> str:
    """
    Generate the path for the 'custom' attribute for open enumerations for a
    given path.

    If a NeXus concept has an open enumeration and a different value than the suggested ones are used,

    - for fields, an attribute @custom=True.
    - for attributes, an additional attribute @my_attribute_custom=True (where my_attribute is the name
      of the attribute with the open enumeration)

    shall be added to the file. This function creates the path for this custom attribute.

    Args:
        path (str): The original path string.

    Returns:
        str: The modified path string representing the custom attribute path.
    """
    if path.rsplit("/", maxsplit=1)[-1].startswith("@"):
        attr_name = path.rsplit("/", maxsplit=1)[-1][1:]  # remove "@"
        return f"{path}_custom"
    return f"{path}/@custom"


def is_valid_enum(
    value: Any,
    nxdl_enum: list,
    nxdl_enum_open: bool,
    path: str,
    mapping: MutableMapping,
):
    """Validate a value against an NXDL enumeration and handle custom attributes.

    This function checks whether a given value conforms to the specified NXDL
    enumeration. If the enumeration is open (`nxdl_enum_open`), it may create or
    check a corresponding custom attribute in the `mapping`.

    Args:
        value (Any): The value to validate.
        nxdl_enum (list): The NXDL enumeration to validate against.
        nxdl_enum_open (bool): Whether the enumeration is open to custom values.
        path (str): The path of the value in the dataset.
        mapping (MutableMapping): The object (dict or HDF5 group) holding custom attributes.

    """

    if isinstance(value, dict) and "compress" in value:
        value = value["compress"]

    if nxdl_enum is not None:
        if (
            isinstance(value, np.ndarray)
            and isinstance(nxdl_enum, list)
            and isinstance(nxdl_enum[0], list)
        ):
            enum_value = list(value)
        else:
            enum_value = value

        if enum_value not in nxdl_enum:
            if nxdl_enum_open:
                custom_path = get_custom_attr_path(path)

                if isinstance(mapping, (h5py.Group, h5py.Dataset)):
                    # HDF5 object passed directly — the custom attr lives on its own attrs.
                    # custom_path is like "/entry/field/@attr_custom" or "/entry/field/@custom";
                    # only the last component (after the final "@") matters.
                    attr_name = custom_path.rsplit("@", 1)[-1]
                    custom_attr = decode_if_bytes(mapping.attrs.get(attr_name))
                    custom_added_auto = False
                else:
                    custom_attr = mapping.get(custom_path)
                    custom_added_auto = True

                if custom_attr == True:  # noqa: E712
                    collector.collect_and_log(
                        path,
                        ValidationProblem.OpenEnumWithCustom,
                        nxdl_enum,
                        value,
                    )
                elif custom_attr == False:  # noqa: E712
                    collector.collect_and_log(
                        path,
                        ValidationProblem.OpenEnumWithCustomFalse,
                        nxdl_enum,
                        value,
                    )

                elif custom_attr is None:
                    try:
                        mapping[custom_path] = True
                    except (ValueError, TypeError):
                        # HDF5 objects are read-only during validation.
                        # Custom attribute cannot be set.
                        pass
                    collector.collect_and_log(
                        path,
                        ValidationProblem.OpenEnumWithMissingCustom,
                        nxdl_enum,
                        value,
                        custom_added_auto,
                    )
            else:
                collector.collect_and_log(
                    path, ValidationProblem.InvalidEnum, nxdl_enum, value
                )


def is_valid_enum_hdf(
    hdf_node: h5py.Dataset,
    nxdl_enum: list,
    nxdl_enum_open: bool,
    path: str,
    mapping: MutableMapping,
):
    """Validate a value in hdf_node against an NXDL enumeration and handle custom attributes.

    This function checks whether a given value conforms to the specified NXDL
    enumeration. If the enumeration is open (`nxdl_enum_open`), it may create or
    check a corresponding custom attribute in the `mapping`.

    Args:
        dataset (h5py.Dataset): The HDF5 dataset whose value(s) to validate.
        nxdl_enum (list): The NXDL enumeration to validate against.
        nxdl_enum_open (bool): Whether the enumeration is open to custom values.
        path (str): The path of the value in the dataset.
        mapping (MutableMapping): The object (dict or HDF5 group) holding custom attributes.
    """

    if nxdl_enum is not None:
        value = decode_if_bytes(hdf_node[()])
        if (
            isinstance(value, np.ndarray)
            and isinstance(nxdl_enum, list)
            and isinstance(nxdl_enum[0], list)
        ):
            enum_value = list(value)
        else:
            enum_value = value

        if enum_value not in nxdl_enum:
            if nxdl_enum_open:
                custom_path = get_custom_attr_path(path)

                if isinstance(mapping, h5py.Group):
                    parent_path, attr_name = custom_path.rsplit("@", 1)
                    custom_attr = mapping.get(parent_path).attrs.get(attr_name)
                    custom_added_auto = False
                else:
                    custom_attr = mapping.get(custom_path)
                    custom_added_auto = True

                if custom_attr == True:  # noqa: E712
                    collector.collect_and_log(
                        path,
                        ValidationProblem.OpenEnumWithCustom,
                        nxdl_enum,
                        value,
                    )
                elif custom_attr == False:  # noqa: E712
                    collector.collect_and_log(
                        path,
                        ValidationProblem.OpenEnumWithCustomFalse,
                        nxdl_enum,
                        value,
                    )
                elif custom_attr is None:
                    try:
                        mapping[custom_path] = True
                    except ValueError:
                        # we are in the HDF5 validation, cannot set custom attribute.
                        pass
                    collector.collect_and_log(
                        path,
                        ValidationProblem.OpenEnumWithMissingCustom,
                        nxdl_enum,
                        value,
                        custom_added_auto,
                    )
            else:
                collector.collect_and_log(
                    path, ValidationProblem.InvalidEnum, nxdl_enum, value
                )


def split_class_and_name_of(name: str) -> tuple[str | None, str]:
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


def check_reserved_suffix(
    path: str,
    mapping: Mapping[str, Any],
) -> None:
    """
    Check if an associated field exists for a key with a reserved suffix.

    Reserved suffixes imply the presence of an associated base field (e.g.,
    "temperature_errors" implies "temperature" must exist in the mapping).

    Parameters
    ----------
    path : str
        The full path in the HDF5 file (e.g., "/entry1/sample/temperature_errors").
    mapping : Mapping[str, Any]
        A mapping of sibling names (keys) to values/datasets.
    """
    parent_path, name = path.rsplit("/", 1)
    concept_name, instance_name = split_class_and_name_of(name)

    for suffix in RESERVED_SUFFIXES:
        if instance_name.endswith(suffix):
            associated_field = instance_name.rsplit(suffix, 1)[0]
            if associated_field not in mapping:
                if not any(
                    k.startswith(parent_path)
                    and (k.endswith((associated_field, f"[{associated_field}]")))
                    for k in mapping
                ):
                    collector.collect_and_log(
                        path,
                        ValidationProblem.ReservedSuffixWithoutField,
                        associated_field,
                        suffix,
                    )
                    return
            break  # Found suffix, and it passed


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
    prefixes = RESERVED_PREFIXES.get(nx_type)
    if not prefixes or not appdef_name:
        return

    name = path.rsplit("/", 1)[-1]

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
                appdef_name,
                path,
                None,
            )
            return
        if allowed_context == "all":
            # We can freely use this prefix everywhere.
            return

        if allowed_context != appdef_name:
            collector.collect_and_log(
                prefix,
                ValidationProblem.ReservedPrefixInWrongContext,
                appdef_name,
                path,
                allowed_context,
            )
            return


@cache
def path_in_data_dict(nxdl_path: str, data_keys: tuple[str, ...]) -> list[str]:
    """Checks if there is an accepted variation of path in the dictionary & returns the path."""
    found_keys = []
    for key in data_keys:
        if nxdl_path == convert_data_converter_dict_to_nxdl_path(key):
            found_keys.append(key)
    return found_keys


def check_for_optional_parent(path: str, nxdl_root: ET._Element) -> str:
    """Finds a parent in the branch that is optional and returns its path or <<NOT_FOUND>>.

    .. deprecated::
        Use NexusNode parent chain with ``optionality`` checks instead.
        TODO: remove together with only caller ``add_inherited_children``
    """
    parent_path = path.rsplit("/", 1)[0]

    if parent_path == "":
        return "<<NOT_FOUND>>"

    parent_nxdl_path = convert_data_converter_dict_to_nxdl_path(parent_path)
    elem = get_node_at_nxdl_path(nxdl_path=parent_nxdl_path, elem=nxdl_root)

    if nexus_get_required_string(elem) in ("<<OPTIONAL>>", "<<RECOMMENDED>>"):
        return parent_path

    return check_for_optional_parent(parent_path, nxdl_root)


def is_node_required(nxdl_key, nxdl_root):
    """Checks whether a node at given nxdl path is required.

    .. deprecated::
        Use ``NexusNode.optionality == "required"`` instead.
        TODO: remove together with only caller ``all_required_children_are_set``
    """
    if nxdl_key[nxdl_key.rindex("/") + 1 :] == "@units":
        return False
    if nxdl_key[nxdl_key.rindex("/") + 1] == "@":
        nxdl_key = (
            nxdl_key[0 : nxdl_key.rindex("/") + 1]
            + nxdl_key[nxdl_key.rindex("/") + 2 :]
        )
    node = get_node_at_nxdl_path(nxdl_key, elem=nxdl_root, exc=False)
    return nexus_get_required_string(node) == "<<REQUIRED>>"


def all_required_children_are_set(optional_parent_path, data, nxdl_root):
    """Walks over optional parent's children and makes sure all required ones are set.

    .. deprecated::
        Use NexusNode tree traversal with optionality checks instead.
        TODO: remove, not called anymore
    """
    for key in data:
        if key in data["lone_groups"]:
            continue
        nxdl_key = convert_data_converter_dict_to_nxdl_path(key)
        name = nxdl_key[nxdl_key.rfind("/") + 1 :]
        renamed_path = f"{optional_parent_path}/{name}"
        if (
            nxdl_key[: nxdl_key.rfind("/")]
            == convert_data_converter_dict_to_nxdl_path(optional_parent_path)
            and is_node_required(nxdl_key, nxdl_root)
            and (renamed_path not in data or data[renamed_path] is None)
        ):
            return False

    return True


def is_nxdl_path_a_child(nxdl_path: str, parent: str):
    """Takes an NXDL path for an element and an NXDL parent and confirms it is a child.

    .. deprecated::
        Use NexusNode parent-child relations via anytree instead.
        TODO: remove, not called anymore
    """
    while nxdl_path.rfind("/") != -1:
        nxdl_path = nxdl_path[0 : nxdl_path.rfind("/")]
        if parent == nxdl_path:
            return True
    return False


def is_group_part_of_path(path_to_group: str, path_of_entry: str) -> bool:
    """Returns true if a group is contained in a path.

    .. deprecated::
        TODO: remove together with only caller ``does_group_exist``
    """
    tokens_group = path_to_group.split("/")
    tokens_entry = convert_data_converter_dict_to_nxdl_path(path_of_entry).split("/")

    if len(tokens_entry) < len(tokens_group):
        return False

    for tog, toe in zip(tokens_group, tokens_entry):
        if tog != toe:
            return False

    return True


def does_group_exist(path_to_group, data):
    """Returns True if the group or any children are set.

    .. deprecated::
        TODO: remove, not called anymore
    """
    path_to_group = convert_data_converter_dict_to_nxdl_path(path_to_group)
    for path in data:
        if is_group_part_of_path(path_to_group, path) and data[path] is not None:
            return True
    return False


def get_concept_basepath(path: str) -> str:
    """Get the concept path from the path.

    .. deprecated::
        Use ``NexusNode.concept_path`` instead.
        TODO: remove, not called anymore
    """
    path_list = path.split("/")
    concept_path = []
    for p in path_list:
        if re.search(r"[A-Z]", p):
            concept_path.append(p)
    return "/" + "/".join(concept_path)


def get_first_group(root):
    """Helper function to get the actual first group element from the NXDL.

    .. deprecated::
        Use ``generate_tree_from`` to build a NexusNode tree instead of walking raw NXDL XML.
        TODO: remove, not called anymore
    """
    for child in root:
        if remove_namespace_from_tag(child.tag) == "group":
            return child
    return root


def check_for_valid_atom_types(atoms: str | list):
    """Check for whether atom exists in periodic table."""

    if isinstance(atoms, list):
        for elm in atoms:
            if elm not in chemical_symbols[1:]:
                logger.warning(
                    f"The element {elm} is not found in the periodic table, "
                    f"check for correct element name"
                )
    elif isinstance(atoms, str):
        if atoms not in chemical_symbols[1:]:
            logger.warning(
                f"The element {atoms} is not found in the periodic table, "
                f"check for correct element name"
            )


def convert_to_hill(atoms_typ):
    """Convert list of atom into to hill."""
    if not isinstance(atoms_typ, list) and isinstance(atoms_typ, set):
        atoms_typ = list(atoms_typ)
    atoms_typ = sorted(atoms_typ)
    atom_list = []
    if "C" in atoms_typ:
        atom_list.append("C")
    if "H" in atoms_typ:
        atom_list.append("H")
    if atom_list:
        for char in atom_list:
            atoms_typ.remove(char)
    return atom_list + list(atoms_typ)


def add_default_root_attributes(data, filename, append: bool = False):
    """
    Takes a dict/Template and adds NXroot fields/attributes that are inherently available
    """

    def update_and_warn(key: str, value: str):
        if key in data and data[key] != value:
            logger.warning(
                f"The NXroot entry '{key}' (value: {data[key]}) should not be changed by "
                f"the reader. This is overwritten by the actually used value '{value}'"
            )
        data[key] = value

    update_and_warn("/@NX_class", "NXroot")
    update_and_warn("/@file_name", filename)
    update_and_warn("/@file_time", str(datetime.now(timezone.utc).astimezone()))
    update_and_warn("/@file_update_time", data["/@file_time"])
    update_and_warn(
        "/@NeXus_repository",
        "https://github.com/FAIRmat-NFDI/nexus_definitions/"
        f"blob/{get_nexus_version_hash()}",
    )
    update_and_warn("/@NeXus_release", get_nexus_version())
    update_and_warn("/@HDF5_Version", ".".join(map(str, h5py.h5.get_libversion())))
    update_and_warn("/@h5py_version", h5py.__version__)
    update_and_warn("/@creator", "pynxtools")
    update_and_warn("/@creator_version", get_pynxtools_version())
    if append:
        update_and_warn("/@append_mode", "True")


def write_nexus_def_to_entry(data, entry_name: str, nxdl_def: str):
    """
    Writes the used nexus definition and version to /ENTRY/definition
    """

    def update_and_warn(key: str, value: str, overwrite=False):
        if key in data and data[key] is not None and data[key] != value:
            report = (
                f"This is overwritten by the actually used value '{data[key]}'"
                if overwrite
                else f"The provided version '{data[key]}' is kept. We assume you know what you are doing."
            )
            logger.log(
                logging.WARNING if overwrite else logging.INFO,
                f"The entry '{key}' (value: {value}) should not be changed by "
                f"the reader. {report}",
            )
        if overwrite or data.get(key) is None:
            data[key] = value

    update_and_warn(f"/ENTRY[{entry_name}]/definition", nxdl_def, overwrite=True)
    update_and_warn(
        f"/ENTRY[{entry_name}]/definition/@version",
        get_nexus_version(),
        overwrite=False,
    )
    update_and_warn(
        f"/ENTRY[{entry_name}]/definition/@URL",
        "https://github.com/FAIRmat-NFDI/nexus_definitions/"
        f"blob/{get_nexus_version_hash()}",
        overwrite=False,
    )


def extract_atom_types(formula, mode="hill"):
    """Extract atom types form chemical formula."""
    atom_types: set = set()
    element: str = ""

    for char in formula:
        if char.isalpha():
            if char.isupper() and element == "":
                element = char
            elif char.isupper() and element != "" and element.isupper():
                check_for_valid_atom_types(element)
                atom_types.add(element)
                element = char
            elif char.islower() and element.isupper():
                element = element + char
                check_for_valid_atom_types(element)
                atom_types.add(element)
                element = ""

        else:
            if element.isupper():
                check_for_valid_atom_types(element)
                atom_types.add(element)
            element = ""
    if element.isupper():
        atom_types.add(element)

    atom_types = list(atom_types)
    atom_types = sorted(atom_types)

    if mode == "hill":
        return convert_to_hill(atom_types)

    return atom_types


# pylint: disable=too-many-branches
def transform_to_intended_dt(str_value: Any) -> Any | None:
    """Transform string to the intended data type, if not then return str_value.

    E.g '2.5E-2' will be transformed into 2.5E-2
    tested with: '2.4E-23', '28', '45.98', 'test', ['59', '3.00005', '498E-34'],
                 '23 34 444 5000', None
    with result: 2.4e-23, 28, 45.98, test, [5.90000e+01 3.00005e+00 4.98000e-32],
                 np.array([23 34 444 5000]), None
    NOTE: add another arg in this func for giving 'hint' what kind of data like
        numpy array or list
    Parameters
    ----------
    str_value : str
        Data from other format that comes as string e.g. string of list.

    Returns
    -------
    Union[str, int, float, np.ndarray]
        Converted data type

    TODO: is this function used anywhere? if not, deprecate/remove
    """

    symbol_list_for_data_separation = [";", " "]
    transformed: Any = None

    if isinstance(str_value, list):
        try:
            transformed = np.array(str_value, dtype=np.float64)
            return transformed
        except ValueError:
            pass

    elif isinstance(str_value, np.ndarray):
        return str_value
    elif isinstance(str_value, str):
        try:
            transformed = int(str_value)
        except ValueError:
            try:
                transformed = float(str_value)
            except ValueError:
                if "[" in str_value and "]" in str_value:
                    transformed = json.loads(str_value)
        if transformed is not None:
            return transformed
        for sym in symbol_list_for_data_separation:
            if sym in str_value:
                parts = str_value.split(sym)
                modified_parts: list = []
                for part in parts:
                    part = transform_to_intended_dt(part)
                    if isinstance(part, int | float):
                        modified_parts.append(part)
                    else:
                        return str_value
                return transform_to_intended_dt(modified_parts)

    return str_value


def nested_dict_to_slash_separated_path(
    nested_dict: dict, flattened_dict: dict, parent_path=""
):
    """Convert nested dict into slash separated path upto certain level.

    .. deprecated::
        TODO: remove — no known callers outside this module.
    """
    sep = "/"

    for key, val in nested_dict.items():
        path = parent_path + sep + key
        if isinstance(val, dict):
            nested_dict_to_slash_separated_path(val, flattened_dict, path)
        else:
            flattened_dict[path] = val


def _decode_bytes_scalar(value: Any, encoding: str) -> Any:
    """Decode scalar byte-like values and keep all other scalars unchanged."""
    if isinstance(value, (bytes, np.bytes_)):
        return value.decode(encoding)
    return value


def _decode_bytes_recursive(value: Any, encoding: str) -> Any:
    """Recursively decode byte-like values in nested containers."""
    if isinstance(value, list):
        # TODO: For very large nested payloads this recursion can be expensive.
        # Revisit with a lower-overhead iterative/container-specialized path.
        return [_decode_bytes_recursive(item, encoding) for item in value]

    if isinstance(value, tuple):
        return tuple(_decode_bytes_recursive(item, encoding) for item in value)

    if isinstance(value, dict):
        return {k: _decode_bytes_recursive(v, encoding) for k, v in value.items()}

    return _decode_bytes_scalar(value, encoding)


def decode_if_bytes(value: Any, encoding: str = "utf-8") -> Any:
    """Decode text-like bytes to Python strings while preserving numeric types.

    This function is optimized for common scalar/ndarray paths and falls back to
    recursive decoding for nested Python containers.

    TODO: generally usable, move to ``nexus/utils.py``
    """
    if isinstance(value, np.ndarray):
        if value.dtype.kind == "S":
            return np.char.decode(value, encoding)
        if value.dtype.kind == "O":
            if value.size == 1:
                return _decode_bytes_recursive(value[0], encoding)
            return np.vectorize(_decode_bytes_recursive, otypes=[object])(
                value, encoding
            )
        return value

    return _decode_bytes_recursive(value, encoding)


def validate_data_dict(*args, **kwargs):
    """Backwards-compatibility shim.

    Defined here (rather than via the __init__.py monkey-patch) to break a circular
    import that arises when nexus.nexus_tree moved out of the dataconverter package:
      nexus.nexus_tree → dataconverter.helpers → dataconverter.__init__ → validation → nexus.nexus_tree

    .. deprecated::
        TODO: marked for deprecation, remove in future release.

    """
    from pynxtools.dataconverter.validation import validate_data_dict as _impl

    return _impl(*args, **kwargs)
