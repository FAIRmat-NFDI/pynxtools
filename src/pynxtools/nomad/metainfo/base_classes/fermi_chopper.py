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
# Run `pynx nomad generate-metainfo --nxdl NXfermi_chopper` to regenerate.
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

__all__ = ["FermiChopper"]


class FermiChopper(Component):
    """
    A Fermi chopper, possibly with curved slits.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXfermi_chopper",
            category="base",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=("geometry of the fermi chopper"),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the chopper and NXoff_geometry to describe its shape instead",
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
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-type-field"
        ],
        description=("Fermi chopper type"),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    rotation_speed = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-rotation-speed-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("chopper rotation speed"),
        a_nexus_field=NeXusField(
            name="rotation_speed",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("radius of chopper"),
        a_nexus_field=NeXusField(
            name="radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    slit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-slit-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("width of an individual slit"),
        a_nexus_field=NeXusField(
            name="slit",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    r_slit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-r-slit-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("radius of curvature of slits"),
        a_nexus_field=NeXusField(
            name="r_slit",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-number-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("number of slits"),
        a_nexus_field=NeXusField(
            name="number",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-height-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("input beam height"),
        a_nexus_field=NeXusField(
            name="height",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-width-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("input beam width"),
        a_nexus_field=NeXusField(
            name="width",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "distance. Note, it is recommended to use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Wavelength transmitted by chopper"),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("energy selected"),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    absorbing_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-absorbing-material-field"
        ],
        description=("absorbing material"),
        a_nexus_field=NeXusField(
            name="absorbing_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    transmitting_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-transmitting-material-field"
        ],
        description=("transmitting material"),
        a_nexus_field=NeXusField(
            name="transmitting_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfermi_chopper.html#nxfermi_chopper-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a fermi chopper."
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
