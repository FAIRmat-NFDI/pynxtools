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
from typing import Any, Optional, Union

import h5py
import numpy as np
import pandas as pd
from ase import Atoms
from ase.data import atomic_numbers
from scipy.spatial import cKDTree
from toposort import toposort_flatten

try:
    from nomad.datamodel import EntryArchive, EntryMetadata
    from nomad.datamodel.data import ArchiveSection, EntryData, Schema
    from nomad.datamodel.metainfo import basesections
    from nomad.datamodel.metainfo.annotations import ELNAnnotation
    from nomad.datamodel.metainfo.basesections import (
        ActivityResult,
        ActivityStep,
        BaseSection,
        Component,
        CompositeSystem,
        CompositeSystemReference,
        Entity,
        EntityReference,
        InstrumentReference,
        Measurement,
    )
    from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
    from nomad.datamodel.metainfo.workflow import Link, Task, Workflow
    from nomad.datamodel.results import Material, Relation, Results, System
    from nomad.metainfo import (
        Attribute,
        Bytes,
        Datetime,
        Definition,
        MEnum,
        Package,
        Property,
        Quantity,
        SchemaPackage,
        Section,
        SubSection,
    )
    from nomad.metainfo.data_type import Datatype, Number
    from nomad.metainfo.metainfo import resolve_variadic_name
    from nomad.normalizing.common import nomad_atoms_from_ase_atoms
    from nomad.normalizing.topology import add_system, add_system_info
    from nomad.utils import get_logger, hash, strip

except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

from pynxtools import NX_DOC_BASES, get_definitions_url
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nexus_definitions_path
from pynxtools.nomad.utils import (
    FIELD_STATISTICS,
    NX_TYPES,
    REPLACEMENT_FOR_NX,
    _rename_nx_for_nomad,
    get_quantity_base_name,
)
from pynxtools.units import NXUnitSet, ureg

# URL_REGEXP from
# https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
URL_REGEXP = re.compile(
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
    r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"
    r'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
)

# noinspection HttpUrlsUsage
XML_NAMESPACES = {"nx": "http://definition.nexusformat.org/nxdl/3.1"}


# TO DO the validation still show some problems. Most notably there are a few higher
# dimensional fields with non number types, which the metainfo does not support

section_definitions: dict[str, Section] = dict()

logger_ = get_logger(__name__)


class NexusBaseSection(BaseSection):
    def normalize(self, archive, logger):
        if self.__dict__["nx_name"]:
            self.name = self.__dict__["nx_name"]
        super().normalize(archive, logger)


class NexusActivityStep(ActivityStep):
    reference = Quantity(
        type=ArchiveSection,
        description="A reference to a NeXus Activity Step.",
        a_eln=ELNAnnotation(
            component="ReferenceEditQuantity",
            label="section reference",
        ),
    )


class AnchoredReference(EntityReference):
    def normalize(self, archive, logger):
        def create_Entity(lab_id, archive, f_name, qunt_name):
            entitySec = Entity()
            entitySec.lab_id = lab_id
            entitySec.name = qunt_name
            entity = EntryArchive(
                data=entitySec,
                m_context=archive.m_context,
                metadata=EntryMetadata(
                    entry_type="identifier", domain="nexus", readonly=True
                ),
            )
            with archive.m_context.raw_file(f_name, "w") as f_obj:
                json.dump(entity.m_to_dict(with_meta=True), f_obj)
            archive.m_context.process_updated_raw_file(f_name)

        def get_entry_reference(archive, f_name):
            """Returns a reference to data from entry."""

            upload_id = archive.metadata.upload_id
            entry_id = hash(upload_id, f_name)
            return f"../uploads/{upload_id}/archive/{entry_id}#data"

        super().normalize(archive, logger)
        if not self.reference:
            lab_hash = hashlib.md5(self.lab_id.encode()).hexdigest()
            # skip any special characters e.g. /
            parent_concept = self.m_parent.m_def.name
            filter_name = re.split("([0-9a-zA-Z.]+)", self.name)[1]
            f_name = f"{parent_concept}_{filter_name}_{lab_hash}.archive.json"
            create_Entity(self.lab_id, archive, f_name, self.name)
            self.reference = get_entry_reference(archive, f_name)


