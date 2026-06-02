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
# Run `pynx nomad generate-metainfo --nx-class NXscan_controller` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ScanController"]


class ScanController(Component):
    """
    The scan box or scan controller is a component that is used to deflect a
    beam of charged particles in a controlled manner.

    The scan box is instructed by (an) instance(s) of :ref:`NXprogram`, some
    control software, which is not necessarily the same program as the one
    controlling other parts of the instrument.

    The scan box directs the probe of charged particles (electrons, ions) to
    controlled locations according to a scan scheme and plan.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXscan_controller.html#nxscan_controller"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXscan_controller",
            category="base",
        ),
    )

    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        description=(
            "Details about components which realize the deflection technically. "
            "This concept should be used for all those components that implement "
            "the scanning of the beam, while components like beam blankers etc. "
            "should use rather the NXdeflector concept of the NXebeam_column "
            "base class."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    circuit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.circuit.Circuit",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcircuit",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    scan_schema = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXscan_controller.html#nxscan_controller-scan-schema-field"
        ],
        description=(
            "Name of the typically tech-partner-specific term that specifies an "
            "automated protocol which details how the components of the scan_box "
            "and the instrument work together to achieve a controlled scanning "
            "of the beam (over the sample surface). Oftentimes users do not need "
            "to or are not able to disentangle the intricate details of the "
            "spatiotemporal dynamics of their instrument. Instead, often they "
            "rely on the assumption that the instrument and its controlling "
            "programs work as expected. The field scan_schema can be used to add "
            "some constraints on how the beam was scanned over the surface."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="scan_schema",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    dwell_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXscan_controller.html#nxscan_controller-dwell-time-field"
        ],
        dimensionality="[time]",
        description=(
            "Time period during which the beam remains at one position. This "
            "concept is related to term `Dwell Time`_ of the EMglossary "
            "standard. .. _Dwell Time: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000015"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="dwell_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    flyback_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXscan_controller.html#nxscan_controller-flyback-time-field"
        ],
        dimensionality="[time]",
        description=(
            "Time period during which the beam moves from the final position of "
            "one scan line to the starting position of the subsequent scan line. "
            "This concept is related to term `Flyback Time`_ of the EMglossary "
            "standard. .. _Flyback Time: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000028"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="flyback_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
