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

import hashlib
import json
import os
import os.path
import pickle
import re
import sys

# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union

import numpy as np

try:
    from nomad import utils
    from nomad.datamodel import EntryArchive, EntryMetadata
    from nomad.datamodel.data import EntryData
    from nomad.datamodel.metainfo.basesections import (
        BaseSection,
        Component,
        CompositeSystem,
        Entity,
        EntityReference,
        Instrument,
    )
    from nomad.datamodel.metainfo.eln import BasicEln
    from nomad.metainfo import (
        Attribute,
        Bytes,
        Datetime,
        Definition,
        MEnum,
        Package,
        Quantity,
        Section,
        SubSection,
    )
    from nomad.metainfo.data_type import (
        Bytes,
        Datatype,
        Datetime,
        Number,
        m_bool,
        m_complex128,
        m_float64,
        m_int,
        m_int64,
        m_str,
    )
    from nomad.metainfo.metainfo import resolve_variadic_name
    from nomad.utils import get_logger, strip
    from toposort import toposort_flatten
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

from pynxtools import get_definitions_url
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nexus_definitions_path
from pynxtools.nomad.utils import __REPLACEMENT_FOR_NX, __rename_nx_for_nomad

# __URL_REGEXP from
# https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
__URL_REGEXP = re.compile(
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
    r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"
    r'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
)

# noinspection HttpUrlsUsage
__XML_NAMESPACES = {"nx": "http://definition.nexusformat.org/nxdl/3.1"}

# TO DO the validation still show some problems. Most notably there are a few higher
# dimensional fields with non number types, which the metainfo does not support

__section_definitions: Dict[str, Section] = dict()

__logger = get_logger(__name__)

__BASESECTIONS_MAP: Dict[str, Any] = {
    __rename_nx_for_nomad("NXfabrication"): [Instrument],
    __rename_nx_for_nomad("NXsample"): [CompositeSystem],
    __rename_nx_for_nomad("NXsample_component"): [Component],
    __rename_nx_for_nomad("NXidentifier"): [EntityReference],
    # "object": BaseSection,
}


VALIDATE = False

__XML_PARENT_MAP: Dict[ET.Element, ET.Element]
__NX_DOC_BASES: Dict[str, str] = {
    "https://github.com/nexusformat/definitions.git": "https://manual.nexusformat.org/classes",
    "https://github.com/FAIRmat-NFDI/nexus_definitions.git": "https://fairmat-nfdi.github.io/nexus_definitions/classes",
}

__PACKAGE_NAME = "pynxtools.nomad.schema"
__GROUPING_NAME = "NeXus"

from nomad import utils

logger_ = utils.get_logger(__name__)


def get_nx_type(nx_type: str) -> Optional[Datatype]:
    """
    Get the nexus type by name
    """
    __NX_TYPES = {  # Primitive Types,  'ISO8601' is the only type not defined here
        "NX_COMPLEX": m_complex128,
        "NX_FLOAT": m_float64,
        "NX_CHAR": m_str,
        "NX_BOOLEAN": m_bool,
        "NX_INT": m_int64,
        "NX_UINT": m_int,
        "NX_NUMBER": m_float64,
        "NX_POSINT": m_int,
        "NX_BINARY": Bytes,
        "NX_DATE_TIME": Datetime,
    }

    if nx_type in __NX_TYPES:
        if nx_type in ("NX_UINT", "NX_POSINT"):
            return __NX_TYPES[nx_type](dtype=np.uint64).no_type_check().no_shape_check()
        return __NX_TYPES[nx_type]().no_type_check().no_shape_check()
    return None


