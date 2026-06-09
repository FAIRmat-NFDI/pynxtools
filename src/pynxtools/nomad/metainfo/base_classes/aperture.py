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
# Run `pynx nomad generate-metainfo --nxdl NXaperture` to regenerate.
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

__all__ = ["Aperture"]


class Aperture(Component):
    """
    A beamline aperture.

    Note, the group was incorrectly documented as deprecated, but it is not and
    it is in common use.

    You can specify the geometry of the aperture using either NXoff_geometry or
    for simpler geometry shape and size.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaperture.html#nxaperture"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXaperture",
            category="base",
        ),
    )

    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("Use this group to describe the shape of the aperture."),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.positioner.Positioner",
        repeats=True,
        variable=True,
        description=("Stores the raw positions of aperture motors."),
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=(
            "Location and shape of aperture .. TODO: documentation needs "
            "improvement, contributions welcome * description of terms is poor "
            "and leaves much to interpretation * Describe what is meant by "
            "translation _here_ and ... * Similar throughout base classes * Some "
            "base classes do this much better * Such as where is the gap "
            "written?"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the aperture and :ref:`NXoff_geometry` to describe its shape",
        ),
    )
    BLADE_GEOMETRY = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=False,
        description=("location and shape of each blade"),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="BLADE_GEOMETRY",
            name_type="specified",
            optionality="optional",
            deprecated="Use :ref:`NXoff_geometry` instead to describe the shape of the aperture",
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=("Describe any additional information in a note."),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaperture.html#nxaperture-depends-on-field"
        ],
        description=(
            "The reference point of the aperture is its center in the x and y "
            "axis. The reference point on the z axis is the surface of the "
            "aperture pointing towards the source. In complex (asymmetric) "
            "geometries an NXoff_geometry group can be used to provide an "
            "unambiguous reference. .. image:: aperture/aperture.png :width: 40%"
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaperture.html#nxaperture-material-field"
        ],
        description=("Absorbing material of the aperture"),
        a_nexus_field=NeXusField(
            name="material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaperture.html#nxaperture-description-field"
        ],
        description=("Description of aperture"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    shape = Quantity(
        type=MEnum(
            [
                "straight slit",
                "curved slit",
                "pinhole",
                "circle",
                "square",
                "hexagon",
                "octagon",
                "bladed",
                "open",
                "grid",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaperture.html#nxaperture-shape-field"
        ],
        description=("Shape of the aperture."),
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "straight slit",
                "curved slit",
                "pinhole",
                "circle",
                "square",
                "hexagon",
                "octagon",
                "bladed",
                "open",
                "grid",
            ],
        ),
    )
    size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXaperture.html#nxaperture-size-field"
        ],
        dimensionality="[length]",
        description=(
            "The relevant dimension for the aperture, i.e. slit width, pinhole "
            "and iris diameter"
        ),
        a_nexus_field=NeXusField(
            name="size",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