class NexusIdentifiers(ArchiveSection):
    Nexus_identifiers = SubSection(
        section_def=AnchoredReference,
        repeats=True,
        description="These are the NOMAD references correspond to NeXus identifierNAME fields.",
    )

    def normalize(self, archive, logger):
        # Consider multiple identifiers exists in the same group/section
        def generate_anchored_reference_and_normalize(
            attr_obj, id_value, idname, is_full_storage=False
        ):
            """Generate anchored reference, connect to m quantities, and normalize."""
            field_n = idname.split("__field")[0]
            logger.info(f"Lab id {id_value} to be created")
            nx_id = AnchoredReference(lab_id=id_value, name=field_n)
            if not is_full_storage:
                nx_data_path = attr_obj.m_get_quantity_attribute(
                    idname, "m_nx_data_path"
                )
                nx_data_file = attr_obj.m_get_quantity_attribute(
                    idname, "m_nx_data_file"
                )
            else:
                nx_data_path = attr_obj.attributes.get("m_nx_data_path")
                nx_data_file = attr_obj.attributes.get("m_nx_data_file")

            nx_id.m_set_section_attribute("m_nx_data_path", nx_data_path)
            nx_id.m_set_section_attribute("m_nx_data_file", nx_data_file)

            self.Nexus_identifiers.append(nx_id)
            nx_id.normalize(archive, logger)

        identifiers = [
            key
            for key in self.__dict__.keys()
            if key.startswith("identifier") and key.endswith("__field")
        ]
        if identifiers:
            self.Nexus_identifiers = []
            for identifier in identifiers:
                if not (val := getattr(self, identifier)):
                    continue
                if isinstance(val, dict):
                    for idname, idobj in val.items():
                        generate_anchored_reference_and_normalize(
                            idobj, idobj.value, idname, True
                        )
                else:
                    generate_anchored_reference_and_normalize(self, val, identifier)
        super().normalize(archive, logger)


class NexusActivityResult(ActivityResult):
    reference = Quantity(
        type=ArchiveSection,
        description="A reference to a NeXus Activity Result.",
        a_eln=ELNAnnotation(
            component="ReferenceEditQuantity",
            label="section reference",
        ),
    )


class NexusMeasurement(Measurement, Schema, PlotSection):
    def normalize(self, archive, logger):
        try:
            app_entry = getattr(self, "ENTRY")
            if len(app_entry) < 1:
                raise AttributeError()
            self.steps = []
            for entry in app_entry:
                ref = NexusActivityStep(name=entry.name, reference=entry)
                if entry.start_time__field is not None:
                    if (self.datetime is None) or (
                        self.datetime > entry.start_time__field
                    ):
                        self.datetime = entry.start_time__field
                self.steps.append(ref)
                mapping = {
                    ActivityStep: (NexusActivityStep, self.steps),
                    basesections.Instrument: (InstrumentReference, self.instruments),
                    CompositeSystem: (CompositeSystemReference, self.samples),
                    ActivityResult: (NexusActivityResult, self.results),
                }
                for sec in entry.m_all_contents():
                    for cls, (ref_cls, collection) in mapping.items():
                        if isinstance(sec, cls):
                            collection.append(ref_cls(name=sec.name, reference=sec))
                            break
            if self.m_def.name == "Root":
                self.method = "Generic Experiment"
            else:
                self.method = self.m_def.name + " Experiment"
        except (AttributeError, TypeError):
            pass
        super(basesections.Activity, self).normalize(archive, logger)

        if archive.results.eln.methods is None:
            archive.results.eln.methods = []
        if self.method:
            archive.results.eln.methods.append(self.method)
        else:
            archive.results.eln.methods.append(self.m_def.name)
        if archive.workflow2 is None:
            archive.workflow2 = Workflow(name=self.name)
        # steps to tasks
        act_array = archive.workflow2.tasks
        existing_items = {(task.name, task.section) for task in act_array}
        new_items = [
            item.reference.to_task()
            for item in self.steps
            if (item.name, item) not in existing_items
        ]
        act_array.extend(new_items)
        # samples to inputs
        act_array = archive.workflow2.inputs
        existing_items = {(link.name, link.section) for link in act_array}
        new_items = [
            Link(name=item.name, section=item.reference)
            for item in self.samples
            if (item.name, item.reference) not in existing_items
        ]
        act_array.extend(new_items)

        # results to outputs
        act_array = archive.workflow2.outputs
        existing_items = {(link.name, link.section) for link in act_array}
        new_items = [
            Link(name=item.name, section=item.reference)
            for item in self.results
            if (item.name, item.reference) not in existing_items
        ]
        act_array.extend(new_items)


BASESECTIONS_MAP: dict[str, Any] = {
    "NXfabrication": [basesections.Instrument],
    "NXsample": [CompositeSystem],
    "NXsample_component": [Component],
    "NXobject": [NexusIdentifiers],
    "NXentry": [NexusActivityStep],
    "NXprocess": [NexusActivityStep],
    "NXdata": [NexusActivityResult],
}


VALIDATE = False
XML_PARENT_MAP: dict[ET.Element, ET.Element]

PACKAGE_NAME = "pynxtools.nomad.schema"


