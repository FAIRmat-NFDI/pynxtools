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
# Run `pynx nomad generate-metainfo --nxdl NXspm_piezo_sensor` to regenerate.
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
