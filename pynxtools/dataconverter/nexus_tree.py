from typing import Literal, Optional, Tuple

from anytree import RenderTree, Resolver
from anytree.node.nodemixin import NodeMixin
from pydantic import BaseModel


class ReadOnlyError(RuntimeError):
    pass


class NexusNode(BaseModel, NodeMixin):
    name: str
    type: Literal["group", "field", "attribute"]
    optionality: Literal["required", "recommended", "optional"]
    variadic: bool

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


class NexusGroup(NexusNode):
    nx_class: str
    occurrence_limits: Tuple[Optional[int], Optional[int]] = (None, None)

    def __repr__(self) -> str:
        return (
            f"{self.nx_class[2:].upper()}[{self.name.lower()}] ({self.optionality[:3]})"
        )


class NexusEntity(NexusNode):
    type: Literal["field", "attribute"]
    # TODO: Unit can also be a literal
    unit: Optional[str] = None
    # TODO: Add complete list of all supported nexus types
    # We can also restrict this to the nexus types that are supported by pynx
    dtype: Optional[
        Literal[
            "NX_CHAR",
            "NX_BINARY",
            "NX_BOOLEAN",
            "NX_CHAR",
            "NX_DATE_TIME",
            "ISO8601",
            "NX_FLOAT",
            "NX_INT",
            "NX_UINT",
            "NX_NUMBER",
            "NX_POSINT",
            "NX_COMPLEX",
        ]
    ] = None

    def __repr__(self) -> str:
        if self.type == "attribute":
            return f"@{self.name} ({self.optionality[:3]})"
        return f"{self.name} ({self.optionality[:3]})"


def reset_check(graph: nx.DiGraph):
    for node in graph.nodes:
        node["is_valid"] = False


if __name__ == "__main__":
    root = NexusGroup(
        name="/",
        nx_class="NXroot",
        type="group",
        optionality="required",
        variadic=False,
        parent=None,
    )
    NexusEntity(
        name="default",
        type="attribute",
        optionality="optional",
        variadic=False,
        parent=root,
    )
    entry = NexusGroup(
        name="ENTRY",
        nx_class="NXentry",
        type="group",
        optionality="optional",
        variadic=True,
        parent=root,
    )
    instrument = NexusGroup(
        name="INSTRUMENT",
        nx_class="NXinstrument",
        type="group",
        optionality="optional",
        variadic=True,
        parent=entry,
    )
    some_field = NexusEntity(
        name="my_setting",
        type="field",
        optionality="required",
        variadic=False,
        parent=instrument,
    )

    print(RenderTree(root))
    resolver = Resolver("name")
    print(resolver.get(root, "ENTRY/INSTRUMENT/my_setting"))


"""
Double graph structure

One graph holds the concepts for the nexus appdef structure.
An entry is directly relatable to a node (split the path).
This can be used to recursively validate the nexus structure.

Two step process:
1. Run to concept graph and validate if all directly required fields are present.
2. Go through the entries, map them to the concept graph and validate them recursively.
"""