def get_nx_type(nx_type: str) -> Optional[Datatype]:
    """
    Get the nexus type by name
    """
    if nx_type in NX_TYPES:
        return NX_TYPES[nx_type]().no_type_check().no_shape_check()
    return None


# def _to_camel_case(snake_str: str, upper: bool = False) -> str:
#     """
#     Take as input a snake case variable and return a camel case one
#     """
#     components = snake_str.split("_")

#     if upper:
#         return "".join(x.capitalize() for x in components)

#     return components[0] + "".join(x.capitalize() for x in components[1:])


def _if_base(xml_node: ET.Element) -> bool:
    """
    retrieves the category from the root element
    """

    def to_root(xml_node: ET.Element) -> ET.Element:
        """
        get the root element
        """
        elem = xml_node
        while True:
            parent = XML_PARENT_MAP.get(elem)
            if parent is None:
                break
            elem = parent

        return elem

    return to_root(xml_node).get("category") == "base"


def _if_repeats(name: str, max_occurs: str) -> bool:
    repeats = any(char.isupper() for char in name) or max_occurs == "unbounded"

    if max_occurs.isdigit():
        repeats = repeats or int(max_occurs) > 1

    return repeats


def _if_template(name: Optional[str]) -> bool:
    return name is None or name.lower() != name


