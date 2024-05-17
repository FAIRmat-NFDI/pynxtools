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
"""
`NexusNode` and its subclasses are a tree implementation based on anytree.
They are used to represent the structure of an NeXus application definition.

The `NexusNode` representation is typically spares, i.e., it only contains
everything present in the application definition.
However, all necessary parameters are added from the inheritance chain
on the fly when the tree is generated.

It also allows for adding further nodes from the inheritance chain on the fly.
"""

from typing import List, Literal, Optional, Set, Tuple, Union

import lxml.etree as ET
from anytree.node.nodemixin import NodeMixin
from pydantic import BaseModel, InstanceOf

from pynxtools.dataconverter.helpers import (
    contains_uppercase,
    get_nxdl_root_and_path,
    remove_namespace_from_tag,
)

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

# This is the NeXus namespace for finding tags.
# It's updated from the nxdl file when `generate_tree_from`` is called.
namespaces = {"nx": "http://definition.nexusformat.org/nxdl/3.1"}


class NexusNode(BaseModel, NodeMixin):
    """
    A NexusNode represents one node in the NeXus tree.
    It can be either a `group`, `field`, `attribute` or `choice` for which it has
    respective subclasses.

    Args:
        name (str):
            The name of the node.
        type (Literal["group", "field", "attribute", "choice"]):
            The type of the node, e.g., xml tag in the nxdl file.
        optionality (Literal["required", "recommended", "optional"], optional):
            The optionality of the node.
            This is automatically set on init (in the respective subclasses)
            based on the values found in the nxdl file.
            Defaults to "required".
        variadic (bool):
            True if the node name is variadic and can be matched against multiple names.
            This is set automatically on init and will be True if the name contains
            any uppercase characets and False otherwise.
            Defaults to False.
        variadic_siblings (List[InstanceOf["NexusNode"]]):
            Variadic siblings are names which are connected to each other, e.g.,
            `AXISNAME` and `AXISNAME_indices` belong together and are variadic siblings.
            Defaults to [].
        inheritance (List[InstanceOf[ET._Element]]):
            The inheritance chain of the node.
            The first element of the list is the xml representation of this node.
            All following elements are the xml nodes of the node if these are
            present in parent classes.
            Defaults to [].
        parent: (Optional[NexusNode]):
            The parent of the node.
            This is used by anytree to automatically build parents and children relations
            for a tree, i.e., setting the parent of a node is enough to add it to the tree
            and to its parent's children.
            For the root this is None.
    """

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

    def __init__(self, parent: Optional["NexusNode"], **data) -> None:
        super().__init__(**data)
        self.variadic = contains_uppercase(self.name)
        self.parent = parent

    def _construct_inheritance_chain_from_parent(self):
        if self.parent is None:
            return
        for xml_elem in self.parent.inheritance:
            elem = xml_elem.find(
                f"nx:{self.type}/[@name='{self.name}']", namespaces=namespaces
            )
            if elem is not None:
                self.inheritance.append(elem)

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

    def search_child_with_name(
        self, names: Union[Tuple[str, ...], str]
    ) -> Optional["NexusNode"]:
        """
        This searches a child or children with `names` in the current node.
        If the child is not found as a direct child,
        it will search in the inheritance chain and add the child to the tree.

        Args:
            names (Union[Tuple[str, ...], str]):
                Either a single string or a tuple of string.
                In case this is a string the child with the specific name is searched.
                If it is a tuple, the first match is used.

        Returns:
            Optional[NexusNode]:
                The node of the child which was added. None if no child was found.
        """
        if isinstance(names, str):
            names = (names,)
        for name in names:
            direct_child = next((x for x in self.children if x.name == name), None)
            if direct_child is not None:
                return direct_child
            if name in self.get_all_children_names():
                return self.add_inherited_node(name)
        return None

    def get_all_children_names(self, depth: Optional[int] = None) -> Set[str]:
        """
        Get all children names of the current node up to a certain depth.
        Only `field`, `group` `choice` or `attribute` are considered as children.

        Args:
            depth (Optional[int], optional):
                The inheritance depth up to which get children names.
                `depth=1` will return only the children of the current node.
                `depth=None` will return all children names of all parents.
                Defaults to None.

        Raises:
            ValueError: If depth is not int or negativ.

        Returns:
            Set[str]: A set of children names.
        """
        if depth is not None and (not isinstance(depth, int) or depth < 0):
            raise ValueError("Depth must be a positive integer or None")

        names = set()
        for elem in self.inheritance[:depth]:
            for subelems in elem.xpath(
                (
                    r"*[self::nx:field or self::nx:group "
                    r"or self::nx:attribute or self::nx:choice]"
                ),
                namespaces=namespaces,
            ):
                if "name" in subelems.attrib:
                    names.add(subelems.attrib["name"])
                elif "type" in subelems.attrib:
                    names.add(subelems.attrib["type"][2:].upper())

        return names

    def required_fields_and_attrs_names(
        self,
        prev_path: str = "",
        level: Literal["required", "recommended", "optional"] = "required",
    ) -> List[str]:
        """
        Gets all required fields and attributes names of the current node and its children.

        Args:
            prev_path (str, optional):
                The path prefix to attach to the names found at this node. Defaults to "".
            level (Literal["required", "recommended", "optional"], optional):
                Denotes which level of requiredness should be returned.
                Setting this to `required` will return only required fields and attributes.
                Setting this to `recommended` will return
                both required and recommended fields and attributes.
                Setting this to "optional" will return all fields and attributes
                directly present in the application definition but no fields
                inherited from the base classes.
                Defaults to "required".

        Returns:
            List[str]: A list of required fields and attributes names.
        """
        lvl_map = {
            "required": ("required",),
            "recommended": ("recommended", "required"),
            "optional": ("optional", "recommended", "required"),
        }

        req_children = []
        optionalities = lvl_map.get(level, ("required",))
        for child in self.children:
            if child.optionality not in optionalities:
                continue

            if child.type == "attribute":
                req_children.append(f"{prev_path}/@{child.name}")
                continue

            if child.type == "field":
                req_children.append(f"{prev_path}/{child.name}")
                if isinstance(child, NexusEntity) and child.unit is not None:
                    req_children.append(f"{prev_path}/{child.name}/@units")

            req_children.extend(
                child.required_fields_and_attrs_names(
                    prev_path=f"{prev_path}/{child.name}", level=level
                )
            )

        return req_children

    def get_docstring(self, depth: Optional[int] = None) -> List[str]:
        """
        Gets the docstrings of the current node and its parents up to a certain depth.

        Args:
            depth (Optional[int], optional):
                The depth up to which to retrieve the docstrings.
                If this is None all docstrings of all parents are returned.
                Defaults to None.

        Raises:
            ValueError: If depth is not int or negativ.

        Returns:
            List[str]: A list of docstrings one for each parent doc.
        """
        if depth is not None and depth < 0:
            raise ValueError("Depth must be a positive integer or None")

        docstrings = []
        for elem in self.inheritance[:depth][::-1]:
            doc = elem.find("nx:doc", namespaces=namespaces)
            if doc is not None:
                docstrings.append(doc.text)

        return docstrings

    def _build_inheritance_chain(self, xml_elem: ET._Element) -> List[ET._Element]:
        name = xml_elem.attrib.get("name")
        inheritance_chain = [xml_elem]
        for elem in self.inheritance:
            inherited_elem = elem.xpath(
                f"nx:group[@type='{xml_elem.attrib['type']}' and @name='{name}']"
                if name is not None
                else f"nx:group[@type='{xml_elem.attrib['type']}']",
                namespaces=namespaces,
            )
            if inherited_elem and inherited_elem[0] not in inheritance_chain:
                inheritance_chain.append(inherited_elem[0])
        bc_xml_root, _ = get_nxdl_root_and_path(xml_elem.attrib["type"])
        inheritance_chain.append(bc_xml_root)

        return inheritance_chain

    def add_node_from(self, xml_elem: ET._Element) -> Optional["NexusNode"]:
        """
        Adds a children node to this node based on an xml element.
        The appropriate subclass is chosen based on the xml tag.

        Args:
            xml_elem (lxml.etree._Element):
                The nxdl xml node. Defaults to None.

        Returns:
            Optional["NexusNode"]:
                The children node which was added.
                None if the tag of the xml element is not known.
        """
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
            inheritance_chain = self._build_inheritance_chain(xml_elem)
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
        """
        Adds a children node to this node based on the inheritance chain of the node.

        Args:
            name (str): The name of the node to add.

        Returns:
            Optional["NexusNode"]:
                The NexusNode which was added.
                None if no matching subelement was found to add.
        """
        for elem in self.inheritance:
            xml_elem = elem.xpath(
                f"*[self::nx:field or self::nx:group or self::nx:attribute][@name='{name}']",
                namespaces=namespaces,
            )
            if not xml_elem:
                # Find group by naming convention
                xml_elem = elem.xpath(
                    f"*[self::nx:group][@type='NX{name.lower()}']",
                    namespaces=namespaces,
                )
            if xml_elem:
                new_node = self.add_node_from(xml_elem[0])
                new_node.optionality = "optional"
                return new_node
        return None


