# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXelectron_detector (see
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
# Run `pynx nomad generate-metainfo --nxdl NXelectron_detector` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.detector import Detector

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ElectronDetector"]


class ElectronDetector(Detector):
    """
    A subclass of NXdetector for detectors that detect electrons.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectron_detector.html#nxelectron_detector"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXelectron_detector",
            category="base",
        ),
    )

    amplifier_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectron_detector.html#nxelectron_detector-amplifier-type-field"
        ],
        description=("Type of electron amplifier, MCP, channeltron, etc."),
        a_nexus_field=NeXusField(
            name="amplifier_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    detector_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectron_detector.html#nxelectron_detector-detector-type-field"
        ],
        description=(
            "Description of the electron detector type, DLD, Phosphor+CCD, CMOS."
        ),
        a_nexus_field=NeXusField(
            name="detector_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    detector_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectron_detector.html#nxelectron_detector-detector-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("Voltage applied to the electron detector."),
        a_nexus_field=NeXusField(
            name="detector_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    amplifier_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectron_detector.html#nxelectron_detector-amplifier-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("Voltage applied to the amplifier."),
        a_nexus_field=NeXusField(
            name="amplifier_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    amplifier_bias = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectron_detector.html#nxelectron_detector-amplifier-bias-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("The low voltage of the amplifier might not be the ground."),
        a_nexus_field=NeXusField(
            name="amplifier_bias",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
