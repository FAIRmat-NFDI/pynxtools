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
# Run `pynx nomad generate-metainfo --nxdl NXcoordinate_system` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CoordinateSystem"]


class CoordinateSystem(Object):
    """
    Base class to detail a coordinate system (CS).

    Instances of ``NXcoordinate_system`` can be used to describe coordinate
    systems other than the default `NeXus coordinate system
    <https://manual.nexusformat.org/design.html#the-nexus-coordinate-system>`_.

    Whenever possible, all instances of :ref:`NXcoordinate_system` should be
    used at the top-level (i.e, directly below ``NXentry``) within an
    application definition or within a NeXus file.

    ``NXcoordinate_system`` can be part of the transformations chain using
    :ref:`NXtransformations`, where it acts as a linear change-of-basis
    transformation (using a 3x3 matrix with the basis vectors ``x``, `y``, and
    ``z`` as columns).

    Any group that has an optional ``depends_on`` field or any field that has
    an optional ``depends_on`` attribute has a fallback when ``depends_on`` is
    not provided. The fallback behavior involves traversing up the hierarchy
    until the first ancestor that contains one and only one
    ``NXcoordinate_system`` group is found. If such an ancestor exists, its
    coordinate system applies. If none is found or more than one instance of
    ``NXcoordinate_system`` is found at the same level, then the current
    coordinate system is not defined with respect to anything else. As an
    example, if there is only one ``NXcoordinate_system`` called
    "my_coordinate_system" defined directly under ``NXentry``, each optional
    ``depends_on`` field/attribute that is not defined automatically defaults
    to ``depends_on=my_coordinate_system``.

    How many groups of type ``NXcoordinate_system`` should be used in an
    application definition?

    * 0; if there is no instance of ``NXcoordinate_system`` across the entire
    tree, you can use ``depends_on="."`` to state that this transformation
    depends on the default `NeXus coordinate system
    <https://manual.nexusformat.org/design.html#the-nexus-coordinate-system>`_
    (which is the same as the one used by `McStas <https://mcstas.org/>`_).

    For the sake of clarity, even in this case it is better to be explicit and
    consistent for every other coordinate system definition to support users
    with interpreting the content and logic behind every instance of the tree.

    The default NeXus coordinate system (i.e., the McStas coordinate system)
    can be expressed as follows:

    .. code-block::

    mcstas@NXcoordinate_system x = [1, 0, 0] y = [0, 1, 0] z = [0, 0, 1]
    @y_direction = "opposite to gravity" @z_direction = "direction of the
    primary beam"

    Note that this assumes that the direction of the beam is not defined in the
    ``NXbeam`` instance.

    * 1; if only one :ref:`NXcoordinate_system` is defined, it should be placed
    as high up in the tree hierarchy (ideally right below an instance of
    NXentry) of the application definition tree as possible. This coordinate
    system shall be named such that it is clear how this coordinate system is
    typically referred to in a community. For the NeXus McStas coordinate
    system, it is advised to call it ``mcstas`` for the sake of improved
    clarity.

    If this is the case, it is assumed that this ``NXcoordinate_system``
    overwrites the NeXus default McStas coordinate system, i.e. users can
    thereby conveniently and explicitly specify the coordinate system that they
    wish to use.

    This case has the advantage that it is explicit and offers no ambiguities.
    However, in reality typically multiple coordinate systems have to be
    mastered especially for complex multi-signal modality experiments.

    If this case is realized, the best practice is that in every case where
    this coordinate system should be referred to the respective group has a
    ``depends_on`` field, to clearly indicate which specific coordinate systems
    is referred to.

    * 2 and more; as soon as more than one :ref:`NXcoordinate_system` is
    specified somewhere in the tree, different interpretations are possible as
    to which of these coordinate systems apply or take preference. While these
    ambiguities should be avoided if possible, the opportunity for multiples
    instances enables to have coordinate system conventions that are specific
    for some part of the NeXus tree. This is especially useful for deep groups
    where multiple scientific methods are combined or cases where having a
    definition of global conversion tables how to convert between
    representations in different coordinate systems is not desired or available
    for now.

    To resolve the possible ambiguities which specific coordinate systems in an
    :ref:`NXtransformations` train is referred to, it is even more important to
    use the ``depends_on`` field in groups and the ``depends_on`` attribute in
    NXtransformations to refer to one of the ``NXcoordinate_system`` instances.

    In the case of two or more instances of ``NXcoordinate_system`` it is
    advised to specify the relationship between the two coordinate systems by
    using the :ref:`NXtransformations` group within ``NXcoordinate_system``.

    In any case, users are encouraged to write explicit and clean
    ``depends_on`` fields in all groups that encode information for which the
    interpretation of coordinate systems and transformations is relevant. If
    these ``depends_on`` instances are not provided or no instance of
    ``NX_coordinate_system`` exists in the upper part of the hierarchy, the
    application definition is considered underconstrained. Note that this is
    the case for all files that were created before ``NXcoordinate_system`` was
    added.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcoordinate_system",
            category="base",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=True,
        variable=True,
        description=(
            "Collection of axis-based translations and rotations to describe "
            "this coordinate system with respect to another coordinate system."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    origin = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-origin-field"
        ],
        description=(
            "Human-readable field describing where the origin of this CS is. "
            "Exemplar values could be *left corner of the lab bench*, *door "
            "handle* *pinhole through which the electron beam exits the pole "
            "piece*, *barycenter of the triangle*, *center of mass of the "
            "stone*."
        ),
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-type-field"
        ],
        description=("Coordinate system type."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["undefined", "cartesian"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    x_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-x-alias-field"
        ],
        description=("Opportunity to define an alias for the name of the x-axis."),
        a_nexus_field=NeXusField(
            name="x_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    x_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-x-direction-field"
        ],
        description=(
            "Human-readable field telling in which direction the x-axis points "
            "if that instance of :ref:`NXcoordinate_system` has no reference to "
            "any parent and as such is the world reference frame. Exemplar "
            "values could be direction of gravity."
        ),
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Basis unit vector along the first axis which spans the coordinate "
            "system. This axis is frequently referred to as the x-axis in "
            "Euclidean space and the i-axis in reciprocal space. Note that `x``, "
            "``y``, and ``z`` must constitute a basis, i.e., a set of linearly "
            "independent vectors that span the vector space."
        ),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-y-alias-field"
        ],
        description=("Opportunity to define an alias for the name of the y-axis."),
        a_nexus_field=NeXusField(
            name="y_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    y_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-y-direction-field"
        ],
        description=(
            "Human-readable field telling in which direction the y-axis points "
            "if that instance of :ref:`NXcoordinate_system` has no reference to "
            "any parent and as such is the mighty world reference frame. See "
            "docstring of ``x_direction`` for further details."
        ),
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Basis unit vector along the second axis which spans the coordinate "
            "system. This axis is frequently referred to as the y-axis in "
            "Euclidean space and the j-axis in reciprocal space."
        ),
        a_nexus_field=NeXusField(
            name="y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    z_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-z-alias-field"
        ],
        description=("Opportunity to define an alias for the name of the z-axis."),
        a_nexus_field=NeXusField(
            name="z_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    z_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-z-direction-field"
        ],
        description=(
            "Human-readable field telling in which direction the z-axis points "
            "if that instance of :ref:`NXcoordinate_system` has no reference to "
            "any parent and as such is the mighty world reference frame. See "
            "docstring of x_alias for further details."
        ),
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[3],
        description=(
            "Basis unit vector along the third axis which spans the coordinate "
            "system. This axis is frequently referred to as the z-axis in "
            "Euclidean space and the k-axis in reciprocal space."
        ),
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcoordinate_system.html#nxcoordinate_system-depends-on-field"
        ],
        description=(
            "This specifies the relation to another coordinate system by "
            "pointing to the last transformation in the transformation chain in "
            "the NXtransformations group."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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
