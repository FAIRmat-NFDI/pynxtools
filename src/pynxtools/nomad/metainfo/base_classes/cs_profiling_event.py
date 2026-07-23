# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcs_profiling_event (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXcs_profiling_event` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.data import ArchiveSection
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

__all__ = ["CsProfilingEvent"]


class CsProfilingEvent(Object, ArchiveSection):
    """
    Computer science description of a profiling event.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcs_profiling_event",
            category="base",
            symbols={"n_processes": "Number of processes."},
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the event tracking started."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-end-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the event tracking ended."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-description-field"
        ],
        description=(
            "Free-text description what was monitored/executed during the event."
        ),
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
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-elapsed-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Wall-clock time how long the event took. This may be in principle "
            "end_time minus start_time; however usage of eventually more precise "
            "timers may warrant to use a finer temporal discretization, and thus "
            "demand for a more precise record of the wall-clock time. Elapsed "
            "time may contain time portions where resources were idling."
        ),
        a_nexus_field=NeXusField(
            name="elapsed_time",
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
    max_processes = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-max-processes-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The number of nominal processes that the app invoked during the "
            "execution of this event. The main idea behind this field e.g. for "
            "apps which use e.g. MPI (Message Passing Interface) parallelization "
            "is to communicate how many processes were used. For sequentially "
            "running apps number_of_processes and number_of_threads is one. If "
            "the app exclusively uses GPU parallelization, number_of_gpus can be "
            "larger than one. If no GPU is used, number_of_gpus is zero, even "
            "though the hardware may have GPUs installed."
        ),
        a_nexus_field=NeXusField(
            name="max_processes",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    max_threads = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-max-threads-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The number of nominal threads that the app invoked at during the "
            "execution of this event. Specifically here the maximum number of "
            "threads used for the high-level threading library used (e.g. "
            "OMP_NUM_THREADS), posix."
        ),
        a_nexus_field=NeXusField(
            name="max_threads",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    max_gpus = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-max-gpus-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The number of nominal GPUs that the app invoked during the "
            "execution of this event."
        ),
        a_nexus_field=NeXusField(
            name="max_gpus",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    max_virtual_memory_snapshot = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-max-virtual-memory-snapshot-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Maximum amount of virtual memory allocated per process during the event."
        ),
        a_nexus_field=NeXusField(
            name="max_virtual_memory_snapshot",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    max_resident_memory_snapshot = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling_event.html#nxcs_profiling_event-max-resident-memory-snapshot-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Maximum amount of resident memory allocated per process during the event."
        ),
        a_nexus_field=NeXusField(
            name="max_resident_memory_snapshot",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
