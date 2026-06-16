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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_tool_config` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_common import (
    ApmParaprobeToolCommon,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_parameters import (
    ApmParaprobeToolParameters,
)
from pynxtools.nomad.metainfo.base_classes.cg_cylinder import CgCylinder
from pynxtools.nomad.metainfo.base_classes.cg_ellipsoid import CgEllipsoid
from pynxtools.nomad.metainfo.base_classes.cg_face_list_data_structure import (
    CgFaceListDataStructure,
)
from pynxtools.nomad.metainfo.base_classes.cg_hexahedron import CgHexahedron
from pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask import (
    CsFilterBooleanMask,
)
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.match_filter import MatchFilter
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.spatial_filter import SpatialFilter
from pynxtools.nomad.metainfo.base_classes.subsampling_filter import SubsamplingFilter

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeToolConfig"]


class ApmParaprobeToolConfig(Entry):
    """
    Application definition for a (configuration) file of a tool from the
    paraprobe-toolbox.

    The paraprobe-toolbox is a collection of open-source tools for performing
    efficient analyses of point cloud data where each point can represent atoms
    or (molecular) ions. A key application of the toolbox has been for research
    in the field of Atom Probe Tomography (APT) and related Field Ion
    Microscopy (FIM):

    * `paraprobe-toolbox <https://www.gitlab.com/paraprobe/paraprobe-toolbox>`_
    * `M. Kühbach et al. <https://paraprobe-toolbox.readthedocs.io/en/main/>`_

    The toolbox does not replace but complements existent software tools in
    this research field. Given its capabilities of handling points as objects
    with properties and enabling analyses of the spatial arrangement of and
    inter- sections between geometric primitives, the software can equally be
    used for analyzing data in Materials Science and Materials Engineering.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tool_config",
            category="application",
        ),
    )

    apm_paraprobe_tool_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParameters",
        repeats=True,
        variable=True,
        description=("A specific configuration to achieve a processing result"),
    )
    common = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigCommon",
        repeats=False,
    )

    definition = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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


