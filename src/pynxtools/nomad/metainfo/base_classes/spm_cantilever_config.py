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
# Run `pynx nomad generate-metainfo --nxdl NXspm_cantilever_config` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmCantileverConfig"]


class SpmCantileverConfig(Object):
    """
    This file defines the NXspm_cantilever_config base class, which contains
    configuration information about the cantilever used in the AFM (atomic
    force microscopy) experiments.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_cantilever_config",
            category="base",
        ),
    )

    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_cantilever_config.SpmCantileverConfigCalibration",
        repeats=True,
        variable=True,
        description=("The calibration information of the cantilever."),
    )

    cantilever_coating = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-cantilever-coating-field"
        ],
        description=("The coating material of the cantilever."),
        a_nexus_field=NeXusField(
            name="cantilever_coating",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    curvature_radiusN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-curvature-radiusn-field"
        ],
        variable=True,
        description=(
            "The radius of curvature of the cantilever tip. The (substring) N "
            "denotes X or Y."
        ),
        a_nexus_field=NeXusField(
            name="curvature_radiusN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    cantilever_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-cantilever-type-field"
        ],
        description=(
            "The shape of the cantilever as a general text, such as A-shape, "
            "beam, or arrow."
        ),
        a_nexus_field=NeXusField(
            name="cantilever_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    cantilever_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-cantilever-length-field"
        ],
        dimensionality="[length]",
        description=(
            "Nominal length between base and end of the cantilever in micrometers."
        ),
        a_nexus_field=NeXusField(
            name="cantilever_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    cantilever_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-cantilever-width-field"
        ],
        dimensionality="[length]",
        description=("Nominal width of the cantilever in microns."),
        a_nexus_field=NeXusField(
            name="cantilever_width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    cantilever_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-cantilever-thickness-field"
        ],
        dimensionality="[length]",
        description=("Nominal thickness of the cantilever in microns."),
        a_nexus_field=NeXusField(
            name="cantilever_thickness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    resonance_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-resonance-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=(
            "Nominal free resonance frequency of the cantilever in air i.e., out "
            "of interaction force."
        ),
        a_nexus_field=NeXusField(
            name="resonance_frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    amplitude_excitation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-amplitude-excitation-field"
        ],
        description=(
            "Either the drive amplitude in mv for the driving cantilever or the "
            "free-oscillation amplitude which is the resulted movement amplitude "
            "without interaction to the surface."
        ),
        a_nexus_field=NeXusField(
            name="amplitude_excitation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    fermi_level = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-fermi-level-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("The Fermi level of the cantilever material."),
        a_nexus_field=NeXusField(
            name="fermi_level",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    resonance_amplitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-resonance-amplitude-field"
        ],
        dimensionality="[length]",
        description=(
            "Nominal free resonance amplitude of the cantilever in air, in nm "
            "i.e., out of interaction force."
        ),
        a_nexus_field=NeXusField(
            name="resonance_amplitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    spring_constant = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-spring-constant-field"
        ],
        description=("The spring constant coefficient of the cantilever."),
        a_nexus_field=NeXusField(
            name="spring_constant",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
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


class SpmCantileverConfigCalibration(Calibration):
    """
    The calibration information of the cantilever.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-calibration-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    sensitivity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever_config.html#nxspm_cantilever_config-calibration-sensitivity-field"
        ],
        description=(
            "A force applied to the cantilever tip will cause a change in "
            "cantilever's oscillation amplitude (in dynamic mode) or deflection "
            "of the cantilever. The sensitivity of the cantilever is calculated "
            "as the ratio of this change to the force causing it."
        ),
        a_nexus_field=NeXusField(
            name="sensitivity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
