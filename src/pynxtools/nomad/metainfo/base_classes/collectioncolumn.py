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
# Run `pynx nomad generate-metainfo --nxdl NXcollectioncolumn` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import MEnum, Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Collectioncolumn"]


class Collectioncolumn(Component):
    """
    Electron collection column of an electron analyzer.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcollectioncolumn",
            category="base",
        ),
    )

    aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=True,
        variable=True,
        description=(
            "The size and position of an aperture inserted in the column, e.g. "
            "field aperture or contrast aperture"
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
        description=("Deflectors in the collection column section"),
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
        description=("Individual lenses in the collection column section"),
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    scheme = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-scheme-field"
        ],
        description=(
            "Scheme of the electron collection lens, i.e. angular dispersive, "
            "spatial dispersive, momentum dispersive, non-dispersive, etc."
        ),
        a_nexus_field=NeXusField(
            name="scheme",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    extractor_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-extractor-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("Voltage applied to the extractor lens"),
        a_nexus_field=NeXusField(
            name="extractor_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    extractor_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-extractor-current-field"
        ],
        dimensionality="[current]",
        description=(
            "Current necessary to keep the extractor lens at a set voltage. "
            "Variations indicate leakage, field emission or arc currents to the "
            "extractor lens."
        ),
        a_nexus_field=NeXusField(
            name="extractor_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    working_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-working-distance-field"
        ],
        dimensionality="[length]",
        description=("Distance between sample and detector entrance"),
        a_nexus_field=NeXusField(
            name="working_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    lens_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-lens-mode-field"
        ],
        description=("Labelling of the lens setting in use."),
        a_nexus_field=NeXusField(
            name="lens_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    projection = Quantity(
        type=MEnum(["real", "reciprocal"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-projection-field"
        ],
        description=(
            "The space projected in the angularly dispersive directions, real or "
            "reciprocal"
        ),
        a_nexus_field=NeXusField(
            name="projection",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["real", "reciprocal"],
        ),
    )
    angular_acceptance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-angular-acceptance-field"
        ],
        dimensionality="[angle]",
        description=(
            "Acceptance angle of the collection column. This concept is related "
            "to term `7.4`_ of the ISO 18115-1:2023 standard. .. _7.4: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:7.4"
        ),
        a_nexus_field=NeXusField(
            name="angular_acceptance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    spatial_acceptance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-spatial-acceptance-field"
        ],
        dimensionality="[length]",
        description=("Acceptance length or area of the collection column."),
        a_nexus_field=NeXusField(
            name="spatial_acceptance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    magnification = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcollectioncolumn.html#nxcollectioncolumn-magnification-field"
        ],
        dimensionality="dimensionless",
        description=("The magnification of the electron lens assembly."),
        a_nexus_field=NeXusField(
            name="magnification",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
