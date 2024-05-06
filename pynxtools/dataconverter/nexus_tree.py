from typing import Annotated, List, Literal, Optional, Tuple

import lxml.etree as ET
from anytree.node.nodemixin import NodeMixin
from pydantic import BaseModel, Field, InstanceOf

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
