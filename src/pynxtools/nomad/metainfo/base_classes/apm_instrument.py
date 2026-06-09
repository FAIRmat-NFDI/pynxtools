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
# Run `pynx nomad generate-metainfo --nxdl NXapm_instrument` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmInstrument"]


class ApmInstrument(Instrument):
    """
    Base class for instrument-related details of a real or simulated atom probe
    tomograph or field-ion microscope.

    For collecting data and experiments which are simulations of an atom probe
    microscope or a session with such instrument use the :ref:`NXapm`
    application definition and the :ref:`NXapm_event_data` groups it provides.

    This base class implements the concept of :ref:`NXapm` whereby (meta)data
    are distinguished whether these typically change during a session,
    so-called dynamic, or not, so-called static metadata. This design allows to
    store e.g. hardware related concepts only once instead of demanding that
    each image or spectrum from the session needs to be stored also with the
    static metadata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_instrument",
            category="base",
            symbols={
                "p": "Number of pulses collected in between start_time and end_time\n                inside a parent instance of :ref:`NXapm_event_data`."
            },
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )
    reflectron = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrumentReflectron",
        repeats=False,
        description=(
            "Device which reduces ToF differences of ions in ToF experiments. "
            "For atom probe the reflectron can be considered an energy "
            "compensation device. Such a device can be realized technically e.g. "
            "with a Poschenrieder lens. Consult the following U.S. patents for "
            "further details: * 3863068 and 6740872 for the reflectron * 8134119 "
            "for the curved reflectron"
        ),
    )
    decelerate_electrode = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
        repeats=False,
        description=("A counter electrode of the LEAP 6000 series atom probes."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="decelerate_electrode",
            name_type="specified",
            optionality="optional",
        ),
    )
    local_electrode = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrumentLocalElectrode",
        repeats=False,
        description=(
            "A local electrode guiding the ion flight path. Also called counter "
            "or extraction electrode."
        ),
    )
    ion_detector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrumentIonDetector",
        repeats=False,
        description=(
            "Detector for taking raw time-of-flight and ion/hit impact positions data."
        ),
    )
    pulser = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrumentPulser",
        repeats=False,
        description=(
            "Laser- and/or voltage-pulsing device to trigger ion removal. When "
            "the base class NXapm_instrument is used in the NXapm application "
            "definition, the values for the following fields: * pulse_frequency "
            "* pulse_fraction * pulse_voltage * pulse_number * standing_voltage "
            "* pulse_energy * incidence_vector * pinhole_position * "
            "spot_position should be recorded in the order of, and assumed "
            "associated, with the pulse_id in an instance of "
            ":ref:`NXapm_event_data`."
        ),
    )
    stage = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.Manipulator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stage",
            name_type="specified",
            optionality="optional",
        ),
    )
    analysis_chamber = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrumentAnalysisChamber",
        repeats=False,
    )
    buffer_chamber = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="buffer_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )
    load_lock_chamber = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="load_lock_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )
    getter_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pump.Pump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="getter_pump",
            name_type="specified",
            optionality="optional",
        ),
    )
    roughening_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pump.Pump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="roughening_pump",
            name_type="specified",
            optionality="optional",
        ),
    )
    turbomolecular_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pump.Pump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="turbomolecular_pump",
            name_type="specified",
            optionality="optional",
        ),
    )
    control = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrumentControl",
        repeats=False,
        description=(
            "Relevant quantities during a measurement with a LEAP system as were "
            "suggested by `T. Blum et al. "
            "<https://doi.org/10.1002/9781119227250.ch18>`_."
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-type-field"
        ],
        description=("Which type of instrument."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "Inspico",
                "3DAP",
                "LAWATAP",
                "LEAP 3000 Si",
                "LEAP 3000X Si",
                "LEAP 3000 HR",
                "LEAP 3000X HR",
                "LEAP 4000 Si",
                "LEAP 4000X Si",
                "LEAP 4000 HR",
                "LEAP 4000X HR",
                "LEAP 5000 XS",
                "LEAP 5000 XR",
                "LEAP 5000 R",
                "EIKOS",
                "EIKOS-UV",
                "LEAP 6000 XR",
                "LEAP INVIZO",
                "Photonic AP",
                "TeraSAT",
                "TAPHR",
                "Modular AP",
                "Titanium APT",
                "Extreme UV APT",
            ],
            open_enum=True,
        ),
    )
    location = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-location-field"
        ],
        description=(
            "Location of the lab or place where the instrument is installed. "
            "Using GEOREF is preferred."
        ),
        a_nexus_field=NeXusField(
            name="location",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    flight_path = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-flight-path-field"
        ],
        dimensionality="[length]",
        description=(
            "Nominal flight path The value can be extracted from the "
            "CAnalysis.CSpatial.fFlightPath field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="flight_path",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-comment-field"
        ],
        description=("Free-text field for additional comments."),
        a_nexus_field=NeXusField(
            name="comment",
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


class ApmInstrumentReflectron(Component):
    """
    Device which reduces ToF differences of ions in ToF experiments.

    For atom probe the reflectron can be considered an energy compensation
    device. Such a device can be realized technically e.g. with a Poschenrieder
    lens.

    Consult the following U.S. patents for further details:

    * 3863068 and 6740872 for the reflectron * 8134119 for the curved
    reflectron
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-reflectron-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="reflectron",
            name_type="specified",
            optionality="optional",
        ),
    )

    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-reflectron-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "The maximum voltage applied to the reflectron, relative to system ground."
        ),
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmInstrumentLocalElectrode(Component):
    """
    A local electrode guiding the ion flight path. Also called counter or
    extraction electrode.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-local-electrode-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="local_electrode",
            name_type="specified",
            optionality="optional",
        ),
    )

    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-local-electrode-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("Acceleration voltage"),
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    aperture_type = Quantity(
        type=MEnum(["n/a", "conical", "feedthrough", "custom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-local-electrode-aperture-type-field"
        ],
        description=(
            "The type of aperture used when the local_electrode has an aperture "
            "or acts as an aperture in addition to acting as an extraction "
            "electrode. The local electrode is a component which combines "
            "functionalities of :ref:`NXelectromagnetic_lens`, "
            ':ref:`NXaperture`, if not even :ref:`NXdeflector`: * "n/a", use '
            'when no aperture is present in the experiment * "conical", '
            'conical aperture with a circular hole * "feedthrough", an '
            "aperture where the specimen protrudes through a circular hole * "
            '"custom", a user modified aperture, which is otherwise '
            "non-standard"
        ),
        a_nexus_field=NeXusField(
            name="aperture_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["n/a", "conical", "feedthrough", "custom"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmInstrumentIonDetector(Detector):
    """
    Detector for taking raw time-of-flight and ion/hit impact positions data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-ion-detector-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="ion_detector",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal_amplitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-ion-detector-signal-amplitude-field"
        ],
        dimensionality="[current]",
        shape=["*"],
        description=(
            "Amplitude of the signal detected on the multi-channel plate (MCP). "
            "This field should be used for storing the signal amplitude quantity "
            "within ATO files when the detector was an MCP. The ATO file format "
            "is used primarily by the atom probe group of the GPM in Rouen, "
            "France."
        ),
        a_nexus_field=NeXusField(
            name="signal_amplitude",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    mcp_efficiency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-ion-detector-mcp-efficiency-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The value can be extracted from the CRunHeader.fMcpEfficiency field "
            "of a CamecaRoot RHIT file."
        ),
        a_nexus_field=NeXusField(
            name="mcp_efficiency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    mesh_efficiency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-ion-detector-mesh-efficiency-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The value can be extracted from the CRunHeader.fMeshEfficiency "
            "field of a CamecaRoot RHIT file."
        ),
        a_nexus_field=NeXusField(
            name="mesh_efficiency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmInstrumentPulser(Component):
    """
    Laser- and/or voltage-pulsing device to trigger ion removal.

    When the base class NXapm_instrument is used in the NXapm application
    definition, the values for the following fields:

    * pulse_frequency * pulse_fraction * pulse_voltage * pulse_number *
    standing_voltage * pulse_energy * incidence_vector * pinhole_position *
    spot_position

    should be recorded in the order of, and assumed associated, with the
    pulse_id in an instance of :ref:`NXapm_event_data`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-pulser-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="pulser",
            name_type="specified",
            optionality="optional",
        ),
    )

    sourceID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.source.Source",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="sourceID",
            name_type="partial",
            optionality="optional",
        ),
    )

    pulse_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-pulser-pulse-mode-field"
        ],
        description=("Detail whereby ion extraction is triggered methodologically."),
        a_nexus_field=NeXusField(
            name="pulse_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["laser", "voltage", "laser_and_voltage"],
            open_enum=True,
        ),
    )
    pulse_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-pulser-pulse-frequency-field"
        ],
        dimensionality="1 / [time]",
        description=("Frequency with which the pulser fire(s)."),
        a_nexus_field=NeXusField(
            name="pulse_frequency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
    )
    pulse_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-pulser-pulse-fraction-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Fraction of the pulse_voltage that is applied in addition to the "
            "standing_voltage at peak voltage of a pulse. If a standing voltage "
            "is applied, this gives nominal pulse fraction (as a function of "
            "standing voltage). Otherwise, this field should not be present."
        ),
        a_nexus_field=NeXusField(
            name="pulse_fraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    pulse_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-pulser-pulse-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Pulsed voltage, in laser pulsing mode this field can be omitted."
        ),
        a_nexus_field=NeXusField(
            name="pulse_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    pulse_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-pulser-pulse-number-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Absolute number of pulses starting from the beginning of the experiment."
        ),
        a_nexus_field=NeXusField(
            name="pulse_number",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    standing_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-pulser-standing-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Direct current voltage between the specimen and the (local "
            "electrode) in the case of local electrode atom probe (LEAP) "
            "instrument. Otherwise, the standing voltage applied to the sample, "
            "relative to system ground."
        ),
        a_nexus_field=NeXusField(
            name="standing_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmInstrumentAnalysisChamber(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-analysis-chamber-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="analysis_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )

    pressure_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="pressure_sensor",
            name_type="specified",
            optionality="optional",
        ),
    )

    flight_path = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-analysis-chamber-flight-path-field"
        ],
        dimensionality="[length]",
        description=(
            "The space inside the atom probe along which ions pass nominally "
            "when they leave the specimen and travel to the detector."
        ),
        a_nexus_field=NeXusField(
            name="flight_path",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmInstrumentControl(Parameters):
    """
    Relevant quantities during a measurement with a LEAP system as were
    suggested by `T. Blum et al.
    <https://doi.org/10.1002/9781119227250.ch18>`_.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-control-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="control",
            name_type="specified",
            optionality="optional",
        ),
    )

    evaporation_control = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-control-evaporation-control-field"
        ],
        description=(
            "Parameter that defines the rules and control loops whereby the "
            "pulser and other components of the instrument are controlled during "
            "evaporation."
        ),
        a_nexus_field=NeXusField(
            name="evaporation_control",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    target_detection_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_instrument.html#nxapm_instrument-control-target-detection-rate-field"
        ],
        description=(
            "Parameter that assure maintenance of a significant yet not too high "
            "ion influx on the detector to avoid detection losses."
        ),
        a_nexus_field=NeXusField(
            name="target_detection_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