class NexusChoice(NexusNode):
    """
    A representation of a NeXus choice.
    It just collects children of the choice from which to choose one.

    Args:
        type (Literal["choice"]):
            Just ties this node to the choice tag in the nxdl file.
            Should and cannot be manually altered.
            Defaults to "choice".
    """

    type: Literal["choice"] = "choice"

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._construct_inheritance_chain_from_parent()
        self._set_optionality()


class NexusGroup(NexusNode):
    """
    A NexusGroup represents a group in the NeXus tree
    adding the nx_class and occurrence_limits to the NexusNode.

    Args:
        nx_class (str):
        occurence_limits (Tuple[Optional[int], Optional[int]]):
            Denotes the minimum and maximum number of occurrences of the group.
            First element denotes the minimum, second one the maximum.
            If the respective value is None, then there is no limit.
            This is set automatically on init based on the values found in the nxdl file.
            Defaults to (None, None).
    """

    nx_class: str
    occurrence_limits: Tuple[
        # TODO: Use Annotated[int, Field(strict=True, ge=0)] for py>3.8
        Optional[int],
        Optional[int],
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
    """
    A NexusEntity represents a field or an attribute in the NeXus tree.

    Args:
        type (Literal["field", "attribute"]):
            The type of the entity is restricted to either a `field` or an `attribute`.
        unit (Optional[NexusUnitCategory]):
            The unit of the entity.
            This is set automatically on init based on the values found in the nxdl file.
            Also the base classes of these entities are considered.
            Defaults to None.
        dtype (NexusType):
            The nxdl datatype of the entity.
            This is set automatically on init based on the values found in the nxdl file.
            Also the base classes of these entities are considered.
            If it is not present in any of the xml nodes, it will be set to `NX_CHAR`.
            Defaults to "NX_CHAR".
        items (Optional[List[str]]):
            This is a restriction of the field value to a list of items.
            Only applies to nodes of dtype `NX_CHAR`.
            This is set automatically on init based on the values found in the nxdl file.
            Also the base classes of these entities are considered.
            If there is no restriction this is set to None.
            Defaults to None.
        shape (Optional[Tuple[Optional[int], ...]]):
            The shape of the entity as given by the dimensions tag.
            This is set automatically on init based on the values found in the nxdl file.
            Also the base classes of these entities are considered.
            If there is no dimension present in any of the xml nodes, it will be set to None.
            Contains None for unbounded dimensions.
            Symbols in either the `rank` or `value` attribute are not considered
            and result in an unbounded shape.
            Defaults to None.
    """

    type: Literal["field", "attribute"]
    unit: Optional[NexusUnitCategory] = None
    dtype: NexusType = "NX_CHAR"
    items: Optional[List[str]] = None
    shape: Optional[Tuple[Optional[int], ...]] = None

    def _set_type(self):
        for elem in self.inheritance:
            if "type" in elem.attrib:
                self.dtype = elem.attrib["type"]
                return

    def _set_unit(self):
        for elem in self.inheritance:
            if "units" in elem.attrib:
                self.unit = elem.attrib["units"]
                return

    def _set_items(self):
        if not self.dtype == "NX_CHAR":
            return
        for elem in self.inheritance:
            enum = elem.find(f"nx:enumeration", namespaces=namespaces)
            if enum is not None:
                self.items = []
                for items in enum.findall(f"nx:item", namespaces=namespaces):
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
    """
    Generates a NexusNode tree from an application definition.
    NexusNode is based on anytree nodes and anytree's functions can be used
    for displaying and traversal of the tree.

    Args:
        appdef (str): The application definition name to generate the NexusNode tree from.

    Returns:
        NexusNode: The tree representing the application definition.
    """

    def add_children_to(parent: NexusNode, xml_elem: ET._Element) -> None:
        """
        This adds children from the `xml_elem` xml node to the NexusNode `parent` node.
        This only considers `field`, `attribute`, `choice` and `group` xml tags
        as children.
        The function is recursivly called until no more children are found.

        Args:
            parent (NexusNode): The NexusNode to attach the children to.
            xml_elem (ET._Element): The xml node to get the children from.
        """
        current_elem = parent.add_node_from(xml_elem)

        for child in xml_elem.xpath(
            (
                r"*[self::nx:field or self::nx:group "
                r"or self::nx:attribute or self::nx:choice]"
            ),
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
        inheritance=[appdef_xml_root],
    )
    # Set root attributes
    nx_root, _ = get_nxdl_root_and_path("NXroot")
    for root_attrib in nx_root.findall("nx:attribute", namespaces=namespaces):
        child = tree.add_node_from(root_attrib)
        child.optionality = "optional"

    entry = appdef_xml_root.find("nx:group[@type='NXentry']", namespaces=namespaces)
    add_children_to(tree, entry)

    return tree
