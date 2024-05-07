from functools import lru_cache
from typing import Annotated, List, Literal, Optional, Tuple

import lxml.etree as ET
from anytree.node.nodemixin import NodeMixin
from pydantic import BaseModel, Field, InstanceOf

from pynxtools.dataconverter.convert import get_nxdl_root_and_path
from pynxtools.dataconverter.helpers import (
    contains_uppercase,
    get_first_group,
    remove_namespace_from_tag,
)
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_inherited_nodes

NexusType = Literal[
    "ISO8601",
    "NX_BINARY",
    "NX_BOOLEAN",
    "NX_CCOMPLEX",
    "NX_CHAR",
    "NX_CHAR_OR_NUMBER",
    "NX_COMPLEX",
    "NX_DATE_TIME",
    "NX_FLOAT",
    "NX_INT",
    "NX_NUMBER",
    "NX_PCOMPLEX",
    "NX_POSINT",
    "NX_QUATERNION",
    "NX_UINT",
]

# TODO: Get types from nxdlTypes.xsd
NexusUnitCategory = Literal[
    "NX_ANGLE",
    "NX_ANY",
    "NX_AREA",
    "NX_CHARGE",
    "NX_COUNT",
    "NX_CROSS_SECTION",
    "NX_CURRENT",
    "NX_DIMENSIONLESS",
    "NX_EMITTANCE",
    "NX_ENERGY",
    "NX_FLUX",
    "NX_FREQUENCY",
    "NX_LENGTH",
    "NX_MASS",
    "NX_MASS_DENSITY",
    "NX_MOLECULAR_WEIGHT",
    "NX_PERIOD",
    "NX_PER_AREA",
    "NX_PER_LENGTH",
    "NX_POWER",
    "NX_PRESSURE",
    "NX_PULSES",
    "NX_SCATTERING_LENGTH_DENSITY",
    "NX_SOLID_ANGLE",
    "NX_TEMPERATURE",
    "NX_TIME",
    "NX_TIME_OF_FLIGHT",
    "NX_TRANSFORMATION",
    "NX_UNITLESS",
    "NX_VOLTAGE",
    "NX_VOLUME",
    "NX_WAVELENGTH",
    "NX_WAVENUMBER",
]


class ReadOnlyError(RuntimeError):
    pass


class NexusNode(BaseModel, NodeMixin):
    name: str
    type: Literal["group", "field", "attribute", "choice"]
    optionality: Literal["required", "recommended", "optional"]
    variadic: bool
    variadic_siblings: List[InstanceOf["NexusNode"]] = []

    def __init__(self, parent, **data) -> None:
        super().__init__(**data)
        self.__readonly = False
        self.parent = parent
        self.__readonly = True

    def _pre_attach(self, parent):
        if self.__readonly:
            raise ReadOnlyError()

    def _pre_detach(self, parent):
        raise ReadOnlyError()

    @lru_cache(maxsize=None)
    def get_path(self) -> str:
        current_node = self
        names: List[str] = []
        while current_node.parent is not None:
            names.insert(0, current_node.name)
            current_node = current_node.parent
        return "/" + "/".join(names)


class NexusChoice(NexusNode):
    type: Literal["choice"] = "choice"


class NexusGroup(NexusNode):
    nx_class: str
    occurrence_limits: Tuple[
        Optional[Annotated[int, Field(strict=True, ge=0)]],
        Optional[Annotated[int, Field(strict=True, ge=0)]],
    ] = (None, None)
    inheritance: List[InstanceOf[ET._Element]] = []

    def __repr__(self) -> str:
        return (
            f"{self.nx_class[2:].upper()}[{self.name.lower()}] ({self.optionality[:3]})"
        )


class NexusEntity(NexusNode):
    type: Literal["field", "attribute"]
    unit: Optional[NexusUnitCategory] = None
    dtype: Optional[NexusType] = None
    items: Optional[List[str]] = None
    shape: Optional[Tuple[Optional[int], ...]] = None

    def __repr__(self) -> str:
        if self.type == "attribute":
            return f"@{self.name} ({self.optionality[:3]})"
        return f"{self.name} ({self.optionality[:3]})"


