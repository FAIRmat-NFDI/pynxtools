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
# Run `pynx nomad generate-metainfo --nx-class NXcs_profiling` to regenerate.
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

__all__ = ["CsProfiling"]


class CsProfiling(Object):
    """
    Computer science description for performance and profiling data of an
    application.

    Performance monitoring and benchmarking of software is a task where
    questions can be asked at various levels of detail. In general, there are
    three main contributions to performance:

    * Hardware capabilities and configuration * Software configuration and
    capabilities * Dynamic effects of the system in operation and the system
    working together with eventually multiple computers, especially when these
    have to exchange information across a network and these are used usually by
    multiple users.

    At the most basic level users may wish to document how long e.g. a data
    analysis with a scientific software, i.e. an app took.

    A frequent idea is here to answer practical questions like how critical is
    the effect on the workflow of the scientists, i.e. is the analysis possible
    in a few seconds or would it take days if I were to run this analysis on a
    comparable machine? For this more qualitative performance monitoring,
    mainly the order of magnitude is relevant, as well as how this was achieved
    using parallelization (i.e. reporting the number of CPU and GPU resources
    used, the number of processes and threads configured, and providing basic
    details about the computer).

    At more advanced levels benchmarks may go as deep as detailed temporal
    tracking of individual processor instructions, their relation to other
    instructions, the state of call stacks; in short eventually the entire app
    execution history and hardware state history. Such analyses are mainly used
    for performance optimization, i.e. by software and hardware developers as
    well as for tracking bugs. Specialized software exists which documents such
    performance data in specifically-formatted event log files or databases.

    This base class cannot and should not replace these specific solutions for
    now. Instead, the intention of the base class is to serve scientists at the
    basic level to enable simple monitoring of performance data and log
    profiling data of key algorithmic steps or parts of computational
    workflows, so that these pieces of information can guide users which order
    of magnitude differences should be expected or not.

    Developers of application definitions should add additional fields and
    references to e.g. more detailed performance data to which they wish to
    link the metadata in this base class.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcs_profiling",
            category="base",
        ),
    )

    cs_computer = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_computer.CsComputer",
        repeats=True,
        variable=True,
        description=(
            "A collection with one or more computing nodes each with own "
            "resources. This can be as simple as a laptop or the nodes of a "
            "cluster computer."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_computer",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    eventID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_profiling_event.CsProfilingEvent",
        repeats=True,
        variable=True,
        description=(
            "A collection of individual profiling event data which detail e.g. "
            "how much time the app took for certain computational steps and/or "
            "how much memory was consumed during these operations. ID is an "
            "increasing unsigned integer starting at 1."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling_event",
            name="eventID",
            name_type="partial",
            optionality="optional",
        ),
    )

    current_working_directory = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-current-working-directory-field"
        ],
        description=("Path to the directory from which the tool was called."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="current_working_directory",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    command_line_call = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-command-line-call-field"
        ],
        description=("Command line call with arguments if applicable."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="command_line_call",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the app was started."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-end-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the app terminated or crashed."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        description=(
            "Wall-clock time how long the app execution took. This may be in "
            "principle end_time minus start_time; however usage of eventually "
            "more precise timers may warrant to use a finer temporal "
            "discretization, and thus demands a more precise record of the "
            "wall-clock time."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="total_elapsed_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    max_processes = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-max-processes-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The number of nominal processes that the app invoked at runtime. "
            "The main idea behind this field e.g. for apps which use e.g. MPI "
            "(Message Passing Interface) parallelization is to communicate how "
            "many processes were used. For sequentially running apps "
            "number_of_processes and number_of_threads is one. If the app "
            "exclusively uses GPU parallelization, number_of_gpus can be larger "
            "than one. If no GPU is used, number_of_gpus is zero, even though "
            "the hardware may have GPUs installed."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="max_processes",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    max_threads = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-max-threads-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The number of nominal threads that the app invoked at runtime. "
            "Specifically here the maximum number of threads used for the "
            "high-level threading library used (e.g. OMP_NUM_THREADS), posix."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="max_threads",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    max_gpus = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcs_profiling.html#nxcs_profiling-max-gpus-field"
        ],
        dimensionality="dimensionless",
        description=("The number of nominal GPUs that the app invoked at runtime."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="max_gpus",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
