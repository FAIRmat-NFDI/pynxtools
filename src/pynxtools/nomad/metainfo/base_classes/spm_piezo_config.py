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
# Run `pynx nomad generate-metainfo --nxdl NXspm_piezo_config` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.spm_piezoelectric_material import (
    SpmPiezoelectricMaterial,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmPiezoConfig"]


class SpmPiezoConfig(Object):
    """
    A base class describing piezo actuator settings for scanning probe
    microscopy.

    Piezoelectric actuators work utilizing the inverse-piezoelectric effect,
    when a voltage is applied on the material and it deforms proportional to
    the applied voltage. Description below shows calibration coefficients and
    other configuration parameters of open loop piezo actuators (that is
    actuators without capacitive sensor feedback systems).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_piezo_config",
            category="base",
        ),
    )

    piezo_material = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_config.SpmPiezoConfigPiezoMaterial",
        repeats=False,
        description=(
            "The material description and properties of the piezoelectric "
            "scanner materials."
        ),
    )
    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_config.SpmPiezoConfigCalibration",
        repeats=False,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class SpmPiezoConfigPiezoMaterial(SpmPiezoelectricMaterial):
    """
    The material description and properties of the piezoelectric scanner
    materials.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-piezo-material-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_piezoelectric_material",
            name="piezo_material",
            name_type="specified",
            optionality="optional",
        ),
    )

    curvature_radiusN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-piezo-material-curvature-radiusn-field"
        ],
        variable=True,
        dimensionality="[length]",
        unit="m",
        description=(
            "The N (substring) denotes X or Y. There are 2 parameters in X and Y "
            "directions. It can be set approximately to the length of the piezo "
            "tube along X and Y axis."
        ),
        a_nexus_field=NeXusField(
            name="curvature_radiusN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmPiezoConfigCalibration(Calibration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibration_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_piezo_config.SpmPiezoConfigCalibrationCalibrationParameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="calibration_parameters",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibration_type = Quantity(
        type=MEnum(["active", "passive"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-calibration-type-field"
        ],
        description=(
            "The name of the calibration type, sometimes it is called `active "
            "calibration`."
        ),
        a_nexus_field=NeXusField(
            name="calibration_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["active", "passive"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    calibration_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-calibration-name-field"
        ],
        description=(
            "A specific name of the calibration (e.g. active type with name 'LHe')."
        ),
        a_nexus_field=NeXusField(
            name="calibration_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    calibration_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-calibration-date-field"
        ],
        description=("The date of the calibration."),
        a_nexus_field=NeXusField(
            name="calibration_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    calibratedAXIS = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-calibratedaxis-field"
        ],
        variable=True,
        description=(
            "The AXIS (substring) denotes X, Y or Z, e.g., calibrated_x. There "
            "are three directions X, Y, and Z for calibration, along with three "
            "available parameters each: Calibration (m/V), Range (m), and HV "
            "gain. Only two of these parameters are required to define the "
            "calibration. Consequently, when any value is changed, one of the "
            "other values will be automatically updated."
        ),
        a_nexus_field=NeXusField(
            name="calibratedAXIS",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    hv_gainN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-hv-gainn-field"
        ],
        variable=True,
        description=(
            "The N (substring) denotes X or Y or Z, e.g., hv_gain_x. In some "
            "systems, there is an HV gain readout feature. For these systems, "
            "the HV gain should be automatically adjusted whenever the gain is "
            "changed at the high voltage amplifier."
        ),
        a_nexus_field=NeXusField(
            name="hv_gainN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    rangeN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-rangen-field"
        ],
        variable=True,
        dimensionality="[length]",
        unit="m",
        description=(
            "The N (substring) denotes X or Y or Z, e.g., range_x. There are 3 "
            "parameters in X, Y and Z directions. The range is the maximum "
            "distance the piezo can move."
        ),
        a_nexus_field=NeXusField(
            name="rangeN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    tiltN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-tiltn-field"
        ],
        variable=True,
        dimensionality="[angle]",
        unit="radian",
        description=(
            "The N (substring) denotes X and Y directions (e.g., tilt_x), and "
            "for both directions tilt needs to be adjusted according to the "
            "actual surface."
        ),
        a_nexus_field=NeXusField(
            name="tiltN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    drift_correction_status = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-drift-correction-status-field"
        ],
        description=(
            "The drift correction status (true / false) in calibration step of piezo."
        ),
        a_nexus_field=NeXusField(
            name="drift_correction_status",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    driftN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-driftn-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "The N (substring) denotes X, Y and Z directions (e.g., drift_x). "
            "Define the drift speed [m/s] for all three axes. When the "
            "compensation is on, the piezo will start to move at that speed."
        ),
        a_nexus_field=NeXusField(
            name="driftN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpmPiezoConfigCalibrationCalibrationParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-calibration-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="calibration_parameters",
            name_type="specified",
            optionality="optional",
        ),
    )

    coefficientN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-calibration-parameters-coefficientn-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "The calibration coefficient is the ratio of the actual distance "
            "moved by the piezo due to the voltage or external force applied to "
            "the piezo. It is also called first-order correction. The N "
            "(substring) denotes X and Y directions (e.g., coefficient_x)."
        ),
        a_nexus_field=NeXusField(
            name="coefficientN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    second_order_correctionN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezo_config.html#nxspm_piezo_config-calibration-calibration-parameters-second-order-correctionn-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "The N (substring) denotes X and Y directions (e.g., "
            "second_order_correction_x). If you know them, you can enter the 2nd "
            "order piezo characteristics to compensate the error for that axis. "
            "The following equation shows the interpretation of the 2nd order "
            "correction parameters, For the X-piezo: :math:`U_x = \\frac{1}{c_x} "
            "\\cdot X + c_{xx} \\cdot X^2` with units: :math:`[V] = "
            "\\frac{[V]}{[m]} \\cdot [m] + \\frac{[V]}{[m^2]} \\cdot [m^2]` "
            "where cx is the calibration of the piezo X and cxx is the 2nd order "
            "correction. The unit for the second-order correction is "
            "(:math:`\\frac{V}{m^2}`)."
        ),
        a_nexus_field=NeXusField(
            name="second_order_correctionN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
