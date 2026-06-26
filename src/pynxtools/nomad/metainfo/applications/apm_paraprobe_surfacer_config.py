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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_surfacer_config` to regenerate.
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
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfig,
    ApmParaprobeToolConfigTaskconfig,
)
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeSurfacerConfig"]


class ApmParaprobeSurfacerConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the paraprobe-surfacer
    tool.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_surfacer_config",
            category="application",
            symbols={
                "n_alpha_values": "Number of alpha values (and offset values) to probe.",
                "n_values": "How many different match values does the filter specify.",
            },
        ),
    )

    surface_meshingID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_config.ApmParaprobeSurfacerConfigSurface_meshingID",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_surfacer_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_surfacer_config"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_surfacer_config",
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


class ApmParaprobeSurfacerConfigSurface_meshingID(ApmParaprobeToolConfigTaskconfig):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="surface_meshingID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    preprocessing = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_surfacer_config.ApmParaprobeSurfacerConfigSurface_meshingIDPreprocessing",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="preprocessing",
            name_type="specified",
            optionality="required",
        ),
    )

    alpha_value_choice = Quantity(
        type=MEnum(
            [
                "convex_hull_naive",
                "convex_hull_refine",
                "smallest_solid",
                "cgal_optimal",
                "set_of_values",
                "set_of_alpha_wrappings",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-alpha-value-choice-field"
        ],
        description=(
            "Specifies which method to use to define the alpha value. The value "
            "*convex_hull_naive* is the default. The setting instructs the tool "
            "to use a fast specialized algorithm for computing only the convex "
            "hull. The resulting triangles can be skinny. The value "
            "*convex_hull_refine* instructs to tool to refine the quality of the "
            "mesh resulting from *convex_hull_naive* via triangle flipping and "
            "splitting. The value *smallest_solid* instructs the CGAL library to "
            "choose a value which realizes an alpha-shape that is the smallest "
            "solid. The value *cgal_optimal* instructs the CGAL library to "
            "choose a value which the library considers as to be an optimal "
            "value. Details are defined in the respective section of the CGAL "
            "library on 3D alpha shapes. The value *set_of_values* instructs the "
            "tool to compute a list collection of alpha-shapes for the specified "
            "alpha-values. The value *set_of_alpha_wrappings* instructs the tool "
            "to generate a set of so-called alpha wrappings. These are similar "
            "to alpha-shapes but provide additional guarantees (such as "
            "watertightness and proximity constraints) on the resulting "
            "wrapping."
        ),
        a_nexus_field=NeXusField(
            name="alpha_value_choice",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "convex_hull_naive",
                "convex_hull_refine",
                "smallest_solid",
                "cgal_optimal",
                "set_of_values",
                "set_of_alpha_wrappings",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    alpha_values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-alpha-values-field"
        ],
        shape=["*"],
        description=(
            "Array of alpha values to use when alpha_value_choice is "
            "set_of_values or when alpha_value_choice is set_of_alpha_wrappings."
        ),
        a_nexus_field=NeXusField(
            name="alpha_values",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    offset_values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-offset-values-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Array of offset values to use when alpha_value_choice is "
            "set_of_alpha_wrappings. The array of alpha_values and offset_values "
            "define a sequence of (alpha and offset value)."
        ),
        a_nexus_field=NeXusField(
            name="offset_values",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    has_exterior_facets = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-has-exterior-facets-field"
        ],
        description=(
            "Specifies if the tool should compute the set of exterior triangle "
            "facets for each alpha complex (for convex hull, alpha shapes, and "
            "wrappings)."
        ),
        a_nexus_field=NeXusField(
            name="has_exterior_facets",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_closure = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-has-closure-field"
        ],
        description=(
            "Specifies if the tool should check if the alpha complex of exterior "
            "triangular facets is a closed polyhedron."
        ),
        a_nexus_field=NeXusField(
            name="has_closure",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    has_interior_tetrahedra = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-has-interior-tetrahedra-field"
        ],
        description=(
            "Specifies if the tool should compute all interior tetrahedra of the "
            "alpha complex (currently only for alpha shapes)."
        ),
        a_nexus_field=NeXusField(
            name="has_interior_tetrahedra",
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


class ApmParaprobeSurfacerConfigSurface_meshingIDPreprocessing(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-preprocessing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="preprocessing",
            name_type="specified",
            optionality="required",
        ),
    )

    method = Quantity(
        type=MEnum(["default", "percolation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-preprocessing-method-field"
        ],
        description=(
            "Specifies the method that is used to preprocess the point cloud "
            "prior to the alpha-shape computation. The option *default* "
            "specifies that no such filtering is applied. The option "
            "*percolation* specifies that a Hoshen-Kopelman percolation analysis "
            "is used to identify points that lie closer to the edge of the "
            "dataset. Details about the methods are reported in `M. Kühbach et "
            "al. <https://doi.org/10.1038/s41524-020-00486-1>`_."
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["default", "percolation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    kernel_width = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_surfacer_config.html#nxapm_paraprobe_surfacer_config-entry-surface-meshingid-preprocessing-kernel-width-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "When using the *percolation* preprocessing, this is the width of "
            "the kernel for identifying which ions are in voxels close to the "
            "edge of the point cloud."
        ),
        a_nexus_field=NeXusField(
            name="kernel_width",
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
