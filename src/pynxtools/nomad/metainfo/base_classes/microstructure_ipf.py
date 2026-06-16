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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_ipf` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructureIpf"]


class MicrostructureIpf(Process):
    """
    Base class to store an inverse pole figure (IPF) mapping (IPF map).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_ipf",
            category="base",
            symbols={
                "v": "Number of pixel along the slow direction used for the IPF color key.",
                "u": "Number of pixel along the fast direction used for the IPF color key.",
                "n_z": "Number of pixel along the slowest direction, typically labeled z or k.",
                "n_y": "Number of pixel along the slow direction, typically labeled y or j.",
                "n_x": "Number of pixel along the fast direction, typically labeled x or i.",
                "n_rgb": "Number of RGB values along the fastest direction, always three.",
            },
        ),
    )

    input_grid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_grid.CgGrid",
        repeats=False,
        description=(
            "Details about the original grid, i.e. the grid for which the IPF "
            "map was computed when that IPF map was exported from the tech "
            "partner's file format representation."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="input_grid",
            name_type="specified",
            optionality="optional",
        ),
    )
    output_grid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_grid.CgGrid",
        repeats=False,
        description=(
            "Details about the grid onto which the IPF is recomputed. Rescaling "
            "the visualization of the IPF map may be needed to enable "
            "visualization in specific software tools like H5Web."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="output_grid",
            name_type="specified",
            optionality="optional",
        ),
    )
    map = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_ipf.MicrostructureIpfMap",
        repeats=False,
        description=(
            "Inverse pole figure mapping. Instances named phase0 should by "
            "definition refer to the null phase notIndexed. Inspect the "
            "definition of :ref:`NXphase` and its field phase_id for further "
            "details. Details about possible regridding and associated "
            "interpolation during the computation of the IPF map visualization "
            "can be stored using the input_grid, output_grid, and interpolation "
            "fields. The main purpose of this map is to offer a normalized "
            "default representation of the IPF map for consumption by a research "
            "data management system (RDMS)."
        ),
    )
    legend = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_ipf.MicrostructureIpfLegend",
        repeats=False,
        description=(
            "The color code which maps color to orientation in the fundamental "
            "zone. For each stereographic standard triangle (SST), i.e. a "
            "rendering of the fundamental zone of the crystal-symmetry-reduced "
            "orientation space SO3, it is possible to define a color model which "
            "assigns a color to each point in the fundamental zone. Different "
            "mapping models are used. These implement (slightly) different "
            "scaling relations. Differences exist across representations of tech "
            "partners. Differences are which base colors of the RGB color model "
            "are placed in which extremal position of the SST and where the "
            "white point is located. For further details see: * [G. Nolze et "
            "al.](https://doi.org/10.1107/S1600576716012942) * [S. Patala et "
            "al.](https://doi.org/10.1016/j.pmatsci.2012.04.002). Details are "
            "implementation-specific and not standardized yet."
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-depends-on-field"
        ],
        description=(
            "Reference to an instance of :ref:`NXcoordinate_system` in which the "
            "axes axis_z, axis_y, and axis_x are defined."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    color_model = Quantity(
        type=MEnum(["tsl", "mtex"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-color-model-field"
        ],
        description=("The algorithm whereby orientations are colored."),
        a_nexus_field=NeXusField(
            name="color_model",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["tsl", "mtex"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    projection_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-projection-direction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[3],
        description=(
            "The direction normal vector along which orientations are projected."
        ),
        a_nexus_field=NeXusField(
            name="projection_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    projection_direction__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-projection-direction-depends-on-attribute"
        ],
        description=(
            "Reference to an instance of :ref:`NXcoordinate_system` in which the "
            "projection_direction is defined. If the field depends_on is not "
            "provided but parents of the instance of this base class or its "
            "specializations define an instance of :ref:`NXcoordinate_system`, "
            "projection_direction is defined in this coordinate system. If "
            "nothing is provided, it is assumed that projection_direction is "
            "defined in the McStas coordinate system."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="projection_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    interpolation = Quantity(
        type=MEnum(["nearest_neighbour"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-interpolation-field"
        ],
        description=(
            "How where orientation values at positions of input_grid computed to "
            "values on output_grid. Nearest neighbour means the orientation of "
            "the closed (Euclidean distance) grid point of the input_grid was "
            "taken."
        ),
        a_nexus_field=NeXusField(
            name="interpolation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["nearest_neighbour"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="nearest_neighbour",
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


class MicrostructureIpfMap(Data):
    """
    Inverse pole figure mapping.

    Instances named phase0 should by definition refer to the null phase
    notIndexed. Inspect the definition of :ref:`NXphase` and its field phase_id
    for further details.

    Details about possible regridding and associated interpolation during the
    computation of the IPF map visualization can be stored using the
    input_grid, output_grid, and interpolation fields.

    The main purpose of this map is to offer a normalized default
    representation of the IPF map for consumption by a research data management
    system (RDMS).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-map-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="map",
            name_type="specified",
            optionality="optional",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-map-data-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Inverse pole figure color code for each map coordinate. Different "
            "types of AXISNAME dimensional scale axes are found in practice. A "
            "few examples: * No scaling, e.g. pixel position values like 0, 1, "
            "2, 3 pixel. Pixels on the map can be distinguished but that map is "
            "disconnected from any sample surface context and eventually "
            "physical scaling * Scaling but no offset, e.g. calibrated pixel "
            "position 0., 0.5, 1.0, 1.5 micron. Pixels on the map can be "
            "compared for their distance to obtain e.g. size of features but the "
            "position of the map relative to the e.g. the sample surface is "
            "unclear. For IPF maps this is the most frequently reported "
            "situation. * Scaling and offset, which resolves also the absolute "
            "position of the map in relation to the sample surface. This is "
            "useful information for stitching multiple mappings together and "
            "other processing where precise and accurate position data are "
            "relevant e.g. for correlative materials characterization. Three "
            "types of dimensional constraints for maps are possible: * (n_x, 3), "
            "a one-dimensional map, typically used for coarse sampling and "
            "crystal size statistics. * (n_y, n_x, 3), a two-dimensional map, "
            "the most frequently found reported * (n_z, n_y, n_x, 3), a "
            "three-dimensional map, these are commonly generated using "
            "computational methods, or in cases multiple EBSD maps have been "
            "stitched/reconstructed into a three-dimensional map."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    axis_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-map-axis-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Pixel center coordinate calibrated for step size along the z axis "
            "of the map."
        ),
        a_nexus_field=NeXusField(
            name="axis_z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-map-axis-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Pixel center coordinate calibrated for step size along the y axis "
            "of the map."
        ),
        a_nexus_field=NeXusField(
            name="axis_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-map-axis-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Pixel center coordinate calibrated for step size along the x axis "
            "of the map."
        ),
        a_nexus_field=NeXusField(
            name="axis_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureIpfLegend(Data):
    """
    The color code which maps color to orientation in the fundamental zone.

    For each stereographic standard triangle (SST), i.e. a rendering of the
    fundamental zone of the crystal-symmetry-reduced orientation space SO3, it
    is possible to define a color model which assigns a color to each point in
    the fundamental zone.

    Different mapping models are used. These implement (slightly) different
    scaling relations. Differences exist across representations of tech
    partners.

    Differences are which base colors of the RGB color model are placed in
    which extremal position of the SST and where the white point is located.

    For further details see:

    * [G. Nolze et al.](https://doi.org/10.1107/S1600576716012942) * [S. Patala
    et al.](https://doi.org/10.1016/j.pmatsci.2012.04.002).

    Details are implementation-specific and not standardized yet.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-legend-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="legend",
            name_type="specified",
            optionality="optional",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-legend-data-field"
        ],
        shape=["*", "*", 3],
        description=("Inverse pole figure color code for each map coordinate."),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-legend-axis-y-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Pixel along the y-axis."),
        a_nexus_field=NeXusField(
            name="axis_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    axis_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_ipf.html#nxmicrostructure_ipf-legend-axis-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Pixel along the x-axis."),
        a_nexus_field=NeXusField(
            name="axis_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
