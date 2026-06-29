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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_odf` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructureOdf"]


class MicrostructureOdf(Process):
    """
    Base class to store an orientation distribution function (ODF).

    An orientation distribution function is a probability distribution that
    details how much volume of material has a specific orientation. An ODF is
    computed from pole figure data in a computational process called `pole
    figure inversion <https://doi.org/10.1107/S0021889808030112>`_.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_odf",
            category="base",
            symbols={
                "n_varphi_two": "Number of pixel per varphi section plot along the :math:`\\varphi_2` slow\n                direction.",
                "n_capital_phi": "Number of pixel per varphi section plot along the :math:`\\Phi` fast direction.",
                "n_varphi_one": "Number of pixel per varphi section plot along the :math:`\\varphi_1` fastest\n                direction.",
                "k": "Number of local maxima evaluated in the component analysis.",
                "n_pos": "Number of sampled positions in orientation space.",
            },
        ),
    )

    configuration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_odf.MicrostructureOdfConfiguration",
        repeats=False,
        description=("Details about the algorithm used for computing the ODF."),
    )
    characteristics = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_odf.MicrostructureOdfCharacteristics",
        repeats=False,
        description=(
            "Group to store descriptors for a rough classification of an ODF."
        ),
    )
    kth_extrema = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_odf.MicrostructureOdfKthExtrema",
        repeats=False,
        description=(
            "Group to store descriptors and summary statistics for extrema of the ODF."
        ),
    )
    sampling = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_odf.MicrostructureOdfSampling",
        repeats=False,
        description=("The ODF intensity values (weights) as sampled with a software."),
    )
    phi_two_plot = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_odf.MicrostructureOdfPhiTwoPlot",
        repeats=False,
        description=(
            "Visualization of the ODF intensity as discretized orthogonal "
            "sections through orientation space parameterized using Bunge-Euler "
            "angles. This is one example of typical default plots used in the "
            "texture community in materials engineering. Mind that the "
            "orientation space is a distorted space when it using an Euler angle "
            "parameterization. Therefore, equivalent orientations show intensity "
            "contributions in eventually multiple locations."
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


class MicrostructureOdfConfiguration(Parameters):
    """
    Details about the algorithm used for computing the ODF.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-configuration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="configuration",
            name_type="specified",
            optionality="optional",
        ),
    )

    crystal_symmetry_point_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-configuration-crystal-symmetry-point-group-field"
        ],
        description=(
            "Point group of the crystal structure of the phase for which the "
            "here documented phase-dependent ODF was computed following the "
            "notation of the International Table of Crystallography."
        ),
        a_nexus_field=NeXusField(
            name="crystal_symmetry_point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    specimen_symmetry_point_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-configuration-specimen-symmetry-point-group-field"
        ],
        description=(
            "Point group assumed for additionally considered sample symmetries "
            "following the notation of the International Table of "
            "Crystallography."
        ),
        a_nexus_field=NeXusField(
            name="specimen_symmetry_point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    kernel_halfwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-configuration-kernel-halfwidth-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Halfwidth of the kernel."),
        a_nexus_field=NeXusField(
            name="kernel_halfwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    kernel_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-configuration-kernel-name-field"
        ],
        description=("Name of the kernel."),
        a_nexus_field=NeXusField(
            name="kernel_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-configuration-resolution-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Resolution of the kernel."),
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureOdfCharacteristics(Process):
    """
    Group to store descriptors for a rough classification of an ODF.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-characteristics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="characteristics",
            name_type="specified",
            optionality="optional",
        ),
    )

    texture_index = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-characteristics-texture-index-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The texture index :math:`t = \\int_{\\mathcal{SO(3)}} f(R)^{2}dR` "
            "with :math:`f(R)`, denoting the ODF is evaluated in orientation "
            "space :math:`\\mathcal{SO(3)}`. The higher it is the texture index "
            "the sharper it is the ODF."
        ),
        a_nexus_field=NeXusField(
            name="texture_index",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureOdfKthExtrema(Process):
    """
    Group to store descriptors and summary statistics for extrema of the ODF.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-kth-extrema-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="kth_extrema",
            name_type="specified",
            optionality="optional",
        ),
    )

    extrema = Quantity(
        type=MEnum(["minima", "maxima"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-kth-extrema-extrema-field"
        ],
        description=(
            "Minima or maxima, if extrema is set to minima values for location "
            "and volume_fraction are sorted in increasing order. If extrema is "
            "set to maxima values for location and volume_fraction are sorted in "
            "decreasing order. Therefore, the global extremum is always the "
            "first entry in location and volume_fraction."
        ),
        a_nexus_field=NeXusField(
            name="extrema",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["minima", "maxima"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    kth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-kth-extrema-kth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Number of local extrema evaluated"),
        a_nexus_field=NeXusField(
            name="kth",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    theta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-kth-extrema-theta-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Disorientation threshold within which intensity of the ODF is "
            "integrated for the component analysis."
        ),
        a_nexus_field=NeXusField(
            name="theta",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    location = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-kth-extrema-location-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 3],
        description=(
            "Euler angle representation :math:`\\varphi_1`, :math:`\\Phi`, "
            ":math:`\\varphi_2` of the kth-most maxima in decreasing order of "
            "the intensity maximum."
        ),
        a_nexus_field=NeXusField(
            name="location",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    volume_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-kth-extrema-volume-fraction-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "Integrated ODF intensity within a theta angular region of the "
            "orientation space :math:`SO3` about each location (obeying "
            "symmetries) as specified for each location."
        ),
        a_nexus_field=NeXusField(
            name="volume_fraction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureOdfSampling(Process):
    """
    The ODF intensity values (weights) as sampled with a software.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-sampling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="sampling",
            name_type="specified",
            optionality="optional",
        ),
    )

    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-sampling-resolution-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Sampling resolution"),
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    euler = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-sampling-euler-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", 3],
        description=(
            "Bunge-Euler (i.e. ZXZ convention) locations of each position in "
            "orientation space for which a weight was sampled."
        ),
        a_nexus_field=NeXusField(
            name="euler",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-sampling-weight-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Weight at each sampled position following the order in euler."),
        a_nexus_field=NeXusField(
            name="weight",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureOdfPhiTwoPlot(Data):
    """
    Visualization of the ODF intensity as discretized orthogonal sections
    through orientation space parameterized using Bunge-Euler angles.

    This is one example of typical default plots used in the texture community
    in materials engineering.

    Mind that the orientation space is a distorted space when it using an Euler
    angle parameterization. Therefore, equivalent orientations show intensity
    contributions in eventually multiple locations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-phi-two-plot-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="phi_two_plot",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-phi-two-plot-intensity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*", "*"],
        description=(
            "ODF intensity at probed locations relative to the intensity of the "
            "null model of a random texture."
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    varphi_one = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-phi-two-plot-varphi-one-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Pixel center angular position along the :math:`\\varphi_1` direction."
        ),
        a_nexus_field=NeXusField(
            name="varphi_one",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    capital_phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-phi-two-plot-capital-phi-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Pixel center angular position along the :math:`\\Phi` direction."
        ),
        a_nexus_field=NeXusField(
            name="capital_phi",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    varphi_two = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_odf.html#nxmicrostructure_odf-phi-two-plot-varphi-two-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Pixel center angular position along the :math:`\\varphi_2` direction."
        ),
        a_nexus_field=NeXusField(
            name="varphi_two",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
