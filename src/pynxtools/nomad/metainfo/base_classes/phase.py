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
# Run `pynx nomad generate-metainfo --nx-class NXphase` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Phase"]


class Phase(Object):
    """
    Base class to describe a (thermodynamic) phase as a component of a
    material.

    Instances of phases can be crystalline.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXphase.html#nxphase"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXphase",
            category="base",
        ),
    )

    unit_cell = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.unit_cell.UnitCell",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXunit_cell",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.atom.Atom",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    phase_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXphase.html#nxphase-phase-id-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Identifier for each phase. The value 0 is reserved for the unknown "
            "phase that represents the null-model (no sufficiently significant "
            "information available). In other words, the phase_name is n/a aka "
            "notIndexed. The phase_id value should match with the integer suffix "
            "of the group name which represents that instance in a NeXus/HDF5 "
            "file, i.e. if three phases were used e.g. 0, 1, and 2, three "
            "instances of :ref:`NXphase` named phase0, phase1, and phase2 should "
            "be stored in that HDF5 file."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="phase_id",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXphase.html#nxphase-name-field"
        ],
        description=(
            "Given name as an alias for identifying this phase. If the phase_id "
            "is 0 and one would like to use the field name, the value should be "
            "n/a or notIndexed."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
