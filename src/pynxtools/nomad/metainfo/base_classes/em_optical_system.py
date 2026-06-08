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
# Run `pynx nomad generate-metainfo --nxdl NXem_optical_system` to regenerate.
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

__all__ = ["EmOpticalSystem"]


class EmOpticalSystem(Object):
    """
    Base class for qualifying an electron optical system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_optical_system",
            category="base",
        ),
    )

    camera_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-camera-length-field"
        ],
        dimensionality="[length]",
        description=(
            "Distance which is present between the specimen surface and the "
            "detector plane. This concept is related to term `Camera Length`_ of "
            "the EMglossary standard. .. _Camera Length: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000008"
        ),
        a_nexus_field=NeXusField(
            name="camera_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    magnification = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-magnification-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The factor of enlargement of the apparent size, not the physical "
            "size, of an object."
        ),
        a_nexus_field=NeXusField(
            name="magnification",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    defocus = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-defocus-field"
        ],
        dimensionality="[length]",
        description=(
            "The defocus aberration constant (oftentimes referred to as c_1_0). "
            "See respective details in :ref:`NXaberration` class instances."
        ),
        a_nexus_field=NeXusField(
            name="defocus",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    semi_convergence_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-semi-convergence-angle-field"
        ],
        dimensionality="[angle]",
        description=(
            "The angle which is given by the semi-opening angle of the cone in a "
            "convergent beam. This concept is related to term `Convergence "
            "Angle`_ of the EMglossary standard. .. _Convergence Angle: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000010"
        ),
        a_nexus_field=NeXusField(
            name="semi_convergence_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    field_of_view = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-field-of-view-field"
        ],
        dimensionality="[length]",
        description=(
            "The extent of the observable parts of the specimen given the "
            "current magnification and other settings of the instrument."
        ),
        a_nexus_field=NeXusField(
            name="field_of_view",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    working_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-working-distance-field"
        ],
        dimensionality="[length]",
        description=(
            "Distance which is determined along the optical axis within the "
            "column from (1) the lower end of the final optical element between "
            "the source and the specimen stage; to (2) the point where the beam "
            "is focused. This concept is related to term `Working Distance`_ of "
            "the EMglossary standard. .. _Working Distance: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000050"
        ),
        a_nexus_field=NeXusField(
            name="working_distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    probe = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-probe-field"
        ],
        shape=[2],
        description=(
            "Geometry of the cross-section formed when the primary beam shines "
            "onto the specimen surface. Reported as length of the semiaxes of "
            "the ellipsoidal cross-section with semiaxes values sorted by "
            "decreasing length."
        ),
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    probe_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-probe-current-field"
        ],
        dimensionality="[current]",
        description=(
            "Electrical current which arrives at the specimen. This concept is "
            "related to term `Probe Current`_ of the EMglossary standard. .. "
            "_Probe Current: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000041"
        ),
        a_nexus_field=NeXusField(
            name="probe_current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    dose_management = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-dose-management-field"
        ],
        description=(
            "Specify further details how incipient electron or ion dose was "
            "quantified (using beam_current, probe_current). `Reference "
            "<https://doi.org/10.1017/S1551929522000840>`_ discusses an approach "
            "for (electron) dose monitoring in an electron microscope. The unit "
            "of the nominal dose rate is e-/(angstrom^2*s)."
        ),
        a_nexus_field=NeXusField(
            name="dose_management",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    dose_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-dose-rate-field"
        ],
        dimensionality="1 / [length] ** 2 / [time]",
        description=("Nominal dose rate."),
        a_nexus_field=NeXusField(
            name="dose_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="1/(angstrom^2*s)",
        ),
    )
    rotation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-rotation-field"
        ],
        dimensionality="[angle]",
        description=(
            "In the process of passing through an :ref:`NXelectromagnetic_lens` "
            "electrons are typically accelerated on a helical path about the "
            "optical axis. This causes an image rotation whose strength is "
            "affected by the magnification. Microscopes may be equipped with "
            "compensation methods (implemented in hardware or software) that "
            "reduce but not necessarily eliminate this rotation. See `L. Reimer "
            "<https://doi.org/10.1007/978-3-540-38967-5>`_ for details."
        ),
        a_nexus_field=NeXusField(
            name="rotation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    focal_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-focal-length-field"
        ],
        dimensionality="[length]",
        description=(
            "Distance which lies between the principal plane of the lens and the "
            "focal point along the optical axis. This concept is related to term "
            "`Focal Length`_ of the EMglossary standard. .. _Focal Length: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000029"
        ),
        a_nexus_field=NeXusField(
            name="focal_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    tilt_correction = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-tilt-correction-field"
        ],
        description=(
            "Details about an imaging setting used during acquisition to correct "
            "perspective distortion when imaging a tilted surface or cross "
            "section. This concept is related to term `Tilt Correction`_ of the "
            "EMglossary standard. .. _Tilt Correction: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000047"
        ),
        a_nexus_field=NeXusField(
            name="tilt_correction",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    dynamic_focus_correction = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-dynamic-focus-correction-field"
        ],
        description=(
            "Details about a dynamic focus correction used. This concept is "
            "related to term `Dynamic Focus Correction`_ of the EMglossary "
            "standard. .. _Dynamic Focus Correction: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000016"
        ),
        a_nexus_field=NeXusField(
            name="dynamic_focus_correction",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    dynamic_refocusing = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_optical_system.html#nxem_optical_system-dynamic-refocusing-field"
        ],
        description=(
            "Details about a workflow used to keep the specimen in focus by "
            "automatic means. This concept is related to term `Dynamic "
            "Refocusing`_ of the EMglossary standard. .. _Dynamic Refocusing: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000017"
        ),
        a_nexus_field=NeXusField(
            name="dynamic_refocusing",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
