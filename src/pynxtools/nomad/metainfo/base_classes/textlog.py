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
# Run `pynx nomad generate-metainfo --nxdl NXtextlog` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Textlog"]


class Textlog(Object):
    """
    Textual Information recorded as a function of time.

    This is very similar to an :ref:`NXlog` but aimed at character rather than
    numeric data. It is to cover use cases when character data is to be
    recorded but using a large number of e.g. :ref:`NXnote` classes is
    undesirable.

    It would be used for cases like:

    - Status or error messages from hardware or software - Character based
    metadata e.g. labels that may vary during data collection

    Data is stored with times at which they were measured as elapsed time since
    a starting time recorded in ISO8601 format. The time units are specified in
    the units attribute. An optional scaling attribute can be used to
    accommodate non standard clocks.

    In order to make random access to timestamped data faster there is an
    optional array pair of ``cue_timestamp_zero`` and ``cue_index``. The
    ``cue_timestamp_zero`` will contain coarser timestamps than in the time
    array, say every five minutes. The ``cue_index`` will then contain the
    index into the time,value pair of arrays for that coarser
    ``cue_timestamp_zero``.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtextlog",
            category="base",
            symbols={"n": "Number of logged values"},
        ),
    )

    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            'Time of logged entry. The times are relative to the "start" '
            'attribute and in the units specified in the "units" attribute. '
            "Please note that absolute timestamps under unix are relative to "
            '``1970-01-01T00:00:00.0Z``. The "scaling_factor" attribute, when '
            "present, has to be applied to the time values in order to arrive at "
            'the units specified in the units attribute. The "scaling_factor" '
            "allows for arbitrary time units such as ticks of some hardware "
            "clock."
        ),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    time__start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-time-start-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="time",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    time__scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-time-scaling-factor-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="scaling_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="time",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-value-field"
        ],
        shape=["*"],
        description=(
            "String array of logged values, same length and dimensionality as "
            "``time`` array field. If you have stored multiple items here and "
            "wish each to be interpreted separately by the reader then you can "
            'specify a "separator" attribute to indicate how to split them up. '
            "However you should consider whether it is clearer to write multiple "
            "``value`` elements with the same ``time``, or separate NXtextlog "
            "instances, instead."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    value__separator = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-value-separator-attribute"
        ],
        description=(
            "Optional character string that can be used to specify how to split "
            "a text ``value`` into multiple items."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="separator",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="value",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-description-field"
        ],
        description=("Description of logged value"),
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
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-duration-field"
        ],
        flexible_unit=True,
        description=("Total time log was taken"),
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    cue_timestamp_zero = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-cue-timestamp-zero-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Timestamps matching the corresponding cue_index into the time, value pair."
        ),
        a_nexus_field=NeXusField(
            name="cue_timestamp_zero",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    cue_timestamp_zero__start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-cue-timestamp-zero-start-attribute"
        ],
        description=('If missing start is assumed to be the same as for "time".'),
        a_nexus_attribute=NeXusAttribute(
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="cue_timestamp_zero",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    cue_timestamp_zero__scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-cue-timestamp-zero-scaling-factor-attribute"
        ],
        description=('If missing start is assumed to be the same as for "time".'),
        a_nexus_attribute=NeXusAttribute(
            name="scaling_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="cue_timestamp_zero",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    cue_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtextlog.html#nxtextlog-cue-index-field"
        ],
        description=(
            "Index into the time, value pair matching the corresponding "
            "cue_timestamp_zero."
        ),
        a_nexus_field=NeXusField(
            name="cue_index",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
