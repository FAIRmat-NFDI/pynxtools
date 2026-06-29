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
# Run `pynx nomad generate-metainfo --nxdl NXxrot` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.applications.xbase import Xbase, XbaseData, XbaseSample
from pynxtools.nomad.metainfo.base_classes.attenuator import Attenuator
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xrot"]


class Xrot(Xbase):
    """
    raw data from a rotation camera, extends :ref:`NXxbase`

    This is the application definition for raw data from a rotation camera. It
    extends :ref:`NXxbase`, so the full definition is the content of
    :ref:`NXxbase` plus the data defined here.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxrot",
            category="application",
            symbols={"nP": "Number of points"},
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrot.XrotInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrot.XrotSample",
        repeats=False,
    )
    name_group = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrot.XrotName",
        repeats=False,
    )

    definition = Quantity(
        type=MEnum(["NXxrot"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxrot"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxrot",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
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


class XrotInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrot.XrotInstrumentDetector",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector",
            name_type="specified",
            optionality="required",
        ),
    )
    attenuator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrot.XrotInstrumentAttenuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name="attenuator",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrotInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-instrument-detector-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector",
            name_type="specified",
            optionality="required",
        ),
    )

    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-instrument-detector-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", "*", "*"],
        description=("The polar_angle (two theta) where the detector is placed."),
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    beam_center_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-instrument-detector-beam-center-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the x position where the direct beam would hit the "
            "detector. This is a length, not a pixel position, and can be "
            "outside of the actual detector."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    beam_center_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-instrument-detector-beam-center-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the y position where the direct beam would hit the "
            "detector. This is a length, not a pixel position, and can be "
            "outside of the actual detector."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrotInstrumentAttenuator(Attenuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-instrument-attenuator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name="attenuator",
            name_type="specified",
            optionality="required",
        ),
    )

    attenuator_transmission = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-instrument-attenuator-attenuator-transmission-field"
        ],
        flexible_unit=True,
        a_nexus_field=NeXusField(
            name="attenuator_transmission",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrotSample(XbaseSample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-sample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "This is an array holding the sample rotation start angle at each "
            "scan point"
        ),
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    rotation_angle_step = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-sample-rotation-angle-step-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "This is an array holding the step made for sample rotation angle at "
            "each scan point"
        ),
        a_nexus_field=NeXusField(
            name="rotation_angle_step",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrotName(XbaseData):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-name-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="name",
            name_type="specified",
            optionality="required",
        ),
    )

    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxrot.html#nxxrot-entry-name-rotation-angle-link"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        a_nexus_link=NeXusLink(
            name="rotation_angle",
            target="/NXentry/NXsample/rotation_angle",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
