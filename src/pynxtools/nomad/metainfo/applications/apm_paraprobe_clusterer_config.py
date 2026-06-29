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
# Run `pynx nomad generate-metainfo --nxdl NXapm_paraprobe_clusterer_config` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmParaprobeClustererConfig"]


class ApmParaprobeClustererConfig(ApmParaprobeToolConfig):
    """
    Application definition for a configuration file of the paraprobe-clusterer
    tool.

    The tool paraprobe-clusterer evaluates how points cluster in space.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_paraprobe_clusterer_config",
            category="application",
            symbols={
                "n_ivec_max": "Maximum number of atoms per molecular ion. Should be 32 for paraprobe.",
                "n_clust_algos": "Number of clustering algorithms used.",
                "n_ions": "Number of different iontypes to distinguish during clustering.",
            },
        ),
    )

    cameca_to_nexus = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigCamecaToNexus",
        repeats=False,
        description=(
            "This process maps results from a cluster analysis made with IVAS / "
            "AP Suite into an interoperable representation. IVAS / AP Suite "
            "usually exports such results as a list of reconstructed ion "
            "positions with one cluster label per position. These labels are "
            "reported via the mass-to-charge-state-ratio column of what is "
            "effectively a binary file that is formatted like a POS file but "
            "cluster labels written out using floating point numbers."
        ),
    )
    cluster_analysisID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigClusterAnalysisID",
        repeats=True,
        variable=True,
        description=(
            "This process performs a cluster analysis on a reconstructed dataset "
            "or a ROI within it."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm_paraprobe_clusterer_config"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm_paraprobe_clusterer_config"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXapm_paraprobe_clusterer_config",
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


class ApmParaprobeClustererConfigCamecaToNexus(ApmParaprobeToolConfigTaskconfig):
    """
    This process maps results from a cluster analysis made with IVAS / AP Suite
    into an interoperable representation. IVAS / AP Suite usually exports such
    results as a list of reconstructed ion positions with one cluster label per
    position. These labels are reported via the mass-to-charge-state-ratio
    column of what is effectively a binary file that is formatted like a POS
    file but cluster labels written out using floating point numbers.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="cameca_to_nexus",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    reconstruction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigCamecaToNexusReconstruction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="reconstruction",
            name_type="specified",
            optionality="required",
        ),
    )
    results = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigCamecaToNexusResults",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="results",
            name_type="specified",
            optionality="required",
        ),
    )

    recover_evaporation_id = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-recover-evaporation-id-field"
        ],
        description=(
            "Specifies if paraprobe-clusterer should use the evaporation_ids "
            "from reconstruction for recovering for each position in the "
            ":ref:`NXnote` results the closest matching position (within "
            "floating point accuracy). This can be useful when users wish to "
            "recover the original evaporation_id, which IVAS /AP Suite drops "
            "when writing their *.indexed.* cluster results POS files that is "
            "referred to results."
        ),
        a_nexus_field=NeXusField(
            name="recover_evaporation_id",
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


class ApmParaprobeClustererConfigCamecaToNexusReconstruction(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-reconstruction-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-reconstruction-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-reconstruction-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-reconstruction-algorithm-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-reconstruction-position-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-reconstruction-mass-to-charge-field"
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


class ApmParaprobeClustererConfigCamecaToNexusResults(Note):
    """
    File with the results of the cluster analyses that was computed with IVAS /
    AP suite (e.g. maximum-separation method clustering algorithm `J. Hyde et
    al. <https://doi.org/10.1557/PROC-650-R6.6>`_). The information is stored
    in an improper (.indexed.) POS file as a matrix of floating point
    quadruplets, one quadruplet for each ion. The first three values of each
    quadruplet encode the position of the ion. The fourth value is the integer
    identifier of the cluster encoded as a floating point number.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-results-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="results",
            name_type="specified",
            optionality="required",
        ),
    )

    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-results-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-results-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cameca-to-nexus-results-algorithm-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeClustererConfigClusterAnalysisID(ApmParaprobeToolConfigTaskconfig):
    """
    This process performs a cluster analysis on a reconstructed dataset or a
    ROI within it.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_paraprobe_tool_parameters",
            name="cluster_analysisID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    surface_distance = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigClusterAnalysisIDSurfaceDistance",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="surface_distance",
            name_type="specified",
            optionality="optional",
        ),
    )
    dbscan = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigClusterAnalysisIDDbscan",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="dbscan",
            name_type="specified",
            optionality="required",
        ),
    )
    hdbscan = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config.ApmParaprobeClustererConfigClusterAnalysisIDHdbscan",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="hdbscan",
            name_type="specified",
            optionality="required",
        ),
    )

    ion_type_filter = Quantity(
        type=MEnum(["resolve_element"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-ion-type-filter-field"
        ],
        description=(
            "How should iontypes be considered during the cluster analysis. The "
            "value resolve_all will set an ion active in the analysis regardless "
            "of which iontype it is. The value resolve_unknown will set an ion "
            "active when it is of the UNKNOWNTYPE. The value resolve_ion will "
            "set an ion active if it is of the specific iontype, irregardless of "
            "its nuclide structure. The value resolve_element will set an ion "
            "active and account as many times for it, as the (molecular) ion "
            "contains atoms of elements in the whitelist "
            "ion_query_nuclide_vector. The value resolve_isotope will set an ion "
            "active and account as many times for it, as the (molecular) ion "
            "contains nuclides in the whitelist ion_query_nuclide_vector. In "
            "effect, ion_query_nuclide_vector acts as a whitelist to filter "
            "which ions are considered as source ions of the correlation "
            "statistics and how the multiplicity of each ion will be factorized. "
            "This is relevant as in atom probe we have the situation that an ion "
            "of a molecular ion with more than one nuclide, say Ti O for example "
            "is counted potentially several times because at that position "
            "(reconstructed) position it has been assumed that there was a Ti "
            "and an O atom. This multiplicity affects the size of the feature "
            "and its chemical composition."
        ),
        a_nexus_field=NeXusField(
            name="ion_type_filter",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["resolve_element"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="resolve_element",
        ),
    )
    ion_query_nuclide_vector = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-ion-query-nuclide-vector-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=(
            "Matrix of nuclide vectors, as many as rows as different candidates "
            "for iontypes should be distinguished as possible source iontypes. "
            "In the simplest case, the matrix contains only the proton number of "
            "the element in the row, all other values set to zero."
        ),
        a_nexus_field=NeXusField(
            name="ion_query_nuclide_vector",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeClustererConfigClusterAnalysisIDSurfaceDistance(Note):
    """
    Distance between each ion and triangulated surface mesh.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-surface-distance-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-surface-distance-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-surface-distance-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-surface-distance-algorithm-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-surface-distance-distance-field"
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


class ApmParaprobeClustererConfigClusterAnalysisIDDbscan(Process):
    """
    Settings for DBScan clustering algorithm. For original details about the
    algorithm and (performance-relevant) details consider:

    * `M. Ester et al. <https://dx.doi.org/10.5555/3001460.3001507>`_ * `M.
    Götz et al. <https://dx.doi.org/10.1145/2834892.2834894>`_

    For details about how the DBScan algorithms is the key behind the specific
    modification known as the maximum-separation method in the atom probe
    community consider `E. Jägle et al.
    <https://dx.doi.org/10.1017/S1431927614013294>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-dbscan-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="dbscan",
            name_type="specified",
            optionality="required",
        ),
    )

    high_throughput_method = Quantity(
        type=MEnum(["tuple", "combinatorics"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-dbscan-high-throughput-method-field"
        ],
        description=(
            "Strategy how a set of cluster analyses with different parameter is "
            "executed: * For tuple as many runs are performed as parameter "
            "values have been defined. * For combinatorics individual parameter "
            "arrays are looped over. As an example we may provide ten entries "
            "for eps and three entries for min_pts. If high_throughput_method is "
            "set to tuple, the analysis is invalid because we have an "
            "insufficient number of min_pts values to pair them with our ten eps "
            "values. By contrast, if high_throughput_method is set to "
            "combinatorics, the tool will run three individual min_pts runs for "
            "each eps value, resulting in a total of 30 analyses. A typical "
            "example from the literature `M. Kühbach et al. "
            "<https://dx.doi.org/10.1038/s41524-020-00486-1>`_ can be instructed "
            "via setting eps to an array of values np.linspace(0.2, 5.0, "
            "nums=241, endpoint=True), one min_pts value that is equal to 1, and "
            "high_throughput_method set to combinatorics."
        ),
        a_nexus_field=NeXusField(
            name="high_throughput_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["tuple", "combinatorics"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    eps = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-dbscan-eps-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Array of epsilon (eps) parameter values."),
        a_nexus_field=NeXusField(
            name="eps",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    min_pts = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-dbscan-min-pts-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Array of minimum points (min_pts) parameter values."),
        a_nexus_field=NeXusField(
            name="min_pts",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmParaprobeClustererConfigClusterAnalysisIDHdbscan(Process):
    """
    Settings for the HPDBScan clustering algorithm.

    * L. McInnes et al. <https://dx.doi.org/10.21105/joss.00205>`_ *
    scikit-learn hdbscan library
    `<https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html>`_

    See also this documentation for details about the parameter. Here we use
    the terminology of the hdbscan documentation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-hdbscan-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="hdbscan",
            name_type="specified",
            optionality="required",
        ),
    )

    high_throughput_method = Quantity(
        type=MEnum(["tuple", "combinatorics"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-hdbscan-high-throughput-method-field"
        ],
        description=(
            "Strategy how runs with different parameter values are composed, "
            "following the explanation for high_throughput_method of dbscan."
        ),
        a_nexus_field=NeXusField(
            name="high_throughput_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["tuple", "combinatorics"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    min_cluster_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-hdbscan-min-cluster-size-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=("Array of min_cluster_size parameter values."),
        a_nexus_field=NeXusField(
            name="min_cluster_size",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    min_samples = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-hdbscan-min-samples-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=("Array of min_samples parameter values."),
        a_nexus_field=NeXusField(
            name="min_samples",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    cluster_selection_epsilon = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-hdbscan-cluster-selection-epsilon-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=("Array of cluster_selection parameter values."),
        a_nexus_field=NeXusField(
            name="cluster_selection_epsilon",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm_paraprobe_clusterer_config.html#nxapm_paraprobe_clusterer_config-entry-cluster-analysisid-hdbscan-alpha-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=("Array of alpha parameter values."),
        a_nexus_field=NeXusField(
            name="alpha",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
