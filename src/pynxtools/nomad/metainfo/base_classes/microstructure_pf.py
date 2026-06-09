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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_pf` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructurePf"]


class MicrostructurePf(Process):
    """
    Base class to store a pole figure (PF) computation.

    A pole figure is the X-ray diffraction intensity for specific integrated
    peaks for a hemispherical illumination of a real or virtual specimen.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_pf",
            category="base",
            symbols={
                "n_y": "Number of pixel per pole figure in the slow direction.",
                "n_x": "Number of pixel per pole figure in the fast direction.",
            },
        ),
    )

    configuration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_pf.MicrostructurePfConfiguration",
        repeats=False,
        description=(
            "Details about the algorithm that was used to compute the pole figure."
        ),
    )
    pf = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_pf.MicrostructurePfPf",
        repeats=False,
        description=("Pole figure."),
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


class MicrostructurePfConfiguration(Parameters):
    """
    Details about the algorithm that was used to compute the pole figure.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-configuration-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-configuration-crystal-symmetry-point-group-field"
        ],
        description=(
            "Point group of the crystal structure of the phase for which the "
            "pole figure was computed following the notation of the "
            "International Table of Crystallography."
        ),
        a_nexus_field=NeXusField(
            name="crystal_symmetry_point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    specimen_symmetry_point_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-configuration-specimen-symmetry-point-group-field"
        ],
        description=(
            "Point group of assumed sample symmetries following the notation of "
            "the International Table of Crystallography."
        ),
        a_nexus_field=NeXusField(
            name="specimen_symmetry_point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    halfwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-configuration-halfwidth-field"
        ],
        dimensionality="[angle]",
        description=("Halfwidth of the kernel."),
        a_nexus_field=NeXusField(
            name="halfwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    miller_indices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-configuration-miller-indices-field"
        ],
        description=(
            "Miller (:math:`(hkl)[uvw]`) or Miller-Bravais indices used to "
            "specify the pole figure."
        ),
        a_nexus_field=NeXusField(
            name="miller_indices",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-configuration-resolution-field"
        ],
        dimensionality="[angle]",
        description=("Resolution of the kernel."),
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructurePfPf(Data):
    """
    Pole figure.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-pf-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pf",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-pf-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=("Pole figure intensity."),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    axis_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-pf-axis-y-field"
        ],
        shape=["*"],
        description=(
            "Pixel center along y direction in the equatorial plane of a "
            "stereographic projection of the unit sphere."
        ),
        a_nexus_field=NeXusField(
            name="axis_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_pf.html#nxmicrostructure_pf-pf-axis-x-field"
        ],
        shape=["*"],
        description=(
            "Pixel center along x direction in the equatorial plane of a "
            "stereographic projection of the unit sphere."
        ),
        a_nexus_field=NeXusField(
            name="axis_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
