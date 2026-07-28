# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXspm_piezo_sensor (see
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
# Run `pynx nomad generate-metainfo --nxdl NXspm_piezo_sensor` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmPiezoSensor"]


class SpmPiezoSensor(Sensor):
    """
    This piezo sensor group refers to the height (or Z) piezo sensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_sensor.html#nxspm_piezo_sensor"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_piezo_sensor",
            category="base",
        ),
    )

    piezo_configuration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_config.SpmPiezoConfig",
        repeats=False,
        description=(
            "The piezo configuration information like piezoelectric calibration "
            "and material properties."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezo_config",
            name="piezo_configuration",
            name_type="specified",
            optionality="optional",
        ),
    )
    spm_positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_positioner.SpmPositioner",
        repeats=True,
        variable=True,
        description=(
            "The positioner information like the position of the tip, the "
            "position of the sample, PID controller etc."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_positioner",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    piezo_material = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezoelectric_material.SpmPiezoelectricMaterial",
        repeats=False,
        description=(
            "The material description and properties of the piezoelectric "
            "scanner materials."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezoelectric_material",
            name="piezo_material",
            name_type="specified",
            optionality="optional",
        ),
    )

    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_sensor.html#nxspm_piezo_sensor-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The x position (e.g., target or averaged target value) of the piezo."
        ),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_sensor.html#nxspm_piezo_sensor-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The y position (e.g., target or averaged target value) of the piezo."
        ),
        a_nexus_field=NeXusField(
            name="y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_sensor.html#nxspm_piezo_sensor-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The z position (e.g., target or averaged target value) of the piezo."
        ),
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    AXISoffset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_sensor.html#nxspm_piezo_sensor-axisoffset-value-field"
        ],
        variable=True,
        dimensionality="[length]",
        unit="m",
        description=(
            "The offset value for the piezo axis (X, Y, or Z) that will be added "
            "to the measured value."
        ),
        a_nexus_field=NeXusField(
            name="AXISoffset_value",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