class NXUnitSet:
    """
    maps from `NX_` token to dimensionality
    None -> disable dimensionality check
    '1' -> dimensionless quantities
    'transformation' -> Specially handled in metainfo
    """

    mapping: dict = {
        "NX_ANGLE": "[angle]",
        "NX_ANY": None,
        "NX_AREA": "[area]",
        "NX_CHARGE": "[charge]",
        "NX_COUNT": "1",
        "NX_CROSS_SECTION": "[area]",
        "NX_CURRENT": "[current]",
        "NX_DIMENSIONLESS": "1",
        "NX_EMITTANCE": "[length] * [angle]",
        "NX_ENERGY": "[energy]",
        "NX_FLUX": "1 / [time] / [area]",
        "NX_FREQUENCY": "[frequency]",
        "NX_LENGTH": "[length]",
        "NX_MASS": "[mass]",
        "NX_MASS_DENSITY": "[mass] / [volume]",
        "NX_MOLECULAR_WEIGHT": "[mass] / [substance]",
        "NX_PERIOD": "[time]",
        "NX_PER_AREA": "1 / [area]",
        "NX_PER_LENGTH": "1 / [length]",
        "NX_POWER": "[power]",
        "NX_PRESSURE": "[pressure]",
        "NX_PULSES": "1",
        "NX_SCATTERING_LENGTH_DENSITY": "1 / [area]",
        "NX_SOLID_ANGLE": "[angle] * [angle]",
        "NX_TEMPERATURE": "[temperature]",
        "NX_TIME": "[time]",
        "NX_TIME_OF_FLIGHT": "[time]",
        "NX_TRANSFORMATION": "transformation",
        "NX_UNITLESS": "1",
        "NX_VOLTAGE": "[energy] / [current] / [time]",
        "NX_VOLUME": "[volume]",
        "NX_WAVELENGTH": "[length]",
        "NX_WAVENUMBER": "1 / [length]",
    }

    @staticmethod
    def normalise(value: str) -> str:
        """
        Normalise the given token
        """
        value = value.upper()
        if not value.startswith("NX_"):
            value = "NX_" + value
        return value

    @staticmethod
    def is_nx_token(value: str) -> bool:
        """
        Check if a given token is one of NX tokens
        """
        return NXUnitSet.normalise(value) in NXUnitSet.mapping.keys()


def __to_camel_case(snake_str: str, upper: bool = False) -> str:
    """
    Take as input a snake case variable and return a camel case one
    """
    components = snake_str.split("_")

    if upper:
        return "".join(x.capitalize() for x in components)

    return components[0] + "".join(x.capitalize() for x in components[1:])


def __to_root(xml_node: ET.Element) -> ET.Element:
    """
    get the root element
    """
    elem = xml_node
    while True:
        parent = __XML_PARENT_MAP.get(elem)
        if parent is None:
            break
        elem = parent

    return elem


def __if_base(xml_node: ET.Element) -> bool:
    """
    retrieves the category from the root element
    """
    return __to_root(xml_node).get("category") == "base"


def __if_repeats(name: str, max_occurs: str) -> bool:
    repeats = any(char.isupper() for char in name) or max_occurs == "unbounded"

    if max_occurs.isdigit():
        repeats = repeats or int(max_occurs) > 1

    return repeats


def __if_template(name: Optional[str]) -> bool:
    return name is None or name.lower() != name


def __get_documentation_url(
    xml_node: ET.Element, nx_type: Optional[str]
) -> Optional[str]:
    """
    Get documentation url
    """
    if nx_type is None:
        return None

    anchor_segments = []
    if nx_type != "class":
        anchor_segments.append(nx_type)

    while True:
        nx_type = xml_node.get("type")
        if nx_type:
            nx_type = nx_type.replace("NX", "")
        segment = xml_node.get("name", nx_type)  # type: ignore
        anchor_segments.append(segment.replace("_", "-"))

        xml_parent = xml_node
        xml_node = __XML_PARENT_MAP.get(xml_node)
        if xml_node is None:
            break

    definitions_url = get_definitions_url()

    doc_base = __NX_DOC_BASES.get(
        definitions_url, "https://manual.nexusformat.org/classes"
    )
    nx_package = xml_parent.get("nxdl_base").split("/")[-1]
    anchor = "-".join([name.lower() for name in reversed(anchor_segments)])
    return f"{doc_base}/{nx_package}/{anchor_segments[-1]}.html#{anchor}"


def __to_section(name: str, **kwargs) -> Section:
    """
    Returns the 'existing' metainfo section for a given top-level nexus base-class name.

    This function ensures that sections for these base-classes are only created once.
    This allows to access the metainfo section even before it is generated from the base
    class nexus definition.
    """

    if name in __section_definitions:
        section = __section_definitions[name]
        section.more.update(**kwargs)
        return section

    section = Section(validate=VALIDATE, name=name, **kwargs)
    __section_definitions[name] = section

    return section


