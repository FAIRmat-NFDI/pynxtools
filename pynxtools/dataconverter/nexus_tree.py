from functools import lru_cache
from typing import Annotated, List, Literal, Optional, Set, Tuple

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
    "NX_BINARY",
    "NX_BOOLEAN",
    "NX_CCOMPLEX",
    "NX_CHAR",
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

namespaces = {"nx": "http://definition.nexusformat.org/nxdl/3.1"}


class ReadOnlyError(RuntimeError):
    pass


class NexusNode(BaseModel, NodeMixin):
    name: str
    type: Literal["group", "field", "attribute", "choice"]
    optionality: Literal["required", "recommended", "optional"] = "required"
    variadic: bool = False
    variadic_siblings: List[InstanceOf["NexusNode"]] = []
    inheritance: List[InstanceOf[ET._Element]] = []

    def _set_optionality(self):
        if not self.inheritance:
            return
        if self.inheritance[0].attrib.get("recommended"):
            self.optionality = "recommended"
        elif self.inheritance[0].attrib.get("optional"):
            self.optionality = "optional"

    def __init__(self, parent, **data) -> None:
        super().__init__(**data)
        self.variadic = contains_uppercase(self.name)
        self.__readonly = False
        self.parent = parent
        self.__readonly = True

    def _pre_attach(self, parent):
        if self.__readonly:
            raise ReadOnlyError()

    def _pre_detach(self, parent):
        raise ReadOnlyError()

    def _construct_inheritance_chain_from_parent(self):
        if self.parent is None:
            return
        for xml_elem in self.parent.inheritance:
            elem = xml_elem.find(
                f"nx:{self.type}/[@name='{self.name}']", namespaces=namespaces
            )
            if elem is not None:
                self.inheritance.append(elem)

    @lru_cache(maxsize=None)
    def get_path(self) -> str:
        """
        Gets the path of the current node based on the node name.

        Returns:
            str: The full path up to the parent of the current node.
        """
        current_node = self
        names: List[str] = []
        while current_node.parent is not None:
            names.insert(0, current_node.name)
            current_node = current_node.parent
        return "/" + "/".join(names)

    def get_all_parent_names(self) -> Set[str]:
        names = set()
        for elem in self.inheritance:
            for subelems in elem.xpath(
                r"*[self::nx:field or self::nx:group or self::nx:attribute]",
                namespaces=namespaces,
            ):
                if "name" in subelems.attrib:
                    names.add(subelems.attrib["name"])
                elif "type" in subelems.attrib:
                    names.add(subelems.attrib["type"][2:].upper())

        return names

    def add_node_from(self, xml_elem: ET._Element) -> Optional["NexusNode"]:
        tag = remove_namespace_from_tag(xml_elem.tag)
        if tag in ("field", "attribute"):
            name = xml_elem.attrib.get("name")
            current_elem = NexusEntity(
                parent=self,
                name=name,
                type=tag,
            )
        elif tag == "group":
            name = xml_elem.attrib.get("name", xml_elem.attrib["type"][2:].upper())
            *_, inheritance_chain = get_inherited_nodes("", elem=xml_elem)
            current_elem = NexusGroup(
                parent=self,
                type=tag,
                name=name,
                nx_class=xml_elem.attrib["type"],
                inheritance=inheritance_chain,
            )
        elif tag == "choice":
            current_elem = NexusChoice(
                parent=self,
                name=xml_elem.attrib["name"],
                variadic=contains_uppercase(xml_elem.attrib["name"]),
            )
        else:
            # TODO: Tags: link
            # We don't know the tag, skip processing children of it
            # TODO: Add logging or raise an error as this is not a known nxdl tag
            return None

        return current_elem

    def add_inherited_node(self, name: str) -> Optional["NexusNode"]:
        for elem in self.inheritance:
            xml_elem = elem.find(
                f"nx:{self.type}[@name='{name}']", namespaces=namespaces
            )
            if xml_elem is not None:
                return self.add_node_from(xml_elem)
        return None

    def get_path_and_node(self) -> Tuple[str, List[ET._Element]]:
        current_node = self
        names: List[str] = []
        while current_node is not None and not isinstance(current_node, NexusGroup):
            names.insert(0, current_node.name)
            current_node = current_node.parent
        return "/".join(names), current_node.inheritance


class NexusChoice(NexusNode):
    type: Literal["choice"] = "choice"

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._construct_inheritance_chain_from_parent()


