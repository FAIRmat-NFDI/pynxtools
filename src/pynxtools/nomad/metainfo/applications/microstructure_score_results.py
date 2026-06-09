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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_score_results` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.microstructure import Microstructure
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.program import Program

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructureScoreResults"]


class MicrostructureScoreResults(Entry):
    """
    Application definition for storing results of the SCORE cellular automata
    model.

    The SCORE cellular automata model for primary recrystallization is an
    example of a typical materials engineering application used within the
    field of so-called Integral Computational Materials Engineering (ICME)
    whereby one can simulate the evolution of microstructures.

    Specifically the SCORE model can be used to simulate the growth of nuclei
    during static recrystallization. The model is described in the literature:

    * `M. Kühbach et al. <https://doi.org/10.1016/j.actamat.2016.01.068>`_ *
    `C. Haase et al. <https://doi.org/10.1016/j.actamat.2015.08.057>`_ * `M.
    Diehl et al. <https://doi.org/10.1088/1361-651X/ab51bd>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_score_results",
            category="application",
            symbols={
                "n_summary_stats": "The total number of summary statistic log entries",
                "n_b": "Number of boundaries of the bounding box or primitive about the computational\n                domain",
                "n_p": "Number of parameter required for chosen orientation parameterization",
                "n_tex": "Number of texture components identified",
                "d": "Dimensionality",
                "c": "Cardinality",
                "n_front": "Number of active cells in the (recrystallization) front",
                "n_grains": "Number of grains in the computer simulation",
            },
        ),
    )

    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsConfig",
        repeats=False,
        description=(
            "Configuration file with the parameterization of the SCORE model "
            "that was used for this simulation."
        ),
    )
    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_profiling.CsProfiling",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="optional",
        ),
    )
    program1 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsProgram1",
        repeats=False,
        description=("Name of the program with which the simulation was performed."),
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsEnvironment",
        repeats=False,
        description=(
            "Programs and libraries representing the computational environment"
        ),
    )
    sample_reference_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSampleReferenceFrame",
        repeats=False,
    )
    discretization = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsDiscretization",
        repeats=False,
    )
    spatiotemporalID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalID",
        repeats=True,
        variable=True,
        description=(
            "Documentation of the spatiotemporal evolution for each CA domain. "
            "SCORE is a hybrid parallelized code that can evolve multiple "
            "replicas in parallel. The set of replicas is distributed across MPI "
            "processes. Each such replica is then evolved via OpenMP "
            "multi-threading."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXmicrostructure_score_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmicrostructure_score_results"],
        ),
    )
    identifier_simulation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-identifier-simulation-field"
        ],
        description=("Simulation ID as an alias to refer to this simulation."),
        a_nexus_field=NeXusField(
            name="identifier_simulation",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-description-field"
        ],
        description=(
            "Discouraged free-text field to add further details to the computation."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the simulation was started."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-end-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the simulation ended."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
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


class MicrostructureScoreResultsConfig(Note):
    """
    Configuration file with the parameterization of the SCORE model that was
    used for this simulation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-config-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-config-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-config-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsProgram1(Program):
    """
    Name of the program with which the simulation was performed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-program1-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="program1",
            name_type="specified",
            optionality="required",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-program1-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-program1-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsEnvironment(Collection):
    """
    Programs and libraries representing the computational environment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="optional",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSampleReferenceFrame(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="sample_reference_frame",
            name_type="specified",
            optionality="required",
        ),
    )

    type = Quantity(
        type=MEnum(["cartesian"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["cartesian"],
        ),
    )
    handedness = Quantity(
        type=MEnum(["right_handed"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-handedness-field"
        ],
        a_nexus_field=NeXusField(
            name="handedness",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["right_handed"],
        ),
    )
    origin = Quantity(
        type=MEnum(["front_bottom_left"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-origin-field"
        ],
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["front_bottom_left"],
        ),
    )
    x_alias = Quantity(
        type=MEnum(["rolling_direction"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-x-alias-field"
        ],
        a_nexus_field=NeXusField(
            name="x_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["rolling_direction"],
        ),
    )
    x_direction = Quantity(
        type=MEnum(["east"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-x-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["east"],
        ),
    )
    y_alias = Quantity(
        type=MEnum(["transverse_direction"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-y-alias-field"
        ],
        a_nexus_field=NeXusField(
            name="y_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["transverse_direction"],
        ),
    )
    y_direction = Quantity(
        type=MEnum(["in"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-y-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["in"],
        ),
    )
    z_alias = Quantity(
        type=MEnum(["normal_direction"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-z-alias-field"
        ],
        a_nexus_field=NeXusField(
            name="z_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["normal_direction"],
        ),
    )
    z_direction = Quantity(
        type=MEnum(["north"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-sample-reference-frame-z-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["north"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsDiscretization(Microstructure):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="discretization",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    boundary = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_hexahedron.CgHexahedron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="boundary",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalID(Process):
    """
    Documentation of the spatiotemporal evolution for each CA domain.

    SCORE is a hybrid parallelized code that can evolve multiple replicas in
    parallel. The set of replicas is distributed across MPI processes. Each
    such replica is then evolved via OpenMP multi-threading.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="spatiotemporalID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    summary_statistics = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="summary_statistics",
            name_type="specified",
            optionality="required",
        ),
    )
    microstructureID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.Microstructure",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="microstructureID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
