from typing import Annotated, Literal, Optional, Tuple

from anytree import RenderTree, Resolver
from anytree.node.nodemixin import NodeMixin
from pydantic import BaseModel, Field


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
    occurrence_limits: Tuple[
        Optional[Annotated[int, Field(strict=True, ge=0)]],
        Optional[Annotated[int, Field(strict=True, ge=0)]],
    ] = (None, None)

    def __repr__(self) -> str:
        return (
            f"{self.nx_class[2:].upper()}[{self.name.lower()}] ({self.optionality[:3]})"
        )


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


class NexusEntity(NexusNode):
    type: Literal["field", "attribute"]
    unit: Optional[NexusUnitCategory] = None
    dtype: Optional[NexusType] = None

    def __repr__(self) -> str:
        if self.type == "attribute":
            return f"@{self.name} ({self.optionality[:3]})"
        return f"{self.name} ({self.optionality[:3]})"


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
