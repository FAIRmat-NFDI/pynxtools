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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_score_config` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.cg_grid import CgGrid
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.microstructure import Microstructure
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructureScoreConfig"]


class MicrostructureScoreConfig(Entry):
    """
    Application definition to configure a simulation with the SCORE model.

    * `M. Kühbach et al. <https://doi.org/10.1016/j.actamat.2016.01.068>`_ *
    `M. Diehl et al. <https://doi.org/10.1088/1361-651X/ab51bd>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_score_config",
            category="application",
            symbols={
                "n_dg_ori": "Number of Bunge-Euler angle triplets for deformed grains.",
                "n_rx_ori": "Number of Bunge-Euler angle triplets for recrystallization nuclei.",
                "n_ori": "Number of texture components to analyze.",
                "n_drag": "Number of support points for the linearized drag profile.",
                "n_temp": "Number of support points for the desired time-temperature profile.",
                "n_defrag": "Number of entries when to defragment i.e. garbage collect the memory holding\n                state information for recrystallized cells.",
                "n_snapshot": "Number of entries when to collect snapshots of the evolving microstructure.",
                "n_su": "Number of solitary unit domains to export.",
                "d": "Dimensionality of the simulation.",
            },
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
    userID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="userID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigSample",
        repeats=False,
    )
    program1 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigProgram1",
        repeats=False,
        description=("Name of the program whereby this config file was created."),
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigEnvironment",
        repeats=False,
        description=(
            "Programs and libraries representing the computational environment"
        ),
    )
    material = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigMaterial",
        repeats=False,
        description=(
            "(Mechanical) properties of the material which scale the amount of "
            "stored (elastic) energy in the system and thus mainly affect "
            "recrystallization kinetics. Temperature-dependent lattice softening "
            "of the shear modulus :math:`G(T)` is modeled according to `Nadal "
            "and Le Poac <https://dx.doi.org/10.1063/1.1539913>`_ i.e., "
            ":math:`G(T) = \\frac{1}{\\mathfrak{J}(\\frac{T}{T_m})} G_0 (1 - a "
            "\\frac{T}{T_m})` with :math:`G_0` shear_modulus_zero, :math:`a` "
            "nadal_lepoac_a, :math:`\\zeta` nadal_lepoac_zeta, and "
            ":math:`\\mathfrak{J}(\\frac{T}{T_m}) = 1 + "
            "exp(\\frac{\\frac{T}{T_m} - 1}{\\zeta(1 - "
            "\\frac{T}{T_m(1+\\zeta)})})`. The temperature-dependent Burgers "
            "vector :math:`b(T)` is modeled with a second order approximation "
            ":math:`b(T) = b_0 (1 + (a_2 T^2 + a_1 T + a_0))` with :math:`a_2` "
            "lattice_expansion_second, :math:`a_1` lattice_expansion_first, and "
            ":math:`a_0` lattice_expansion_null."
        ),
    )
    deformation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDeformation",
        repeats=False,
        description=(
            "Details about the geometry and properties of the polycrystal that "
            "represents the starting configuration (typically a deformed "
            "microstructure) for the simulation."
        ),
    )
    nucleation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigNucleation",
        repeats=False,
        description=(
            "Phenomenological model according to which recrystallization nuclei "
            "are placed into the domain. Studying the growth of these nuclei is "
            "the main purpose of a SCORE simulation."
        ),
    )
    grain_boundary_mobility = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigGrainBoundaryMobility",
        repeats=False,
        description=(
            "Model for the assumed mobility of grain boundaries with different "
            "disorientation implemented as a parameterized Turnbull's model for "
            "thermally-activated grain boundary migration."
        ),
    )
    stored_energy_recovery = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigStoredEnergyRecovery",
        repeats=False,
        description=(
            "Time-dependent reduction of the stored energy to account for "
            "recovery effects."
        ),
    )
    dispersoid_drag = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDispersoidDrag",
        repeats=False,
        description=(
            "Reduction of the grain boundary migration speed due to the presence "
            "of dispersoids through which the total grain boundary area of the "
            "recrystallization front can be reduced while the boundary is "
            "arrested at the dispersoids."
        ),
    )
    component_analysis = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigComponentAnalysis",
        repeats=False,
    )
    time_temperature = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigTimeTemperature",
        repeats=False,
        description=("Desired simulated time-temperature profile"),
    )
    discretization = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDiscretization",
        repeats=False,
        description=(
            "Relevant data to instantiate a starting configuration that is "
            "typically a microstructure in deformed conditions where (elastic) "
            "energy is stored in the form of crystal defects (mostly "
            "dislocations). The SCORE model does not resolve individual "
            "dislocations but works with one homogenized mean-field density per "
            "grain. For simulations that are instantiated from EBSD datasets or "
            "crystal plasticity simulations individual values are available for "
            "each voxel that may be used as is for each voxel or may need a "
            "pre-processing of the data to coarse-grain material point-specific "
            "values to values averaged per deformed grain."
        ),
    )
    numerics = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigNumerics",
        repeats=False,
        description=(
            "Criteria which enable to stop the simulation in a controlled manner "
            "and assure a stable numerical integration. Whichever criterion is "
            "fulfilled first stops the simulation."
        ),
    )
    solitary_unit = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigSolitaryUnit",
        repeats=False,
    )

    definition = Quantity(
        type=MEnum(["NXmicrostructure_score_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmicrostructure_score_config"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXmicrostructure_score_config",
        ),
    )
    identifier_simulation = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-identifier-simulation-field"
        ],
        description=("An alias to refer to this simulation."),
        a_nexus_field=NeXusField(
            name="identifier_simulation",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-description-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the configuration file was created."
        ),
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


class MicrostructureScoreConfigSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="recommended",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-sample-dimensionality-field"
        ],
        description=("Dimensionality of the simulation."),
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["1", "2", "3"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    is_simulation = Quantity(
        type=MEnum(["experiment", "simulation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-sample-is-simulation-field"
        ],
        description=("A qualifier whether the sample is a real one or a virtual one."),
        a_nexus_field=NeXusField(
            name="is_simulation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["experiment", "simulation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-sample-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the specimen. If the specimen substance has multiple "
            "components, all elements from each component must be included in "
            "`atom_types`. The purpose of the field is to offer research data "
            "management systems an opportunity to parse the relevant elements "
            "without having to interpret these from other sources."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigProgram1(Program):
    """
    Name of the program whereby this config file was created.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-program1-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="program1",
            name_type="specified",
            optionality="recommended",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-program1-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-program1-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigEnvironment(Collection):
    """
    Programs and libraries representing the computational environment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigEnvironmentProgramID",
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


class MicrostructureScoreConfigEnvironmentProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-environment-programid-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-environment-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-environment-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigMaterial(Parameters):
    """
    (Mechanical) properties of the material which scale the amount of stored
    (elastic) energy in the system and thus mainly affect recrystallization
    kinetics.

    Temperature-dependent lattice softening of the shear modulus :math:`G(T)`
    is modeled according to `Nadal and Le Poac
    <https://dx.doi.org/10.1063/1.1539913>`_ i.e., :math:`G(T) =
    \frac{1}{\\mathfrak{J}(\frac{T}{T_m})} G_0 (1 - a \frac{T}{T_m})` with
    :math:`G_0` shear_modulus_zero, :math:`a` nadal_lepoac_a, :math:`\\zeta`
    nadal_lepoac_zeta, and :math:`\\mathfrak{J}(\frac{T}{T_m}) = 1 +
    exp(\frac{\frac{T}{T_m} - 1}{\\zeta(1 - \frac{T}{T_m(1+\\zeta)})})`.

    The temperature-dependent Burgers vector :math:`b(T)` is modeled with a
    second order approximation :math:`b(T) = b_0 (1 + (a_2 T^2 + a_1 T + a_0))`
    with :math:`a_2` lattice_expansion_second, :math:`a_1`
    lattice_expansion_first, and :math:`a_0` lattice_expansion_null.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="material",
            name_type="specified",
            optionality="required",
        ),
    )

    melting_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-melting-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=("Empirical melting temperature measured at standard conditions."),
        a_nexus_field=NeXusField(
            name="melting_temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )
    shear_modulus_zero = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-shear-modulus-zero-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        description=("Shear modulus at zero Kelvin."),
        a_nexus_field=NeXusField(
            name="shear_modulus_zero",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_PRESSURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "pascal"},
    )
    nadal_lepoac_a = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-nadal-lepoac-a-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Constant :math:`a` in the Nadal-Le Poac-based model of the "
            "temperature-dependent shear modulus."
        ),
        a_nexus_field=NeXusField(
            name="nadal_lepoac_a",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    nadal_lepoac_zeta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-nadal-lepoac-zeta-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Constant :math:`\\zeta` in the Nadal-Le Poac-based model of the "
            "temperature- dependent shear modulus."
        ),
        a_nexus_field=NeXusField(
            name="nadal_lepoac_zeta",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    burgers_vector_zero = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-burgers-vector-zero-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Magnitude of the Burgers vector at zero Kelvin."),
        a_nexus_field=NeXusField(
            name="burgers_vector_zero",
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
    lattice_expansion_second = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-lattice-expansion-second-field"
        ],
        flexible_unit=True,
        description=(
            "Constant :math:`a_2` in the second-order model that is used for "
            "quantifying the temperature-dependent Burgers vector."
        ),
        a_nexus_field=NeXusField(
            name="lattice_expansion_second",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    lattice_expansion_first = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-lattice-expansion-first-field"
        ],
        flexible_unit=True,
        description=(
            "Constant :math:`a_1` in the second-order model that is used for "
            "quantifying the temperature-dependent Burgers vector."
        ),
        a_nexus_field=NeXusField(
            name="lattice_expansion_first",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    lattice_expansion_null = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-material-lattice-expansion-null-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Constant :math:`a_0` in the second-order model that is used for "
            "quantifying the temperature-dependent Burgers vector."
        ),
        a_nexus_field=NeXusField(
            name="lattice_expansion_null",
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


class MicrostructureScoreConfigDeformation(Parameters):
    """
    Details about the geometry and properties of the polycrystal that
    represents the starting configuration (typically a deformed microstructure)
    for the simulation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="deformation",
            name_type="specified",
            optionality="required",
        ),
    )

    ensemble = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDeformationEnsemble",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="ensemble",
            name_type="specified",
            optionality="optional",
        ),
    )
    ebsd = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDeformationEbsd",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="ebsd",
            name_type="specified",
            optionality="optional",
        ),
    )
    damask = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDeformationDamask",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="damask",
            name_type="specified",
            optionality="optional",
        ),
    )

    model = Quantity(
        type=MEnum(["cuboidal", "poisson_voronoi", "ebsd", "damask"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-model-field"
        ],
        description=(
            "Which model should be used to generate a starting microstructure. * "
            "cuboidal, a regular array of equally-shaped cuboidal grains * "
            "poisson_voronoi, a discretized Poisson Voronoi tessellation * ebsd, "
            "a microstructure synthesized based on a simulated or a measured "
            "EBSD orientation map * damask, the result of a simulation from "
            "`DAMASK <https://damask-multiphysics.org>`_."
        ),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["cuboidal", "poisson_voronoi", "ebsd", "damask"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    extent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-extent-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Extent of each deformed grain in voxel along the x, y, and z "
            "direction when model is cuboidal."
        ),
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Average spherical diameter when model is poisson_voronoi."),
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigDeformationEnsemble(Parameters):
    """
    Settings for instantiating properties of deformed grains when model is
    cuboidal or poisson.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ensemble-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="ensemble",
            name_type="specified",
            optionality="optional",
        ),
    )

    bunge_euler = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ensemble-bunge-euler-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 3],
        description=(
            "Set of Bunge-Euler orientations (:math:`\\varphi_1`, :math:`\\Phi`, "
            ":math:`\\varphi_2` ) out of which the orientations of deformed "
            "grains are sampled."
        ),
        a_nexus_field=NeXusField(
            name="bunge_euler",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    stored_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ensemble-stored-energy-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Set of stored elastic energy quantified as a dislocation density "
            "which is assigned to deformed grains with orientations from "
            "bunge_euler with index queries matching for the bunge_euler and "
            "stored_energy fields."
        ),
        a_nexus_field=NeXusField(
            name="stored_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigDeformationEbsd(Note):
    """
    Settings for instantiating properties of deformed grains from an EBSD
    orientation map when model is cuboidal or poisson.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ebsd-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="ebsd",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ebsd-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ebsd-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ebsd-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    stepsize = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-ebsd-stepsize-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Extent of the pixel of the EBSD orientation mapping assuming "
            "square-shaped pixels or cube-shaped voxels respectively."
        ),
        a_nexus_field=NeXusField(
            name="stepsize",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigDeformationDamask(Note):
    """
    Settings for instantiating properties of deformed grains and nuclei when
    model is damask.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-damask-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="damask",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-damask-file-name-field"
        ],
        description=(
            "Name of the DREAM.3D HDF5 file that was instantiated from the a "
            "previously performed DAMASK simulation."
        ),
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-damask-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-deformation-damask-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigNucleation(Parameters):
    """
    Phenomenological model according to which recrystallization nuclei are
    placed into the domain. Studying the growth of these nuclei is the main
    purpose of a SCORE simulation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-nucleation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="nucleation",
            name_type="specified",
            optionality="required",
        ),
    )

    ensemble = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigNucleationEnsemble",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="ensemble",
            name_type="specified",
            optionality="required",
        ),
    )

    spatial_distribution = Quantity(
        type=MEnum(["csr", "damask"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-nucleation-spatial-distribution-field"
        ],
        description=(
            "According to which model will the nuclei become distributed "
            "spatially: * csr, complete spatial randomness * custom, "
            "implementation-specific * gb, nuclei placed at grain boundaries"
        ),
        a_nexus_field=NeXusField(
            name="spatial_distribution",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["csr", "damask"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    incubation_time = Quantity(
        type=MEnum(["site_saturation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-nucleation-incubation-time-field"
        ],
        description=(
            "According to which model will the nuclei start to grow: * "
            "site_saturation, instantaneously"
        ),
        a_nexus_field=NeXusField(
            name="incubation_time",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["site_saturation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="site_saturation",
        ),
    )
    orientation = Quantity(
        type=MEnum(["ensemble", "random", "damask"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-nucleation-orientation-field"
        ],
        description=(
            "According to which model will the nuclei get their orientation "
            "assigned: * ensemble, picking randomly one from "
            "ensemble/bunge_euler * random, picking randomly on the SO3 * "
            "damask, picking based on information provided in deformation/damask"
        ),
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["ensemble", "random", "damask"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigNucleationEnsemble(Parameters):
    """
    Settings for instantiating properties of nuclei for recrystallizing grains.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-nucleation-ensemble-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="ensemble",
            name_type="specified",
            optionality="required",
        ),
    )

    bunge_euler = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-nucleation-ensemble-bunge-euler-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 3],
        description=(
            "Set of Bunge-Euler orientations (:math:`\\varphi_1`, :math:`\\Phi`, "
            ":math:`\\varphi_2` ) out of which the orientations of "
            "nuclei/recrystallized grains are sampled."
        ),
        a_nexus_field=NeXusField(
            name="bunge_euler",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    incubation_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-nucleation-ensemble-incubation-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Incubation time which is assigned to deformed grains with "
            "orientations from bunge_euler with index queries matching for the "
            "bunge_euler and stored_energy fields."
        ),
        a_nexus_field=NeXusField(
            name="incubation_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigGrainBoundaryMobility(Parameters):
    """
    Model for the assumed mobility of grain boundaries with different
    disorientation implemented as a parameterized Turnbull's model for
    thermally-activated grain boundary migration.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="grain_boundary_mobility",
            name_type="specified",
            optionality="required",
        ),
    )

    sebald_gottstein = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigGrainBoundaryMobilitySebaldGottstein",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="sebald_gottstein",
            name_type="specified",
            optionality="optional",
        ),
    )
    rollett_holm = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigGrainBoundaryMobilityRollettHolm",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="rollett_holm",
            name_type="specified",
            optionality="required",
        ),
    )

    model = Quantity(
        type=MEnum(["sebald_gottstein", "rollett_holm"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-model-field"
        ],
        description=(
            "Which type of fundamental model for the grain boundary mobility. "
            "Grain boundaries with disorientation angle smaller than 15 degree "
            "are considered as low-angle grain boundaries. Other grain "
            "boundaries are high-angle boundaries."
        ),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["sebald_gottstein", "rollett_holm"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigGrainBoundaryMobilitySebaldGottstein(Parameters):
    """
    Parameter of the Sebald-Gottstein migration model.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-sebald-gottstein-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="sebald_gottstein",
            name_type="specified",
            optionality="optional",
        ),
    )

    lagb_pre_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-sebald-gottstein-lagb-pre-factor-field"
        ],
        flexible_unit=True,
        description=("Pre-exponential factor for low-angle grain boundaries."),
        a_nexus_field=NeXusField(
            name="lagb_pre_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    lagb_enthalpy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-sebald-gottstein-lagb-enthalpy-field"
        ],
        flexible_unit=True,
        description=("Migration activation enthalpy for low-angle grain boundaries."),
        a_nexus_field=NeXusField(
            name="lagb_enthalpy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    hagb_pre_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-sebald-gottstein-hagb-pre-factor-field"
        ],
        flexible_unit=True,
        description=("Pre-exponential factor for high-angle grain boundaries."),
        a_nexus_field=NeXusField(
            name="hagb_pre_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    hagb_enthalpy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-sebald-gottstein-hagb-enthalpy-field"
        ],
        flexible_unit=True,
        description=("Migration activation enthalpy for high-angle grain boundaries."),
        a_nexus_field=NeXusField(
            name="hagb_enthalpy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    special_pre_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-sebald-gottstein-special-pre-factor-field"
        ],
        flexible_unit=True,
        description=(
            "Pre-exponential factor for high-angle grain boundaries which in "
            "bicrystal or other tailored experiments showed a particular high "
            "mobility."
        ),
        a_nexus_field=NeXusField(
            name="special_pre_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    special_enthalpy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-sebald-gottstein-special-enthalpy-field"
        ],
        flexible_unit=True,
        description=(
            "Migration activation enthalpy for high-angle grain boundaries which "
            "in bicrystal or other tailored experiments showed a particular high "
            "mobility."
        ),
        a_nexus_field=NeXusField(
            name="special_enthalpy",
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


class MicrostructureScoreConfigGrainBoundaryMobilityRollettHolm(Parameters):
    """
    Parameter of the Rollett-Holm migration model.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-rollett-holm-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="rollett_holm",
            name_type="specified",
            optionality="required",
        ),
    )

    m_null = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-rollett-holm-m-null-field"
        ],
        flexible_unit=True,
        description=(
            "Pre-exponential factor for the fastest grain boundary in the system."
        ),
        a_nexus_field=NeXusField(
            name="m_null",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    enthalpy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-rollett-holm-enthalpy-field"
        ],
        flexible_unit=True,
        description=(
            "Migration activation enthalpy for the fastest grain boundary in the "
            "system."
        ),
        a_nexus_field=NeXusField(
            name="enthalpy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    c1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-rollett-holm-c1-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Mobility scaling factor :math:`c_1`. Typically 0.99 or higher but not 1."
        ),
        a_nexus_field=NeXusField(
            name="c1",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    c2 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-rollett-holm-c2-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Mobility scaling factor :math:`c_2`. Typically 5."),
        a_nexus_field=NeXusField(
            name="c2",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    c3 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-grain-boundary-mobility-rollett-holm-c3-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Mobility scaling factor :math:`c_3`. Typically 9."),
        a_nexus_field=NeXusField(
            name="c3",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigStoredEnergyRecovery(Parameters):
    """
    Time-dependent reduction of the stored energy to account for recovery
    effects.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-stored-energy-recovery-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="stored_energy_recovery",
            name_type="specified",
            optionality="required",
        ),
    )

    model = Quantity(
        type=MEnum(["none"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-stored-energy-recovery-model-field"
        ],
        description=("Which type of recovery model."),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["none"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="none",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigDispersoidDrag(Parameters):
    """
    Reduction of the grain boundary migration speed due to the presence of
    dispersoids through which the total grain boundary area of the
    recrystallization front can be reduced while the boundary is arrested at
    the dispersoids.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="dispersoid_drag",
            name_type="specified",
            optionality="required",
        ),
    )

    zener_smith = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDispersoidDragZenerSmith",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="zener_smith",
            name_type="specified",
            optionality="optional",
        ),
    )

    model = Quantity(
        type=MEnum(["none", "zener_smith"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-model-field"
        ],
        description=("Which type of drag model."),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["none", "zener_smith"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigDispersoidDragZenerSmith(Parameters):
    """
    Parameter of the Zener-Smith drag model when model is zener_smith.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="zener_smith",
            name_type="specified",
            optionality="optional",
        ),
    )

    radius_evolution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDispersoidDragZenerSmithRadiusEvolution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="radius_evolution",
            name_type="specified",
            optionality="required",
        ),
    )

    pre_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-pre-factor-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Configuration-dependent constant which factorizes the drag pressure."
        ),
        a_nexus_field=NeXusField(
            name="pre_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    surface_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-surface-energy-field"
        ],
        flexible_unit=True,
        description=(
            "Average surface energy of the grain-boundary-dispersoid-surface "
            "configuration which factorizes the drag pressure."
        ),
        a_nexus_field=NeXusField(
            name="surface_energy",
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


class MicrostructureScoreConfigDispersoidDragZenerSmithRadiusEvolution(Data):
    """
    Assumed dispersoid mean radius-time profile
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="radius_evolution",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    radius_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-radius-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="radius_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-title-field"
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
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Support point of the linearized curve of simulated time matching a "
            "specific support point of the average dispersoid radius."
        ),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="time",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Support point of the linearized curve of the average dispersoid radius."
        ),
        a_nexus_field=NeXusField(
            name="radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    radius__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-dispersoid-drag-zener-smith-radius-evolution-radius-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="radius",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigComponentAnalysis(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-component-analysis-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="component_analysis",
            name_type="specified",
            optionality="required",
        ),
    )

    names = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-component-analysis-names-field"
        ],
        shape=["*"],
        description=("Given name(s) of a texture component."),
        a_nexus_field=NeXusField(
            name="names",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    bunge_euler = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-component-analysis-bunge-euler-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 3],
        description=(
            "Bunge-Euler angle representation :math:`\\varphi_1`, :math:`\\Phi`, "
            ":math:`\\varphi_2` of the texture components in sequence of the "
            "names field."
        ),
        a_nexus_field=NeXusField(
            name="bunge_euler",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    theta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-component-analysis-theta-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Integration radius that constraints the theta angular region of the "
            "orientation space (SO3) about each central location (obeying "
            "symmetries) as specified by bunge_euler indexed in the same "
            "sequence as the bunge_euler and names fields."
        ),
        a_nexus_field=NeXusField(
            name="theta",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigTimeTemperature(Data):
    """
    Desired simulated time-temperature profile
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="time_temperature",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    temperature_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-temperature-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="temperature_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-title-field"
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
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "Support point of the linearized curve of simulated time matching a "
            "specific support point of the temperature."
        ),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="time",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        shape=["*"],
        description=("Support point of the linearized curve of the temperature."),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )
    temperature__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-time-temperature-temperature-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="temperature",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigDiscretization(Microstructure):
    """
    Relevant data to instantiate a starting configuration that is typically a
    microstructure in deformed conditions where (elastic) energy is stored in
    the form of crystal defects (mostly dislocations). The SCORE model does not
    resolve individual dislocations but works with one homogenized mean-field
    density per grain. For simulations that are instantiated from EBSD datasets
    or crystal plasticity simulations individual values are available for each
    voxel that may be used as is for each voxel or may need a pre-processing of
    the data to coarse-grain material point-specific values to values averaged
    per deformed grain.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-discretization-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="discretization",
            name_type="specified",
            optionality="required",
        ),
    )

    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigDiscretizationGrid",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigDiscretizationGrid(CgGrid):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-discretization-grid-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="required",
        ),
    )

    extent = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-discretization-grid-extent-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[3],
        description=(
            "Extend of each CA domain in voxel along the x, y, and z direction. "
            "Deformation of sheet material is assumed. The x axis is assumed "
            "pointing along the rolling direction. The y axis is assumed "
            "pointing along the transverse direction. The z axis is assumed "
            "pointing along the normal direction."
        ),
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    cell_dimensions = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-discretization-grid-cell-dimensions-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Edge length of the material point that in SCORE is discretized via "
            "equisized cubic voxels."
        ),
        a_nexus_field=NeXusField(
            name="cell_dimensions",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigNumerics(Parameters):
    """
    Criteria which enable to stop the simulation in a controlled manner and
    assure a stable numerical integration. Whichever criterion is fulfilled
    first stops the simulation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="numerics",
            name_type="specified",
            optionality="required",
        ),
    )

    cell_cache = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_score_config.MicrostructureScoreConfigNumericsCellCache",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="cell_cache",
            name_type="specified",
            optionality="required",
        ),
    )

    max_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-max-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Maximum recrystallized volume fraction."),
        a_nexus_field=NeXusField(
            name="max_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    max_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-max-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Maximum simulated physical time."),
        a_nexus_field=NeXusField(
            name="max_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    max_iteration = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-max-iteration-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Maximum number of iteration steps."),
        a_nexus_field=NeXusField(
            name="max_iteration",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    max_delta_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-max-delta-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Maximum fraction equivalent to the migration of the fastest grain "
            "boundary in the system how much a cell may be consumed in a single "
            "iteration."
        ),
        a_nexus_field=NeXusField(
            name="max_delta_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    x_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-x-set-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "List of target values at which recrystallized volume fractions the "
            "state of the CA is evaluated and stored. The code documents summary "
            "statistics like recrystallized volume fraction for each iteration "
            "and the volume of each grain. Furthermore, snapshots of the "
            "microstructure are stored. These can take much disk space though "
            "because SCORE is able to evolve CA with up to :math:`1600^3` cells. "
            "Snapshot data document the current microstructure including the "
            "assignment of grains and cells surplus the state of the "
            "recrystallization front. Despite these, data about the cells that "
            "define the recrystallization front make up for approximately one "
            "order of magnitude less cells than present in the domain. For the "
            "cells in this front, though, more data have to be collected than "
            "just a grain identifier."
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


class MicrostructureScoreConfigNumericsCellCache(Parameters):
    """
    Parameter which control the memory management of cells in the
    recrystallization front.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-cell-cache-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="cell_cache",
            name_type="specified",
            optionality="required",
        ),
    )

    initial = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-cell-cache-initial-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Fraction of the total number of cells in the CA which should "
            "initially be allocated for offering storage for cells making up the "
            "recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="initial",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    realloc = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-cell-cache-realloc-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "By how much more times should the already allocated memory be "
            "increased to offer space for storing states of cells in the "
            "recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="realloc",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    defragment = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-cell-cache-defragment-field"
        ],
        description=(
            "Should the cache for cells in the recrystallization front be "
            "defragmented on-the-fly or not."
        ),
        a_nexus_field=NeXusField(
            name="defragment",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    defragment_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-numerics-cell-cache-defragment-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Target values at which recrystallized volume fraction the cache for "
            "cells in the recrystallization front will be defragmented "
            "on-the-fly. Defragmentation packs active cells closer into main "
            "memory to reduce cache misses in subsequent evaluations of the "
            "recrystallization front."
        ),
        a_nexus_field=NeXusField(
            name="defragment_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureScoreConfigSolitaryUnit(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-solitary-unit-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="solitary_unit",
            name_type="specified",
            optionality="required",
        ),
    )

    apply = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-solitary-unit-apply-field"
        ],
        description=(
            "Perform a statistical analyses of the results as it was proposed by "
            "M. Kühbach (solitary unit model ensemble approach)."
        ),
        a_nexus_field=NeXusField(
            name="apply",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    number_of_domains = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-solitary-unit-number-of-domains-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "How many independent cellular automaton domains should be instantiated."
        ),
        a_nexus_field=NeXusField(
            name="number_of_domains",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    rediscretization = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_score_config.html#nxmicrostructure_score_config-entry-solitary-unit-rediscretization-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Into how many time steps should the real time interval be "
            "discretized upon during post-processing the results with the "
            "solitary unit modeling approach."
        ),
        a_nexus_field=NeXusField(
            name="rediscretization",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