class NexusGroup(NexusNode):
    nx_class: str
    occurrence_limits: Tuple[
        Optional[Annotated[int, Field(strict=True, ge=0)]],
        Optional[Annotated[int, Field(strict=True, ge=0)]],
    ] = (None, None)

    def _set_occurence_limits(self):
        if not self.inheritance:
            return
        xml_elem = self.inheritance[0]
        max_occurs = (
            None
            if xml_elem.attrib.get("maxOccurs") == "unbounded"
            or xml_elem.attrib.get("maxOccurs") is None
            else int(xml_elem.attrib.get("maxOccurs"))
        )
        self.occurrence_limits = (
            int(xml_elem.attrib.get("minOccurs"))
            if xml_elem.attrib.get("minOccurs") is not None
            else None,
            max_occurs,
        )

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._set_occurence_limits()
        self._set_optionality()

    def __repr__(self) -> str:
        return (
            f"{self.nx_class[2:].upper()}[{self.name.lower()}] ({self.optionality[:3]})"
        )


class NexusEntity(NexusNode):
    type: Literal["field", "attribute"]
    unit: Optional[NexusUnitCategory] = None
    dtype: NexusType = "NX_CHAR"
    items: Optional[List[str]] = None
    shape: Optional[Tuple[Optional[int], ...]] = None

    def _set_type(self):
        for elem in self.inheritance:
            dtype = elem.find(
                f"nx:{self.type}[@name='{self.name}']", namespaces=namespaces
            )
            if dtype is not None and "type" in dtype.attrib:
                self.dtype = dtype.attrib.get("type")
                return

    def _set_unit(self):
        for elem in self.inheritance:
            if "units" in elem.attrib:
                self.unit = elem.attrib["units"]
                return

    def _set_items(self):
        if not self.type == "NX_CHAR":
            return
        for elem in self.inheritance:
            enum = elem.find(f"nx:enumeration", namespaces=namespaces)
            if enum is not None:
                self.items = []
                for items in elem.findall(f"nx:item", namespaces=namespaces):
                    self.items.append(items.attrib["value"])
                return

    def _set_shape(self):
        for elem in self.inheritance:
            dimension = elem.find(f"nx:dimensions", namespaces=namespaces)
            if dimension is not None:
                break
        if not self.inheritance or dimension is None:
            return

        rank = dimension.attrib.get("rank")
        if rank is not None and not isinstance(rank, int):
            try:
                int(rank)
            except ValueError:
                # TODO: Handling of symbols
                return
        xml_dim = dimension.findall("nx:dim", namespaces=namespaces)
        rank = rank if rank is not None else len(xml_dim)
        dims: List[Optional[int]] = [None] * int(rank)
        for dim in xml_dim:
            idx = int(dim.attrib["index"])
            if "value" not in dim.attrib:
                # This is probably an old dim element with ref
                return
            try:
                value = int(dim.attrib["value"])
                dims[idx - 1] = value
            except ValueError:
                # TODO: Handling of symbols
                pass

        self.shape = tuple(dims)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._construct_inheritance_chain_from_parent()
        self._set_unit()
        self._set_type()
        self._set_items()
        self._set_optionality()
        self._set_shape()

    def __repr__(self) -> str:
        if self.type == "attribute":
            return f"@{self.name} ({self.optionality[:3]})"
        return f"{self.name} ({self.optionality[:3]})"


def generate_tree_from(appdef: str) -> NexusNode:
    def add_children_to(parent: NexusNode, xml_elem: ET._Element) -> None:
        current_elem = parent.add_node_from(xml_elem)

        for child in xml_elem.xpath(
            r"*[self::nx:field or self::nx:group or self::nx:attribute]",
            namespaces=namespaces,
        ):
            add_children_to(current_elem, child)

    appdef_xml_root, _ = get_nxdl_root_and_path(appdef)
    global namespaces
    namespaces = {"nx": appdef_xml_root.nsmap[None]}

    tree = NexusGroup(
        name=appdef_xml_root.attrib["name"],
        nx_class="NXroot",
        type="group",
        optionality="required",
        variadic=False,
        parent=None,
        inheritance=get_inherited_nodes("", elem=appdef_xml_root)[2],
    )
    entry = appdef_xml_root.find("nx:group[@type='NXentry']", namespaces=namespaces)
    add_children_to(tree, entry)

    return tree
