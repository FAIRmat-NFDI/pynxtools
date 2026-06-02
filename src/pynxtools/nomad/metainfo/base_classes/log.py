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
# Run `pynx nomad generate-metainfo --nx-class NXlog` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Log"]


class Log(Object):
    """
    Information recorded as a function of time.

    Description of information that is recorded against time. There are two
    common use cases for this:

    - When logging data such as temperature during a run - When data is taken
    in streaming mode data acquisition, i.e. just timestamp, value pairs are
    stored and correlated later in data reduction with other data,

    In both cases, NXlog contains the logged or streamed values and the times
    at which they were measured as elapsed time since a starting time recorded
    in ISO8601 format. The time units are specified in the units attribute. An
    optional scaling attribute can be used to accommodate non standard clocks.

    This method of storing logged data helps to distinguish instances in which
    a variable contains signal or axis coordinate values of plottable data, in
    which case it is stored in an :ref:`NXdata` group, and instances in which
    it is logged during the run, when it should be stored in an :ref:`NXlog`
    group.

    In order to make random access to timestamped data faster there is an
    optional array pair of ``cue_timestamp_zero`` and ``cue_index``. The
    ``cue_timestamp_zero`` will contain coarser timestamps than in the time
    array, say every five minutes. The ``cue_index`` will then contain the
    index into the time,value pair of arrays for that coarser
    ``cue_timestamp_zero``.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXlog",
            category="base",
        ),
    )

    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-time-field"
        ],
        dimensionality="[time]",
        description=(
            'Time of logged entry. The times are relative to the "start" '
            'attribute and in the units specified in the "units" attribute. '
            "Please note that absolute timestamps under unix are relative to "
            "``1970-01-01T00:00:00.0Z``. The scaling_factor, when present, has "
            "to be applied to the time values in order to arrive at the units "
            "specified in the units attribute. The scaling_factor allows for "
            "arbitrary time units such as ticks of some hardware clock."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-time-start-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="time",
        ),
    )
    time__scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-time-scaling-factor-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="scaling_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="time",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-value-field"
        ],
        description=(
            "Array of logged value, such as temperature. If this is a single "
            "value the dimensionality is nEntries. However, NXlog can also be "
            "used to store multi dimensional time stamped data such as images. "
            "In this example the dimensionality of values would be "
            "value[nEntries,xdim,ydim]."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    raw_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-raw-value-field"
        ],
        description=("Array of raw information, such as thermocouple voltage"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="raw_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-description-field"
        ],
        description=("Description of logged value"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    average_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-average-value-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="average_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    average_value_error = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-average-value-error-field"
        ],
        description=(
            "estimated uncertainty (often used: standard deviation) of average_value"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="average_value_error",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
            deprecated="see: https://github.com/nexusformat/definitions/issues/639",
        ),
    )
    average_value_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-average-value-errors-field"
        ],
        description=(
            "estimated uncertainty (often used: standard deviation) of average_value"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="average_value_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    minimum_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-minimum-value-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="minimum_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    maximum_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-maximum-value-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="maximum_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-duration-field"
        ],
        description=("Total time log was taken"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    cue_timestamp_zero = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-cue-timestamp-zero-field"
        ],
        dimensionality="[time]",
        description=(
            "Timestamps matching the corresponding cue_index into the time, value pair."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="cue_timestamp_zero",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    cue_timestamp_zero__start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-cue-timestamp-zero-start-attribute"
        ],
        description=('If missing start is assumed to be the same as for "time".'),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="cue_timestamp_zero",
        ),
    )
    cue_timestamp_zero__scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-cue-timestamp-zero-scaling-factor-attribute"
        ],
        description=('If missing start is assumed to be the same as for "time".'),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="scaling_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="cue_timestamp_zero",
        ),
    )
    cue_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXlog.html#nxlog-cue-index-field"
        ],
        description=(
            "Index into the time, value pair matching the corresponding "
            "cue_timestamp_zero."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="cue_index",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
