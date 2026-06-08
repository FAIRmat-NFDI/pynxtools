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
# Run `pynx nomad generate-metainfo --nxdl NXspindispersion` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Spindispersion"]


class Spindispersion(Component):
    """
    Class to describe spin filters in photoemission experiments.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspindispersion.html#nxspindispersion"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspindispersion",
            category="base",
        ),
    )

    scattering_target_history = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.history.History",
        repeats=False,
        description=(
            "A set of activities that occurred to the ``scattering_target`` "
            "prior to/during the. experiment. For example, this group can be "
            "used to describe the preparation of the ``scattering_target``."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXhistory",
            name="scattering_target_history",
            name_type="specified",
            optionality="optional",
        ),
    )
    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        description=("Deflectors in the spin dispersive section"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    electromagnetic_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electromagnetic_lens.ElectromagneticLens",
        repeats=True,
        variable=True,
        description=("Individual lenses in the spin dispersive section"),
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspindispersion.html#nxspindispersion-type-field"
        ],
        description=("Type of spin detector, VLEED, SPLEED, Mott, etc."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    figure_of_merit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspindispersion.html#nxspindispersion-figure-of-merit-field"
        ],
        dimensionality="dimensionless",
        description=("Figure of merit of the spin detector"),
        a_nexus_field=NeXusField(
            name="figure_of_merit",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    shermann_function = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspindispersion.html#nxspindispersion-shermann-function-field"
        ],
        dimensionality="dimensionless",
        description=("Effective Shermann function, calibrated spin selectivity factor"),
        a_nexus_field=NeXusField(
            name="shermann_function",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    scattering_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspindispersion.html#nxspindispersion-scattering-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("Energy of the spin-selective scattering"),
        a_nexus_field=NeXusField(
            name="scattering_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    scattering_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspindispersion.html#nxspindispersion-scattering-angle-field"
        ],
        dimensionality="[angle]",
        description=("Angle of the spin-selective scattering"),
        a_nexus_field=NeXusField(
            name="scattering_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    scattering_target = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspindispersion.html#nxspindispersion-scattering-target-field"
        ],
        description=("Name of the target"),
        a_nexus_field=NeXusField(
            name="scattering_target",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
