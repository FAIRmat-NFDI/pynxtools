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
# Run `pynx nomad generate-metainfo --nxdl NXaberration` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import Quantity, Section

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Aberration"]


class Aberration(Object):
    """
    Quantified aberration coefficient in an aberration_model.

    For an introduction in the details about aberrations with relevance for
    electron microscopy see `R. Dunin-Borkowski et al.
    <https://doi.org/10.1017/9781316337455.022>`_ and `S. J. Pennycock and P.
    D. Nellist <https://doi.org/10.1007/978-1-4419-7200-2>`_ (page 44ff, and
    page 118ff) for different definitions available and further details. Table
    7-2 of Ibid. publication (page 305ff) documents how to convert from the
    Nion to the CEOS definitions. Conversion tables are also summarized by `Y.
    Liao <https://www.globalsino.com/EM/page3740.html>`_ an introduction.

    The use of the base class is not restricted to electron microscopy but can
    also be useful for classical optics.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXaberration",
            category="base",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration-magnitude-field"
        ],
        description=("Magnitude of the aberration"),
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    magnitude_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration-magnitude-errors-field"
        ],
        description=("Uncertainty of the magnitude of the aberration"),
        a_nexus_field=NeXusField(
            name="magnitude_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    magnitude_errors_model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration-magnitude-errors-model-field"
        ],
        description=(
            "Free-text description how magnitude_errors was quantified e.g. via "
            "the 95% confidence interval, variance, standard deviation, using "
            "which algorithm or statistical model."
        ),
        a_nexus_field=NeXusField(
            name="magnitude_errors_model",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    delta_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration-delta-time-field"
        ],
        dimensionality="[time]",
        description=("Time elapsed since the last measurement."),
        a_nexus_field=NeXusField(
            name="delta_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration-angle-field"
        ],
        dimensionality="[angle]",
        description=(
            "For the CEOS definitions the C aberrations are radial-symmetric and "
            "have no angle entry, while the A, B, D, S, or R aberrations are "
            "n-fold symmetric and have an angle entry. For the NION definitions "
            "the coordinate system differs to the one used in CEOS and instead "
            "two aberration coefficients a and b are used."
        ),
        a_nexus_field=NeXusField(
            name="angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration-name-field"
        ],
        description=("Given name to this aberration."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaberration.html#nxaberration-alias-field"
        ],
        description=("Alias to name or refer to this specific type of aberration."),
        a_nexus_field=NeXusField(
            name="alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