def __get_enumeration(xml_node: ET.Element) -> Optional[MEnum]:
    """
    Get the enumeration field from xml node
    """
    enumeration = xml_node.find("nx:enumeration", __XML_NAMESPACES)
    if enumeration is None:
        return None

    items = enumeration.findall("nx:item", __XML_NAMESPACES)

    return MEnum([value.attrib["value"] for value in items])


def __add_common_properties(xml_node: ET.Element, definition: Definition):
    """
    Adds general metainfo definition properties (e.g., deprecated, docs, optional, ...)
    from the given nexus XML node to the given metainfo definition.
    """
    xml_attrs = xml_node.attrib

    # Read properties from potential base section. Those are not inherited, but we
    # duplicate them for a nicer presentation
    if isinstance(definition, Section) and definition.base_sections:
        base_section = definition.base_sections[0]
        if base_section.description:
            definition.description = base_section.description
        if base_section.deprecated:
            definition.deprecated = base_section.deprecated
        if base_section.more:
            definition.more.update(**base_section.more)

    links = []
    doc_url = __get_documentation_url(xml_node, definition.more.get("nx_kind"))
    if doc_url:
        links.append(doc_url)

    doc = xml_node.find("nx:doc", __XML_NAMESPACES)
    if doc is not None and doc.text is not None:
        definition.description = strip(doc.text)
        links.extend(
            [match[0] for match in __URL_REGEXP.findall(definition.description)]
        )

    if links:
        definition.links = links

    for key, value in xml_attrs.items():
        if key == "deprecated":
            definition.deprecated = value
            continue
        if "nxdl_base" in key or "schemaLocation" in key:
            continue
        definition.more["nx_" + key] = value

    if "optional" not in xml_attrs:
        definition.more["nx_optional"] = __if_base(xml_node)


def __create_attributes(xml_node: ET.Element, definition: Union[Section, Quantity]):
    """
    Add all attributes in the given nexus XML node to the given
    Quantity or SubSection using the Attribute class (new mechanism).

    todo: account for more attributes of attribute, e.g., default, minOccurs
    """
    for attribute in xml_node.findall("nx:attribute", __XML_NAMESPACES):
        name = __rename_nx_for_nomad(attribute.get("name"), is_attribute=True)

        nx_enum = __get_enumeration(attribute)
        if nx_enum:
            nx_type = nx_enum
            nx_shape: List[str] = []
        else:
            nx_type = get_nx_type(attribute.get("type", "NX_CHAR"))  # type: ignore
            has_bound = False
            has_bound |= "minOccurs" in attribute.attrib
            has_bound |= "maxOccurs" in attribute.attrib
            if has_bound:
                nx_min_occurs = attribute.get("minOccurs", "0")  # type: ignore
                nx_max_occurs = attribute.get("maxOccurs", "*")  # type: ignore
                if nx_max_occurs == "unbounded":
                    nx_max_occurs = "*"
                nx_shape = [f"{nx_min_occurs}..{nx_max_occurs}"]
            else:
                nx_shape = []

        m_attribute = Attribute(
            name=name, variable=__if_template(name), shape=nx_shape, type=nx_type
        )

        for name, value in attribute.items():
            m_attribute.more[f"nx_{name}"] = value

        __add_common_properties(attribute, m_attribute)

        definition.attributes.append(m_attribute)


def __add_additional_attributes(definition: Definition):
    if "m_nx_data_path" not in definition.attributes:
        definition.attributes.append(
            Attribute(
                name="m_nx_data_path",
                variable=False,
                shape=[],
                type=str,
                description="This is a nexus template property. "
                "This attribute holds the actual path of the value in the nexus data.",
            )
        )

    if "m_nx_data_file" not in definition.attributes:
        definition.attributes.append(
            Attribute(
                name="m_nx_data_file",
                variable=False,
                shape=[],
                type=str,
                description="This is a nexus template property. "
                "This attribute holds the actual file name of the nexus data.",
            )
        )

    if isinstance(definition, Quantity):
        # TODO We should also check the shape of the quantity and the datatype as
        # the statistics are always mapping on float64 even if quantity values are ints
        if definition.type not in [np.float64, np.int64, np.uint64] and not isinstance(
            definition.type, Number
        ):
            return

        for nx_array_attr in [
            "nx_data_mean",
            "nx_data_var",
            "nx_data_min",
            "nx_data_max",
        ]:
            if nx_array_attr in definition.all_attributes:
                continue
            definition.attributes.append(
                Attribute(
                    name=nx_array_attr,
                    variable=False,
                    shape=[],
                    type=np.float64,
                    description="This is a NeXus template property. "
                    "This attribute holds specific statistics of the NeXus data array.",
                )
            )


