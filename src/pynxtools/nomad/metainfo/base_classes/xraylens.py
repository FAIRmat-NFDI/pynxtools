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
# Run `pynx nomad generate-metainfo --nx-class NXxraylens` to regenerate.
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

__all__ = ["Xraylens"]


class Xraylens(Component):
    """
    An X-ray lens, typically at a synchrotron X-ray beam line.

    Based on information provided by Gerd Wellenreuther (DESY).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxraylens",
            category="base",
        ),
    )

    cylinder_orientation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=("Orientation of the cylinder axis."),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="cylinder_orientation",
            name_type="specified",
            optionality="optional",
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

    lens_geometry = Quantity(
        type=MEnum(["paraboloid", "spherical", "elliptical", "hyperbolical"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-lens-geometry-field"
        ],
        description=("Geometry of the lens"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="lens_geometry",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["paraboloid", "spherical", "elliptical", "hyperbolical"],
        ),
    )
    symmetric = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-symmetric-field"
        ],
        description=("Is the device symmetric?"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="symmetric",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    cylindrical = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-cylindrical-field"
        ],
        description=("Is the device cylindrical?"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="cylindrical",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    focus_type = Quantity(
        type=MEnum(["line", "point"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-focus-type-field"
        ],
        description=("The type of focus of the lens"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="focus_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["line", "point"],
        ),
    )
    lens_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-lens-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of the lens"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="lens_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    lens_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-lens-length-field"
        ],
        dimensionality="[length]",
        description=("Length of the lens"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="lens_length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    curvature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-curvature-field"
        ],
        dimensionality="[length]",
        description=("Radius of the curvature as measured in the middle of the lens"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="curvature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    aperture = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-aperture-field"
        ],
        dimensionality="[length]",
        description=("Diameter of the lens."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="aperture",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    number_of_lenses = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-number-of-lenses-field"
        ],
        description=("Number of lenses that make up the compound lens."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="number_of_lenses",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    lens_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-lens-material-field"
        ],
        description=("Material used to make the lens."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="lens_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    gas = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-gas-field"
        ],
        description=("Gas used to fill the lens"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="gas",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    gas_pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-gas-pressure-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        description=("Gas pressure in the lens"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="gas_pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PRESSURE",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXxraylens.html#nxxraylens-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a x-ray lens."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
