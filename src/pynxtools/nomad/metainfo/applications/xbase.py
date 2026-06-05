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
# Run `pynx nomad generate-metainfo --nx-class NXxbase` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xbase"]


class Xbase(Entry):
    """
    This definition covers the common parts of all monochromatic single crystal
    raw data application definitions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxbase",
            category="application",
            symbols={
                "nP": "Number of points",
                "nXPixels": "Number of X pixels",
                "nYPixels": "Number of Y pixels",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xbase.XbaseSample",
        repeats=False,
    )
    control = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xbase.XbaseControl",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        description=(
            "The name of this group id data if there is only one detector; if "
            "there are several the names will be data1, data2, data3 and will "
            "point to the corresponding detector groups in the instrument "
            "hierarchy."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-title-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-start-time-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXxbase"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxbase"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class XbaseSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    orientation_matrix = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-orientation-matrix-field"
        ],
        shape=[3, 3],
        description=(
            "The orientation matrix according to Busing and Levy conventions. "
            "This is not strictly necessary as the UB can always be derived from "
            "the data. But let us bow to common usage which includes the UB "
            "nearly always."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="orientation_matrix",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    unit_cell = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-unit-cell-field"
        ],
        dimensionality="[length]",
        shape=[6],
        description=(
            "The unit cell, a, b, c, alpha, beta, gamma. Again, not strictly "
            "necessary, but normally written."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="unit_cell",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-temperature-field"
        ],
        dimensionality="[temperature]",
        shape=["*"],
        description=(
            "The sample temperature or whatever sensor represents this value best"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )
    x_translation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-x-translation-field"
        ],
        dimensionality="[length]",
        description=(
            "Translation of the sample along the X-direction of the laboratory "
            "coordinate system"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="x_translation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    y_translation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-y-translation-field"
        ],
        dimensionality="[length]",
        description=(
            "Translation of the sample along the Y-direction of the laboratory "
            "coordinate system"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="y_translation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-distance-field"
        ],
        dimensionality="[length]",
        description=(
            "Translation of the sample along the Z-direction of the laboratory "
            "coordinate system"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XbaseControl(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-control-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name="control",
            name_type="specified",
            optionality="required",
        ),
    )

    mode = Quantity(
        type=MEnum(["monitor", "timer"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-control-mode-field"
        ],
        description=(
            "Count to a preset value based on either clock time (timer) or "
            "received monitor counts (monitor)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["monitor", "timer"],
        ),
    )
    preset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-control-preset-field"
        ],
        description=("preset value for time or monitor"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="preset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    integral = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-control-integral-field"
        ],
        description=("Total integral monitor counts"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="integral",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
