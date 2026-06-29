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
# Run `pynx nomad generate-metainfo --nxdl NXspm_positioner` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.actuator import Actuator
from pynxtools.nomad.metainfo.base_classes.pid_controller import PidController
from pynxtools.nomad.metainfo.base_classes.positioner import Positioner

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmPositioner"]


class SpmPositioner(Positioner):
    """
    An extension of positioner, used to maintain a measurement signal through a
    feedback loop, specialized for scanning probe microscopy applications.

    The component positions the spm head or cantilever tip on the surface of
    the sample thus maps 2D scan of the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_positioner",
            category="base",
        ),
    )

    z_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_positioner.SpmPositionerZController",
        repeats=False,
        description=(
            "This controller's task is to continuously adjust the Z position of "
            "tip (e.g., in topography scan in STM/STS experiment) in order to "
            "keep the selected control signal as close as possible to the Set "
            "Point. Different control signals lead to different controller's "
            "behavior. The second PID feedback loop intends to position the tip "
            "in the Z direction. p_gain (proportional gain) from z_controller "
            "refers to K_p value from PID controller. i_gain (integral gain) "
            "from z_controller refers to K_i value from PID controller. setpoint "
            "from z_controller refers to setpoint from PID controller. Usually, "
            "the same controller, (z_controller) will be used for positioning "
            "the tip in three dimensional space. In this case, the controller "
            "coefficients (proportional, integral, differential) and other "
            "characteristic constants will be the same. Otherwise, for separate "
            "controllers positioning the tip in 3D space use the :ref:`feedback "
            "</NXspm_positioner/actuator/feedback-group>` controller in "
            "actuator."
        ),
    )
    actuator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_positioner.SpmPositionerActuator",
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


class SpmPositionerZController(PidController):
    """
    This controller's task is to continuously adjust the Z position of tip
    (e.g., in topography scan in STM/STS experiment) in order to keep the
    selected control signal as close as possible to the Set Point. Different
    control signals lead to different controller's behavior.

    The second PID feedback loop intends to position the tip in the Z
    direction.

    p_gain (proportional gain) from z_controller refers to K_p value from PID
    controller. i_gain (integral gain) from z_controller refers to K_i value
    from PID controller. setpoint from z_controller refers to setpoint from PID
    controller.

    Usually, the same controller, (z_controller) will be used for positioning
    the tip in three dimensional space. In this case, the controller
    coefficients (proportional, integral, differential) and other
    characteristic constants will be the same. Otherwise, for separate
    controllers positioning the tip in 3D space use the :ref:`feedback
    </NXspm_positioner/actuator/feedback-group>` controller in actuator.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name="z_controller",
            name_type="specified",
            optionality="optional",
        ),
    )

    D_t = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-d-t-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "The derivative time constant of the derivative part of the PID "
            "controller. Proportional Derivative constant K_d can be expressed "
            "as :math:`K_d = K_p D_t`."
        ),
        a_nexus_field=NeXusField(
            name="D_t",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    I_t = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-i-t-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "The integral time constant of the integral part of the PID "
            "controller. Proportional Integral constant K_i can be expressed as "
            ":math:`K_i = \\frac{K_p}{I_t}`."
        ),
        a_nexus_field=NeXusField(
            name="I_t",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "To indicate the relative tip position z between tip and sample. The "
            "tip position can also be varied when the z_controller is not "
            "running."
        ),
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    set_point = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-set-point-field"
        ],
        flexible_unit=True,
        description=(
            "The set point for the z-controller to be fixed and the target value "
            "could be height or current."
        ),
        a_nexus_field=NeXusField(
            name="set_point",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    feedback_on = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-feedback-on-field"
        ],
        description=(
            "The status of the controller PID feedback system in z-axis is ON / "
            "OFF. E.g., for constant height mode, the z-controller feedback "
            "system is off."
        ),
        a_nexus_field=NeXusField(
            name="feedback_on",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    tip_lift = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-tip-lift-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("If the tip is lifted from the stable point."),
        a_nexus_field=NeXusField(
            name="tip_lift",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    switch_off_delay = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-switch-off-delay-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("The switch-off delay of the controller from its stable point."),
        a_nexus_field=NeXusField(
            name="switch_off_delay",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    z_offset_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-z-offset-value-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Offset added to the initial averaged tip position on Z-axis before "
            "starting scan."
        ),
        a_nexus_field=NeXusField(
            name="z_offset_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    z_average_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-z-average-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "The averaging time for stabilizing the Z position. Usually, the "
            "signal for z-position contains noise, to reduce the noise impacts, "
            "z-position is being averaged over this time window."
        ),
        a_nexus_field=NeXusField(
            name="z_average_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    z_controller_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-z-controller-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Time taken by the Z controller to switch mode e.g., feedback off "
            "from on and vice versa. In this time window, controller fixed its "
            "position if feedback changed to off mode."
        ),
        a_nexus_field=NeXusField(
            name="z_controller_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    z_controller_hold = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-z-controller-hold-field"
        ],
        description=(
            "Controller feedback system status: OFF / ON. The "
            "`z_controller_hold-field` is True, refers feedback system off "
            "(mostly case in STS bias spectra) and False refers feedback system "
            "on (mostly case in STM constant current spectra)."
        ),
        a_nexus_field=NeXusField(
            name="z_controller_hold",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    final_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-final-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The final Z position of the tip after the scan. This parameter is "
            "used to indicate any unexpected displacement of the tip."
        ),
        a_nexus_field=NeXusField(
            name="final_z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    controller_label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-z-controller-controller-label-field"
        ],
        description=(
            "Controller label. This label which will be displayed at places "
            "where you can select a channel or controller."
        ),
        a_nexus_field=NeXusField(
            name="controller_label",
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


class SpmPositionerActuator(Actuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_positioner.html#nxspm_positioner-actuator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuator",
            name_type="specified",
            optionality="optional",
        ),
    )

    feedback = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pid_controller.PidController",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name="feedback",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
