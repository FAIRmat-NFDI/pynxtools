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
# Run `pynx nomad generate-metainfo --nxdl NXrotations` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import Quantity, Section

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Rotations"]


class Rotations(Object):
    """
    Base class to detail a set of rotations, orientations, and disorientations.

    For getting a more detailed insight into the discussion of the
    parameterized description of orientations in materials science see:

    * `H.-J. Bunge <https://doi.org/10.1016/C2013-0-11769-2>`_ * `T. B. Britton
    et al. <https://doi.org/10.1016/j.matchar.2016.04.008>`_ * `D. Rowenhorst
    et al. <https://doi.org/10.1088/0965-0393/23/8/083501>`_ * `A. Morawiec
    <https://doi.org/10.1007/978-3-662-09156-2>`_

    Once orientations are defined, one can continue to characterize the
    misorientation and specifically the disorientation. The misorientation
    describes the rotation that is required to register the lattices of two
    oriented objects (like crystal lattice) into a crystallographic equivalent
    orientation:

    * `R. Bonnet <https://doi.org/10.1107/S0567739480000186>`_

    The concepts of mis- and disorientation are relevant when analyzing the
    crystallography of interfaces.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXrotations",
            category="base",
            symbols={
                "c": "The cardinality of the set, i.e. the number of value tuples.",
                "n_phases": "How many phases with usually different crystal and symmetry are distinguished.",
            },
        ),
    )

    reference_frame = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-reference-frame-field"
        ],
        description=(
            "Reference to an instance of :ref:`NXcoordinate_system` which "
            "contextualizes how the here reported parameterized quantities can "
            "be interpreted."
        ),
        a_nexus_field=NeXusField(
            name="reference_frame",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    crystal_symmetry = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-crystal-symmetry-field"
        ],
        shape=["*"],
        description=(
            "Point group which defines the symmetry of the crystal. This has to "
            "be at least a single string. If crystal_symmetry is not provided, "
            "point group 1 is assumed. In the case that misorientation or "
            "disorientation fields are used and the two crystal sets resolve for "
            "phases with a different crystal symmetry, this field needs to "
            "encode two strings: The first string is for phase A. The second "
            "string is for phase B. An example of this most complex case is the "
            "description of the disorientation between crystals adjoining a "
            "hetero-phase boundary."
        ),
        a_nexus_field=NeXusField(
            name="crystal_symmetry",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_symmetry = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-sample-symmetry-field"
        ],
        shape=["*"],
        description=(
            "Point group which defines an assumed symmetry imprinted upon "
            "processing the material/sample which could give rise to or may "
            "justify to use a simplified description of rotations, orientations, "
            "misorientations, and disorientations via numerical procedures that "
            "are known as symmetrization. If sample_symmetry is not provided, "
            "point group 1 is assumed. The traditionally used symmetrization "
            "operations within the texture community in Materials Science, "
            "though, have become obsolete thanks to improvements in methods, "
            "software, and available computing power. Therefore, users are "
            "encouraged to set the sample_symmetry to 1 (triclinic). In practice "
            "one often faces situations where indeed these assumed symmetries "
            "are anyway not fully observed, and thus an accepting of eventual "
            "inaccuracies just for the sake of reporting a simplified "
            "symmetrized description should be avoided."
        ),
        a_nexus_field=NeXusField(
            name="sample_symmetry",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    rotation_quaternion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-rotation-quaternion-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 4],
        description=(
            "The set of rotations expressed in quaternion parameterization "
            "considering crystal_symmetry and sample_symmetry. Rotations which "
            "should be interpreted as antipodal are not marked as such."
        ),
        a_nexus_field=NeXusField(
            name="rotation_quaternion",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    rotation_euler = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-rotation-euler-field"
        ],
        dimensionality="[angle]",
        shape=["*", 3],
        description=(
            "The set of rotations expressed in Euler angle parameterization "
            "considering the same applied symmetries as detailed for the field "
            "rotation_quaternion. To interpret Euler angles correctly, it is "
            "necessary to inspect the rotation conventions behind "
            "reference_frame to resolve which of the many possible Euler-angle "
            "conventions (Bunge ZXZ, XYZ, Kocks, Tait, etc.) were used."
        ),
        a_nexus_field=NeXusField(
            name="rotation_euler",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    is_antipodal = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-is-antipodal-field"
        ],
        shape=["*"],
        description=(
            "True for all those value tuples which have assumed antipodal "
            "symmetry. False for all others."
        ),
        a_nexus_field=NeXusField(
            name="is_antipodal",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    orientation_quaternion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-orientation-quaternion-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 4],
        description=(
            "The set of orientations expressed in quaternion parameterization "
            "and obeying symmetry for equivalent cases as detailed in "
            "crystal_symmetry and sample_symmetry. The supplementary field "
            "is_antipodal can be used to mark orientations with the antipodal "
            "property."
        ),
        a_nexus_field=NeXusField(
            name="orientation_quaternion",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    orientation_euler = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-orientation-euler-field"
        ],
        dimensionality="[angle]",
        shape=["*", 3],
        description=(
            "The set of orientations expressed in Euler angle parameterization "
            "following the same assumptions like for orientation_quaternion. To "
            "interpret Euler angles correctly, it is necessary to inspect the "
            "rotation conventions behind reference_frame to resolve which of the "
            "many Euler-angle conventions possible (Bunge ZXZ, XYZ, Kocks, Tait, "
            "etc.) were used."
        ),
        a_nexus_field=NeXusField(
            name="orientation_euler",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    misorientation_quaternion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-misorientation-quaternion-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 4],
        description=(
            "The set of misorientations expressed in quaternion parameterization "
            "obeying symmetry operations for equivalent misorientations as "
            "defined by crystal_symmetry and sample_symmetry. The misorientation "
            "should not be confused with the disorientation, as for the latter "
            "the angular argument is expected to be the minimal obeying "
            "symmetries."
        ),
        a_nexus_field=NeXusField(
            name="misorientation_quaternion",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    misorientation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-misorientation-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=(
            "Misorientation angular argument (eventually signed) following the "
            "same symmetry assumptions as expressed for the field "
            "misorientation_quaternion."
        ),
        a_nexus_field=NeXusField(
            name="misorientation_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    misorientation_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-misorientation-axis-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 3],
        description=(
            "Misorientation axis (normalized) and signed following the same "
            "symmetry assumptions as expressed for the field "
            "misorientation_angle."
        ),
        a_nexus_field=NeXusField(
            name="misorientation_axis",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    disorientation_quaternion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-disorientation-quaternion-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 4],
        description=(
            "The set of disorientations expressed in quaternion parameterization "
            "obeying symmetry operations for equivalent disorientations as "
            "defined by crystal_symmetry and sample_symmetry."
        ),
        a_nexus_field=NeXusField(
            name="disorientation_quaternion",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    disorientation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-disorientation-angle-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        description=(
            "Disorientations angular argument (should not be signed, see `D. "
            "Rowenhorst et al. "
            "<https://doi.org/10.1088/0965-0393/23/8/083501>`_) following the "
            "same symmetry assumptions as expressed for the field "
            "disorientation_quaternion."
        ),
        a_nexus_field=NeXusField(
            name="disorientation_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    disorientation_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXrotations.html#nxrotations-disorientation-axis-field"
        ],
        dimensionality="dimensionless",
        shape=["*", 3],
        description=(
            "Disorientations axis (normalized) following the same symmetry "
            "assumptions as expressed for the field disorientation_angle."
        ),
        a_nexus_field=NeXusField(
            name="disorientation_axis",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
