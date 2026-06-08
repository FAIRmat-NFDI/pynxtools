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
# Run `pynx nomad generate-metainfo --nxdl NXdelocalization` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.match_filter import MatchFilter
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Delocalization"]


class Delocalization(Object):
    """
    Base class of the configuration and results of a delocalization algorithm.

    Delocalization is used to distribute point-like objects on a grid to obtain
    e.g. smoother count, composition, or concentration values of scalar fields
    and compute gradients of these fields.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdelocalization.html#nxdelocalization"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdelocalization",
            category="base",
            symbols={
                "n_p": "Number of points/objects.",
                "n_m": "Number of mark data per point/object.",
                "n_atoms": "Number of atoms in the whitelist.",
                "n_nuclides": "Number of isotopes in the whitelist.",
            },
        ),
    )

    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_grid.CgGrid",
        repeats=False,
        description=("Details about the grid on which the delocalization is applied."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="optional",
        ),
    )
    weighting_model = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.delocalization.DelocalizationWeightingModel",
        repeats=False,
        description=(
            "The weighting model specifies how mark data are mapped to a weight "
            "per point/object."
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


class DelocalizationWeightingModel(MatchFilter):
    """
    The weighting model specifies how mark data are mapped to a weight per
    point/object.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdelocalization.html#nxdelocalization-weighting-model-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmatch_filter",
            name="weighting_model",
            name_type="specified",
            optionality="optional",
        ),
    )

    weighting_method = Quantity(
        type=MEnum(["default", "element", "isotope"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdelocalization.html#nxdelocalization-weighting-model-weighting-method-field"
        ],
        description=(
            "As an example from the research field of atom probe points/objects "
            "are (molecular) ions. Different methods are used for weighting "
            "ions: * default, points get all the same weight 1., which for atom "
            "probe is equivalent to (molecular) iontype-based delocalization. * "
            "element, points get as much weight as they have atoms representing "
            "a nuclide with a proton number that is matching to a respective "
            "entry in whitelist. In atom probe jargon, this means "
            "atomic_decomposition. * isotope, points get as much weight as they "
            "have atoms representing a nuclides from a respective entry in "
            "whitelist. In atom probe jargon, this means isotope_decomposition."
        ),
        a_nexus_field=NeXusField(
            name="weighting_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["default", "element", "isotope"],
        ),
    )
    method = Quantity(
        type=MEnum(["whitelist"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdelocalization.html#nxdelocalization-weighting-model-method-field"
        ],
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["whitelist"],
        ),
    )
    match = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdelocalization.html#nxdelocalization-weighting-model-match-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "A list of nuclides based on which to evaluate the weight. Nuclides "
            "need to exist in the nuclide table. Values are nuclide (isotope) "
            "hash values using the following hashing rule :math:`H = Z + N "
            "\\cdot 256` with :math:`Z` the number of protons and :math:`N` the "
            "number of neutrons of the nuclide. For elements set :math:`N` to "
            "zero."
        ),
        a_nexus_field=NeXusField(
            name="match",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    mark = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdelocalization.html#nxdelocalization-weighting-model-mark-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Attribute data for each member of the point cloud. For APM these "
            "are the iontypes generated via ranging. The number of mark data per "
            "point is 1 in the case for atom probe."
        ),
        a_nexus_field=NeXusField(
            name="mark",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdelocalization.html#nxdelocalization-weighting-model-weight-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Weighting factor with which the integrated intensity per grid cell "
            "is multiplied specifically for each point/object. For APM the "
            "weight are positive integer values, specifically the multiplicity "
            "of the ion, according to the details of the weighting_method."
        ),
        a_nexus_field=NeXusField(
            name="weight",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
