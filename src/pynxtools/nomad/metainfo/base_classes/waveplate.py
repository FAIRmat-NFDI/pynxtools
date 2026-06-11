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
# Run `pynx nomad generate-metainfo --nxdl NXwaveplate` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Waveplate"]


class Waveplate(Component):
    """
    A waveplate or retarder.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXwaveplate",
            category="base",
            symbols={
                "N_spectrum": "Size of the wavelength array for which the refractive index of the material\n                and/or coating is given.",
                "N_wavelengths": "Number of discrete wavelengths for which the waveplate is designed. If it\n                operates for a range of wavelengths then N_wavelengths = 2 and the minimum\n                and maximum values of the range should be provided.",
            },
        ),
    )

    retardance_distribution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("Wavelength resolved retardance of the waveplate."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="retardance_distribution",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.waveplate.WaveplateSubstrate",
        repeats=False,
        description=(
            "Describe the material of the substrate of the waveplate in "
            "substrate/substrate_material and provide its index of refraction in "
            "substrate/index_of_refraction_substrate, if known."
        ),
    )
    coating = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.waveplate.WaveplateCoating",
        repeats=False,
        description=(
            "Is the waveplate coated? If yes, specify the type and material of "
            "the coating and the wavelength range for which it is designed. If "
            "known, you may also provide its index of refraction."
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-type-field"
        ],
        description=("Type of waveplate (e.g. achromatic or zero-order)."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "zero-order",
                "achromatic",
                "multiple-order",
                "dual-wavelength",
            ],
            open_enum=True,
        ),
    )
    retardance = Quantity(
        type=MEnum(["full-wave", "half-wave", "quarter-wave"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-retardance-field"
        ],
        description=(
            "Specify the retardance of the waveplate (e.g. full-wave, half-wave "
            "(lambda/2), quarter-wave (lambda/4))."
        ),
        a_nexus_field=NeXusField(
            name="retardance",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["full-wave", "half-wave", "quarter-wave"],
        ),
    )
    wavelengths = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-wavelengths-field"
        ],
        shape=["*"],
        description=(
            "Discrete wavelengths for which the waveplate is designed. If the "
            "waveplate operates over an entire range of wavelengths, enter the "
            "minimum and maximum values of the wavelength range (in this case "
            'N_wavelengths = 2). In this case, also use type="achromatic".'
        ),
        a_nexus_field=NeXusField(
            name="wavelengths",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Diameter of the waveplate (if the waveplate is circular)."),
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    clear_aperture = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-clear-aperture-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Clear aperture of the device (e.g. 90% of diameter for a disc or "
            "90% of length/height for square geometry)."
        ),
        a_nexus_field=NeXusField(
            name="clear_aperture",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    reflectance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-reflectance-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Average reflectance of the waveplate in percentage."),
        a_nexus_field=NeXusField(
            name="reflectance",
            type="NX_NUMBER",
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


class WaveplateSubstrate(Sample):
    """
    Describe the material of the substrate of the waveplate in
    substrate/substrate_material and provide its index of refraction in
    substrate/index_of_refraction_substrate, if known.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-substrate-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-substrate-substrate-material-field"
        ],
        description=(
            "Specify the material of the waveplate. If the device has a coating "
            "it should be described in coating/coating_material."
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-substrate-substrate-thickness-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Thickness of the waveplate substrate."),
        a_nexus_field=NeXusField(
            name="substrate_thickness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    index_of_refraction_substrate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-substrate-index-of-refraction-substrate-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the waveplate substrate. Specify at "
            "given wavelength (or energy, wavenumber etc.) values."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction_substrate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class WaveplateCoating(Sample):
    """
    Is the waveplate coated? If yes, specify the type and material of the
    coating and the wavelength range for which it is designed. If known, you
    may also provide its index of refraction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-coating-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="coating",
            name_type="specified",
            optionality="optional",
        ),
    )

    coating_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-coating-coating-type-field"
        ],
        description=(
            "Specify the coating type (e.g. dielectric, anti-reflection (AR), "
            "multilayer coating etc.)."
        ),
        a_nexus_field=NeXusField(
            name="coating_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    coating_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-coating-coating-material-field"
        ],
        description=("Specify the coating material."),
        a_nexus_field=NeXusField(
            name="coating_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    coating_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-coating-coating-thickness-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Thickness of the coating."),
        a_nexus_field=NeXusField(
            name="coating_thickness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    wavelength_range_coating = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-coating-wavelength-range-coating-field"
        ],
        shape=[2],
        description=(
            "Wavelength range for which the coating is designed. Enter the "
            "minimum and maximum values of the wavelength range."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_range_coating",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )
    index_of_refraction_coating = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXwaveplate.html#nxwaveplate-coating-index-of-refraction-coating-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the coating. Specify at given "
            "spectral values (wavelength, energy, wavenumber etc.)."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction_coating",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
