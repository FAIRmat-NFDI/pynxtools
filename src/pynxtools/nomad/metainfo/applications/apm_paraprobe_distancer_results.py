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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_distancer_results` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_results import (
    ApmParaprobeToolResults,
)
from pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_process import (
    ApmParaprobeToolProcess,
)
from pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask import (
    CsFilterBooleanMask,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeDistancerResults"]


class ApmParaprobeDistancerResults(ApmParaprobeToolResults):
    """
    Application definition for a results file of the paraprobe-distancer tool.

    The tool paraprobe-distancer tool evaluates exactly the shortest Euclidean
    distance for each member of a set of points against a set of triangles.

    Triangles can represent for instance the facets of a triangulated surface
    mesh like those returned by paraprobe-surfacer or any other set of
    triangles. Triangles do not have to be connected.

    Currently, paraprobe-distancer does not check if the respectively specified
    triangle sets are consistent, what their topology is, or whether or not
    these triangles are consistently oriented.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_distancer_results",
            category="application",
            symbols={
                "n_ions": "The total number of points, i.e. ions in the reconstruction.",
                "n_tri": "The total number of triangles in the set.",
            },
        ),
    )

    point_to_triangleID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_distancer_results.ApmParaprobeDistancerResultsPointToTriangleID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_distancer_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_distancer_results"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_distancer_results",
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


class ApmParaprobeDistancerResultsPointToTriangleID(ApmParaprobeToolProcess):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_process",
            name="point_to_triangleID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    sign_valid = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_distancer_results.ApmParaprobeDistancerResultsPointToTriangleIDSignValid",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="sign_valid",
            name_type="specified",
            optionality="optional",
        ),
    )
    window_triangles = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_distancer_results.ApmParaprobeDistancerResultsPointToTriangleIDWindowTriangles",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="window_triangles",
            name_type="specified",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The shortest analytical distance of each point to their "
            "respectively closest triangle from the joint triangle set."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    indices_triangle = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-indices-triangle-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "For each point the identifier of the triangle for which the "
            "shortest distance was found."
        ),
        a_nexus_field=NeXusField(
            name="indices_triangle",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_point = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-indices-point-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "A support field to enable the visualization of each point by an "
            "explicit identifier on the interval [0, n_ions - 1]. The field can "
            "be used to visualize the points as a function of their distance to "
            "the triangle set (e.g. via XDMF/Paraview)."
        ),
        a_nexus_field=NeXusField(
            name="indices_point",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeDistancerResultsPointToTriangleIDSignValid(CsFilterBooleanMask):
    """
    A bitmask that identifies which of the distance values is assumed to have a
    consistent sign because the closest triangle had a consistent outer unit
    normal defined.

    For points whose bit is set to 0 the distance is correct but the sign is
    not reliable.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-sign-valid-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="sign_valid",
            name_type="specified",
            optionality="optional",
        ),
    )

    number_of_triangles = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-sign-valid-number-of-triangles-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Number of triangles covered by the mask."),
        a_nexus_field=NeXusField(
            name="number_of_triangles",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-sign-valid-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Bitdepth of the elementary datatype that is used to store the "
            "information content of the mask (typically 8 bit, uint8)."
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-sign-valid-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The content of the mask. Like for all masks used in the tools of "
            "the paraprobe-toolbox, padding is used when number_of_objects is "
            "not an integer multiple of bitdepth. If padding is used, padded "
            "bits are set to 0."
        ),
        a_nexus_field=NeXusField(
            name="mask",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeDistancerResultsPointToTriangleIDWindowTriangles(CsFilterBooleanMask):
    """
    A bitmask that identifies which of the triangles in the set were considered
    when certain triangles have been filtered out.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-window-triangles-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="window_triangles",
            name_type="specified",
            optionality="optional",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-window-triangles-number-of-objects-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-window-triangles-bitdepth-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_distancer_results.html#nxapm_paraprobe_distancer_results-entry-point-to-triangleid-window-triangles-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="mask",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
