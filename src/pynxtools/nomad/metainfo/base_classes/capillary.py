# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcapillary (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXcapillary` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    maximum_incident_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-maximum-incident-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="maximum_incident_angle",
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
    accepting_aperture = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-accepting-aperture-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="accepting_aperture",
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
    working_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcapillary.html#nxcapillary-working-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="working_distance",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
