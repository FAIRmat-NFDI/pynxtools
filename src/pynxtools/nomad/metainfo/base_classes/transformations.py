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
# Run `pynx nomad generate-metainfo --nx-class NXtransformations` to regenerate.
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

__all__ = ["Transformations"]


class Transformations(Object):
    """
    Collection of axis-based translations and rotations to describe a geometry.
    May also contain axes that do not move and therefore do not have a
    transformation type specified, but are useful in understanding coordinate
    frames within which transformations are done, or in documenting important
    directions, such as the direction of gravity.

    A nested sequence of transformations lists the translation and rotation
    steps needed to describe the position and orientation of any movable or
    fixed device.

    There will be one or more transformations (axes) defined by one or more
    fields for each transformation. Transformations can also be described by
    NXlog groups when the values change with time. The all-caps name
    ``AXISNAME`` designates the particular axis generating a transformation
    (e.g. a rotation axis or a translation axis or a general axis). The
    attribute ``units="NX_TRANSFORMATION"`` designates the units will be
    appropriate to the ``transformation_type`` attribute:

    * ``NX_LENGTH`` for ``translation`` * ``NX_ANGLE`` for ``rotation`` *
    ``NX_UNITLESS`` for axes for which no transformation type is specified

    This class will usually contain all axes of a sample stage or goniometer or
    a detector. The NeXus default McSTAS coordinate frame is assumed, but
    additional useful coordinate axes may be defined by using axes for which no
    transformation type has been specified.

    The entry point (``depends_on``) will be outside of this class and point to
    a field in here (or to an instance of ``NX_coordinate_system``). Following
    the chain may also require following ``depends_on`` links to
    transformations outside, for example to a common base table. If a relative
    path is given, it is relative to the group enclosing the ``depends_on``
    specification.

    For a chain of three transformations, where :math:`T_1` depends on
    :math:`T_2` and that in turn depends on :math:`T_3`, the final
    transformation :math:`T_f` is

    .. math:: T_f = T_3 T_2 T_1

    In explicit terms, the transformations are a subset of affine
    transformations expressed as 4x4 matrices that act on homogeneous
    coordinates, :math:`w=(x,y,z,1)^T`.

    For rotation and translation,

    .. math:: T_r &= \begin{pmatrix} R & o \\ 0_3 & 1 \\end{pmatrix} \\ T_t &=
    \begin{pmatrix} I_3 & t + o \\ 0_3 & 1 \\end{pmatrix}

    where :math:`R` is the usual 3x3 rotation matrix, :math:`o` is an offset
    vector, :math:`0_3` is a row of 3 zeros, :math:`I_3` is the 3x3 identity
    matrix and :math:`t` is the translation vector.

    :math:`o` is given by the ``offset`` attribute, :math:`t` is given by the
    ``vector`` attribute multiplied by the field value, and :math:`R` is
    defined as a rotation about an axis in the direction of ``vector``, of
    angle of the field value.

    NOTE

    One possible use of ``NXtransformations`` is to define the motors and
    transformations for a diffractometer (goniometer). Such use is mentioned in
    the ``NXinstrument`` base class. Use one ``NXtransformations`` group for
    each diffractometer and name the group appropriate to the device.
    Collecting the motors of a sample table or xyz-stage in an
    NXtransformations group is equally possible.

    Following the section on the general description of axis in
    NXtransformations is a section which documents the fields commonly used
    within NeXus for positioning purposes and their meaning. Whenever there is
    a need for positioning a beam line component please use the existing names.
    Use as many fields as needed in order to position the component. Feel free
    to add more axis if required. In the description given below, only those
    attributes which are defined through the name are specified. Add the other
    attributes of the full set:

    * vector * offset * transformation_type * depends_on

    as needed.

    NOTE

    ``NXtransformations`` follows the **active** transformation convention.
    This means that the transformation describes how an object is moved or
    rotated within the coordinate system. In other words, the transformation
    actively changes the position or orientation of the object itself. This is
    in contrast to a **passive** transformation, which changes the frame of
    reference or coordinate system, while the object remains fixed. In case it
    is needed to describe multiple coordinate systems, it is strongly suggested
    to use the :ref:`NXcoordinate_system` base class.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtransformations",
            category="base",
            ignore_extra_groups=True,
            ignore_extra_fields=True,
            ignore_extra_attributes=True,
        ),
    )

    AXISNAME = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-field"
        ],
        variable=True,
        description=(
            "Units need to be appropriate for translation or rotation The name "
            "of this field is not forced. The user is free to use any name that "
            "does not cause confusion. When using more than one ``AXISNAME`` "
            "field, make sure that each field name is unique in the same group, "
            "as required by HDF5. The values given should be the start points of "
            "exposures for the corresponding frames. The end points should be "
            "given in ``AXISNAME_end``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="AXISNAME",
            type="NX_NUMBER",
            name_type="any",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    AXISNAME__transformation_type = Quantity(
        type=MEnum(["translation", "rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-transformation-type-attribute"
        ],
        description=(
            "The transformation_type may be ``translation``, in which case the "
            "values are linear displacements along the axis, ``rotation``, in "
            "which case the values are angular rotations around the axis. If "
            "this attribute is omitted, this is an axis for which there is no "
            "motion to be specified, such as the direction of gravity, or the "
            "direction to the source, or a basis vector of a coordinate frame. "
            "In this case the value of the ``AXISNAME`` field is not used and "
            "can be set to the number ``NaN``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["translation", "rotation"],
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-vector-attribute"
        ],
        shape=[3],
        description=(
            "Three values that define the axis for this transformation. The axis "
            "should be normalized to unit length, making it dimensionless. For "
            "``translation`` axes the direction should be chosen for increasing "
            "displacement. For general axes, an appropriate direction should be "
            "chosen. By default, for ``rotation`` axes that do not explicitly "
            "depend on a coordinate system, the direction should be chosen for a "
            "right-handed rotation with increasing angle. Note, McStas is a "
            "right handed coordinate system. If the ``NXtransformation`` depends "
            "on a coordinate system (i.e., its ``depends_on`` attribute (or a "
            "``depends_on`` further up the transformation chain) points to an "
            "instance of :ref:`NXcoordinate_system`), the rotation convention is "
            "the same as the handedness of the coordinate system (as defined by "
            "the determinant of its base vectors): * Rotations in left-handed "
            "coordinate systems are left-handed (i.e., they follow the left-hand "
            "grip rule). In a left-handed coordinate system, positive rotation "
            "about an axis is clockwise when looking from a point on the "
            "positive axis towards its origin (from infinity towards the "
            "origin). * Rotations in right-handed coordinate systems are "
            "right-handed (i.e., they follow the right-hand grip rule). In a "
            "right-handed coordinate system, positive rotation about an axis is "
            "counter-clockwise when looking from a point on the positive axis "
            "towards its origin (from infinity towards the origin). Note that by "
            "using this convention, the transformation matrices in both left- "
            "and right-handed coordinate systems are the same."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-offset-attribute"
        ],
        shape=[3],
        description=(
            "A fixed offset applied before the transformation (three vector "
            "components). This is not intended to be a substitute for a fixed "
            "``translation`` axis but, for example, as the mechanical offset "
            "from mounting the axis to its dependency."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__offset_units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-offset-units-attribute"
        ],
        description=(
            "Units of the offset. Values should be consistent with NX_LENGTH."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="offset_units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-depends-on-attribute"
        ],
        description=(
            "Points to the path of a field defining the axis on which this "
            'instance of NXtransformations depends or the string ".". It can '
            "also point to an instance of ``NX_coordinate_system`` if this "
            'transformation depends on it. If it is the string ".", it is '
            "explicitly pointing towards the default `NeXus coordinate system "
            "<https://manual.nexusformat.org/design.html#the-nexus-coordinate-system>`_."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__equipment_component = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-equipment-component-attribute"
        ],
        description=(
            "An arbitrary identifier of a component of the equipment to which "
            "the transformation belongs, such as 'detector_arm' or "
            "'detector_module'. NXtransformations with the same "
            "equipment_component label form a logical grouping which can be "
            "combined together into a single change-of-basis operation."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="equipment_component",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME_end = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-end-field"
        ],
        variable=True,
        description=(
            "``AXISNAME_end`` is a placeholder for a name constructed from the "
            "actual name of an axis to which ``_end`` has been appended. The "
            "values in this field are the end points of the motions that start "
            "at the corresponding positions given in the ``AXISNAME`` field."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="AXISNAME_end",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    AXISNAME_increment_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXtransformations.html#nxtransformations-axisname-increment-set-field"
        ],
        variable=True,
        description=(
            "``AXISNAME_increment_set`` is a placeholder for a name constructed "
            "from the actual name of an axis to which ``_increment_set`` has "
            "been appended. The value of this optional field is the intended "
            "average range through which the corresponding axis moves during the "
            "exposure of a frame. Ideally, the value of this field added to each "
            "value of ``AXISNAME`` would agree with the corresponding values of "
            "``AXISNAME_end``, but there is a possibility of significant "
            "differences. Use of ``AXISNAME_end`` is recommended."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="AXISNAME_increment_set",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
