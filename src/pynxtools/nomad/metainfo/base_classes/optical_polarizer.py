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
# Run `pynx nomad generate-metainfo --nxdl NXoptical_polarizer` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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
from pynxtools.nomad.metainfo.base_classes.shape import Shape

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["OpticalPolarizer"]


class OpticalPolarizer(Component):
    """
    An optical polarizer.

    Information on the properties of polarizer is provided e.g.
    [here](https://www.rp-photonics.com/polarizers.html).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXoptical_polarizer",
            category="base",
            symbols={
                "N_spectrum": "Size of the wavelength array for which the refractive index of the material\n                and/or coating is given.",
                "N_spectrum_RT": "Size of the wavelength array for which the reflectance or transmission of\n                the polarizer is given.",
            },
        ),
    )

    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_polarizer.OpticalPolarizerShape",
        repeats=True,
        variable=True,
        description=(
            "Describe the geometry (shape, dimension etc.) of the device. "
            "Specify the dimensions in 'SHAPE/size'. A sketch of the device "
            "should be provided in the 'sketch(NXdata)' field to clarify (i) the "
            "shape and dimensions of the device, and (ii) the input and outputs "
            "(i.e. the direction of the incoming and outcoming (split) beams)."
        ),
    )
    substrate = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_polarizer.OpticalPolarizerSubstrate",
        repeats=False,
        description=(
            "Properties of the substrate material of the polarizer. If the "
            "device has a coating specify the coating material and its "
            "properties in ``coatingTYPE``."
        ),
    )
    coatingTYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_polarizer.OpticalPolarizerCoatingTYPE",
        repeats=True,
        variable=True,
        description=(
            "If the device has a coating describe the material and its "
            "properties. Some basic information can be found e.g. [here] "
            "(https://www.opto-e.com/basics/reflection-transmission-and-coatings). "
            "If the back and front side of the polarizer are coated with "
            "different materials, you may define two coatings (e.g. "
            "coating_front and coating_back)."
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-type-field"
        ],
        description=("Type of the polarizer"),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "dichroic",
                "linear",
                "circular",
                "Glan-Thompson prism",
                "Nicol prism",
                "Glan-Taylor prism",
                "Glan-Focault prism",
                "Wollaston prism",
                "Normarski prism",
                "Senarmont prism",
                "thin-film polarizer",
                "wire grid polarizer",
            ],
            open_enum=True,
        ),
    )
    polarizer_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-polarizer-angle-field"
        ],
        dimensionality="[angle]",
        description=("Angle of the polarizer."),
        a_nexus_field=NeXusField(
            name="polarizer_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANGLE",
        ),
    )
    acceptance_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-acceptance-angle-field"
        ],
        dimensionality="[angle]",
        shape=[2],
        description=("Acceptance angle of the polarizer (range)."),
        a_nexus_field=NeXusField(
            name="acceptance_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANGLE",
        ),
    )
    wavelength_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-wavelength-range-field"
        ],
        dimensionality="[length]",
        shape=[2],
        description=(
            "Wavelength range for which the polarizer is designed. Enter the "
            "minimum and maximum wavelength (lower and upper limit) of the "
            "range."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_WAVELENGTH",
        ),
    )
    extinction_ratio = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-extinction-ratio-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Extinction ratio (maximum to minimum transmission)."),
        a_nexus_field=NeXusField(
            name="extinction_ratio",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    reflection = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-reflection-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Reflection of the polarizer at given wavelength values."),
        a_nexus_field=NeXusField(
            name="reflection",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    transmission = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-transmission-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Transmission of the polarizer at given wavelength values."),
        a_nexus_field=NeXusField(
            name="transmission",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
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


class OpticalPolarizerShape(Shape):
    """
    Describe the geometry (shape, dimension etc.) of the device. Specify the
    dimensions in 'SHAPE/size'. A sketch of the device should be provided in
    the 'sketch(NXdata)' field to clarify (i) the shape and dimensions of the
    device, and (ii) the input and outputs (i.e. the direction of the incoming
    and outcoming (split) beams).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-shape-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    sketch = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="sketch",
            name_type="specified",
            optionality="optional",
        ),
    )

    shape = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-shape-shape-field"
        ],
        description=("Describe the shape (plate, cube, wedged, prism etc.)."),
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["cube", "cylinder", "plate", "prism", "wedged"],
            open_enum=True,
        ),
    )
    size = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-shape-size-field"
        ],
        shape=["*", "*"],
        description=(
            "Physical extent of the device. The device might be made up of one "
            "or more objects (NX_objects). The meaning and location of the axes "
            "used will vary according to the value of the 'shape' variable. "
            "'N_shapepar' defines how many parameters: * For 'cube' the "
            "parameters are (width, length). * For 'cylinder' the parameters are "
            "(diameter, length). * For 'plate' the parameters are (width, "
            "height, length). * For 'prism' the parameters are (width, height, "
            "length). * For 'wedged' the parameters are (width, height, shortest "
            "length). The wedge angle should be provided in 'SHAPE/wedge_angle'. "
            "* For 'other' the parameters may be (A, B, C, ...) with the labels "
            "defined in the sketch plotted in 'SHAPE/sketch'."
        ),
        a_nexus_field=NeXusField(
            name="size",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    wedge_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-shape-wedge-angle-field"
        ],
        dimensionality="[angle]",
        description=("Wedge angle if 'shape' is 'wedged'."),
        a_nexus_field=NeXusField(
            name="wedge_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalPolarizerSubstrate(Sample):
    """
    Properties of the substrate material of the polarizer. If the device has a
    coating specify the coating material and its properties in ``coatingTYPE``.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-substrate-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="substrate",
            name_type="specified",
            optionality="optional",
        ),
    )

    substrate_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-substrate-substrate-material-field"
        ],
        description=("Specify the substrate material of the polarizer."),
        a_nexus_field=NeXusField(
            name="substrate_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-substrate-substrate-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of the polarizer substrate."),
        a_nexus_field=NeXusField(
            name="substrate_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    index_of_refraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-substrate-index-of-refraction-field"
        ],
        dimensionality="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the polarizer material. Specify at "
            "given spectral values (wavelength, energy, wavenumber etc.)."
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


class OpticalPolarizerCoatingTYPE(Sample):
    """
    If the device has a coating describe the material and its properties. Some
    basic information can be found e.g. [here]
    (https://www.opto-e.com/basics/reflection-transmission-and-coatings). If
    the back and front side of the polarizer are coated with different
    materials, you may define two coatings (e.g. coating_front and
    coating_back).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-coatingtype-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="coatingTYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-coatingtype-material-field"
        ],
        description=("Describe the coating material (e.g. MgF2)."),
        a_nexus_field=NeXusField(
            name="material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    index_of_refraction_coating = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_polarizer.html#nxoptical_polarizer-coatingtype-index-of-refraction-coating-field"
        ],
        dimensionality="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the coating. Specify at given "
            "spectral values (wavelength, energy, wavenumber etc.)."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction_coating",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