def _get_documentation_url(
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
        xml_node = XML_PARENT_MAP.get(xml_node)
        if xml_node is None:
            break

    definitions_url = get_definitions_url()

    doc_base = NX_DOC_BASES.get(
        definitions_url, "https://manual.nexusformat.org/classes"
    )
    nx_package = xml_parent.get("nxdl_base").split("/")[-1]
    anchor = "-".join([name.lower() for name in reversed(anchor_segments)])
    nx_file = anchor_segments[-1].replace("-", "_")
    return f"{doc_base}/{nx_package}/{nx_file}.html#{anchor}"


def nxdata_ensure_definition(
    self,
    def_or_name: Property | str,
    *,
    hint: str | None = None,
) -> Property:
    current_cls = section_definitions[f"{_rename_nx_for_nomad('NXdata')}"].section_cls
    if isinstance(def_or_name, str):
        # check enums for or actual values of signals and axes
        # TODO: also check symbol table dimensions
        acceptable_data: list[str] = []
        acceptable_axes: list[str] = []
        # set filter string according
        chk_name = def_or_name.split("_errors")[0]
        if chk_name in acceptable_data:
            filters = ["DATA"]
        elif chk_name in acceptable_axes:
            filters = ["AXISNAME"]
        else:
            filters = ["DATA", "AXISNAME", "FIELDNAME_errors"]
        # get the reduced options
        newdefinitions = {}
        for dname, definition in self.m_def.all_aliases:
            if dname not in filters:
                newdefinitions[dname] = definition
        # run the query
        definition = resolve_variadic_name(newdefinitions, def_or_name, hint)
        return definition
    return super(current_cls, self)._ensure_definition(
        def_or_name,
        hint,
    )


def to_section(name: str, **kwargs) -> Section:
    """
    Returns the 'existing' metainfo section for a given top-level nexus base-class name.

    This function ensures that sections for these base-classes are only created once.
    This allows to access the metainfo section even before it is generated from the base
    class nexus definition.
    """

    if name in section_definitions:
        section = section_definitions[name]
        section.more.update(**kwargs)
        return section

    section = Section(validate=VALIDATE, name=name, **kwargs)
    section_definitions[name] = section

    if name == "Data":
        section._ensure_defintion = nxdata_ensure_definition

    return section


def _get_enumeration(xml_node: ET.Element) -> tuple[Optional[MEnum], Optional[bool]]:
    """
    Get the enumeration field from xml node
    """
    enumeration = xml_node.find("nx:enumeration", XML_NAMESPACES)
    if enumeration is None:
        return None, None

    items = enumeration.findall("nx:item", XML_NAMESPACES)
    open_enum = (
        bool(enumeration.attrib["open"]) if "open" in enumeration.attrib else False
    )

    return MEnum([value.attrib["value"] for value in items]), open_enum


def _add_common_properties(xml_node: ET.Element, definition: Definition):
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
    doc_url = _get_documentation_url(xml_node, definition.more.get("nx_kind"))
    if doc_url:
        links.append(doc_url)

    doc = xml_node.find("nx:doc", XML_NAMESPACES)
    if doc is not None and doc.text is not None:
        definition.description = strip(doc.text)
        links.extend([match[0] for match in URL_REGEXP.findall(definition.description)])

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
        definition.more["nx_optional"] = _if_base(xml_node)


def _create_attributes(
    xml_node: ET.Element, definition: Union[Section, Quantity], field: Quantity = None
):
    """
    Add all attributes in the given nexus XML node to the given
    Quantity or SubSection using a specially named Quantity class.

    todo: account for more attributes of attribute, e.g., default, minOccurs
    """
    for attribute in xml_node.findall("nx:attribute", XML_NAMESPACES):
        name = _rename_nx_for_nomad(attribute.get("name"), is_attribute=True)

        # nameType
        nx_name_type = attribute.get("nameType", "specified")
        if nx_name_type == "any":
            name = name.upper()

        shape: list = []
        nx_enum, nx_enum_open = _get_enumeration(attribute)
        if nx_enum and not nx_enum_open:
            nx_type = nx_enum
            nx_shape: list[str] = []
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

        a_name = (field.more["nx_name"] if field else "") + "___" + name
        m_attribute = Quantity(
            name=a_name,
            variable=(_if_template(name) and (nx_name_type in ["any", "partial"]))
            or (field.variable if field else False),
            shape=shape,
            type=nx_type,
            flexible_unit=True,
        )
        m_attribute.more.update(
            dict(nx_kind="attribute")  # , nx_type=nx_type, nx_shape=nx_shape)
        )

        for name, value in attribute.items():
            m_attribute.more[f"nx_{name}"] = value

        _add_common_properties(attribute, m_attribute)
        # TODO: decide if stats/instancename should be made searchable for attributes, too
        # _add_quantity_stats(definition,m_attribute)

        definition.quantities.append(m_attribute)


def _add_quantity_stats(container: Section, quantity: Quantity):
    # TODO We should also check the shape of the quantity and the datatype as
    # the statistics are always mapping on float64 even if quantity values are ints
    if not quantity.name.endswith("__field"):
        return
    isvariadic = quantity.variable
    notnumber = quantity.type not in [
        np.float64,
        np.int64,
        np.uint64,
    ] and not isinstance(quantity.type, Number)
    if notnumber and not isvariadic:
        return
    basename = get_quantity_base_name(quantity.name)
    if isvariadic:
        container.quantities.append(
            Quantity(
                name=basename + "__name",
                variable=quantity.variable,
                shape=[],
                type=str,
                description="This is a NeXus template property. "
                "This quantity holds the instance name of a NeXus Field.",
            )
        )
    if notnumber:
        return
    for suffix, dtype in zip(
        FIELD_STATISTICS["suffix"][1:],
        FIELD_STATISTICS["type"][1:],
    ):
        container.quantities.append(
            Quantity(
                name=basename + suffix,
                variable=quantity.variable,
                shape=[],
                type=dtype if dtype else quantity.type,
                description="This is a NeXus template property. "
                "This quantity holds specific statistics of the NeXus data array.",
            )
        )


def _add_additional_attributes(definition: Definition, container: Section):
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
        _add_quantity_stats(container, definition)


def _create_field(xml_node: ET.Element, container: Section) -> Quantity:
    """
    Creates a metainfo quantity from the nexus field given as xml node.
    """
    xml_attrs = xml_node.attrib

    # name
    assert "name" in xml_attrs, "Expecting name to be present"
    name = _rename_nx_for_nomad(xml_attrs["name"], is_field=True)

    # nameType
    nx_name_type = xml_attrs.get("nameType", "specified")
    # if nx_name_type == "any":
    #     name = name.upper()

    # type
    nx_type = xml_attrs.get("type", "NX_CHAR")
    nx_nomad_type = get_nx_type(nx_type)
    if nx_nomad_type is None:
        raise NotImplementedError(
            f"Type {nx_type} is not supported for the moment for {name}."
        )

    # enumeration
    enum_type, nx_enum_open = _get_enumeration(xml_node)

    # dimensionality
    nx_dimensionality = xml_attrs.get("units", None)
    if nx_dimensionality:
        if nx_dimensionality == "NX_TRANSFORMATION":
            # TODO: Remove workaround for NX_TRANSFORMATTION
            nx_dimensionality = "NX_ANY"
        dimensionality = NXUnitSet.get_dimensionality(nx_dimensionality)
        if dimensionality is not None:
            dimensionality = str(dimensionality)
        elif nx_dimensionality != "NX_ANY":
            raise NotImplementedError(
                f"Unit {nx_dimensionality} is not supported for {name}."
            )
    else:
        dimensionality = None

    # shape
    shape: list = []
    nx_shape: list = []
    dimensions = xml_node.find("nx:dimensions", XML_NAMESPACES)
    if dimensions is not None:
        for dimension in dimensions.findall("nx:dim", XML_NAMESPACES):
            dimension_value: str = dimension.attrib.get("value", "0..*")
            nx_shape.append(dimension_value)

    value_quantity: Quantity = None  # type: ignore

    # copy from base to inherit from it
    if container.base_sections is not None and len(container.base_sections) > 0:
        # TODO: use resolve_variadic_name to find inheritance among non-exact matchings (also provide data type)
        base_quantity: Quantity = container.base_sections[0].all_quantities.get(name)
        if base_quantity:
            value_quantity = base_quantity.m_copy(deep=True)
            value_quantity.attributes.clear()

    # create quantity
    if value_quantity is None:
        value_quantity = Quantity(name=name, flexible_unit=True)

    value_quantity.variable = _if_template(name) and (
        nx_name_type in ["any", "partial"]
    )

    # check parent type compatibility
    parent_type = getattr(value_quantity, "type", None)
    if not isinstance(parent_type, MEnum):
        # if parent type is not MEnum then overwrite whatever given
        value_quantity.type = (
            enum_type if enum_type and not nx_enum_open else nx_nomad_type
        )
    elif enum_type:
        # only when derived type is also MEnum to allow overwriting
        value_quantity.type = enum_type if not nx_enum_open else nx_nomad_type

    value_quantity.dimensionality = dimensionality
    value_quantity.shape = shape
    value_quantity.more.update(
        dict(nx_kind="field", nx_type=nx_type, nx_shape=nx_shape)
    )

    _add_common_properties(xml_node, value_quantity)

    container.quantities.append(value_quantity)

    _create_attributes(xml_node, container, value_quantity)

    return value_quantity


def _create_group(xml_node: ET.Element, root_section: Section):
    """
    Adds all properties that can be generated from the given nexus group XML node to
    the given (empty) metainfo section definition.
    """
    _create_attributes(xml_node, root_section)

    for group in xml_node.findall("nx:group", XML_NAMESPACES):
        xml_attrs = group.attrib

        assert "type" in xml_attrs, "Expecting type to be present"
        nx_type = _rename_nx_for_nomad(xml_attrs["type"])

        nx_name = xml_attrs.get("name", nx_type.upper())

        # nameType
        nx_name_type = xml_attrs.get(
            "nameType", "specified" if "name" in xml_attrs.keys() else "any"
        )
        # if nx_name_type == "any":
        #     nx_name = nx_name.upper()

        section_name = (
            root_section.name + "__" + _rename_nx_for_nomad(nx_name, is_group=True)
        )
        if section_name == "Root__ENTRY":
            group_section = section_definitions["Entry"]
        else:
            group_section = Section(
                validate=VALIDATE,
                nx_kind="group",
                name=section_name,
                variable=_if_template(nx_name) and (nx_name_type in ["any", "partial"]),
            )
            _add_common_properties(group, group_section)
            _attach_base_section(group_section, root_section, to_section(nx_type))
            section_definitions[section_name] = group_section
        # nx_name = xml_attrs.get(
        #     "name", nx_type.replace(REPLACEMENT_FOR_NX, "").upper()
        # )
        subsection_name = _rename_nx_for_nomad(nx_name, is_group=True)
        group_subsection = SubSection(
            section_def=group_section,
            nx_kind="group",
            name=subsection_name,
            repeats=_if_repeats(nx_name, xml_attrs.get("maxOccurs", "0")),
            variable=_if_template(nx_name) and (nx_name_type in ["any", "partial"]),
        )

        root_section.sub_sections.append(group_subsection)

        _create_group(group, group_section)

    for field in xml_node.findall("nx:field", XML_NAMESPACES):
        _create_field(field, root_section)


def _attach_base_section(section: Section, container: Section, default: Section):
    """
    Potentially adds a base section to the given section, if the given container has
    a base-section with a suitable base.
    """
    try:
        newdefinitions = {}
        for def_name, act_def in container.all_sub_sections.items():
            if (
                "nx_type" in act_def.sub_section.more
                and section.more["nx_type"] == act_def.sub_section.more["nx_type"]
            ):
                newdefinitions[def_name] = act_def.sub_section
        base_section = resolve_variadic_name(
            newdefinitions,
            section.name.split("__")[-1],
            # filter=default,
        )
    except ValueError:
        base_section = None

    if base_section:
        assert base_section.nx_kind == section.nx_kind, "Base section has wrong kind"
    else:
        base_section = default

    section.base_sections = [base_section]


def _create_class_section(xml_node: ET.Element) -> Section:
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

    if nx_category == "application" or (nx_category == "base" and nx_name == "NXroot"):
        nomad_base_sec_cls = (
            [NexusMeasurement]
            if xml_attrs.get("extends") == "NXobject" or nx_name == "NXroot"
            else []
        )
    else:
        nomad_base_sec_cls = BASESECTIONS_MAP.get(nx_name, [NexusBaseSection])

    name = _rename_nx_for_nomad(nx_name)
    class_section: Section = to_section(name, nx_kind=nx_type, nx_category=nx_category)

    if "extends" in xml_attrs:
        nx_base_sec = to_section(_rename_nx_for_nomad(xml_attrs["extends"]))
        class_section.base_sections = [nx_base_sec] + [
            cls.m_def for cls in nomad_base_sec_cls
        ]
    elif name == "Object" or name == "Root":
        class_section.base_sections = [cls.m_def for cls in nomad_base_sec_cls]

    _add_common_properties(xml_node, class_section)

    _create_group(xml_node, class_section)

    return class_section


def _find_cycles(graph):
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


def _sort_nxdl_files(paths):
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
    cycles = _find_cycles(name_dependency_map)
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
            logger_.error(
                "Missing dependency (incorrect group type).",
                target_name=node,
                used_by=parent_nodes,
            )

    return validated_names


def add_section_from_nxdl(xml_node: ET.Element) -> Optional[Section]:
    """
    Creates a metainfo section from a nxdl file.
    """
    try:
        global XML_PARENT_MAP  # pylint: disable=global-statement
        XML_PARENT_MAP = {
            child: parent for parent in xml_node.iter() for child in parent
        }

        return _create_class_section(xml_node)

    except NotImplementedError as err:
        logger_.error(
            "Fail to generate metainfo.",
            target_name=xml_node.attrib["name"],
            exc_info=str(err),
        )
        return None


def create_package_from_nxdl_directories() -> Package:
    """
    Creates a metainfo package from the given nexus directory. Will generate the
    respective metainfo definitions from all the nxdl files in that directory.
    The parent Schema is also populated with all AppDefs and then is is also added to the package.
    """
    package = Package(name=PACKAGE_NAME)

    folder_list = ("base_classes", "contributed_definitions", "applications")
    paths = [
        os.path.join(get_nexus_definitions_path(), folder) for folder in folder_list
    ]

    sections = []
    for nxdl_file in _sort_nxdl_files(paths):
        section = add_section_from_nxdl(nxdl_file)
        if section is not None:
            sections.append(section)
    sections.sort(key=lambda x: x.name)

    nexus_sections = {}
    for section_name in ["_Applications", "_BaseSections"]:  # , '_InnerSections']:
        nexus_sections[section_name] = Section(validate=VALIDATE, name=section_name)
        package.section_definitions.append(nexus_sections[section_name])
    for section in sections:
        package.section_definitions.append(section)
        if section.nx_category == "application" or section.nx_name == "NXroot":
            key = "_Applications"
        elif section.nx_category == "base":
            key = "_BaseSections"
        else:
            key = None

        if key:
            nexus_sections[key].sub_sections.append(
                SubSection(section_def=section, name=section.name)
            )
    for section_name, section in section_definitions.items():
        if "__" in section_name:
            package.section_definitions.append(section)

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

    # try:
    #     load_nexus_schema('')
    # except Exception:
    #     nexus_metainfo_package = create_package_from_nxdl_directories(nexus_section)
    #     try:
    #         save_nexus_schema('')
    #     except Exception:
    #         pass
    nexus_metainfo_package = create_package_from_nxdl_directories()
    nexus_metainfo_package.section_definitions.append(NexusMeasurement.m_def)
    nexus_metainfo_package.section_definitions.append(NexusActivityStep.m_def)
    nexus_metainfo_package.section_definitions.append(NexusActivityResult.m_def)
    nexus_metainfo_package.section_definitions.append(NexusBaseSection.m_def)
    nexus_metainfo_package.section_definitions.append(AnchoredReference.m_def)
    nexus_metainfo_package.section_definitions.append(NexusIdentifiers.m_def)

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
        _add_additional_attributes(section, None)
        for quantity in section.quantities:
            _add_additional_attributes(quantity, section)

    # We skip the Python code generation for now and offer Python classes as variables
    # TO DO not necessary right now, could also be done case-by-case by the nexus parser
    python_module = sys.modules[__name__]
    for section in nexus_metainfo_package.section_definitions:  # pylint: disable=E1133
        setattr(python_module, section.name, section.section_cls)


init_nexus_metainfo()


def normalize_fabrication(self, archive, logger):
    """Normalizer for fabrication section."""
    current_cls = section_definitions[_rename_nx_for_nomad("NXfabrication")].section_cls
    self.name = (
        self.__dict__["nx_name"]
        + " ("
        + ((self.vendor__field + " / ") if self.vendor__field else "")
        + (self.model__field if self.model__field else "")
        + ")"
    )
    super(current_cls, self).normalize(archive, logger)


def normalize_sample_component(self, archive, logger):
    """Normalizer for sample_component section."""
    current_cls = section_definitions[
        _rename_nx_for_nomad("NXsample_component")
    ].section_cls
    if self.name__field:
        self.name = self.name__field
    else:
        self.name = self.__dict__["nx_name"]
    if self.mass__field:
        self.mass = self.mass__field
    # we may want to add normalisation for mass_fraction (calculating from components)
    super(current_cls, self).normalize(archive, logger)


def normalize_sample(self, archive, logger):
    """Normalizer for sample section."""
    current_cls = section_definitions[_rename_nx_for_nomad("NXsample")].section_cls
    self.name = self.__dict__["nx_name"] + (
        " (" + self.name__field + ")" if self.name__field else ""
    )
    # one could also copy local ids to identifier for search purposes
    super(current_cls, self).normalize(archive, logger)


def normalize_entry(self, archive, logger):
    """Normalizer for Entry section."""
    current_cls = section_definitions[_rename_nx_for_nomad("NXentry")].section_cls
    if self.start_time__field:
        self.start_time = self.start_time__field
    self.name = self.__dict__["nx_name"] + (
        " (" + self.title__field + ")" if self.title__field is not None else ""
    )
    # one could also copy local ids to identifier for search purposes
    super(current_cls, self).normalize(archive, logger)


def normalize_process(self, archive, logger):
    """Normalizer for Process section."""
    current_cls = section_definitions[_rename_nx_for_nomad("NXprocess")].section_cls
    if self.date__field:
        self.start_time = self.date__field
    self.name = self.__dict__["nx_name"]
    # one could also copy local ids to identifier for search purposes
    super(current_cls, self).normalize(archive, logger)


def normalize_data(self, archive, logger):
    """Normalizer for Data section."""
    current_cls = section_definitions[_rename_nx_for_nomad("NXdata")].section_cls
    self.name = self.__dict__["nx_name"]
    # one could also copy local ids to identifier for search purposes
    super(current_cls, self).normalize(archive, logger)


def normalize_atom_probe(self, archive, logger):
    current_cls = section_definitions[
        f"{_rename_nx_for_nomad('NXapm')}__ENTRY__atom_probe"
    ].section_cls
    super(current_cls, self).normalize(archive, logger)
    # temporarily disable extra normalisation step
    return

    def plot_3d_plotly(df, palette="Set1"):
        import plotly.express as px
        import plotly.graph_objects as go
        from scipy.spatial import cKDTree

        unique_species = df["element"].unique()
        num_species = len(unique_species)
        base_colors = getattr(px.colors.qualitative, palette)
        colors = (base_colors * ((num_species // len(base_colors)) + 1))[:num_species]

        fig = go.Figure()
        for i, species in enumerate(unique_species):
            subset = df[df["element"] == species]
            fig.add_trace(
                go.Scatter3d(
                    x=subset["x"],
                    y=subset["y"],
                    z=subset["z"],
                    mode="markers",
                    marker=dict(size=1, opacity=0.6, color=colors[i]),
                    name=str(species),
                )
            )

        # Improve axis and box appearance
        fig.update_layout(
            title="3D Atom Probe Reconstruction with Plotly WebGL",
            scene=dict(
                xaxis=dict(
                    showgrid=False,
                    backgroundcolor="white",
                ),
                yaxis=dict(
                    showgrid=False,
                    backgroundcolor="white",
                ),
                zaxis=dict(
                    showgrid=False,
                    backgroundcolor="white",
                ),
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            height=800,
            autosize=True,
            template="plotly_white",
            showlegend=True,
            legend=dict(
                font=dict(size=16),
                itemsizing="constant",
                bgcolor="rgba(255,255,255,0.8)",
            ),
        )
        return fig

    data_path = self.m_attributes["m_nx_data_path"]
    with h5py.File(
        os.path.join(archive.m_context.raw_path(), self.m_attributes["m_nx_data_file"]),
        "r",
    ) as fp:
        if (
            f"{data_path}/reconstruction/reconstructed_positions" not in fp
            or f"{data_path}/mass_to_charge_conversion/mass_to_charge" not in fp
        ):
            return
        if not hasattr(self, "ranging"):
            return
        if not hasattr(self.ranging, "peak_identification"):
            return
        if not hasattr(self.ranging.peak_identification, "ionID"):
            return
        # Load the reconstructed positions and mass-to-charge values
        positions = fp[f"{data_path}/reconstruction/reconstructed_positions"][:]
        mass_to_charge_values = fp[
            f"{data_path}/mass_to_charge_conversion/mass_to_charge"
        ][:].flatten()
        # Build species mapping from ion peak identification groups
        ion_species_map = {}
        for ion in self.ranging.peak_identification.ionID:
            if ion.mass_to_charge_range__field and ion.name__field:
                mass_range = fp[
                    f"{ion.m_attributes['m_nx_data_path']}/mass_to_charge_range"
                ][:]
                species_name = ion.name__field
                # Extract only element name (remove charge states and molecular ions)
                element_name = re.split(r"[^A-Za-z]", species_name)[0]
                if element_name:  # Avoid empty strings
                    ion_species_map[element_name] = mass_range
    # Convert species mapping into an efficient lookup structure
    species_names = list(set(ion_species_map.keys()))  # Ensure unique element names
    mass_ranges = np.array(
        [ion_species_map[s][:, 0] for s in species_names]
    )  # Extract min/max mass
    # Compute midpoints for KD-tree search
    mass_midpoints = mass_ranges.mean(axis=1)
    # Build a KD-tree for fast species assignment
    mass_tree = cKDTree(mass_midpoints.reshape(-1, 1))
    _, nearest_species_idx = mass_tree.query(mass_to_charge_values.reshape(-1, 1))
    # Assign aggregated atomic element labels
    atomic_labels = np.array(species_names)[nearest_species_idx]
    # Filter valid atomic elements using ASE's atomic numbers
    valid_atomic_labels = [
        el if el in atomic_numbers else "X" for el in atomic_labels
    ]  # Replace unknowns with 'X'
    # Convert to a DataFrame for visualization
    df = pd.DataFrame(positions, columns=["x", "y", "z"])
    df["element"] = pd.Categorical(valid_atomic_labels)
    # Downsample data for efficient rendering (adjust fraction as needed)
    df_sampled = df.sample(
        frac=0.02, random_state=42
    )  # Adjust fraction for performance

    # plotly figure
    fig = plot_3d_plotly(df_sampled)
    # find figures hosting subsesction
    figure_host = archive.data
    # apend the figure to the figures list
    figure_host.figures = [PlotlyFigure(figure=fig.to_plotly_json())]

    # normalize to results.material.topology
    # **Create ASE Atoms Object from Downsampled Data (Using Aggregated Elements)**
    def create_ase_atoms(df):
        symbols = df["element"].tolist()
        positions = df[["x", "y", "z"]].values
        return Atoms(symbols=symbols, positions=positions)

    apt_tip = create_ase_atoms(df_sampled)

    # **Build NOMAD Topology Structure with Individual Element Systems**
    def build_nomad_topology(archive):
        if not archive.results:
            archive.results = Results()
        if not archive.results.material:
            archive.results.material = Material()

        # @Pepe-Marquez, can just be checked for existence, elements have at this point
        # along the processing pipeline been already been populated
        elements = list(set(apt_tip.get_chemical_symbols()))
        if not archive.results.material.elements:
            archive.results.material.elements = elements
        else:
            # @Pepe-Marquez why does the storage order of the elements matter here?
            for i in range(len(elements)):
                if archive.results.material.elements[i] != elements[i]:
                    print("WARNING: elements are swapped")

        topology = {}
        system = System(
            atoms=nomad_atoms_from_ase_atoms(apt_tip),
            label="Reconstruction",
            description="Reconstruction of the original atom positions",
            structural_type="bulk",
            dimensionality="3D",
            system_relation=Relation(type="root"),
        )
        add_system_info(system, topology)
        add_system(system, topology)

        child_systems = []
        for element in elements:
            element_indices = (
                np.where(df_sampled["element"] == element)[0].reshape(1, -1).tolist()
            )
            element_system = System(
                atoms_ref=system.atoms,
                indices=element_indices,
                label=f"{element} - Subsystem",
                description=f"Reconstructed subset containing only {element} atoms.",
                structural_type="bulk",
                dimensionality="3D",
                system_relation=Relation(type="subsystem"),
            )
            add_system_info(element_system, topology)
            add_system(element_system, topology, parent=system)
            child_systems.append(f"results/material/topology/{len(topology) - 1}")

        system.child_systems = child_systems
        archive.results.material.topology = list(topology.values())

    build_nomad_topology(archive)


NORMALIZER_MAP: dict[str, Any] = {
    _rename_nx_for_nomad("NXfabrication"): normalize_fabrication,
    _rename_nx_for_nomad("NXsample"): normalize_sample,
    _rename_nx_for_nomad("NXsample_component"): normalize_sample_component,
    _rename_nx_for_nomad("NXentry"): {
        "normalize": normalize_entry,
    },
    _rename_nx_for_nomad("NXprocess"): {
        "normalize": normalize_process,
    },
    _rename_nx_for_nomad("NXdata"): normalize_data,
    f"{_rename_nx_for_nomad('NXapm')}__ENTRY__atom_probe": normalize_atom_probe,
}
# Handling nomad BaseSection and other inherited Section from BaseSection
for nx_name, section in section_definitions.items():
    if nx_name == "NXobject":
        continue

    normalize_func = NORMALIZER_MAP.get(nx_name)

    # Append the normalize method from a function
    if normalize_func:
        if isinstance(normalize_func, dict):
            for key, value in normalize_func.items():
                setattr(section.section_cls, key, value)
        else:
            section.section_cls.normalize = normalize_func
