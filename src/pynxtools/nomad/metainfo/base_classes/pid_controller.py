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
# Run `pynx nomad generate-metainfo --nxdl NXpid_controller` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["PidController"]


class PidController(Component):
    """
    A description of a feedback system in terms of the settings of a
    proportional-integral-derivative (PID) controller.

    Automated control of a physical quantity is often achieved by connecting
    the output of a sensor to an actuator (e.g. using a thermocouple to monitor
    the effect of a heater and influence the power provided to it). The
    physical quantity being operated on is typically referred to as the
    "Process Variable", with the desired value being the "Setpoint" (which may
    vary as a function of time) and the "Error Value" is the time-varying
    function of the difference between the Setpoint value and the concurrent
    measurement of the Process Variable (Error Value = Setpoint - Process
    Variable).

    A PID controller calculates an output value for use as an input signal to
    an actuator via the weighted sum of four terms: * Proportional: the current
    Error Value * Integral: the integral of the Error Value function *
    Derivative: the first derivative of the Error Value function * Feed
    Forward: A model of the physical system (optional)

    The weightings of these terms are given by the corresponding constants: *
    K_p * K_i * K_d * K_ff

    A classic PID controller only implements the P, I and D terms and the
    values of the K_p, K_i and K_d constants are sufficient to fully describe
    the behavior of the feedback system implemented by such a PID controller.
    The inclusion of a Feed Forward term in a feedback system is a modern
    adaptation that aids optimization of the automated control. It is not
    present in all PID controllers, but it is also not uncommon.

    Note that the ``NXpid_controller`` is designed to be a child object of the
    actuator that its output is connected to. The parent object representing
    the actuator is likely to be represented by an ``NXactuator`` or
    ``NXpositioner`` base class, but there is a wide variety of possible
    applications for PID controllers.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXpid_controller",
            category="base",
        ),
    )

    pv_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        description=(
            "The sensor representing the Process Value used in the feedback loop "
            "for the PID. In case multiple sensors were used, this NXsensor "
            "should contain the proper calculated/aggregated value."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="pv_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )

    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-description-field"
        ],
        description=(
            "Description of how the Process Value for the PID controller is "
            "produced by sensor(s) in the setup. For example, a set of sensors "
            "could be averaged over before feeding it back into the loop."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    setpoint = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-setpoint-field"
        ],
        flexible_unit=True,
        description=(
            "The Setpoint(s) used as an input for the PID controller. It can "
            "also be a link to an ``NXsensor.value`` field."
        ),
        a_nexus_field=NeXusField(
            name="setpoint",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    K_p = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-k-p-field"
        ],
        description=(
            "Proportional gain constant. This constant determines how strongly "
            "the output value directly follows the current Error Value. When "
            "this constant dominates, the output value is linearly proportional "
            "to the Error Value."
        ),
        a_nexus_field=NeXusField(
            name="K_p",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    K_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-k-i-field"
        ],
        description=(
            "Integral gain constant. This constant determines how strongly the "
            "output value should react to an accumulated offset in the Error "
            "Value that should have been corrected previously. since the "
            "integral term is proportional to both the magnitude and persistence "
            "of the Error Value over time."
        ),
        a_nexus_field=NeXusField(
            name="K_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    K_d = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-k-d-field"
        ],
        description=(
            "Derivative gain constant. This constant determines how much the "
            "feedback system should anticipate the future value of the Error "
            "Value function through adjustment of the output value that is "
            "proportional to the rate of change (i.e. derivative) of the Error "
            "Value. This term is important for damping oscillations in the "
            "feedback system."
        ),
        a_nexus_field=NeXusField(
            name="K_d",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    K_ff = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-k-ff-field"
        ],
        description=(
            "Feed Forward gain constant. This constant determines how much the "
            "feedback system should rely on a calculated output value to achieve "
            "the desired Process Variable value. A Feed Forward system uses a "
            "model of the physical system to calculate an appropriate output "
            "value to achieve a desired Setpoint value. A description of this "
            "model should be provided in the ``feed_forward_model`` field."
        ),
        a_nexus_field=NeXusField(
            name="K_ff",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    feed_forward_model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-feed-forward-model-field"
        ],
        description=(
            "A description of the model used for the Feed Forward part of the "
            "feedback system. Note that such models typically involve the "
            "Setpoint value, but not the Error Value. The simplest model is "
            "simply proportional to the Setpoint value. For example, the "
            "position (Process Variable) of a sample is measured by a a linear "
            "optical encoder (sensor) and manipulated by a piezoelectric "
            "scanning stage (actuator). The corresponding Feed Forward model "
            "could be that the output value (voltage applied to the piezo) is "
            "proportional to the Setpoint value (measured position of the "
            "sample). A complex model could involve any number of input "
            "variables, mathematical functions, and coefficients in order to "
            "describe the physical system relevant to the PID controller."
        ),
        a_nexus_field=NeXusField(
            name="feed_forward_model",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    control_action = Quantity(
        type=MEnum(["direct", "reverse"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXpid_controller.html#nxpid_controller-control-action-field"
        ],
        description=(
            "The Error Value of PID feedback system is normally constructed in "
            "terms of the correction needed to bring the Process Variable "
            'towards a match with the Setpoint. This "direct" control action '
            "means that a measurement of the Process Variable that is lower than "
            "the Setpoint results in a positive Error Value and a generally "
            "positive control output that tells the actuator to push the value "
            "of the Process Variable upwards. In some implementations, the "
            "actuator will respond to a more positive control output by pushing "
            "the Process Variable towards lower values (e.g. a Peltier cooler) "
            "and so the output of the feedback system must be reversed to match "
            "the behavior of the physical system. A feedback system may also be "
            "implemented with reverse action in order to ensure that failures "
            "(e.g. disconnected sensor output or actuator input) result in a "
            "safe state (e.g. a valve should be left open to release pressure)."
        ),
        a_nexus_field=NeXusField(
            name="control_action",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["direct", "reverse"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
