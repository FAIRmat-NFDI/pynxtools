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
# Run `pynx nomad generate-metainfo --nxdl NXguide` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Guide"]


class Guide(Component):
    """
    A neutron optical element to direct the path of the beam.

    :ref:`NXguide` is used by neutron instruments to describe a guide consists
    of several mirrors building a shape through which neutrons can be guided or
    directed. The simplest such form is box shaped although elliptical guides
    are gaining in popularity. The individual parts of a guide usually have
    common characteristics but there are cases where they are different. For
    example, a neutron guide might consist of 2 or 4 coated walls or a
    supermirror bender with multiple, coated vanes.

    To describe polarizing supermirrors such as used in neutron reflection, it
    may be necessary to revise this definition of :ref:`NXguide` to include
    :ref:`NXpolarizer` and/or :ref:`NXmirror`.

    When even greater complexity exists in the definition of what constitutes a
    *guide*, it has been suggested that :ref:`NXguide` be redefined as a
    :ref:`NXcollection` of :ref:`NXmirror` each having their own
    :ref:`NXgeometry` describing their location(s).

    For the more general case when describing mirrors, consider using
    :ref:`NXmirror`.

    NOTE: The NeXus International Advisory Committee welcomes comments for
    revision and improvement of this definition of :ref:`NXguide`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXguide",
            category="base",
            symbols={
                "nsurf": "number of reflecting surfaces",
                "nwl": "number of wavelengths",
            },
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=(
            "TODO: Explain what this NXgeometry group means. What is intended here?"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the guid and NXoff_geometry to describe its shape instead",
        ),
    )
    reflectivity = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.guide.GuideReflectivity",
        repeats=False,
        description=("Reflectivity as function of reflecting surface and wavelength"),
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

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-description-field"
        ],
        description=("A description of this particular instance of ``NXguide``."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-incident-angle-field"
        ],
        dimensionality="[angle]",
        description=("TODO: documentation needed"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-bend-angle-x-field"
        ],
        dimensionality="[angle]",
        description=("TODO: documentation needed"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-bend-angle-y-field"
        ],
        dimensionality="[angle]",
        description=("TODO: documentation needed"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-interior-atmosphere-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-external-material-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-m-value-field"
        ],
        shape=["*"],
        description=(
            "The ``m`` value for a supermirror, which defines the supermirror "
            "regime in multiples of the critical angle of Nickel."
        ),
        a_nexus_field=NeXusField(
            name="m_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_material = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-substrate-material-field"
        ],
        shape=["*"],
        description=("TODO: documentation needed"),
        a_nexus_field=NeXusField(
            name="substrate_material",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-substrate-thickness-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("TODO: documentation needed"),
        a_nexus_field=NeXusField(
            name="substrate_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    coating_material = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-coating-material-field"
        ],
        shape=["*"],
        description=("TODO: documentation needed"),
        a_nexus_field=NeXusField(
            name="coating_material",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_roughness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-substrate-roughness-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("TODO: documentation needed"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-coating-roughness-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("TODO: documentation needed"),
        a_nexus_field=NeXusField(
            name="coating_roughness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    number_sections = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-number-sections-field"
        ],
        dimensionality="dimensionless",
        description=(
            "number of substrate sections (also called ``nsurf`` as an index in "
            "the ``NXguide`` specification)"
        ),
        a_nexus_field=NeXusField(
            name="number_sections",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-depends-on-field"
        ],
        description=(
            "The entry opening of the guide lies on the reference plane. The "
            "center of the opening on that plane is the reference point on the x "
            "and y axis. The reference plane is orthogonal to the z axis and is "
            "the reference point along the z axis. Given no bend in the guide, "
            "it is parallel with z axis and extends in the positive direction of "
            "the z axis. .. image:: guide/guide.png :width: 40%"
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


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class GuideReflectivity(Data):
    """
    Reflectivity as function of reflecting surface and wavelength
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="reflectivity",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=MEnum(["data"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["data"],
        ),
    )
    axes = Quantity(
        type=MEnum(["surface wavelength"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["surface wavelength"],
        ),
    )
    surface_indices = Quantity(
        type=MEnum(["0"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-surface-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="surface_indices",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["0"],
        ),
    )
    wavelength_indices = Quantity(
        type=MEnum(["1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-wavelength-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="wavelength_indices",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["1"],
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-data-field"
        ],
        shape=["*", "*"],
        description=("reflectivity of each surface as a function of wavelength"),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    surface = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-surface-field"
        ],
        shape=["*"],
        description=(
            "List of surfaces. Probably best to use index numbers but the "
            "specification is very loose."
        ),
        a_nexus_field=NeXusField(
            name="surface",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXguide.html#nxguide-reflectivity-wavelength-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("wavelengths at which reflectivity was measured"),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
