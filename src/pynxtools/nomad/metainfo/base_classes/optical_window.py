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
# Run `pynx nomad generate-metainfo --nxdl NXoptical_window` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.aperture import Aperture
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["OpticalWindow"]


class OpticalWindow(Aperture):
    """
    A window of a cryostat, heater, vacuum chamber or a simple glass slide.

    This describes cryostat windows and other possible influences for
    ellipsometry measurements.

    For environmental measurements, the environment (liquid, vapor etc.) is
    enclosed in a cell, which has windows both in the direction of the source
    (entry window) and the detector (exit window) (looking from the sample).

    The windows also add a phase shift to the light altering the measured
    signal. This shift has to be corrected based on measuring a known sample
    (reference sample) or the actual sample of interest in the environmental
    cell. State if a window correction has been performed in
    'window_effects_corrected'. Reference measurements should be considered as
    a separate experiment (with a separate NeXus file), and the reference data
    shall be :ref:`linked <Design-Links>` in ``reference_data_link``.

    The window is considered to be a part of the sample stage but also beam
    path. Hence, its position within the beam path should be defined by the
    'depends_on' field.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXoptical_window",
            category="base",
        ),
    )

    window_correction = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_window.OpticalWindowWindowCorrection",
        repeats=False,
        description=(
            "Group to describe any window correction - if none performed, then "
            "omit this"
        ),
    )

    window_effects_corrected = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-window-effects-corrected-field"
        ],
        description=(
            "Was a window correction performed? If so, describe the window "
            "correction procedure in ``window_correction/procedure``."
        ),
        a_nexus_field=NeXusField(
            name="window_effects_corrected",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    window_effects_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-window-effects-type-field"
        ],
        description=("Type of effects due to this window on the measurement."),
        a_nexus_field=NeXusField(
            name="window_effects_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "interference effects",
                "light absorption",
                "light scattering",
                "other",
            ],
            open_enum=True,
        ),
    )
    material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-material-field"
        ],
        description=("The material of the window."),
        a_nexus_field=NeXusField(
            name="material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "quartz",
                "diamond",
                "calcium fluoride",
                "zinc selenide",
                "thallium bromoiodide",
                "alkali halide compound",
                "Mylar",
                "other",
            ],
            open_enum=True,
        ),
    )
    material_other = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-material-other-field"
        ],
        description=("If you specified 'other' as material, describe here what it is."),
        a_nexus_field=NeXusField(
            name="material_other",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-thickness-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Thickness of the window."),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    orientation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-orientation-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Angle of the window normal (outer) vs. the substrate normal "
            "(similar to the angle of incidence)."
        ),
        a_nexus_field=NeXusField(
            name="orientation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
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


class OpticalWindowWindowCorrection(Process):
    """
    Group to describe any window correction - if none performed, then omit this
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-window-correction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="window_correction",
            name_type="specified",
            optionality="optional",
        ),
    )

    procedure = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-window-correction-procedure-field"
        ],
        description=(
            "Describe when (before or after the main measurement + time stamp in "
            "'date') and how the window effects have been corrected, i.e. either "
            "mathematically or by performing a reference measurement. In the "
            "latter case, provide the link to to the reference data in "
            "``reference_data_file``."
        ),
        a_nexus_field=NeXusField(
            name="procedure",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    reference_data_link = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_window.html#nxoptical_window-window-correction-reference-data-link-field"
        ],
        description=(
            ":ref:`External link <Design-Links>` to the data field in the NeXus "
            "file which describes the reference data if a reference measurement "
            "for window correction was performed. Ideally, the reference "
            "measurement was performed on the same sample, using the same "
            "conditions as for the actual measurement, with and, if possible, "
            "without windows. It should have been conducted as close in time to "
            "the actual measurement as possible. Ideally, the link uses the "
            "relative path with respect to the actual NeXus file."
        ),
        a_nexus_field=NeXusField(
            name="reference_data_link",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