def __create_field(xml_node: ET.Element, container: Section) -> Quantity:
    """
    Creates a metainfo quantity from the nexus field given as xml node.
    """
    xml_attrs = xml_node.attrib

    # name
    assert "name" in xml_attrs, "Expecting name to be present"

    name = __rename_nx_for_nomad(xml_attrs["name"], is_field=True)

    # type
    nx_type = xml_attrs.get("type", "NX_CHAR")
    nx_nomad_type = get_nx_type(nx_type)
    if nx_nomad_type is None:
        raise NotImplementedError(
            f"Type {nx_type} is not supported for the moment for {name}."
        )

    # enumeration
    enum_type = __get_enumeration(xml_node)

    # dimensionality
    nx_dimensionality = xml_attrs.get("units", None)
    if nx_dimensionality:
        if nx_dimensionality not in NXUnitSet.mapping:
            raise NotImplementedError(
                f"Unit {nx_dimensionality} is not supported for {name}."
            )
        dimensionality = NXUnitSet.mapping[nx_dimensionality]
    else:
        dimensionality = None

    # shape
    shape: list = []
    nx_shape: list = []
    dimensions = xml_node.find("nx:dimensions", __XML_NAMESPACES)
    if dimensions is not None:
        for dimension in dimensions.findall("nx:dim", __XML_NAMESPACES):
            dimension_value: str = dimension.attrib.get("value", "0..*")
            nx_shape.append(dimension_value)

    value_quantity: Quantity = None  # type: ignore

    # copy from base to inherit from it
    if container.base_sections is not None:
        base_quantity: Quantity = container.base_sections[0].all_quantities.get(name)
        if base_quantity:
            value_quantity = base_quantity.m_copy(deep=True)
            value_quantity.attributes.clear()

    # create quantity
    if value_quantity is None:
        value_quantity = Quantity(name=name, flexible_unit=True)

    value_quantity.variable = __if_template(name)

    # check parent type compatibility
    parent_type = getattr(value_quantity, "type", None)
    if not isinstance(parent_type, MEnum):
        # if parent type is not MEnum then overwrite whatever given
        value_quantity.type = enum_type if enum_type else nx_nomad_type
    elif enum_type:
        # only when derived type is also MEnum to allow overwriting
        value_quantity.type = enum_type

    value_quantity.dimensionality = dimensionality
    value_quantity.shape = shape
    value_quantity.more.update(
        dict(nx_kind="field", nx_type=nx_type, nx_shape=nx_shape)
    )

    __add_common_properties(xml_node, value_quantity)

    container.quantities.append(value_quantity)

    __create_attributes(xml_node, value_quantity)

    return value_quantity


def __create_group(xml_node: ET.Element, root_section: Section):
    """
    Adds all properties that can be generated from the given nexus group XML node to
    the given (empty) metainfo section definition.
    """
    __create_attributes(xml_node, root_section)

    for group in xml_node.findall("nx:group", __XML_NAMESPACES):
        xml_attrs = group.attrib

        assert "type" in xml_attrs, "Expecting type to be present"
        nx_type = __rename_nx_for_nomad(xml_attrs["type"])

        nx_name = xml_attrs.get("name", nx_type.upper())
        section_name = __rename_nx_for_nomad(nx_name, is_group=True)
        group_section = Section(validate=VALIDATE, nx_kind="group", name=section_name)

        __attach_base_section(group_section, root_section, __to_section(nx_type))
        __add_common_properties(group, group_section)

        nx_name = xml_attrs.get(
            "name", nx_type.replace(__REPLACEMENT_FOR_NX, "").upper()
        )
        subsection_name = __rename_nx_for_nomad(nx_name, is_group=True)
        group_subsection = SubSection(
            section_def=group_section,
            nx_kind="group",
            name=subsection_name,
            repeats=__if_repeats(nx_name, xml_attrs.get("maxOccurs", "0")),
            variable=__if_template(nx_name),
        )

        root_section.inner_section_definitions.append(group_section)

        root_section.sub_sections.append(group_subsection)

        __create_group(group, group_section)

    for field in xml_node.findall("nx:field", __XML_NAMESPACES):
        __create_field(field, root_section)


