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
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample

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
        section_def="pynxtools.nomad.metainfo.base_classes.optical_lens.OpticalLens",
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
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
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
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
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
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.Manipulator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="sample_stage",
            name_type="specified",
            optionality="optional",
        ),
    )
    software_TYPE = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
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
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
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
        section_def="pynxtools.nomad.metainfo.base_classes.resolution.Resolution",
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
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
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
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
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
