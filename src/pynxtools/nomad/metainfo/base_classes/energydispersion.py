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
# Run `pynx nomad generate-metainfo --nxdl NXenergydispersion` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
# Add normalize() logic directly; it will be preserved on regeneration.
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

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Energydispersion"]


class Energydispersion(Component):
    """
    Energy dispersion section of an electron analyzer.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXenergydispersion",
            category="base",
        ),
    )

    aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=True,
        variable=True,
        description=(
            "Size, position and shape of a slit in dispersive analyzer, e.g. "
            "entrance and exit slits."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        description=("Deflectors in the energy dispersive section"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    electromagnetic_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electromagnetic_lens.ElectromagneticLens",
        repeats=True,
        variable=True,
        description=("Individual lenses in the energy dispersive section"),
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    scheme = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-scheme-field"
        ],
        description=(
            "Energy dispersion scheme employed, for example: tof, hemispherical, "
            "cylindrical, mirror, retarding grid, etc."
        ),
        a_nexus_field=NeXusField(
            name="scheme",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    pass_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-pass-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Mean kinetic energy of the electrons in this energy-dispersive "
            "section of the analyzer. This term should be used for hemispherical "
            "analyzers. This concept is related to term `12.63`_ of the ISO "
            "18115-1:2023 standard. .. _12.63: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.63"
        ),
        a_nexus_field=NeXusField(
            name="pass_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    kinetic_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-kinetic-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Kinetic energy set for this dispersive section. Can be either the "
            "set kinetic energy, or the whole calibrated energy axis of a scan."
        ),
        a_nexus_field=NeXusField(
            name="kinetic_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    drift_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-drift-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("Drift energy for time-of-flight energy dispersive elements."),
        a_nexus_field=NeXusField(
            name="drift_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    center_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-center-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("Center of the energy window"),
        a_nexus_field=NeXusField(
            name="center_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    energy_interval = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-energy-interval-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "The interval of transmitted energies. It can be two different "
            "things depending on whether the scan is fixed or swept. With a "
            "fixed scan it is a 2 vector containing the extrema of the "
            "transmitted energy window (smaller number first). With a swept scan "
            "of m steps it is a 2xm array of windows, one for each measurement "
            "point."
        ),
        a_nexus_field=NeXusField(
            name="energy_interval",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Diameter of the dispersive orbit"),
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
    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Radius of the dispersive orbit"),
        a_nexus_field=NeXusField(
            name="radius",
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
    energy_scan_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-energy-scan-mode-field"
        ],
        description=("Way of scanning the energy axis"),
        a_nexus_field=NeXusField(
            name="energy_scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "fixed_analyzer_transmission",
                "fixed_retardation_ratio",
                "fixed_energy",
                "snapshot",
                "dither",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    tof_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXenergydispersion.html#nxenergydispersion-tof-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Length of the time-of-flight drift electrode"),
        a_nexus_field=NeXusField(
            name="tof_distance",
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
