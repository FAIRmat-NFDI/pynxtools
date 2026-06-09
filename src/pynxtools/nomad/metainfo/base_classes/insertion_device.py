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
# Run `pynx nomad generate-metainfo --nxdl NXinsertion_device` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["InsertionDevice"]


class InsertionDevice(Component):
    """
    An insertion device, as used in a synchrotron light source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXinsertion_device",
            category="base",
        ),
    )

    spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("spectrum of insertion device"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum",
            name_type="specified",
            optionality="optional",
        ),
    )
    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=('"Engineering" position of insertion device'),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the device and NXoff_geometry to describe its shape instead",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the beam line component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    type = Quantity(
        type=MEnum(["undulator", "wiggler", "wavelength_shifter"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-type-field"
        ],
        description=(
            "It is recommended (effective from 2025) to use the "
            '"wavelength_shifter" choice for 3-pole wigglers, while reserving '
            'the generic "wiggler" designation for extended multipole '
            "wigglers."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["undulator", "wiggler", "wavelength_shifter"],
        ),
    )
    gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-gap-field"
        ],
        dimensionality="[length]",
        description=("separation between opposing pairs of magnetic poles"),
        a_nexus_field=NeXusField(
            name="gap",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    taper = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-taper-field"
        ],
        dimensionality="[angle]",
        description=(
            "angular of gap difference between upstream and downstream ends of "
            "the insertion device"
        ),
        a_nexus_field=NeXusField(
            name="taper",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    phase = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-phase-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="phase",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    poles = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-poles-field"
        ],
        dimensionality="dimensionless",
        description=("number of poles"),
        a_nexus_field=NeXusField(
            name="poles",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    magnetic_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-magnetic-wavelength-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="magnetic_wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-k-field"
        ],
        dimensionality="dimensionless",
        description=("beam displacement parameter"),
        a_nexus_field=NeXusField(
            name="k",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-length-field"
        ],
        dimensionality="[length]",
        description=("length of insertion device"),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        description=("total power delivered by insertion device"),
        a_nexus_field=NeXusField(
            name="power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_POWER",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("energy of peak intensity in output spectrum"),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-bandwidth-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("bandwidth of peak energy"),
        a_nexus_field=NeXusField(
            name="bandwidth",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    harmonic = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-harmonic-field"
        ],
        dimensionality="dimensionless",
        description=("harmonic number of peak"),
        a_nexus_field=NeXusField(
            name="harmonic",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a insertion device."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