def nexus_resolve_variadic_name(
    definitions: dict,
    name: str,
    hint: Optional[str] = None,
    filter: Optional[Section] = None,
):
    """
    Resolves a variadic name from a set of possible definitions.

    Parameters:
        definitions (dict): A dictionary of sub-sections defining the search space.
            The keys are the names of the definitions, and the values are objects
            representing those definitions.
        name (str): The variadic name to resolve.
        hint (Optional[str]): An optional hint to refine the search.
        filter (Optional[Section]): A Section object used to filter the definitions
            by type. Only definitions inheriting from this section will be considered.

    Returns:
        str: The resolved name based on the provided definitions, filtered as needed.

    Raises:
        ValueError: If the `definitions` dictionary is empty or if the name cannot
            be resolved.

    Notes:
        - The `resolve_variadic_name` function is assumed to handle the core logic
          of resolving the name within the filtered definitions.
        - Filtering by `inherited_sections` ensures that only definitions related
          to the specified type are considered.
    """
    fitting_definitions = definitions
    if filter:
        fitting_definitions = {}
        for def_name, definition in definitions.items():
            if filter in definition.inherited_sections:
                fitting_definitions[def_name] = definition
    return resolve_variadic_name(fitting_definitions, name, hint)


def __attach_base_section(section: Section, container: Section, default: Section):
    """
    Potentially adds a base section to the given section, if the given container has
    a base-section with a suitable base.
    """
    try:
        base_section = nexus_resolve_variadic_name(
            container.all_inner_section_definitions, section.name, filter=default
        )
    except ValueError:
        base_section = None

    if base_section:
        assert base_section.nx_kind == section.nx_kind, "Base section has wrong kind"
    else:
        base_section = default

    section.base_sections = [base_section]


def __create_class_section(xml_node: ET.Element) -> Section:
    """
    Creates a metainfo section from the top-level nexus definition given as xml node.
    """
    xml_attrs = xml_node.attrib
    assert "name" in xml_attrs, "Expecting name to be present"
    assert "type" in xml_attrs, "Expecting type to be present"
    assert "category" in xml_attrs, "Expecting category to be present"

    nx_name = xml_attrs["name"]
    nx_type = xml_attrs["type"]
    nx_category = xml_attrs["category"]

    nx_name = __rename_nx_for_nomad(nx_name)
    class_section: Section = __to_section(
        nx_name, nx_kind=nx_type, nx_category=nx_category
    )

    nomad_base_sec_cls = __BASESECTIONS_MAP.get(nx_name, [BaseSection])

    if "extends" in xml_attrs:
        nx_base_sec = __to_section(__rename_nx_for_nomad(xml_attrs["extends"]))
        class_section.base_sections = [nx_base_sec] + [
            cls.m_def for cls in nomad_base_sec_cls
        ]

    __add_common_properties(xml_node, class_section)

    __create_group(xml_node, class_section)

    return class_section


def __find_cycles(graph):
    def dfs(node, visited, path):
        visited.add(node)
        path.append(node)

        for neighbor in graph.get(node, set()):
            if neighbor in path:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:]
                cycles.append(cycle)
            elif neighbor not in visited:
                dfs(neighbor, visited, path)

        path.pop()

    cycles = []
    visited = set()

    for node in graph:
        if node not in visited:
            dfs(node, visited, [])

    return cycles


