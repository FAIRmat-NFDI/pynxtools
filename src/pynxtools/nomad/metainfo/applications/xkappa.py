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
# Run `pynx nomad generate-metainfo --nxdl NXxkappa` to regenerate.
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
from pynxtools.nomad.metainfo.applications.xbase import Xbase, XbaseData, XbaseSample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xkappa"]


class Xkappa(Xbase):
    """
    raw data from a kappa geometry (CAD4) single crystal diffractometer,
    extends :ref:`NXxbase`

    This is the application definition for raw data from a kappa geometry
    (CAD4) single crystal diffractometer. It extends :ref:`NXxbase`, so the
    full definition is the content of :ref:`NXxbase` plus the data defined
    here.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxkappa",
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
        section_def="pynxtools.nomad.metainfo.applications.xkappa.XkappaSample",
        repeats=False,
    )
    name_group = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xkappa.XkappaName",
        repeats=False,
    )

    definition = Quantity(
        type=MEnum(["NXxkappa"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxkappa"],
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


class XkappaSample(XbaseSample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-sample-rotation-angle-field"
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
    kappa = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-sample-kappa-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=("This is an array holding the kappa angle at each scan point"),
        a_nexus_field=NeXusField(
            name="kappa",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-sample-phi-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=("This is an array holding the phi angle at each scan point"),
        a_nexus_field=NeXusField(
            name="phi",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-sample-alpha-field"
        ],
        dimensionality="[angle]",
        description=("This holds the inclination angle of the kappa arm."),
        a_nexus_field=NeXusField(
            name="alpha",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XkappaName(XbaseData):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-name-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-name-polar-angle-link"
        ],
        a_nexus_link=NeXusLink(
            name="polar_angle",
            target="/NXentry/NXinstrument/NXdetector/polar_angle",
            optionality="required",
        ),
    )
    rotation_angle = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-name-rotation-angle-link"
        ],
        a_nexus_link=NeXusLink(
            name="rotation_angle",
            target="/NXentry/NXsample/rotation_angle",
            optionality="required",
        ),
    )
    kappa = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-name-kappa-link"
        ],
        a_nexus_link=NeXusLink(
            name="kappa",
            target="/NXentry/NXsample/kappa",
            optionality="required",
        ),
    )
    phi = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxkappa.html#nxxkappa-entry-name-phi-link"
        ],
        a_nexus_link=NeXusLink(
            name="phi",
            target="/NXentry/NXsample/phi",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