class ApmParaprobeToolConfigApmParaprobeToolParameters(ApmParaprobeToolParameters):
    """
    A specific configuration to achieve a processing result
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    reconstruction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersReconstruction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="reconstruction",
            name_type="specified",
            optionality="required",
        ),
    )
    ranging = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersRanging",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="ranging",
            name_type="specified",
            optionality="required",
        ),
    )
    spatial_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspatial_filter",
            name="spatial_filter",
            name_type="specified",
            optionality="required",
        ),
    )
    evaporation_id_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersEvaporationIdFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsubsampling_filter",
            name="evaporation_id_filter",
            name_type="specified",
            optionality="optional",
        ),
    )
    iontype_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersIontypeFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="iontype_filter",
            name_type="specified",
            optionality="optional",
        ),
    )
    hit_multiplicity_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersHitMultiplicityFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="hit_multiplicity_filter",
            name_type="specified",
            optionality="optional",
        ),
    )

    identifier_analysis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-identifier-analysis-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigApmParaprobeToolParametersReconstruction(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-reconstruction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="reconstruction",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-reconstruction-file-name-field"
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
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-reconstruction-checksum-field"
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
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-reconstruction-algorithm-field"
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
    position = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-reconstruction-position-field"
        ],
        a_nexus_field=NeXusField(
            name="position",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    mass_to_charge = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-reconstruction-mass-to-charge-field"
        ],
        a_nexus_field=NeXusField(
            name="mass_to_charge",
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


class ApmParaprobeToolConfigApmParaprobeToolParametersRanging(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-ranging-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="ranging",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-ranging-file-name-field"
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
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-ranging-checksum-field"
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
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-ranging-algorithm-field"
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
    ranging_definitions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-ranging-ranging-definitions-field"
        ],
        a_nexus_field=NeXusField(
            name="ranging_definitions",
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


class ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilter(SpatialFilter):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspatial_filter",
            name="spatial_filter",
            name_type="specified",
            optionality="required",
        ),
    )

    hexahedron_set = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterHexahedronSet",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="hexahedron_set",
            name_type="specified",
            optionality="optional",
        ),
    )
    cylinder_set = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterCylinderSet",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_cylinder",
            name="cylinder_set",
            name_type="specified",
            optionality="optional",
        ),
    )
    ellipsoid_set = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterEllipsoidSet",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_ellipsoid",
            name="ellipsoid_set",
            name_type="specified",
            optionality="optional",
        ),
    )
    polyhedron_set = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyhedron.CgPolyhedron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="polyhedron_set",
            name_type="specified",
            optionality="optional",
        ),
    )
    bitmask = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterBitmask",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="bitmask",
            name_type="specified",
            optionality="optional",
        ),
    )

    windowing_method = Quantity(
        type=MEnum(["entire_dataset", "union_of_primitives", "bitmask"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-windowing-method-field"
        ],
        a_nexus_field=NeXusField(
            name="windowing_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["entire_dataset", "union_of_primitives", "bitmask"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterHexahedronSet(
    CgHexahedron
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-hexahedron-set-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_hexahedron",
            name="hexahedron_set",
            name_type="specified",
            optionality="optional",
        ),
    )

    hexahedra = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterHexahedronSetHexahedra",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedra",
            name_type="specified",
            optionality="required",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-hexahedron-set-dimensionality-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-hexahedron-set-cardinality-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-hexahedron-set-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
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


class ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterHexahedronSetHexahedra(
    CgFaceListDataStructure
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-hexahedron-set-hexahedra-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_face_list_data_structure",
            name="hexahedra",
            name_type="specified",
            optionality="required",
        ),
    )

    vertices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-hexahedron-set-hexahedra-vertices-field"
        ],
        a_nexus_field=NeXusField(
            name="vertices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterCylinderSet(
    CgCylinder
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-cylinder-set-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_cylinder",
            name="cylinder_set",
            name_type="specified",
            optionality="optional",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-cylinder-set-dimensionality-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-cylinder-set-cardinality-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-cylinder-set-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-cylinder-set-center-field"
        ],
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-cylinder-set-height-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="height",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-cylinder-set-radii-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterEllipsoidSet(
    CgEllipsoid
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-ellipsoid-set-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_ellipsoid",
            name="ellipsoid_set",
            name_type="specified",
            optionality="optional",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-ellipsoid-set-dimensionality-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    cardinality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-ellipsoid-set-cardinality-field"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-ellipsoid-set-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-ellipsoid-set-center-field"
        ],
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    half_axes_radii = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-ellipsoid-set-half-axes-radii-field"
        ],
        a_nexus_field=NeXusField(
            name="half_axes_radii",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    orientation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-ellipsoid-set-orientation-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="orientation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigApmParaprobeToolParametersSpatialFilterBitmask(
    CsFilterBooleanMask
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-bitmask-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="bitmask",
            name_type="specified",
            optionality="optional",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-bitmask-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_objects",
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
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-bitmask-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
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
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-spatial-filter-bitmask-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
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


class ApmParaprobeToolConfigApmParaprobeToolParametersEvaporationIdFilter(
    SubsamplingFilter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-evaporation-id-filter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsubsampling_filter",
            name="evaporation_id_filter",
            name_type="specified",
            optionality="optional",
        ),
    )

    min = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-evaporation-id-filter-min-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="min",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    increment = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-evaporation-id-filter-increment-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="increment",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    max = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-evaporation-id-filter-max-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="max",
            type="NX_INT",
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


class ApmParaprobeToolConfigApmParaprobeToolParametersIontypeFilter(MatchFilter):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-iontype-filter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="iontype_filter",
            name_type="specified",
            optionality="optional",
        ),
    )

    method = Quantity(
        type=MEnum(["whitelist", "blacklist"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-iontype-filter-method-field"
        ],
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["whitelist", "blacklist"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    match = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-iontype-filter-match-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="match",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigApmParaprobeToolParametersHitMultiplicityFilter(
    MatchFilter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-hit-multiplicity-filter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="hit_multiplicity_filter",
            name_type="specified",
            optionality="optional",
        ),
    )

    method = Quantity(
        type=MEnum(["whitelist", "blacklist"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-hit-multiplicity-filter-method-field"
        ],
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["whitelist", "blacklist"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    match = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-taskconfig-hit-multiplicity-filter-match-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="match",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigCommon(ApmParaprobeToolCommon):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_common",
            name="common",
            name_type="specified",
            optionality="required",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigCommonProgramID",
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
    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config.ApmParaprobeToolConfigCommonProfiling",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="recommended",
        ),
    )

    status = Quantity(
        type=MEnum(["success", "failure"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-status-field"
        ],
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["success", "failure"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolConfigCommonProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-programid-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-programid-program-version-attribute"
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


class ApmParaprobeToolConfigCommonProfiling(CsProfiling):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-profiling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="recommended",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-profiling-start-time-field"
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
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-profiling-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    total_elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_config.html#nxapm_paraprobe_tool_config-entry-common-profiling-total-elapsed-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        a_nexus_field=NeXusField(
            name="total_elapsed_time",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
