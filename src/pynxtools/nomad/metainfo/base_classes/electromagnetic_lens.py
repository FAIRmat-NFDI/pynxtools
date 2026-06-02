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
# Run `pynx nomad generate-metainfo --nx-class NXelectromagnetic_lens` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ElectromagneticLens"]


class ElectromagneticLens(Component):
    """
    Base class for an electro-magnetic lens or a compound lens.

    For :ref:`NXtransformations` the origin of the coordinate system is placed
    in the center of the lens its pole piece, pinhole, or another point of
    reference. The origin should be specified in the :ref:`NXtransformations`.

    For details of electro-magnetic lenses in the literature see e.g.

    * `L. Reimer: Scanning Electron Microscopy
    <https://doi.org/10.1007/978-3-540-38967-5>`_ * `P. Hawkes: Magnetic
    Electron Lenses
    <https://link.springer.com/book/10.1007/978-3-642-81516-4>`_ * `Y. Liao:
    Practical Electron Microscopy and Database
    <https://www.globalsino.com/EM/>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXelectromagnetic_lens",
            category="base",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-name-field"
        ],
        description=("Name of the lens."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-description-field"
        ],
        description=(
            "Ideally, use instances of ``identifierNAME`` to point to a resource "
            "that provides further details. If such a resource does not exist or "
            "should not be used, use this free text, although it is not "
            "recommended."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    power_setting = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-power-setting-field"
        ],
        description=(
            "Descriptor for the lens excitation when the exact technical details "
            "are unknown or not directly controllable as the control software of "
            "the microscope does not enable or was not configured to display "
            "these values for users. Although this value does not document the "
            "exact physical voltage or excitation, it can still give useful "
            "context to reproduce the lens setting, provided a properly working "
            "instrument and software sets the lens into a similar state to the "
            "technical level possible when no more information is available "
            "physically or accessible legally."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="power_setting",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-mode-field"
        ],
        description=(
            "Descriptor for the operation mode of the lens when other details "
            "are not directly controllable as the control software of the "
            "microscope does not enable or is not configured to display these "
            "values. Like value, the mode can only be interpreted for a specific "
            "microscope but can still be useful to guide users as to how to "
            "repeat the measurement."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Excitation voltage of the lens. For dipoles it is a single number. "
            "For higher order multipoles, it is an array."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-current-field"
        ],
        dimensionality="[current]",
        description=(
            "Excitation current of the lens. For dipoles it is a single number. "
            "For higher-order multipoles, it is an array."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    type = Quantity(
        type=MEnum(
            ["single", "double", "quadrupole", "hexapole", "octupole", "dodecapole"]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-type-field"
        ],
        description=(
            "Qualitative type of lens with respect to the number of pole pieces."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "single",
                "double",
                "quadrupole",
                "hexapole",
                "octupole",
                "dodecapole",
            ],
        ),
    )
    number_of_poles = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXelectromagnetic_lens.html#nxelectromagnetic_lens-number-of-poles-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Qualitative description of the lens based on the number of pole pieces."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="number_of_poles",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
