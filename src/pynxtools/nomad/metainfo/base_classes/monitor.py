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
# Run `pynx nomad generate-metainfo --nxdl NXmonitor` to regenerate.
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

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Monitor"]


class Monitor(Component):
    """
    A monitor of incident beam data.

    It is similar to the :ref:`NXdata` groups containing monitor data and its
    associated axis coordinates, e.g. time_of_flight or wavelength in pulsed
    neutron instruments. However, it may also include integrals, or scalar
    monitor counts, which are often used in both in both pulsed and
    steady-state instrumentation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmonitor",
            category="base",
        ),
    )

    integral_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("Time variation of monitor counts"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="integral_log",
            name_type="specified",
            optionality="optional",
        ),
    )
    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=("Geometry of the monitor"),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the monitor and NXoff_geometry to describe its shape instead",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the beam line component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    mode = Quantity(
        type=MEnum(["monitor", "timer"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-mode-field"
        ],
        description=(
            "Count to a preset value based on either clock time (timer) or "
            "received monitor counts (monitor)."
        ),
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["monitor", "timer"],
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-start-time-field"
        ],
        description=("Starting time of measurement"),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-end-time-field"
        ],
        description=("Ending time of measurement"),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    preset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-preset-field"
        ],
        description=("preset value for time or monitor"),
        a_nexus_field=NeXusField(
            name="preset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-distance-field"
        ],
        dimensionality="[length]",
        description=("Distance of monitor from sample"),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
            deprecated="Use transformations/distance instead",
        ),
    )
    range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-range-field"
        ],
        shape=[2],
        description=(
            "Range (X-axis, Time-of-flight, etc.) over which the integral was "
            "calculated"
        ),
        a_nexus_field=NeXusField(
            name="range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    nominal = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-nominal-field"
        ],
        description=("Nominal reading to be used for normalisation purposes."),
        a_nexus_field=NeXusField(
            name="nominal",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    integral = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-integral-field"
        ],
        description=("Total integral monitor counts"),
        a_nexus_field=NeXusField(
            name="integral",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    type = Quantity(
        type=MEnum(["Fission Chamber", "Scintillator"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["Fission Chamber", "Scintillator"],
        ),
    )
    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-time-of-flight-field"
        ],
        dimensionality="[time]",
        description=("Time-of-flight"),
        a_nexus_field=NeXusField(
            name="time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME_OF_FLIGHT",
        ),
    )
    efficiency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-efficiency-field"
        ],
        dimensionality="dimensionless",
        description=("Monitor efficiency"),
        a_nexus_field=NeXusField(
            name="efficiency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-data-field"
        ],
        description=("Monitor data"),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    sampled_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-sampled-fraction-field"
        ],
        dimensionality="dimensionless",
        description=("Proportion of incident beam sampled by the monitor (0<x<1)"),
        a_nexus_field=NeXusField(
            name="sampled_fraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    count_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-count-time-field"
        ],
        dimensionality="[time]",
        description=(
            "Elapsed actual counting time, can be an array of size ``np`` when "
            "scanning. This is not the difference of the calendar time but the "
            "time the instrument was really counting, without pauses or times "
            "lost due beam unavailability"
        ),
        a_nexus_field=NeXusField(
            name="count_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonitor.html#nxmonitor-depends-on-field"
        ],
        description=(
            "The reference plane of the monitor contains the surface of the "
            "detector that faces the source and is the entry point of the beam. "
            "The reference point of the monitor in the x and y axis is its "
            "centre on this surface. The reference plane is orthogonal to the "
            "the z axis and the reference point on this z axis is where they "
            "intersect. .. image:: monitor/monitor.png :width: 40%"
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
