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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_tessellator_config` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfig,
    ApmParaprobeToolConfigTaskconfig,
)
from pynxtools.nomad.metainfo.base_classes.note import Note

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeTessellatorConfig"]


class ApmParaprobeTessellatorConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the
    paraprobe-tessellator tool.

    The tool paraprobe-tessellator computes a tessellation of the reconstructed
    positions.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tessellator_config",
            category="application",
        ),
    )

    tessellateID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_config.ApmParaprobeTessellatorConfigTessellateID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_tessellator_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_tessellator_config"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_tessellator_config",
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
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class ApmParaprobeTessellatorConfigTessellateID(ApmParaprobeToolConfigTaskconfig):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="tessellateID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    surface_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_tessellator_config.ApmParaprobeTessellatorConfigTessellateIDSurfaceDistance",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="optional",
        ),
    )

    method = Quantity(
        type=MEnum(["default"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-method-field"
        ],
        description=(
            "The method used to compute the tessellation. The value *default* "
            "configures the computation of the Voronoi tessellation."
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["default"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="default",
        ),
    )
    has_cell_volume = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-has-cell-volume-field"
        ],
        description=("Specifies if the tool should report the volume of each cell."),
        a_nexus_field=NeXusField(
            name="has_cell_volume",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_cell_neighbors = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-has-cell-neighbors-field"
        ],
        description=(
            "Specifies if the tool should report the first-order neighbors of "
            "each cell."
        ),
        a_nexus_field=NeXusField(
            name="has_cell_neighbors",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_cell_geometry = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-has-cell-geometry-field"
        ],
        description=(
            "Specifies if the tool should report the facets and vertices of each cell."
        ),
        a_nexus_field=NeXusField(
            name="has_cell_geometry",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_cell_edge_detection = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-has-cell-edge-detection-field"
        ],
        description=(
            "Specifies if the tool should report for each cell if it makes "
            "contact with the tight axis-aligned bounding box about the point "
            "cloud. This can be used to identify if the shape of the cell is "
            "likely affected by the edge of the dataset or if cells are deeply "
            "enough embedded into the point cloud so that the shape of their "
            "cells are not affected anymore by the boundary. This is valuable "
            "information to judge about the significance of finite size effects."
        ),
        a_nexus_field=NeXusField(
            name="has_cell_edge_detection",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeTessellatorConfigTessellateIDSurfaceDistance(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-surface-distance-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="optional",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-surface-distance-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-surface-distance-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-surface-distance-algorithm-field"
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
    distance = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tessellator_config.html#nxapm_paraprobe_tessellator_config-entry-tessellateid-surface-distance-distance-field"
        ],
        a_nexus_field=NeXusField(
            name="distance",
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
