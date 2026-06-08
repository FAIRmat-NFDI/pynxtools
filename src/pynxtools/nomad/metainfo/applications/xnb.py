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
# Run `pynx nomad generate-metainfo --nxdl NXxnb` to regenerate.
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
from pynxtools.nomad.metainfo.applications.xbase import Xbase
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xnb"]


class Xnb(Xbase):
    """
    raw data from a single crystal diffractometer, extends :ref:`NXxbase`

    This is the application definition for raw data from a single crystal
    diffractometer measuring in normal beam mode. It extends :ref:`NXxbase`, so
    the full definition is the content of :ref:`NXxbase` plus the data defined
    here. All angles are logged in order to support arbitrary scans in
    reciprocal space.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxnb",
            category="application",
            symbols={"nP": "Number of points"},
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
        section_def="pynxtools.nomad.metainfo.applications.xnb.XnbSample",
        repeats=False,
    )
    name_group = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xnb.XnbName",
        repeats=False,
    )

    definition = Quantity(
        type=MEnum(["NXxnb"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxnb"],
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-title-field"
        ],
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
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


class XnbSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb-entry-sample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=(
            "This is an array holding the sample rotation angle at each scan point"
        ),
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
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
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XnbName(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb-entry-name-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="name",
            name_type="specified",
            optionality="required",
        ),
    )

    polar_angle = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb-entry-name-polar-angle-link"
        ],
        a_nexus_link=NeXusLink(
            name="polar_angle",
            target="/NXentry/NXinstrument/NXdetector/polar_angle",
            optionality="required",
        ),
    )
    tilt = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb-entry-name-tilt-link"
        ],
        a_nexus_link=NeXusLink(
            name="tilt",
            target="/NXentry/NXinstrument/NXdetector/tilt",
            optionality="required",
        ),
    )
    rotation_angle = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxnb.html#nxxnb-entry-name-rotation-angle-link"
        ],
        a_nexus_link=NeXusLink(
            name="rotation_angle",
            target="/NXentry/NXsample/rotation_angle",
            optionality="required",
        ),
    )
    data_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxbase.html#nxxbase-entry-name-data-link"
        ],
        a_nexus_link=NeXusLink(
            name="data",
            target="/NXentry/NXinstrument/NXdetector/data",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
