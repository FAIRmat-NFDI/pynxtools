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
from pynxtools.nomad.metainfo.base_classes.cg_grid import CgGrid
from pynxtools.nomad.metainfo.base_classes.cg_hexahedron import CgHexahedron
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.microstructure import Microstructure
from pynxtools.nomad.metainfo.base_classes.microstructure_feature import (
    MicrostructureFeature,
)
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
        categories=[ExperimentCategory],
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
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsEnvironmentProgramID",
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


class MicrostructureScoreResultsEnvironmentProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-environment-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-environment-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-environment-programid-program-version-attribute"
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

    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsDiscretizationGrid",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )
    boundary = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsDiscretizationBoundary",
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


class MicrostructureScoreResultsDiscretizationGrid(CgGrid):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-cardinality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="cardinality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    origin = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-origin-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    symmetry = Quantity(
        type=MEnum(["cubic"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-symmetry-field"
        ],
        a_nexus_field=NeXusField(
            name="symmetry",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["cubic"],
        ),
    )
    cell_dimensions = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-cell-dimensions-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="cell_dimensions",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    extent = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-extent-field"
        ],
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    index_offset_cell = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-grid-index-offset-cell-field"
        ],
        a_nexus_field=NeXusField(
            name="index_offset_cell",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsDiscretizationBoundary(CgHexahedron):
    """
    A tight bounding box or sphere or bounding primitive about the grid.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-boundary-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="boundary",
            name_type="specified",
            optionality="required",
        ),
    )

    number_of_boundaries = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-boundary-number-of-boundaries-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "How many distinct boundaries are distinguished? Most grids "
            "discretize a cubic or cuboidal region. In this case six sides can "
            "be distinguished, each making an own boundary."
        ),
        a_nexus_field=NeXusField(
            name="number_of_boundaries",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    boundary_conditions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-boundary-boundary-conditions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[6],
        description=(
            "The boundary conditions for each boundary: * 0 - undefined * 1 - "
            "open * 2 - periodic * 3 - mirror * 4 - von Neumann * 5 - Dirichlet"
        ),
        a_nexus_field=NeXusField(
            name="boundary_conditions",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    boundaries = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-discretization-boundary-boundaries-field"
        ],
        shape=[6],
        description=(
            "Name of the boundaries. Left, right, front, back, bottom, top, The "
            "field must have as many entries as there are number_of_boundaries."
        ),
        a_nexus_field=NeXusField(
            name="boundaries",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDSummaryStatistics",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="summary_statistics",
            name_type="specified",
            optionality="required",
        ),
    )
    microstructureID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDMicrostructureID",
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


class MicrostructureScoreResultsSpatiotemporalIDSummaryStatistics(Process):
    """
    Summary quantities which are the result of some post-processing of the
    snapshot data (averaging, integrating, interpolating) happening for
    practical and performance reasons during the simulation. Place used for
    storing descriptors from continuum mechanics and thermodynamics at the
    scale of the entire ROI.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="summary_statistics",
            name_type="specified",
            optionality="required",
        ),
    )

    kinetics = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsKinetics",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="kinetics",
            name_type="specified",
            optionality="recommended",
        ),
    )
    stress = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsStress",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stress",
            name_type="specified",
            optionality="optional",
        ),
    )
    strain = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsStrain",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="strain",
            name_type="specified",
            optionality="optional",
        ),
    )
    deformation_gradient = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsDeformationGradient",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="deformation_gradient",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsKinetics(Data):
    """
    Evolution of the recrystallized volume fraction over time.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="kinetics",
            name_type="specified",
            optionality="recommended",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    iteration_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-iteration-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="iteration_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    temperature_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-temperature-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="temperature_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    x_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-x-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="x_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Evolution of the physical time not to be confused with wall-clock "
            "time or profiling data."
        ),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    iteration = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-iteration-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Iteration or increment counter."),
        a_nexus_field=NeXusField(
            name="iteration",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        shape=["*"],
        description=("Evolution of the simulated temperature over time."),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-kinetics-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Recrystallized volume fraction."),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsStress(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-stress-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stress",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["cauchy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-stress-type-field"
        ],
        description=("Which type of stress."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["cauchy"],
        ),
    )
    tensor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-stress-tensor-field"
        ],
        shape=["*", 3, 3],
        description=("Applied external stress tensor on the ROI."),
        a_nexus_field=NeXusField(
            name="tensor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsStrain(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-strain-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="strain",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-strain-type-field"
        ],
        description=("Which type of strain."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    tensor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-strain-tensor-field"
        ],
        shape=["*", 3, 3],
        description=("Applied external strain tensor on the ROI."),
        a_nexus_field=NeXusField(
            name="tensor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDSummaryStatisticsDeformationGradient(
    Process
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-deformation-gradient-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="deformation_gradient",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["piola"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-deformation-gradient-type-field"
        ],
        description=("Which type of deformation gradient."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["piola"],
        ),
    )
    tensor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-summary-statistics-deformation-gradient-tensor-field"
        ],
        shape=["*", 3, 3],
        description=("Applied deformation gradient tensor on the ROI."),
        a_nexus_field=NeXusField(
            name="tensor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDMicrostructureID(Microstructure):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="microstructureID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDMicrostructureIDGrid",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="recommended",
        ),
    )
    crystals = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDMicrostructureIDCrystals",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="crystals",
            name_type="specified",
            optionality="required",
        ),
    )
    recrystallization_front = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_results.MicrostructureScoreResultsSpatiotemporalIDMicrostructureIDRecrystallizationFront",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="recrystallization_front",
            name_type="specified",
            optionality="recommended",
        ),
    )

    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Simulated physical time for this snapshot."),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    iteration = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-iteration-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Iteration or increment counter of this snapshot."),
        a_nexus_field=NeXusField(
            name="iteration",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=("Simulated temperature for this snapshot."),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Current recrystallized volume fraction (taking fractional "
            "infections into account)."
        ),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    x_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-x-set-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Target value for which a snapshot was requested for the "
            "recrystallized volume fraction."
        ),
        a_nexus_field=NeXusField(
            name="x_set",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDMicrostructureIDGrid(CgGrid):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-grid-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="recommended",
        ),
    )

    indices_crystal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-grid-indices-crystal-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*", "*"],
        description=("Index for each crystal whereby its metadata can be retrieved."),
        a_nexus_field=NeXusField(
            name="indices_crystal",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    thread_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-grid-thread-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*", "*"],
        description=(
            "Identifier of the OpenMP thread that processed this part of the grid."
        ),
        a_nexus_field=NeXusField(
            name="thread_id",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDMicrostructureIDCrystals(
    MicrostructureFeature
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="crystals",
            name_type="specified",
            optionality="required",
        ),
    )

    representation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_crystals = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-number-of-crystals-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_crystals",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    number_of_phases = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-number-of-phases-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_phases",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    index_offset_crystal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-index-offset-crystal-field"
        ],
        a_nexus_field=NeXusField(
            name="index_offset_crystal",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    indices_crystal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-indices-crystal-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_crystal",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    index_offset_phase = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-index-offset-phase-field"
        ],
        a_nexus_field=NeXusField(
            name="index_offset_phase",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    indices_phase = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-indices-phase-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_phase",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        shape=["*"],
        description=(
            "Volume of each grain (partially transformed cells are accounted "
            "for). Values are reported in multiples of cells, needs "
            "multiplication with cell volume!"
        ),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLUME",
        ),
    )
    bunge_euler = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-bunge-euler-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 3],
        description=("Bunge-Euler angle triplets for each grain."),
        a_nexus_field=NeXusField(
            name="bunge_euler",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    dislocation_density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-dislocation-density-field"
        ],
        shape=["*"],
        description=(
            "Current value for the dislocation density as a measure of the "
            "remaining stored energy in assumed crystal defects inside each "
            "grain."
        ),
        a_nexus_field=NeXusField(
            name="dislocation_density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    is_deformed = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-is-deformed-field"
        ],
        shape=["*"],
        description=("Is the grain deformed."),
        a_nexus_field=NeXusField(
            name="is_deformed",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="recommended",
        ),
    )
    is_recrystallized = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-crystals-is-recrystallized-field"
        ],
        shape=["*"],
        description=("Is the grain recrystallized."),
        a_nexus_field=NeXusField(
            name="is_recrystallized",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreResultsSpatiotemporalIDMicrostructureIDRecrystallizationFront(
    MicrostructureFeature
):
    """
    Details about those cells which in this time step represent the discrete
    recrystallization front.

    Each CA is processed by a team of OpenMP threads.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="recrystallization_front",
            name_type="specified",
            optionality="recommended",
        ),
    )

    halo_region = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-halo-region-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Which cells are currently in a halo region of threads. The halo "
            "region is a layer of cells about the sub-domain of the simulation "
            "grid evolved by a thread."
        ),
        a_nexus_field=NeXusField(
            name="halo_region",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    mobility_weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-mobility-weight-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "So-called mobility weight which is a scaling factor to control the "
            "mobility of the grain boundary that is modelled sweeping cells that "
            "make the discrete recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="mobility_weight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    coordinate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-coordinate-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=(
            "The x, y, z grid coordinates of each cell in the recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="coordinate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    deformed_grain_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-deformed-grain-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Grain identifier assigned to each cell in the recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="deformed_grain_id",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    recrystallized_grain_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-recrystallized-grain-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Grain identifier assigned to each nucleus which affected that cell "
            "in the recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="recrystallized_grain_id",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    thread_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-thread-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Identifier of the OpenMP thread processing each cell in the "
            "recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="thread_id",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    infection_direction = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-infection-direction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Hint about the direction from which the cell was infected."),
        a_nexus_field=NeXusField(
            name="infection_direction",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    recrystallized_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_results.html#nxmicrostructure_score_results-entry-spatiotemporalid-microstructureid-recrystallization-front-recrystallized-fraction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("The fraction to which the cell is assumed transformed."),
        a_nexus_field=NeXusField(
            name="recrystallized_fraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
