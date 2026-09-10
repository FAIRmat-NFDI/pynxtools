# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXabsorption_edge (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXabsorption_edge` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
from pynxtools.nomad.metainfo.base_classes.atom import Atom
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["AbsorptionEdge"]


class AbsorptionEdge(Object):
    """
    An absorption edge is a sharp discontinuity in the X-ray absorption
    spectrum of an atom that occurs when the incident photon energy reaches the
    threshold energy for exciting the atom from its neutral ground state to a
    core-vacancy state.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXabsorption_edge.html#nxabsorption_edge"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXabsorption_edge",
            category="base",
        ),
    )

    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.absorption_edge.AbsorptionEdgeAtom",
        repeats=False,
    )

    name = Quantity(
        type=MEnum(
            [
                "K",
                "L1",
                "L2",
                "L3",
                "L2,3",
                "M1",
                "M2",
                "M3",
                "M2,3",
                "M4",
                "M5",
                "M4,5",
                "N1",
                "N2",
                "N3",
                "N2,3",
                "N4",
                "N5",
                "N4,5",
                "N6",
                "N7",
                "N6,7",
                "O1",
                "O2",
                "O3",
                "O2,3",
                "O4",
                "O5",
                "O4,5",
                "O6",
                "O7",
                "O6,7",
                "P1",
                "P2",
                "P3",
                "P2,3",
                "P4",
                "P5",
                "P4,5",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXabsorption_edge.html#nxabsorption_edge-name-field"
        ],
        description=(
            "Name of the absorption edge using `IUPAC notation`_ (e.g., ``K``, "
            "``L2``, ``M5``), which identifies the core-vacancy state of the "
            "atom. Correspondence between IUPAC notation and electron "
            "configuration, expressed as vacancy notation (superscript "
            ":math:`-1`): .. list-table:: :header-rows: 1 * - IUPAC - Electron "
            "configuration * - K - :math:`1s^{-1}` * - L1 - :math:`2s^{-1}` * - "
            "L2 - :math:`2p_{1/2}^{-1}` * - L3 - :math:`2p_{3/2}^{-1}` * - M1 - "
            ":math:`3s^{-1}` * - M2 - :math:`3p_{1/2}^{-1}` * - M3 - "
            ":math:`3p_{3/2}^{-1}` * - M4 - :math:`3d_{3/2}^{-1}` * - M5 - "
            ":math:`3d_{5/2}^{-1}` * - N1 - :math:`4s^{-1}` * - N2 - "
            ":math:`4p_{1/2}^{-1}` * - N3 - :math:`4p_{3/2}^{-1}` * - N4 - "
            ":math:`4d_{3/2}^{-1}` * - N5 - :math:`4d_{5/2}^{-1}` * - N6 - "
            ":math:`4f_{5/2}^{-1}` * - N7 - :math:`4f_{7/2}^{-1}` * - O1 - "
            ":math:`5s^{-1}` * - O2 - :math:`5p_{1/2}^{-1}` * - O3 - "
            ":math:`5p_{3/2}^{-1}` * - O4 - :math:`5d_{3/2}^{-1}` * - O5 - "
            ":math:`5d_{5/2}^{-1}` * - O6 - :math:`5f_{5/2}^{-1}` * - O7 - "
            ":math:`5f_{7/2}^{-1}` * - P1 - :math:`6s^{-1}` * - P2 - "
            ":math:`6p_{1/2}^{-1}` * - P3 - :math:`6p_{3/2}^{-1}` * - P4 - "
            ":math:`6d_{3/2}^{-1}` * - P5 - :math:`6d_{5/2}^{-1}` Per IUPAC, "
            "subscripts may be dropped when unknown or irrelevant. When two "
            "spin-orbit split levels are not distinguished, they may be written "
            "together (e.g. ``L2,3``). .. _IUPAC notation: "
            "https://doi.org/10.1002/xrs.1300200308"
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "K",
                "L1",
                "L2",
                "L3",
                "L2,3",
                "M1",
                "M2",
                "M3",
                "M2,3",
                "M4",
                "M5",
                "M4,5",
                "N1",
                "N2",
                "N3",
                "N2,3",
                "N4",
                "N5",
                "N4,5",
                "N6",
                "N7",
                "N6,7",
                "O1",
                "O2",
                "O3",
                "O2,3",
                "O4",
                "O5",
                "O4,5",
                "O6",
                "O7",
                "O6,7",
                "P1",
                "P2",
                "P3",
                "P2,3",
                "P4",
                "P5",
                "P4,5",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXabsorption_edge.html#nxabsorption_edge-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("Energy of the absorption edge."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
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


class AbsorptionEdgeAtom(Atom):
    """
    The atom whose core electron is excited at this absorption edge.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXabsorption_edge.html#nxabsorption_edge-atom-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name="atom",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXabsorption_edge.html#nxabsorption_edge-atom-name-field"
        ],
        description=("Chemical symbol of the element (e.g. ``Fe``, ``Cu``)."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
