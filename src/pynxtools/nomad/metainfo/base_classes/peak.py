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
# Run `pynx nomad generate-metainfo --nxdl NXpeak` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Peak"]


class Peak(Object):
    """
    Base class for describing a peak, its functional form, and support values
    i.e., the discretization points at which the function has been evaluated.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpeak.html#nxpeak"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXpeak",
            category="base",
            symbols={
                "dimRank": "Rank of the dependent and independent data arrays\n                (for multivariate scalar-valued fit)."
            },
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.peak.PeakData",
        repeats=False,
    )
    function = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fit_function.FitFunction",
        repeats=False,
        description=(
            "The functional form of the peak. This could be a Gaussian, "
            "Lorentzian, Voigt, etc."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="function",
            name_type="specified",
            optionality="optional",
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpeak.html#nxpeak-label-field"
        ],
        description=(
            "Human-readable label which specifies which concept/entity the peak "
            "represents/identifies."
        ),
        a_nexus_field=NeXusField(
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    total_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpeak.html#nxpeak-total-area-field"
        ],
        description=("Total area under the curve."),
        a_nexus_field=NeXusField(
            name="total_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
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


class PeakData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpeak.html#nxpeak-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="optional",
        ),
    )

    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpeak.html#nxpeak-data-position-field"
        ],
        description=(
            "Position values along one or more data dimensions (to hold the "
            "values for the independent variable)."
        ),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpeak.html#nxpeak-data-intensity-field"
        ],
        description=(
            "This array holds the intensity/count values of the fitted peak at "
            "each position."
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