def get_enumeration_items(elem: ET._Element) -> List[str]:
    items: List[str] = []
    for item_tag in elem:
        if remove_namespace_from_tag(item_tag.tag) == "item":
            items.append(item_tag.attrib["value"])

    return items


def check_enumeration_in_parents_for(node: NexusNode) -> None:
    # TODO
    pass


def check_dimensions_in_parents_for(node: NexusNode) -> None:
    # TODO
    pass


def generate_tree_from(appdef: str) -> NexusNode:
    def add_children_to(parent: NexusNode, xml_elem: ET._Element) -> None:
        tag = remove_namespace_from_tag(xml_elem.tag)

        if tag == "doc":
            return

        optionality: Literal["required", "recommended", "optional"] = "required"
        if xml_elem.attrib.get("recommended"):
            optionality = "recommended"
        elif xml_elem.attrib.get("optional"):
            optionality = "optional"

        if tag in ("field", "attribute"):
            name = xml_elem.attrib.get("name")
            is_variadic = contains_uppercase(xml_elem.attrib["name"])
            current_elem = NexusEntity(
                parent=parent,
                name=name,
                type=tag,
                optionality=optionality,
                variadic=is_variadic,
                unit=xml_elem.attrib.get("units"),
                dtype=xml_elem.attrib.get("type", "NX_CHAR"),
            )
        elif tag == "group":
            name = xml_elem.attrib.get("name", xml_elem.attrib["type"][2:].upper())
            inheritance_chain = get_inherited_nodes("", elem=xml_elem)[2]
            is_variadic = contains_uppercase(name)
            max_occurs = (
                None
                if xml_elem.attrib.get("maxOccurs") == "unbounded"
                else xml_elem.attrib.get("maxOccurs")
            )
            current_elem = NexusGroup(
                parent=parent,
                type=tag,
                name=name,
                nx_class=xml_elem.attrib["type"],
                optionality=optionality,
                variadic=is_variadic,
                occurrence_limits=(
                    xml_elem.attrib.get("minOccurs"),
                    max_occurs,
                ),
                inheritance=inheritance_chain,
            )
        elif tag == "enumeration":
            items = get_enumeration_items(xml_elem)
            parent.items = items
            return
        elif tag == "dimensions":
            rank = xml_elem.attrib["rank"]
            dims: List[Optional[int]] = [None] * int(rank)
            for dim in xml_elem.findall(f"{namespace}dim"):
                idx = int(dim.attrib["index"])
                try:
                    value = int(dim.attrib["value"])
                    dims[idx] = value
                except ValueError:
                    # TODO: Handling of symbols
                    pass

            parent.shape = tuple(dims)
            return
        elif tag == "choice":
            current_elem = NexusChoice(
                parent=parent,
                name=xml_elem.attrib["name"],
                optionality=optionality,
                variadic=contains_uppercase(xml_elem.attrib["name"]),
            )
        else:
            # TODO: Tags: link
            # We don't know the tag, skip processing children of it
            # TODO: Add logging or raise an error as this is not a known nxdl tag
            return

        tags = ("enumeration", "dimensions")
        check_tags_in_base_classes = False
        for child in xml_elem:
            if remove_namespace_from_tag(child.tag) not in tags:
                check_tags_in_base_classes = True
            add_children_to(current_elem, child)

        if check_tags_in_base_classes:
            check_enumeration_in_parents_for(current_elem)
            check_dimensions_in_parents_for(current_elem)

    appdef_xml_root, _ = get_nxdl_root_and_path(appdef)
    entry = get_first_group(appdef_xml_root)
    namespace = "{" + appdef_xml_root.nsmap[None] + "}"

    tree = NexusGroup(
        name=appdef_xml_root.attrib["name"],
        nx_class="NXroot",
        type="group",
        optionality="required",
        variadic=False,
        parent=None,
    )
    add_children_to(tree, entry)

    return tree
