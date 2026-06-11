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
# Run `pynx nomad generate-metainfo --nxdl NXoptical_spectroscopy` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.actuator import Actuator
from pynxtools.nomad.metainfo.base_classes.beam import Beam
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.environment import Environment
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.manipulator import Manipulator
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.optical_lens import OpticalLens
from pynxtools.nomad.metainfo.base_classes.pid_controller import PidController
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.resolution import Resolution
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.transformations import Transformations

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["OpticalSpectroscopy"]


class OpticalSpectroscopy(Entry):
    """
    A general application definition of optical spectroscopy elements, which
    may be used as a template to derive specialized optical spectroscopy
    experiments.

    Possible specializations are ellipsometry, Raman spectroscopy,
    photoluminescence, reflectivity/transmission spectroscopy.

    A general optical experiment consists of (i) a light/photon source, (ii) a
    sample, (iii) a detector.

    For any free-text descriptions, it is recommended to use English, as this
    ensures the most FAIR (Findable, Accessible, Interoperable, and Reusable)
    representation of the information.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXoptical_spectroscopy",
            category="application",
            symbols={
                "N_spectrum": "Length of the spectrum array (e.g. wavelength or energy) of the measured\n                data.",
                "N_measurements": "Number of measurements (1st dimension of measured data arrays). This is\n                equal to the number of parameters scanned. For example, if the experiment\n                was performed at three different temperatures and two different pressures\n                N_measurements = 2*3 = 6.",
            },
        ),
    )

    beam_ref_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyBeamRefFrame",
        repeats=False,
    )
    sample_normal_ref_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopySampleNormalRefFrame",
        repeats=False,
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=True,
        variable=True,
        description=(
            "Contact information and eventually details of at persons who "
            "performed the measurements. This can be for example the principal "
            "investigator or student. Examples are: name, affiliation, address, "
            "telephone number, email, role as well as identifiers such as orcid "
            "or similar. It is recommended to add multiple users if relevant. "
            "Due to data privacy concerns, there is no minimum requirement. If "
            "no user with specific name is allowed to be given, it is required "
            "to assign at least an affiliation"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrument",
        repeats=True,
        variable=True,
        description=(
            "Devices or elements of the optical spectroscopy setup described "
            "with its properties and general information. This includes for "
            "example: - The beam device's or instrument's model, company, serial "
            "number, construction year, etc. - Used software or code - "
            "Experiment descriptive parameters as reference frames, resolution, "
            "calibration - Photon beams with their respective properties such as "
            "angles and polarization - Various optical beam path devices, which "
            "interact, manipulate or measure optical beams - Characteristics of "
            'the medium surrounding the sample - "Beam devices" for a beam '
            "path description - Stages(NXmanipulator) - Sensors and actuators to "
            "control or measure sample or beam properties"
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopySample",
        repeats=True,
        variable=True,
        description=(
            "Properties of the sample, such as sample type, layer structure, "
            "chemical formula, atom types, its history etc. Information about "
            "the sample stage and sample environment should be described in "
            "ENTRY/INSTRUMENT/sample_stage."
        ),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyData",
        repeats=True,
        variable=True,
        description=(
            "Here generic types of data may be saved. This may refer to data "
            "derived from single or multiple raw measurements (i.e. several "
            "intensities are evaluated for different parameters: ellipsometry -> "
            "psi and delta) - i.e. non-raw data. As well plottable data may be "
            "stored/linked here, which provides the most suitable representation "
            "of the data (for the respective community). You may provide "
            "multiple instances of NXdata"
        ),
    )
    measurement_data_calibration_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyMeasurement_data_calibration_TYPE",
        repeats=True,
        variable=True,
    )
    derived_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyDerivedParameters",
        repeats=False,
        description=("Parameters that are derived from the measured data."),
    )

    definition = Quantity(
        type=MEnum(["NXoptical_spectroscopy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-definition-field"
        ],
        description=(
            "An application definition describing a general optical experiment."
        ),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXoptical_spectroscopy"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-definition-version-attribute"
        ],
        description=(
            "Version number to identify which definition of this application "
            "definition was used for this entry/data."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-definition-url-attribute"
        ],
        description=(
            "URL where to find further material (documentation, examples) "
            "relevant to the application definition."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-start-time-field"
        ],
        description=(
            "Datetime of the start of the measurement. Should be a ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise, the local time zone is assumed per ISO8601. It is "
            "required to enter at least one of both measurement times, either "
            '"start_time" or "end_time".'
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-end-time-field"
        ],
        description=(
            "Datetime of the end of the measurement. Should be a ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise the local time zone is assumed per ISO8601. It is "
            "required to enter at least one of both measurement times, either "
            '"start_time" or "end_time".'
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier_experiment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-identifier-experiment-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier_experiment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-experiment-description-field"
        ],
        description=(
            "An optional free-text description of the experiment. Users are "
            "strongly advised to parameterize the description of their "
            "experiment by using respective groups and fields and base classes "
            "instead of writing prose into this field. The reason is that such a "
            "free-text field is difficult to machine-interpret. The motivation "
            "behind keeping this field for now is to learn how far the current "
            "base classes need extension based on user feedback."
        ),
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-experiment-type-field"
        ],
        description=(
            "Specify the type of the optical experiment. Use another term if "
            "none of these methods are suitable. You may specify fundamental "
            "characteristics or properties in the experimental sub-type. For "
            "Raman spectroscopy or ellipsometry use the respective "
            "specializations of NXoptical_spectroscopy."
        ),
        a_nexus_field=NeXusField(
            name="experiment_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "photoluminescence",
                "transmission spectroscopy",
                "reflection spectroscopy",
            ],
            open_enum=True,
        ),
    )
    experiment_sub_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-experiment-sub-type-field"
        ],
        description=(
            "Specify a special property or characteristic of the experiment, "
            "which specifies the generic experiment type."
        ),
        a_nexus_field=NeXusField(
            name="experiment_sub_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["time resolved", "imaging", "pump-probe"],
            open_enum=True,
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


class OpticalSpectroscopyBeamRefFrame(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-beam-ref-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="beam_ref_frame",
            name_type="specified",
            optionality="optional",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-beam-ref-frame-depends-on-field"
        ],
        description=(
            "This refers to the coordinate system along the beam path. The "
            "origin and base is defined at z=0, where the incident beam hits the "
            "sample at the surface."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopySampleNormalRefFrame(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-normal-ref-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="sample_normal_ref_frame",
            name_type="specified",
            optionality="optional",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-normal-ref-frame-depends-on-field"
        ],
        description=(
            "Link to transformations defining the sample-normal base coordinate "
            "system, which is defined such that the positive z-axis is parallel "
            "to the sample normal, and the x-y-plane lies inside the sample "
            "surface."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrument(Instrument):
    """
    Devices or elements of the optical spectroscopy setup described with its
    properties and general information.

    This includes for example: - The beam device's or instrument's model,
    company, serial number, construction year, etc. - Used software or code -
    Experiment descriptive parameters as reference frames, resolution,
    calibration - Photon beams with their respective properties such as angles
    and polarization - Various optical beam path devices, which interact,
    manipulate or measure optical beams - Characteristics of the medium
    surrounding the sample - "Beam devices" for a beam path description -
    Stages(NXmanipulator) - Sensors and actuators to control or measure sample
    or beam properties
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    beam_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentBeam_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_TYPE",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    detector_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentDetector_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector_TYPE",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    source_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentSource_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_TYPE",
            name_type="partial",
            optionality="recommended",
        ),
    )
    monochromator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentMonochromator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    generic_beam_sample_angle_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentGeneric_beam_sample_angle_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="generic_beam_sample_angle_TYPE",
            name_type="partial",
            optionality="recommended",
        ),
    )
    component = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    optical_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentOpticalLens",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXoptical_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    waveplate = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.waveplate.Waveplate",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXwaveplate",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    optical_window = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_window.OpticalWindow",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXoptical_window",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    polfilter_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentPolfilter_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="polfilter_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )
    spectralfilter_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentSpectralfilter_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="spectralfilter_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )
    beam_transfer_matrix_table = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam_transfer_matrix_table.BeamTransferMatrixTable",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam_transfer_matrix_table",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sample_stage = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentSampleStage",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="sample_stage",
            name_type="specified",
            optionality="optional",
        ),
    )
    temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )
    temp_control_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentTemp_control_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="temp_control_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentDeviceInformation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )
    software_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentSoftware_TYPE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="software_TYPE",
            name_type="partial",
            optionality="recommended",
        ),
    )
    instrument_calibration_DEVICE = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentInstrument_calibration_DEVICE",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="instrument_calibration_DEVICE",
            name_type="partial",
            optionality="recommended",
        ),
    )
    wavelength_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentWavelengthResolution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="wavelength_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    angle_reference_frame = Quantity(
        type=MEnum(["beam centered", "sample-normal centered"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-reference-frame-field"
        ],
        description=(
            "Defines the reference frame which is used to describe the sample "
            "orientation with respect to the beam directions. A beam centered "
            "description is the default and uses 4 angles(similar to XRD): - "
            "Omega (angle between sample surface and incident beam) - 2Theta "
            "(angle between the transmitted beam and the detection beam) - Chi "
            "(sample tilt angle, angle between plane#1 and the surface normal, "
            "plane#1 = spanned by incidence beam and detection and detection. If "
            "Chi=0°, then plane#1 is the plane of incidence in reflection "
            "setups) - Phi (inplane rotation of sample, rotation axis is the "
            "samples surface normal) A sample normal centered description is "
            "possible as well: - angle of incidence (angle between incident beam "
            "and sample surface) - angle of detection (angle between detection "
            "beam and sample surface) - angle of incident and detection beam - "
            "angle of in-plane sample rotation (direction along the sample's "
            "surface normal)"
        ),
        a_nexus_field=NeXusField(
            name="angle_reference_frame",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["beam centered", "sample-normal centered"],
        ),
    )
    omega = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-omega-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Angle between sample incident beam and sample surface."),
        a_nexus_field=NeXusField(
            name="omega",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    twotheta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-twotheta-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Angle between incident and detection beam"),
        a_nexus_field=NeXusField(
            name="twotheta",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    chi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-chi-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Sample tilt between sample normal, and the plane spanned by "
            "detection and incident beam."
        ),
        a_nexus_field=NeXusField(
            name="chi",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-phi-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Inplane rotation of the sample, with rotation axis along sample normal."
        ),
        a_nexus_field=NeXusField(
            name="phi",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_incidence = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-incidence-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Angle(s) of the incident beam vs. the normal of the bottom "
            "reflective (substrate) surface in the sample. These two directions "
            "span the plane of incidence."
        ),
        a_nexus_field=NeXusField(
            name="angle_of_incidence",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_detection = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-detection-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Detection angle(s) of the beam reflected or scattered off the "
            "sample vs. the normal of the bottom reflective (substrate) surface "
            "in the sample if not equal to the angle(s) of incidence. These two "
            "directions span the plane of detection."
        ),
        a_nexus_field=NeXusField(
            name="angle_of_detection",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_incident_and_detection_beam = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-incident-and-detection-beam-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Angle between the incident and detection beam. If "
            "angle_of_detection + angle_of_incidence = "
            "angle_of_incident_and_detection_beam, then the setup is a "
            "reflection setup. If angle_of_detection + angle_of_incidence != "
            "angle_of_incident_and_detection_beam then the setup may be a light "
            "scattering setup. (i.e. 90° + 90° != 90°, i.e. incident and "
            "detection beam in the sample surface, but the angle "
            "source-sample-detector is 90°)"
        ),
        a_nexus_field=NeXusField(
            name="angle_of_incident_and_detection_beam",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_in_plane_sample_rotation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-in-plane-sample-rotation-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Angle of the inplane orientation of the sample. This might be an "
            "arbitrary, angle without specific relation to the sample symmetry, "
            "of the angle to a specific sample property (i.e. crystallographic "
            "axis or sample shape such as wafer flat)"
        ),
        a_nexus_field=NeXusField(
            name="angle_of_in_plane_sample_rotation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    lateral_focal_point_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-lateral-focal-point-offset-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Specify if there is a lateral offset on the sample surface, between "
            "the focal points of the incident beam and the detection beam."
        ),
        a_nexus_field=NeXusField(
            name="lateral_focal_point_offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentBeam_TYPE(Beam):
    """
    This can be used to describe properties of a photon beam. A beam can be
    connected to components, via their "inputs" and "outputs".

    It is required to define at least one incident beam which is incident to
    the sample. You may specify if this beam parameters are actually measured
    or just nominal. If this beam is the output of a source, chose the same
    name appendix as for the NXsource instance (e.g. TYPE=532nm)
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_TYPE",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    parameter_reliability = Quantity(
        type=MEnum(["measured", "nominal"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-parameter-reliability-field"
        ],
        description=(
            "Select the reliability of the respective beam characteristics. "
            "Either, the parameters are measured via another device or method or "
            "just given nominally via the properties of a light source "
            "properties (532nm, 100mW)."
        ),
        a_nexus_field=NeXusField(
            name="parameter_reliability",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["measured", "nominal"],
        ),
    )
    incident_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-incident-wavelength-field"
        ],
        a_nexus_field=NeXusField(
            name="incident_wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )
    incident_wavelength_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-incident-wavelength-spread-field"
        ],
        a_nexus_field=NeXusField(
            name="incident_wavelength_spread",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )
    incident_polarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-incident-polarization-field"
        ],
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="incident_polarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    extent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-extent-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="extent",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    associated_source = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-associated-source-field"
        ],
        description=(
            "The path to the device which emitted this beam (light source or "
            "frequency doubler). This parameter is recommended, if the previous "
            "optical element is a photon source. In this way, the properties of "
            "the laser or light source can be described and associated. The beam "
            "should be named with the same appendix as the source, e.g., for "
            "TYPE=532nmlaser, there should be both a NXsource named "
            '"source_532nmlaser" and a NXbeam named "beam_532nmlaser". '
            "Example: /entry/instrument/source_532nmlaser"
        ),
        a_nexus_field=NeXusField(
            name="associated_source",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    beam_polarization_type = Quantity(
        type=MEnum(["linear", "circular", "elliptically", "unpolarized"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-beam-polarization-type-field"
        ],
        a_nexus_field=NeXusField(
            name="beam_polarization_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["linear", "circular", "elliptically", "unpolarized"],
        ),
    )
    linear_beam_sample_polarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-beam-type-linear-beam-sample-polarization-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Angle of the linear polarized light, with respect to a fixed "
            "arbitrary defined 0° position. Note that the zero reference should "
            "be a direction vector for a :ref:`reference_plane "
            "</NXbeam/TRANSFORMATIONS/reference_plane-field>` normal in an "
            ":ref:`NXtransformations` group within :ref:`NXbeam`. This can be "
            "used if no definition of respective coordinate systems for beam and "
            "sample normal is done. If coordinate systems are defined, refer to "
            'beam "incident_polarization".'
        ),
        a_nexus_field=NeXusField(
            name="linear_beam_sample_polarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentDetector_TYPE(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-detector-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detector_TYPE",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    raw_data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentDetector_TYPERawData",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="raw_data",
            name_type="specified",
            optionality="recommended",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    detector_channel_type = Quantity(
        type=MEnum(["single-channel", "multichannel"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-detector-type-detector-channel-type-field"
        ],
        a_nexus_field=NeXusField(
            name="detector_channel_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["single-channel", "multichannel"],
        ),
    )
    detector_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-detector-type-detector-type-field"
        ],
        description=("Description of the detector type."),
        a_nexus_field=NeXusField(
            name="detector_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "CCD",
                "photomultiplier",
                "photodiode",
                "avalanche-photodiode",
                "streak camera",
                "bolometer",
                "golay detectors",
                "pyroelectric detector",
                "deuterated triglycine sulphate",
            ],
            open_enum=True,
        ),
    )
    additional_detector_hardware = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-detector-type-additional-detector-hardware-field"
        ],
        description=(
            "Specify respective hardware which was used for the detector. For "
            "example special electronics required for time-correlated single "
            "photon counting (TCSPC)."
        ),
        a_nexus_field=NeXusField(
            name="additional_detector_hardware",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentDetector_TYPERawData(Data):
    """
    Contains the raw data collected by the detector before calibration. The
    data which is considered raw might change from experiment to experiment due
    to hardware pre-processing of the data. This field ideally collects the
    data with the lowest level of processing possible.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-detector-type-raw-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="raw_data",
            name_type="specified",
            optionality="recommended",
        ),
    )

    signal = Quantity(
        type=MEnum(["raw"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-detector-type-raw-data-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["raw"],
        ),
    )
    raw = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-detector-type-raw-data-raw-field"
        ],
        description=("Raw data before calibration."),
        a_nexus_field=NeXusField(
            name="raw",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentSource_TYPE(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-source-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_TYPE",
            name_type="partial",
            optionality="recommended",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-source-type-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "Synchrotron X-ray Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "UV Laser",
                "Optical Laser",
                "Laser",
                "Dye-Laser",
                "Broadband Tunable Light Source",
                "Halogen lamp",
                "LED",
                "Mercury Cadmium Telluride",
                "Deuterium Lamp",
                "Xenon Lamp",
                "Globar",
            ],
            open_enum=True,
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-source-type-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    standard = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-source-type-standard-field"
        ],
        description=("If available, name/ID/norm of the light source standard."),
        a_nexus_field=NeXusField(
            name="standard",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    associated_beam = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-source-type-associated-beam-field"
        ],
        description=(
            "The path to a beam emitted by this source. Should be named with the "
            "same appendix, e.g., for TYPE=532nmlaser, there should as well be a "
            'NXbeam named "beam_532nmlaser" together with this source instance '
            'named "source_532nmlaser" Example: '
            "/entry/instrument/beam_532nmlaser"
        ),
        a_nexus_field=NeXusField(
            name="associated_beam",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentMonochromator(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-monochromator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentGeneric_beam_sample_angle_TYPE(Transformations):
    """
    Set of transformations, describing the relative orientation of different
    parts of the experiment (beams or sample). You may select one of the
    specified angles for incident and detection beam or sample, and then use
    polar and azimuthal angles to define the direction via spherical
    coordinates. This allows consistent definition between different coordinate
    system. You may refer to self defined coordinate system as well.

    If "angle_reference_frame = beam centered", then this coordinate system is
    used: McStas system (NeXus default)
    (https://manual.nexusformat.org/design.html#mcstas-and-nxgeometry-system)

    i.e. the z-coordinate math:`[0,0,1]` is along the incident beam direction
    and the x-coordinate math:`[1,0,0]` is in the horizontal plane. Hence,
    usually math:`[0,1,0]` is vertically oriented.

    If "angle_reference_frame = sample-normal centered", then this coordinate
    system is used z - math:`[0,0,1]` along sample surface normal x -
    math:`[1,0,0]` defined by sample surface projected incident beam. y -
    math:`[0,1,0]` in the sample surface, orthogonal to z and x. For this case,
    x may be ill defined, if the incident beam is perpendicular to the sample
    surface. In this case, use the beam centered description.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="generic_beam_sample_angle_TYPE",
            name_type="partial",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=MEnum(["incident beam", "detection beam", "sample"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["incident beam", "detection beam", "sample"],
        ),
    )
    polar = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-polar-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Rotation about the y axis (polar rotation within the sample plane)."
        ),
        a_nexus_field=NeXusField(
            name="polar",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    polar__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-polar-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="polar",
            enumeration=["rotation"],
        ),
    )
    polar__vector = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-polar-vector-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="polar",
        ),
    )
    polar__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-polar-depends-on-attribute"
        ],
        description=(
            "Path to a transformation that places the sample surface into the "
            "origin of the arpes_geometry coordinate system."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="polar",
        ),
    )
    azimuth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-azimuth-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Rotation about the z axis (azimuthal rotation within the sample plane)."
        ),
        a_nexus_field=NeXusField(
            name="azimuth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    azimuth__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-azimuth-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="azimuth",
            enumeration=["rotation"],
        ),
    )
    azimuth__vector = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-azimuth-vector-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="azimuth",
        ),
    )
    azimuth__depends_on = Quantity(
        type=MEnum(["offset_tilt"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-generic-beam-sample-angle-type-azimuth-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="azimuth",
            enumeration=["offset_tilt"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentOpticalLens(OpticalLens):
    """
    This is the optical element used to focus or collect light. This may be a
    generic lens or microcope objectives which are used for the Raman
    scattering process.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-optical-lens-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXoptical_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-optical-lens-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["objective", "lens", "glass fiber", "none"],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentPolfilter_TYPE(Component):
    """
    Polarization filter to prepare light to be measured or to be incident on
    the sample. Generic polarization filter properties may be implemented via
    NXfilter_pol at a later stage.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-polfilter-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="polfilter_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="optional",
        ),
    )

    filter_mechanism = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-polfilter-type-filter-mechanism-field"
        ],
        description=(
            "Physical principle of the polarization filter used to create a "
            "defined incident or scattered light state."
        ),
        a_nexus_field=NeXusField(
            name="filter_mechanism",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "polarization by Fresnel reflection",
                "birefringent polarizers",
                "thin film polarizers",
                "wire-grid polarizers",
            ],
            open_enum=True,
        ),
    )
    specific_polarization_filter_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-polfilter-type-specific-polarization-filter-type-field"
        ],
        description=(
            "Specific name or type of the polarizer used. Free text, for "
            "example: Glan-Thompson, Glan-Taylor, Rochon Prism, Wollaston "
            "Polarizer..."
        ),
        a_nexus_field=NeXusField(
            name="specific_polarization_filter_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentSpectralfilter_TYPE(Component):
    """
    Spectral filter used to modify properties of the scattered or incident
    light.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-spectralfilter-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="spectralfilter_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    filter_characteristics = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentSpectralfilter_TYPEFilterCharacteristics",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="filter_characteristics",
            name_type="specified",
            optionality="optional",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="optional",
        ),
    )

    filter_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-spectralfilter-type-filter-type-field"
        ],
        description=(
            "Type of laser-line filter used to suppress the laser, if "
            "measurements close to the laser-line are performed."
        ),
        a_nexus_field=NeXusField(
            name="filter_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "long-pass filter",
                "short-pass filter",
                "notch filter",
                "reflection filter",
                "neutral density filter",
            ],
            open_enum=True,
        ),
    )
    intended_use = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-spectralfilter-type-intended-use-field"
        ],
        description=(
            "Type of laser-line filter used to suppress the laser, if "
            "measurements close to the laser-line are performed."
        ),
        a_nexus_field=NeXusField(
            name="intended_use",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "laser line cleanup",
                "raylight line removal",
                "spectral filtering",
                "intensity manipulation",
            ],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentSpectralfilter_TYPEFilterCharacteristics(Data):
    """
    Properties of the spectral filter such as wavelength dependent transmission
    or reflectivity.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-spectralfilter-type-filter-characteristics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="filter_characteristics",
            name_type="specified",
            optionality="optional",
        ),
    )

    characteristics_type = Quantity(
        type=MEnum(["transmission", "reflection"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-spectralfilter-type-filter-characteristics-characteristics-type-attribute"
        ],
        description=(
            "Which property is used to form the spectral properties of light, "
            "i.e. transmission or reflection properties."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="characteristics_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["transmission", "reflection"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentSampleStage(Manipulator):
    """
    Sample stage (or manipulator) for positioning of the sample. This should
    only contain the spatial orientation of movement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-sample-stage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="sample_stage",
            name_type="specified",
            optionality="optional",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="optional",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="optional",
        ),
    )

    stage_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-sample-stage-stage-type-field"
        ],
        description=("Specify the type of the sample stage."),
        a_nexus_field=NeXusField(
            name="stage_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "manual stage",
                "scanning stage",
                "liquid stage",
                "gas cell",
                "cryostat",
                "heater",
            ],
            open_enum=True,
        ),
    )
    beam_sample_relation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-sample-stage-beam-sample-relation-field"
        ],
        description=(
            "Description of relation of the beam with the sample. How does the "
            "sample hit the beam, e.g. 'center of sample, long edge parallel to "
            "the plane of incidence'. This is redundant if a full orientation "
            'description is done via the stage\'s "transformations" entry.'
        ),
        a_nexus_field=NeXusField(
            name="beam_sample_relation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentTemperatureSensor(Sensor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temperature-sensor-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )

    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temperature-sensor-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    measurement = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temperature-sensor-measurement-field"
        ],
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["temperature"],
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temperature-sensor-value-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentTemp_control_TYPE(Actuator):
    """
    Type of control for the sample temperature. Replace TYPE by "cryostat" or
    "heater" to specify it.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temp-control-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="temp_control_TYPE",
            name_type="partial",
            optionality="optional",
        ),
    )

    pid_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyInstrumentTemp_control_TYPEPidController",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    device_information = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temp-control-type-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    physical_quantity = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temp-control-type-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["temperature"],
        ),
    )
    cooler_or_heater = Quantity(
        type=MEnum(["cooler", "heater"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temp-control-type-cooler-or-heater-field"
        ],
        a_nexus_field=NeXusField(
            name="cooler_or_heater",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["cooler", "heater"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentTemp_control_TYPEPidController(PidController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temp-control-type-pid-controller-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    setpoint = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-temp-control-type-pid-controller-setpoint-field"
        ],
        a_nexus_field=NeXusField(
            name="setpoint",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentDeviceInformation(Fabrication):
    """
    General device information of the optical spectroscopy setup, if suitable
    (e.g. for a tabletop spectrometer or other non-custom build setups). For
    custom build setups, this may be limited to the construction year.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-device-information-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="device_information",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-device-information-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-device-information-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-device-information-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    construction_year = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-device-information-construction-year-field"
        ],
        a_nexus_field=NeXusField(
            name="construction_year",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentSoftware_TYPE(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-software-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="software_TYPE",
            name_type="partial",
            optionality="recommended",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-software-type-program-field"
        ],
        description=(
            "Commercial or otherwise defined given name of the program that was "
            "used to control any parts of the optical spectroscopy setup. The "
            "uppercase TYPE should be replaced by a specification name, i.e. "
            '"software_detector" or "software_stage" to specify the '
            "respective program or software components."
        ),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-software-type-program-version-attribute"
        ],
        description=(
            "Either version with build number, commit hash, or description of a "
            "(online) repository where the source code of the program and build "
            "instructions can be found so that the program can be configured in "
            "such a way that result files can be created ideally in a "
            "deterministic manner."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="program",
        ),
    )
    program__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-software-type-program-url-attribute"
        ],
        description=(
            "Description of the software by persistent resource, where the "
            "program, code, script etc. can be found."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentInstrument_calibration_DEVICE(Calibration):
    """
    Pre-calibration of an arbitrary device of the instrumental setup, which has
    the name DEVICE. You can specify here how, at which time by which method
    the calibration was done. As well the accuracy and a link to the
    calibration dataset.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-instrument-calibration-device-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="instrument_calibration_DEVICE",
            name_type="partial",
            optionality="recommended",
        ),
    )

    calibration_accuracy = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="calibration_accuracy",
            name_type="specified",
            optionality="optional",
        ),
    )

    device_path = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-instrument-calibration-device-device-path-field"
        ],
        description=(
            "Path to the device, which was calibrated. Example: entry/instrument/DEVICE"
        ),
        a_nexus_field=NeXusField(
            name="device_path",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    calibration_status = Quantity(
        type=MEnum(
            [
                "calibration time provided",
                "no calibration",
                "within 1 hour",
                "within 1 day",
                "within 1 week",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-instrument-calibration-device-calibration-status-field"
        ],
        description=(
            "Was a calibration performed? If yes, when was it done? If the "
            "calibration time is provided, it should be specified in "
            "calibration_time."
        ),
        a_nexus_field=NeXusField(
            name="calibration_status",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "calibration time provided",
                "no calibration",
                "within 1 hour",
                "within 1 day",
                "within 1 week",
            ],
        ),
    )
    calibration_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-instrument-calibration-device-calibration-time-field"
        ],
        description=(
            "If calibration status is 'calibration time provided', specify the "
            "ISO8601 date when calibration was last performed before this "
            "measurement. UTC offset should be specified."
        ),
        a_nexus_field=NeXusField(
            name="calibration_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyInstrumentWavelengthResolution(Resolution):
    """
    The overall resolution of the optical instrument.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-wavelength-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="wavelength_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["wavelength"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-wavelength-resolution-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["wavelength"],
        ),
    )
    type = Quantity(
        type=MEnum(["estimated", "derived", "calibrated", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-wavelength-resolution-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["estimated", "derived", "calibrated", "other"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-wavelength-resolution-resolution-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Minimum distinguishable wavelength separation of peaks in spectra."
        ),
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopySample(Sample):
    """
    Properties of the sample, such as sample type, layer structure, chemical
    formula, atom types, its history etc. Information about the sample stage
    and sample environment should be described in
    ENTRY/INSTRUMENT/sample_stage.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    temperature_env = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopySampleTemperatureEnv",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="temperature_env",
            name_type="specified",
            optionality="recommended",
        ),
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopySampleEnvironment",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    sample_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-sample-id-field"
        ],
        description=(
            "Locally unique ID of the sample, used in the research institute or group."
        ),
        a_nexus_field=NeXusField(
            name="sample_id",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    physical_form = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-physical-form-field"
        ],
        description=(
            "State the form of the sample, examples are: thin film, single "
            "crystal, poly crystal, amorphous, single layer, multi layer, "
            "liquid, gas, pellet, powder. Generic properties of liquids or gases "
            "see NXsample properties."
        ),
        a_nexus_field=NeXusField(
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-chemical-formula-field"
        ],
        description=(
            "Chemical formula of the sample. Use the Hill system (explained "
            "here: https://en.wikipedia.org/wiki/Chemical_formula#Hill_system) "
            "to write the chemical formula. In case the sample consists of "
            "several layers, this should be a list of the chemical formulas of "
            "the individual layers, where the first entry is the chemical "
            "formula of the top layer (the one on the front surface, on which "
            "the light incident). The order must be consistent with "
            "layer_structure"
        ),
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the sample. If the sample substance has multiple "
            "components, all elements from each component must be included in "
            "'atom_types'."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    preparation_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-preparation-date-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "when the specimen was prepared. Ideally, report the end of the "
            "preparation, i.e. the last known timestamp when the measured "
            "specimen surface was actively prepared."
        ),
        a_nexus_field=NeXusField(
            name="preparation_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-thickness-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "(Measured) sample thickness. The information is recorded to qualify "
            "if the light used was likely able to shine through the sample. In "
            "this case the value should be set to the actual thickness of the "
            "specimen viewed for an illumination situation where the nominal "
            "surface normal of the specimen is parallel to the optical axis."
        ),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    thickness_determination = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-thickness-determination-field"
        ],
        description=(
            "If a thickness if given, please specify how this thickness was "
            "estimated or determined."
        ),
        a_nexus_field=NeXusField(
            name="thickness_determination",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    layer_structure = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-layer-structure-field"
        ],
        description=(
            "Qualitative description of the layer structure for the sample, "
            "starting with the top layer (i.e. the one on the front surface, on "
            "which the light incident), e.g. native oxide/bulk substrate, or "
            "Si/native oxide/thermal oxide/polymer/peptide."
        ),
        a_nexus_field=NeXusField(
            name="layer_structure",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_orientation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-sample-orientation-field"
        ],
        description=(
            "Specify the sample orientation, how is its sample normal oriented "
            "relative in the laboratory reference frame, incident beam reference "
            "frame."
        ),
        a_nexus_field=NeXusField(
            name="sample_orientation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-substrate-field"
        ],
        description=(
            "If the sample is grown or fixed on a substrate, specify this here "
            "by a free text description."
        ),
        a_nexus_field=NeXusField(
            name="substrate",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopySampleTemperatureEnv(Environment):
    """
    Sample temperature (either controlled or just measured).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-temperature-env-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="temperature_env",
            name_type="specified",
            optionality="recommended",
        ),
    )

    temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="recommended",
        ),
    )
    sample_heater = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_heater",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_cooler = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_cooler",
            name_type="specified",
            optionality="optional",
        ),
    )

    temperature_nominal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-temperature-env-temperature-nominal-field"
        ],
        description=(
            "If no sensor was available for the determination of temperature, "
            "selected a nominal value which represents approximately the "
            "situation of sample temperature."
        ),
        a_nexus_field=NeXusField(
            name="temperature_nominal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "room temperature",
                "liquid helium temperature",
                "liquid nitrogen temperature",
            ],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopySampleEnvironment(Environment):
    """
    Arbitrary sample property which may be varied during the experiment and
    controlled by a device. Examples are pressure, voltage, magnetic field etc.
    Similar to the temperature description of the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-environment-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    sample_medium = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-environment-sample-medium-field"
        ],
        description=("Medium, in which the sample is placed."),
        a_nexus_field=NeXusField(
            name="sample_medium",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "air",
                "vacuum",
                "inert atmosphere",
                "oxidising atmosphere",
                "reducing atmosphere",
                "sealed can",
                "water",
            ],
            open_enum=True,
        ),
    )
    sample_medium_refractive_indices = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-environment-sample-medium-refractive-indices-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=[2, "*"],
        description=(
            "Array of pairs of complex refractive indices n + ik of the medium "
            "for every measured spectral point/wavelength/energy. Only necessary "
            "if the measurement was performed not in air, or something very well "
            "known, e.g. high purity water."
        ),
        a_nexus_field=NeXusField(
            name="sample_medium_refractive_indices",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyData(Data):
    """
    Here generic types of data may be saved. This may refer to data derived
    from single or multiple raw measurements (i.e. several intensities are
    evaluated for different parameters: ellipsometry -> psi and delta) - i.e.
    non-raw data. As well plottable data may be stored/linked here, which
    provides the most suitable representation of the data (for the respective
    community).

    You may provide multiple instances of NXdata
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-data-axes-attribute"
        ],
        shape=["*"],
        description=(
            "Spectrum, i.e. x-axis of the data (e.g. wavelength, energy etc.)"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-data-signal-attribute"
        ],
        description=("Spectrum, i.e. y-axis of the data (e.g. counts, intensity)"),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyMeasurement_data_calibration_TYPE(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-measurement-data-calibration-type-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="measurement_data_calibration_TYPE",
            name_type="partial",
            optionality="recommended",
        ),
    )

    wavelength_calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyMeasurement_data_calibration_TYPEWavelengthCalibration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="wavelength_calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyMeasurement_data_calibration_TYPEWavelengthCalibration(
    Calibration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-measurement-data-calibration-type-wavelength-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="wavelength_calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-measurement-data-calibration-type-wavelength-calibration-calibrated-axis-field"
        ],
        shape=["*"],
        description=("Calibrated wavelength axis."),
        a_nexus_field=NeXusField(
            name="calibrated_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyDerivedParameters(Process):
    """
    Parameters that are derived from the measured data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="derived_parameters",
            name_type="specified",
            optionality="optional",
        ),
    )

    ANALYSIS_program = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.optical_spectroscopy.OpticalSpectroscopyDerivedParametersANALYSIS_program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="ANALYSIS_program",
            name_type="partial",
            optionality="optional",
        ),
    )

    depolarization = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-depolarization-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 1, "*"],
        description=("Light loss due to depolarization as a value in [0-1]."),
        a_nexus_field=NeXusField(
            name="depolarization",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    jones_quality_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-jones-quality-factor-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 1, "*"],
        description=("Jones quality factor."),
        a_nexus_field=NeXusField(
            name="jones_quality_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    reflectivity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-reflectivity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 1, "*"],
        description=("Reflectivity."),
        a_nexus_field=NeXusField(
            name="reflectivity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    transmittance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-transmittance-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 1, "*"],
        description=("Transmittance."),
        a_nexus_field=NeXusField(
            name="transmittance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalSpectroscopyDerivedParametersANALYSIS_program(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-analysis-program-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="ANALYSIS_program",
            name_type="partial",
            optionality="optional",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-analysis-program-program-field"
        ],
        description=(
            "Commercial or otherwise defined given name of the program that was "
            "used to generate or calculate the derived parameters. If home "
            "written, one can provide the actual steps in the NOTE subfield "
            "here."
        ),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-derived-parameters-analysis-program-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
