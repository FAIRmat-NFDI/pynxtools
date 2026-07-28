# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXsolenoid_magnet (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXsolenoid_magnet` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
from pynxtools.nomad.metainfo.base_classes.log import Log

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SolenoidMagnet"]


class SolenoidMagnet(Component):
    """
    definition for a solenoid magnet.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsolenoid_magnet",
            category="base",
        ),
    )

    read_current = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.solenoid_magnet.SolenoidMagnetReadCurrent",
        repeats=False,
    )
    read_voltage = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.solenoid_magnet.SolenoidMagnetReadVoltage",
        repeats=False,
    )

    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-description-field"
        ],
        description=("extended description of the magnet."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.RichTextEditQuantity,
        ),
    )
    beamline_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-beamline-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "define position of beamline element relative to production target"
        ),
        a_nexus_field=NeXusField(
            name="beamline_distance",
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
    set_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-set-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("current set on supply."),
        a_nexus_field=NeXusField(
            name="set_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class SolenoidMagnetReadCurrent(Log):
    """
    current read from supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-current-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_current",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-current-value-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        a_nexus_field=NeXusField(
            name="value",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SolenoidMagnetReadVoltage(Log):
    """
    voltage read from supply.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-voltage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="read_voltage",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsolenoid_magnet.html#nxsolenoid_magnet-read-voltage-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="value",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
