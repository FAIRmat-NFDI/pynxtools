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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_tool_parameters` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeToolParameters"]


class ApmParaprobeToolParameters(Parameters):
    """
    Base class documenting parameters for processing used by all tools of the
    paraprobe-toolbox.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_tool_parameters",
            category="base",
        ),
    )

    reconstruction = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_parameters.ApmParaprobeToolParametersReconstruction",
        repeats=False,
        description=(
            "Specification of the tomographic reconstruction to use for this "
            "analysis. Typically, reconstructions in the field of atom probe "
            "tomography are communicated via files which store at least "
            "reconstructed ion positions and mass-to-charge-state-ratio values. "
            "Container files like HDF5 though can store multiple "
            "reconstructions. Therefore, the position and mass_to_charge "
            "concepts point to specific instances to use for this analysis."
        ),
    )
    ranging = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_parameters.ApmParaprobeToolParametersRanging",
        repeats=False,
        description=(
            "Specification of the ranging definitions to use for this analysis. "
            "Ranging is the process of labeling time-of-flight data with "
            "so-called iontypes (aka ion species). Ideally, iontypes specify the "
            "most likely (molecular) ion that is assumed to have been evaporated "
            "given that its mass-to-charge-state ratio lies within the specific "
            "mass-to-charge-state-ratio value interval of the iontype. The "
            "so-called unknown_type iontype represents the null model of an ion "
            "that has not been ranged (for whatever reasons) or is not "
            "rangeable. The identifier of this special iontype is always the "
            "reserved value 0."
        ),
    )
    surface = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "Specification of the triangulated surface mesh to use for this "
            "analysis. Such a surface mesh can be used to define the edge of the "
            "reconstructed volume to account for finite size effects."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface",
            name_type="specified",
            optionality="optional",
        ),
    )
    surface_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_paraprobe_tool_parameters.ApmParaprobeToolParametersSurfaceDistance",
        repeats=False,
        description=(
            "Specification of the point-to-triangulated-surface-mesh distances "
            "to use for this analysis."
        ),
    )
    spatial_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spatial_filter.SpatialFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXspatial_filter",
            name="spatial_filter",
            name_type="specified",
            optionality="optional",
        ),
    )
    evaporation_id_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.subsampling_filter.SubsamplingFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsubsampling_filter",
            name="evaporation_id_filter",
            name_type="specified",
            optionality="optional",
        ),
    )
    iontype_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.match_filter.MatchFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="iontype_filter",
            name_type="specified",
            optionality="optional",
        ),
    )
    hit_multiplicity_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.match_filter.MatchFilter",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-identifier-analysis-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Internal identifier used by the tool to refer to an analysis. "
            "Simulation ID an alias."
        ),
        a_nexus_field=NeXusField(
            name="identifier_analysis",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-description-field"
        ],
        description=(
            "Possibility for leaving a free-text description about this "
            "analysis. Although offered here for convenience, we strongly "
            "encourage to parameterize such descriptions as much as possible to "
            "support reusage and clearer communication."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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


class ApmParaprobeToolParametersReconstruction(Note):
    """
    Specification of the tomographic reconstruction to use for this analysis.

    Typically, reconstructions in the field of atom probe tomography are
    communicated via files which store at least reconstructed ion positions and
    mass-to-charge-state-ratio values. Container files like HDF5 though can
    store multiple reconstructions. Therefore, the position and mass_to_charge
    concepts point to specific instances to use for this analysis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-reconstruction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="reconstruction",
            name_type="specified",
            optionality="optional",
        ),
    )

    position = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-reconstruction-position-field"
        ],
        description=(
            "Name of the node which resolves the reconstructed ion position "
            "values to use for this analysis."
        ),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    mass_to_charge = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-reconstruction-mass-to-charge-field"
        ],
        description=(
            "Name of the node which resolves the mass-to-charge-state-ratio "
            "values to use for this analysis."
        ),
        a_nexus_field=NeXusField(
            name="mass_to_charge",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolParametersRanging(Note):
    """
    Specification of the ranging definitions to use for this analysis.

    Ranging is the process of labeling time-of-flight data with so-called
    iontypes (aka ion species). Ideally, iontypes specify the most likely
    (molecular) ion that is assumed to have been evaporated given that its
    mass-to-charge-state ratio lies within the specific
    mass-to-charge-state-ratio value interval of the iontype.

    The so-called unknown_type iontype represents the null model of an ion that
    has not been ranged (for whatever reasons) or is not rangeable. The
    identifier of this special iontype is always the reserved value 0.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-ranging-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="ranging",
            name_type="specified",
            optionality="optional",
        ),
    )

    ranging_definitions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-ranging-ranging-definitions-field"
        ],
        description=(
            "Name of the (parent) node directly below which (in the hierarchy) "
            "the ranging definition for (molecular) ions are stored."
        ),
        a_nexus_field=NeXusField(
            name="ranging_definitions",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeToolParametersSurfaceDistance(Note):
    """
    Specification of the point-to-triangulated-surface-mesh distances to use
    for this analysis.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-surface-distance-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="optional",
        ),
    )

    distance = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_tool_parameters.html#nxapm_paraprobe_tool_parameters-surface-distance-distance-field"
        ],
        description=(
            "Absolute path in the (HDF5) file that points to the distance "
            "values. The tool assumes that the values are stored in the same "
            "order as points (ions)."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
