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
# Run `pynx nomad generate-metainfo --nxdl NXem_img` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.image import Image
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmImg"]


class EmImg(Process):
    """
    Base class for method-specific generic imaging with electron microscopes.

    In the majority of cases simple d-dimensional regular scan patterns are
    used to probe regions-of-interest (ROIs). Examples can be single point aka
    spot measurements, line profiles, or (rectangular) surface mappings. The
    latter pattern is the most frequently used.

    For now the base class provides for scans for which the settings, binning,
    and energy resolution is the same for each scan point.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_img.html#nxem_img"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_img",
            category="base",
        ),
    )

    image = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_img.EmImgImage",
        repeats=True,
        variable=True,
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


class EmImgImage(Image):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_img.html#nxem_img-image-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    microstructure = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.Microstructure",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    imaging_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_img.html#nxem_img-image-imaging-mode-field"
        ],
        description=("Which imaging mode was used?"),
        a_nexus_field=NeXusField(
            name="imaging_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "secondary_electron",
                "backscattered_electron",
                "annular_dark_field",
                "cathodoluminescence",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    half_angle_interval = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_img.html#nxem_img-image-half-angle-interval-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=[2],
        description=(
            "Annulus inner (first value) and outer (second value) half angle."
        ),
        a_nexus_field=NeXusField(
            name="half_angle_interval",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