def __sort_nxdl_files(paths):
    """
    Sort all definitions based on dependencies
    """

    name_node_map = {}
    name_dependency_map = {}
    for path in paths:
        for nxdl_file in os.listdir(path):
            if not nxdl_file.endswith(".nxdl.xml"):
                continue
            xml_node = ET.parse(os.path.join(path, nxdl_file)).getroot()
            xml_node.set("nxdl_base", path)
            assert xml_node.get("type") == "group", "definition is not a group"
            xml_name = xml_node.get("name")
            name_node_map[xml_name] = xml_node
            dependency_list = []
            if "extends" in xml_node.attrib:
                dependency_list.append(xml_node.get("extends"))
            for child in xml_node.iter():
                if child.tag.endswith("group") and child.get("type") != xml_name:
                    dependency_list.append(child.get("type"))
            name_dependency_map[xml_name] = set(dependency_list)

    # Find cycles and remove them
    cycles = __find_cycles(name_dependency_map)
    for cycle in cycles:
        name_dependency_map[cycle[-2]].remove(cycle[-1])

    # this sorting can be skipped one should create empty classes instead
    sorted_nodes = toposort_flatten(name_dependency_map)
    validated_names = []
    for node in sorted_nodes:
        if node in name_node_map:
            validated_names.append(name_node_map[node])
        else:
            parent_nodes = []
            for name, dependencies in name_dependency_map.items():
                if node in dependencies:
                    parent_nodes.append(name)
            __logger.error(
                "Missing dependency (incorrect group type).",
                target_name=node,
                used_by=parent_nodes,
            )

    return validated_names


def __add_section_from_nxdl(xml_node: ET.Element) -> Optional[Section]:
    """
    Creates a metainfo section from a nxdl file.
    """
    try:
        global __XML_PARENT_MAP  # pylint: disable=global-statement
        __XML_PARENT_MAP = {
            child: parent for parent in xml_node.iter() for child in parent
        }

        return __create_class_section(xml_node)

    except NotImplementedError as err:
        __logger.error(
            "Fail to generate metainfo.",
            target_name=xml_node.attrib["name"],
            exc_info=str(err),
        )
        return None


def __create_package_from_nxdl_directories(nexus_section: Section) -> Package:
    """
    Creates a metainfo package from the given nexus directory. Will generate the
    respective metainfo definitions from all the nxdl files in that directory.
    """
    package = Package(name=__PACKAGE_NAME)

    folder_list = ("base_classes", "contributed_definitions", "applications")
    paths = [
        os.path.join(get_nexus_definitions_path(), folder) for folder in folder_list
    ]

    sections = []
    for nxdl_file in __sort_nxdl_files(paths):
        section = __add_section_from_nxdl(nxdl_file)
        if section is not None:
            sections.append(section)
    sections.sort(key=lambda x: x.name)

    for section in sections:
        package.section_definitions.append(section)
        if section.nx_category == "application" or (
            section.nx_category == "base" and section.nx_name == "NXroot"
        ):
            nexus_section.sub_sections.append(
                SubSection(section_def=section, name=section.name)
            )

    return package


nexus_metainfo_package: Optional[Package] = None  # pylint: disable=C0103


def save_nexus_schema(suf):
    nexus_metainfo_package
    sch_dict = nexus_metainfo_package.m_to_dict()
    filehandler = open("nexus.obj" + suf, "wb")
    pickle.dump(sch_dict, filehandler)
    filehandler.close()


def load_nexus_schema(suf):
    global nexus_metainfo_package
    file = open("nexus.obj" + suf, "rb")
    sch_dict = pickle.load(file)
    file.close()
    nexus_metainfo_package = Package().m_from_dict(sch_dict)


def init_nexus_metainfo():
    """
    Initializes the metainfo package for the nexus definitions.
    """
    global nexus_metainfo_package  # pylint: disable=global-statement

    if nexus_metainfo_package is not None:
        return

    # We take the application definitions and create a common parent section that allows
    # to include nexus in an EntryArchive.
    nexus_section = Section(
        validate=VALIDATE, name=__GROUPING_NAME, label=__GROUPING_NAME
    )

    # try:
    #     load_nexus_schema('')
    # except Exception:
    #     nexus_metainfo_package = __create_package_from_nxdl_directories(nexus_section)
    #     try:
    #         save_nexus_schema('')
    #     except Exception:
    #         pass
    nexus_metainfo_package = __create_package_from_nxdl_directories(nexus_section)

    nexus_metainfo_package.section_definitions.append(nexus_section)

    # We need to initialize the metainfo definitions. This is usually done automatically,
    # when the metainfo schema is defined though MSection Python classes.
    nexus_metainfo_package.init_metainfo()

    # Add additional NOMAD specific attributes (nx_data_path, nx_data_file, nx_mean, ...)
    # This needs to be done in the right order, base sections first.
    visited_definitions = set()
    sections = list()
    for definition, _, _, _ in nexus_metainfo_package.m_traverse():
        if isinstance(definition, Section):
            for section in reversed([definition] + definition.all_base_sections):
                if section not in visited_definitions:
                    visited_definitions.add(section)
                    sections.append(section)

    for section in sections:
        if not (str(section).startswith("pynxtools.")):
            continue
        __add_additional_attributes(section)
        for quantity in section.quantities:
            __add_additional_attributes(quantity)

    # We skip the Python code generation for now and offer Python classes as variables
    # TO DO not necessary right now, could also be done case-by-case by the nexus parser
    python_module = sys.modules[__name__]
    for section in nexus_metainfo_package.section_definitions:  # pylint: disable=E1133
        setattr(python_module, section.name, section.section_cls)


