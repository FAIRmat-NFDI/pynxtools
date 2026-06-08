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
# Run `pynx nomad generate-metainfo --nxdl NXcapillary` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
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

__all__ = ["Capillary"]


class Capillary(Component):
    """
    A capillary lens to focus the X-ray beam.

    Based on information provided by Gerd Wellenreuther (DESY).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcapillary",
            category="base",
        ),
    )

    gain = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("The gain of the capillary as a function of energy"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="gain",
            name_type="specified",
            optionality="optional",
        ),
    )
    transmission = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("The transmission of the capillary as a function of energy"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["single_bounce", "polycapillary", "conical_capillary"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-type-field"
        ],
        description=("Type of the capillary"),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["single_bounce", "polycapillary", "conical_capillary"],
        ),
    )
    manufacturer = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-manufacturer-field"
        ],
        description=(
            "The manufacturer of the capillary. This is actually important as it "
            "may have an impact on performance."
        ),
        a_nexus_field=NeXusField(
            name="manufacturer",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    maximum_incident_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-maximum-incident-angle-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="maximum_incident_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    accepting_aperture = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-accepting-aperture-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="accepting_aperture",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    working_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-working-distance-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="working_distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    focal_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-focal-size-field"
        ],
        description=("The focal size in FWHM"),
        a_nexus_field=NeXusField(
            name="focal_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a capillary lens."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
