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
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXoptical_fiber` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    SchemaAnnotation,
)
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import (
    NeXusAttribute,
    NeXusChoice,
    NeXusDefinition,
    NeXusField,
    NeXusGroup,
    NeXusLink,
)
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["OpticalFiber"]


class OpticalFiber(Component):
    """
    An optical fiber, e.g. glass fiber.

    Specify the quantities that define the fiber. Fiber optics are described in
    detail [here](https://www.photonics.com/Article.aspx?AID=25151&PID=4), for
    example.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXoptical_fiber",
            category="base",
            symbols={
                "N_spectrum_core": "Length of the spectrum vector (e.g. wavelength or energy) for which the\n                refractive index of the core material is given.",
                "N_spectrum_clad": "Length of the spectrum vector (e.g. wavelength or energy) for which the\n                refractive index of the cladding material is given.",
                "N_spectrum_attenuation": "Length of the spectrum vector (e.g. wavelength or energy) for which the\n                attenuation curve is given.",
            },
        ),
    )

    core = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_fiber.OpticalFiberCore",
        repeats=False,
        description=(
            "Core of the fiber, i.e. the part of the fiber which transmits the light."
        ),
    )
    cladding = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_fiber.OpticalFiberCladding",
        repeats=False,
        description=(
            "Core of the fiber, i.e. the part of the fiber which transmits the light."
        ),
    )
    coating = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_fiber.OpticalFiberCoating",
        repeats=False,
        description=("Coating of the fiber."),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-description-field"
        ],
        description=(
            "Descriptive name or brief description of the fiber, e.g. by stating "
            "its dimension. The dimension of a fiber can be given as 60/100/200 "
            "which refers to a core diameter of 60 micron, a clad diameter of "
            "100 micron, and a coating diameter of 200 micron."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=MEnum(["single mode", "multimode graded index", "multimode step index"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-type-field"
        ],
        description=(
            "Type/mode of the fiber. Modes of fiber transmission are shown in "
            "Fig. 5 "
            "[here](https://www.photonics.com/Article.aspx?AID=25151&PID=4)."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "single mode",
                "multimode graded index",
                "multimode step index",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    dispersion_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-dispersion-type-field"
        ],
        description=("Type of dispersion."),
        a_nexus_field=NeXusField(
            name="dispersion_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["modal", "material", "chromatic"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    dispersion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-dispersion-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Spectrum-dependent (or refractive index-dependent) dispersion of "
            "the fiber. Specify in ps/nm*km."
        ),
        a_nexus_field=NeXusField(
            name="dispersion",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Length of the fiber."),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    spectral_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-spectral-range-field"
        ],
        shape=[2],
        description=(
            "Spectral range for which the fiber is designed. Enter the minimum "
            "and maximum values (lower and upper limit) of the wavelength range."
        ),
        a_nexus_field=NeXusField(
            name="spectral_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    spectral_range__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-spectral-range-units-attribute"
        ],
        description=(
            "Unit of spectral array (e.g. nanometer or angstrom for wavelength, "
            "or electronvolt for energy etc.)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="spectral_range",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    transfer_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-transfer-rate-field"
        ],
        dimensionality="[information] / [time]",
        unit="GB/s",
        description=("Transfer rate of the fiber (in GB per second)."),
        a_nexus_field=NeXusField(
            name="transfer_rate",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="GB/s",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "GB/s"},
    )
    numerical_aperture = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-numerical-aperture-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Numerical aperture (NA) of the fiber."),
        a_nexus_field=NeXusField(
            name="numerical_aperture",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    attenuation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-attenuation-field"
        ],
        dimensionality="[information] / [length]",
        unit="dB/km",
        shape=["*"],
        description=(
            "Wavelength-dependent attenuation of the fiber (specify in dB/km)."
        ),
        a_nexus_field=NeXusField(
            name="attenuation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="dB/km",
        ),
    )
    attenuation__units = Quantity(
        type=MEnum(["dB/km"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-attenuation-units-attribute"
        ],
        description=("Use dB/km."),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="attenuation",
            enumeration=["dB/km"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="dB/km",
        ),
    )
    power_loss = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-power-loss-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Power loss of the fiber in percentage."),
        a_nexus_field=NeXusField(
            name="power_loss",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    acceptance_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-acceptance-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Acceptance angle of the fiber."),
        a_nexus_field=NeXusField(
            name="acceptance_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class OpticalFiberCore(Sample):
    """
    Core of the fiber, i.e. the part of the fiber which transmits the light.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-core-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="core",
            name_type="specified",
            optionality="optional",
        ),
    )

    material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-core-material-field"
        ],
        description=("Specify the material of the core of the fiber."),
        a_nexus_field=NeXusField(
            name="material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-core-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Core diameter of the fiber (e.g. given in micrometer)."),
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    index_of_refraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-core-index-of-refraction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the fiber. Specify at given "
            "wavelength (or energy, wavenumber etc.) values."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalFiberCladding(Sample):
    """
    Core of the fiber, i.e. the part of the fiber which transmits the light.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-cladding-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="cladding",
            name_type="specified",
            optionality="optional",
        ),
    )

    material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-cladding-material-field"
        ],
        description=("Specify the material of the core of the fiber."),
        a_nexus_field=NeXusField(
            name="material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-cladding-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Clad diameter of the fiber (e.g. given in micrometer)."),
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    index_of_refraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-cladding-index-of-refraction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the fiber. Specify at given "
            "wavelength (or energy, wavenumber etc.) values."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalFiberCoating(Sample):
    """
    Coating of the fiber.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-coating-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="coating",
            name_type="specified",
            optionality="optional",
        ),
    )

    material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-coating-material-field"
        ],
        description=("Specify the material of the coating of the fiber."),
        a_nexus_field=NeXusField(
            name="material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_fiber.html#nxoptical_fiber-coating-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Outer diameter of the fiber (e.g. given in micrometer)."),
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