init_nexus_metainfo()


def normalize_fabrication(self, archive, logger):
    """Normalizer for fabrication section."""
    current_cls = __section_definitions[
        __rename_nx_for_nomad("NXfabrication")
    ].section_cls
    super(current_cls, self).normalize(archive, logger)
    self.lab_id = "Hello"


def normalize_sample_component(self, archive, logger):
    """Normalizer for sample_component section."""
    current_cls = __section_definitions[
        __rename_nx_for_nomad("NXsample_component")
    ].section_cls
    if self.name__field:
        self.name = self.name__field
    if self.mass__field:
        self.mass = self.mass__field
    # we may want to add normalisation for mass_fraction (calculating from components)
    super(current_cls, self).normalize(archive, logger)


def normalize_sample(self, archive, logger):
    """Normalizer for sample section."""
    current_cls = __section_definitions[__rename_nx_for_nomad("NXsample")].section_cls
    if self.name__field:
        self.name = self.name__field
    # one could also copy local ids to identifier for search purposes
    super(current_cls, self).normalize(archive, logger)


def normalize_identifier(self, archive, logger):
    """Normalizer for identifier section."""

    def create_Entity(lab_id, archive, f_name):
        entitySec = Entity()
        entitySec.lab_id = lab_id
        entity = EntryArchive(
            data=entitySec,
            m_context=archive.m_context,
            metadata=EntryMetadata(
                entry_type="identifier", domain="nexus"
            ),  # upload_id=archive.m_context.upload_id,
        )
        with archive.m_context.raw_file(f_name, "w") as f_obj:
            json.dump(entity.m_to_dict(with_meta=True), f_obj)
            # json.dump(entity.m_to_dict(), f_obj)
        archive.m_context.process_updated_raw_file(f_name)

    def get_entry_reference(archive, f_name):
        """Returns a reference to data from entry."""
        from nomad.utils import hash

        upload_id = archive.metadata.upload_id
        entry_id = hash(upload_id, f_name)

        return f"/entries/{entry_id}/archive#/data"

    current_cls = __section_definitions[
        __rename_nx_for_nomad("NXidentifier")
    ].section_cls
    # super(current_cls, self).normalize(archive, logger)
    if self.identifier__field:
        logger.info(f"{self.identifier__field} - identifier received")
        self.lab_id = self.identifier__field  # + "__occurrence"
    EntityReference.normalize(self, archive, logger)
    if not self.reference:
        logger.info(f"{self.lab_id} to be created")
        f_name = re.split("([0-9a-zA-Z.]+)", self.lab_id)[1]
        if len(f_name) != len(self.lab_id):
            f_name = f_name + hashlib.md5(self.lab_id.encode()).hexdigest()
        f_name = f"{current_cls.__name__}_{f_name}.archive.json"
        create_Entity(self.lab_id, archive, f_name)
        self.reference = get_entry_reference(archive, f_name)
        logger.info(f"{self.reference} - referenced directly")


__NORMALIZER_MAP: Dict[str, Any] = {
    __rename_nx_for_nomad("NXfabrication"): normalize_fabrication,
    __rename_nx_for_nomad("NXsample"): normalize_sample,
    __rename_nx_for_nomad("NXsample_component"): normalize_sample_component,
    __rename_nx_for_nomad("NXidentifier"): normalize_identifier,
}

# Handling nomad BaseSection and other inherited Section from BaseSection
for nx_name, section in __section_definitions.items():
    if nx_name == "NXobject":
        continue

    normalize_func = __NORMALIZER_MAP.get(nx_name)

    # Append the normalize method from a function
    if normalize_func:
        section.section_cls.normalize = normalize_func
