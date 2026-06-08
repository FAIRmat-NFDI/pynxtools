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
# Run `pynx nomad generate-metainfo --nxdl NXmirror` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Mirror"]


class Mirror(Component):
    """
    A beamline mirror or supermirror.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmirror",
            category="base",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the mirror and NXoff_geometry to describe its shape instead",
        ),
    )
    reflectivity = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("Reflectivity as function of wavelength"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="reflectivity",
            name_type="specified",
            optionality="optional",
        ),
    )
    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.shape.Shape",
        repeats=False,
        description=("A NXshape group describing the shape of the mirror"),
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="optional",
            deprecated="Use NXoff_geometry instead",
        ),
    )
    figure_data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("Numerical description of the surface figure of the mirror."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="figure_data",
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

    type = Quantity(
        type=MEnum(["single", "multi"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["single", "multi"],
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-description-field"
        ],
        description=("description of this mirror"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    incident_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-incident-angle-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="incident_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    bend_angle_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-bend-angle-x-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="bend_angle_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    bend_angle_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-bend-angle-y-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="bend_angle_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    interior_atmosphere = Quantity(
        type=MEnum(["vacuum", "helium", "argon"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-interior-atmosphere-field"
        ],
        a_nexus_field=NeXusField(
            name="interior_atmosphere",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["vacuum", "helium", "argon"],
        ),
    )
    external_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-external-material-field"
        ],
        description=("external material outside substrate"),
        a_nexus_field=NeXusField(
            name="external_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    m_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-m-value-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The m value for a supermirror, which defines the supermirror regime "
            "in multiples of the critical angle of Nickel."
        ),
        a_nexus_field=NeXusField(
            name="m_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    substrate_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-substrate-material-field"
        ],
        a_nexus_field=NeXusField(
            name="substrate_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-substrate-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        a_nexus_field=NeXusField(
            name="substrate_density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    substrate_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-substrate-thickness-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="substrate_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    coating_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-coating-material-field"
        ],
        a_nexus_field=NeXusField(
            name="coating_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_roughness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-substrate-roughness-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="substrate_roughness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    coating_roughness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-coating-roughness-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="coating_roughness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    even_layer_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-even-layer-material-field"
        ],
        a_nexus_field=NeXusField(
            name="even_layer_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    even_layer_density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-even-layer-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        a_nexus_field=NeXusField(
            name="even_layer_density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    odd_layer_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-odd-layer-material-field"
        ],
        a_nexus_field=NeXusField(
            name="odd_layer_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    odd_layer_density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-odd-layer-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        a_nexus_field=NeXusField(
            name="odd_layer_density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    layer_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-layer-thickness-field"
        ],
        dimensionality="[length]",
        description=("An array describing the thickness of each layer"),
        a_nexus_field=NeXusField(
            name="layer_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmirror.html#nxmirror-depends-on-field"
        ],
        description=(
            "Given a flat mirror, the reference plane is the plane which "
            'contains the "entry" surface of the mirror. The reference point '
            "of the mirror in the x and y axis is the centre of the mirror on "
            "that plane. The reference plane is orthogonal to the z axis and the "
            "location of this plane is the reference point on the z axis. The "
            "mirror faces negative z values. .. image:: mirror/mirror.png "
            ":width: 40%"
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
