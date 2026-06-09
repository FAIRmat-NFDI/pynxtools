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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_surfacer_results` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results import (
    ApmParaprobeToolResults,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process import (
    ApmParaprobeToolProcess,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeSurfacerResults"]


class ApmParaprobeSurfacerResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-surfacer tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_surfacer_results",
            category="application",
            symbols={
                "n_ions": "The total number of ions in the reconstruction.",
                "n_v_tri": "The number of vertices of the alpha complex.",
                "n_f_tri": "The number of faces of the alpha complex.",
                "n_f_tri_xdmf": "The total number of XDMF values to represent all faces of triangles via XDMF.",
                "n_f_tet_xdmf": "The total number of XDMF values to represent all faces of tetrahedra via XDMF.",
            },
        ),
    )

    point_set_wrappingID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_results.ApmParaprobeSurfacerResultsPoint_set_wrappingID",
        repeats=True,
        variable=True,
        description=(
            "Paraprobe-surfacer can be used to load a ROI that is the entire or "
            "a sub-set of the ion point cloud. In the point_cloud_wrapping "
            "process the tool computes a triangulated surface mesh which "
            "encloses the ROI/point cloud. This mesh can be seen as a model for "
            "the edge of the dataset. Different algorithms can be used with "
            "paraprobe-surfacer to create this mesh such as convex hulls, "
            "alpha-shapes as their generalization, or alpha wrappings. Ideally, "
            "the resulting mesh should be a watertight polyhedron. This "
            "polyhedron is not necessarily convex. For some algorithms there is "
            "no guarantee that the resulting mesh yields a watertight mesh."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_surfacer_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_surfacer_results"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_results.html#nxapm_paraprobe_tool_results-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
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


class ApmParaprobeSurfacerResultsPoint_set_wrappingID(ApmParaprobeToolProcess):
    """
    Paraprobe-surfacer can be used to load a ROI that is the entire or a
    sub-set of the ion point cloud. In the point_cloud_wrapping process the
    tool computes a triangulated surface mesh which encloses the ROI/point
    cloud. This mesh can be seen as a model for the edge of the dataset.

    Different algorithms can be used with paraprobe-surfacer to create this
    mesh such as convex hulls, alpha-shapes as their generalization, or alpha
    wrappings.

    Ideally, the resulting mesh should be a watertight polyhedron. This
    polyhedron is not necessarily convex. For some algorithms there is no
    guarantee that the resulting mesh yields a watertight mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_results.html#nxapm_paraprobe_surfacer_results-entry-point-set-wrappingid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="point_set_wrappingID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    alpha_complexID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_alpha_complex.CgAlphaComplex",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_alpha_complex",
            name="alpha_complexID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
