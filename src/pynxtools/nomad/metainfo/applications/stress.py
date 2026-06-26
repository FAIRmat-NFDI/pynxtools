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
# Run `pynx nomad generate-metainfo --nxdl NXstress` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.beam import Beam
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.reflections import Reflections
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Stress"]


class Stress(Entry):
    """
    Application definition for stress and strain analysis of crystalline
    material defined by the `EASI-STRESS consortium <https://easi-stress.eu>`_.

    When a crystal is loaded (applied or residual stress) its crystallographic
    parameters change.

    Stress and strain analysis calculates deformation (strain) and the
    associated force (stress) from diffraction data.

    This application definition essentially standardizes the result of
    diffraction pattern analysis from different types of diffraction
    experiments for the purpose of stress and strain analysis. The analysis is
    typically some form of diffraction peak indexing and fitting. The
    experiments are for example

    - energy-dispersive X-ray powder diffraction - angular-dispersive X-ray
    powder diffraction - angular-dispersive neutron powder diffraction -
    time-of-flight (TOF) neutron powder diffraction.

    In addition, the application definition guarantees that the information
    about instrumental setups, measurement conditions, and data analysis
    workflows are described. This ensures not only the reproducability and
    tracability of the measured data, but also the metadata. Since not all
    participating beamlines or instruments can provide an input to all the
    NeXus fields listed in this application definition, not all of them are
    "required".

    However, when possible and technically feasible, the instrument using the
    NXstress application definition is expected to provide the type of
    information outlined below.

    Sample and detector positions can be defined with :ref:`NXtransformations`.
    If you don't specify the direction of gravity and the direction of the beam
    then the standard NeXus Coordinate System is used.

    It is highly recommended that when certain parameters or values are the
    same for all the measurements (acquistions) in the same file, they are
    stored only in one location and then linked in the other instances. For
    example, if during an acquisition all

    instrumental parameters but one stay the same and only the sample table
    moves in one direction (e.g. Xtranslation), then all the static
    instrumental parameters should be saved just once (e.g. in just one NXentry
    or in a *Shared_Information group*) and their values linked to every
    *instrument group* under all the other acquisitions. The value for the
    variable that changes, Xtranslation in this example, is suggested to be
    saved only at every instrument group under each acquistion but not in the
    *Shared_Information group*.

    It is not always necessary to link each field. In case all the fields with
    an entire group are the same, the entire group can be linked.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXstress",
            category="application",
            symbols={
                "n_X": "Number of diffractogram channels.",
                "n_D": "Number of diffractograms. For example the number of energy-dispersive detectors or the number of azimuthal sections in an area detector.",
                "n_Peaks": "Number of reflections.",
                "x_Unit": "Diffractogram X units.",
                "y_Unit": "Diffractogram Y units.",
                "c_Unit": "Converted diffractogram X units (could be the same as *x_Unit*).",
                "n_Temp": "number of temperatures",
                "n_sField": "number of values in applied stress field",
                "nP": "number of scan points (only present in scanning measurements)",
                "i": "number of detector pixels in the first (slowest) direction",
                "j": "number of detector pixels in the second (faster) direction",
            },
        ),
    )

    experiment_responsible = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=False,
        description=("Information about the person who performed the experiment."),
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="experiment_responsible",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressInstrument",
        repeats=False,
    )
    sample_description = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressSampleDescription",
        repeats=True,
        variable=True,
        description=(
            "This is the recommended location for describing parameters "
            "associated with the sample."
        ),
    )
    fit = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressFit",
        repeats=True,
        variable=True,
        description=(
            "Zero or more groups to describe the data processing steps to obtain "
            "the content of this application definition."
        ),
    )
    notes = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=(
            "User description of the data acquisitions. A description of data "
            "analysis goes in the :ref:`fit descriptions "
            "</NXstress/ENTRY/FIT/DESCRIPTION-group>`."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="NOTES",
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    peaks = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressPeaks",
        repeats=False,
        description=(
            "This group contains all diffraction peak parameters that could be "
            "needed for stress and strain calculations. These parameters are "
            "derived from :ref:`peak_parameters "
            "</NXstress/ENTRY/fit/peak_parameters-group>` and additional "
            "metadata."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXstress"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXstress"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXstress",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-title-field"
        ],
        description=("Extended title for the entry."),
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-experiment-identifier-field"
        ],
        description=(
            "Unique identifier for the experiment as defined by the facility "
            "(e.g. DOI, proposal id, ...). At ILL, this could be, for example, "
            "``exp_1-02-286``, ``exp_INDU-229``, or ``exp_INTER-569``."
        ),
        a_nexus_field=NeXusField(
            name="experiment_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-experiment-description-field"
        ],
        description=(
            "Brief summary of the experiment, including key objectives. At least "
            "one of the following information should be provided: * "
            "``energy-dispersive X-ray powder diffraction`` * "
            "``angular-dispersive X-ray powder diffraction`` * "
            "``angular-dispersive neutron powder diffraction`` * "
            "``time-of-flight (TOF) neutron powder diffraction``"
        ),
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-start-time-field"
        ],
        description=(
            "The starting time(s) of measurement(s) which can be provided in "
            "form of a list if multiple measurements are included in the same "
            "NXentry."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-end-time-field"
        ],
        description=(
            "The end time(s) of measurement(s) which can be provided in form of "
            "a list if multiple measurements are included in the same NXentry."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    collection_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-collection-identifier-field"
        ],
        description=(
            "User or Data Acquisition defined identifier from which the content "
            "of this application definition is derived. This can be freely "
            "chosen by the user or the instrument scientist and could be, for "
            "example, ``05_DA_650_AX_B3P5``, ``SENB-14``, ``Quartz``,...."
        ),
        a_nexus_field=NeXusField(
            name="collection_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    collection_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-collection-description-field"
        ],
        description=(
            "Brief summary of the collection, including grouping criteria. The "
            "information provided in this field can highlight, for example, the "
            "measurement setup or information about experimental conditions."
        ),
        a_nexus_field=NeXusField(
            name="collection_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    processing_type = Quantity(
        type=MEnum(["two-theta", "energy", "d-spacing", "time-of-flight", "sin2psi"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-processing-type-field"
        ],
        description=(
            "Describes the way strain :math:`\\varepsilon` can be calculated "
            "from the :ref:`center </NXstress/ENTRY/peaks/center-field>` peak "
            "parameter."
        ),
        a_nexus_field=NeXusField(
            name="processing_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "two-theta",
                "energy",
                "d-spacing",
                "time-of-flight",
                "sin2psi",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    measurement_direction = Quantity(
        type=MEnum(["radial", "longitudinal", "normal", "tangential", "multiple"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-measurement-direction-field"
        ],
        description=(
            "Describes the specific measurement direction covered by the data in "
            "this file."
        ),
        a_nexus_field=NeXusField(
            name="measurement_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["radial", "longitudinal", "normal", "tangential", "multiple"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
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


class StressInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressInstrumentCalibration",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="CALIBRATION",
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )
    beam_intensity_profile = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressInstrumentBeamIntensityProfile",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_intensity_profile",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-name-field"
        ],
        description=(
            "Name of the diffractometer, instrument, or beamline used for the "
            "experiment. This could be, for example, *Strain Analyser for Large "
            "and Small scale engineering Applications*."
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    name__short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-name-short-name-attribute"
        ],
        description=(
            "Short name for the instrument, perhaps the acronym, which would be "
            "for the the example above ``SALSA``."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressInstrumentCalibration(Note):
    """
    This group contains information about the geometry and/or efficiency
    measurement(s).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-calibration-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="CALIBRATION",
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    calibration_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-calibration-calibration-type-field"
        ],
        description=("Describe the type of calibration."),
        a_nexus_field=NeXusField(
            name="calibration_type",
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


class StressInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    type = Quantity(
        type=MEnum(
            [
                "Spallation Neutron Source",
                "Pulsed Reactor Neutron Source",
                "Reactor Neutron Source",
                "Synchrotron X-ray Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "Metal Jet X-ray",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-source-type-field"
        ],
        description=("Type of radiation source"),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "Spallation Neutron Source",
                "Pulsed Reactor Neutron Source",
                "Reactor Neutron Source",
                "Synchrotron X-ray Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "Metal Jet X-ray",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    probe = Quantity(
        type=MEnum(["neutron", "X-ray"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-source-probe-field"
        ],
        description=("Type of radiation probe"),
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["neutron", "X-ray"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressInstrumentDetector(Detector):
    """
    Zero or more of these groups describe the detectors used in the experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-detector-type-field"
        ],
        description=(
            "Description of type such as \\ :sup:`3`\\ He gas cylinder, \\ "
            ":sup:`3`\\ He PSD, scintillator, fission chamber, proportion "
            "counter, ion chamber, CCD, pixel, image plate, CMOS, …"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-detector-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*", "*"],
        description=(
            "This is the distance to the previous component in the instrument; "
            "most often the sample. The usage depends on the nature of the "
            "detector: Most often it is the distance of the detector assembly. "
            "But there are irregular detectors. In this case the distance must "
            "be specified for each detector pixel. Note, it is recommended to "
            "use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    efficiency_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-detector-efficiency-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        description=("efficiency of the detector"),
        a_nexus_field=NeXusField(
            name="efficiency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-detector-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "This field can be two things: 1. For a pixel detector it provides "
            "the nominal wavelength for which the detector has been calibrated. "
            "2. For other detectors this field has to be seen together with the "
            "efficiency field above. For some detectors, the efficiency is "
            "wavelength dependent. Thus this field provides the wavelength axis "
            "for the efficiency field. In this use case, the efficiency and "
            "wavelength arrays must have the same dimensionality."
        ),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressInstrumentBeamIntensityProfile(Beam):
    """
    Defines the dimensions of the beam profile used for probing the sample
    which corresponds to or can be used to determine the instrumental gauge
    volume. A description of the subsequent fields can be found in the folowing
    figure. The term "primary" in the subsequent fields refers to the beam path
    between the sample and the source. The term "secondary" refers to the beam
    path between the sample and the detector(s).

    .. figure:: stress/Beam_profile_sketch3.jpg :width: 70% :alt: Examples for
    the beam intensity profile.

    Some examples for the beam intensity profile. The 1D description of the
    beam profile on the right can equally be applied for the horizontal and
    vertical direction for the primary and the secondary side.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_intensity_profile",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    beam_evaluation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-beam-evaluation-field"
        ],
        description=(
            "If the beam profile was measured, the filename(s) of the "
            "measurement can be specified here."
        ),
        a_nexus_field=NeXusField(
            name="beam_evaluation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    primary_vertical_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-vertical-type-field"
        ],
        description=(
            "Defines the last device right in front of the sample used to shape "
            "the beam. This could be, for example, a :ref:`(radial) collimator "
            "<NXcollimator>` or a :ref:`slit <NXslit>`."
        ),
        a_nexus_field=NeXusField(
            name="primary_vertical_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    primary_vertical_source_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-vertical-source-width-field"
        ],
        description=(
            "Defines the primary beam size intensity profile on the side closer "
            "to the source in the vertical direction."
        ),
        a_nexus_field=NeXusField(
            name="primary_vertical_source_width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    primary_vertical_sample_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-vertical-sample-width-field"
        ],
        description=(
            "Defines the primary beam size intensity profile on the side closer "
            "to the sample in the vertical direction."
        ),
        a_nexus_field=NeXusField(
            name="primary_vertical_sample_width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    primary_vertical_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-vertical-distance-field"
        ],
        description=(
            "Defines the distance between the center of the gauge volume and the "
            "beam shaping device."
        ),
        a_nexus_field=NeXusField(
            name="primary_vertical_distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    primary_vertical_evaluation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-vertical-evaluation-field"
        ],
        description=(
            "Describes how the beam intensity profile in the primary vertical "
            "direction was determined. Examples of valid entries are: "
            "``measured``, ``theoretical``, ``estimated``, ..."
        ),
        a_nexus_field=NeXusField(
            name="primary_vertical_evaluation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    primary_horizontal_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-horizontal-type-field"
        ],
        description=(
            "Defines the last device right in front of the sample used to shape "
            "the beam. This could be, for example, a :ref:`(radial) collimator "
            "<NXcollimator>` or a :ref:`slit <NXslit>`."
        ),
        a_nexus_field=NeXusField(
            name="primary_horizontal_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    primary_horizontal_source_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-horizontal-source-width-field"
        ],
        description=(
            "Defines the primary beam size intensity profile on the side closer "
            "to the source in the horizontal direction."
        ),
        a_nexus_field=NeXusField(
            name="primary_horizontal_source_width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    primary_horizontal_sample_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-horizontal-sample-width-field"
        ],
        description=(
            "Defines the primary beam size intensity profile on the side closer "
            "to the sample in the horizontal direction."
        ),
        a_nexus_field=NeXusField(
            name="primary_horizontal_sample_width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    primary_horizontal_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-horizontal-distance-field"
        ],
        description=(
            "Defines the distance between the center of the gauge volume and the "
            "beam shaping device."
        ),
        a_nexus_field=NeXusField(
            name="primary_horizontal_distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    primary_horizontal_evaluation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-primary-horizontal-evaluation-field"
        ],
        description=(
            "Describes how the beam intensity profile in the primary horizontal "
            "direction was determined. Examples of valid entries are: "
            "``measured``, ``theoretical``, ``estimated``, ..."
        ),
        a_nexus_field=NeXusField(
            name="primary_horizontal_evaluation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    secondary_horizontal_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-secondary-horizontal-type-field"
        ],
        description=(
            "Defines the last device right in front of the sample used to shape "
            "the beam. This could be, for example, a :ref:`(radial) collimator "
            "<NXcollimator>` or a :ref:`slit <NXslit>`."
        ),
        a_nexus_field=NeXusField(
            name="secondary_horizontal_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    secondary_horizontal_detector_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-secondary-horizontal-detector-width-field"
        ],
        description=(
            "Defines the secondary beam size intensity profile on the side "
            "closer to the detector in the horizontal direction."
        ),
        a_nexus_field=NeXusField(
            name="secondary_horizontal_detector_width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    secondary_horizontal_sample_width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-secondary-horizontal-sample-width-field"
        ],
        description=(
            "Defines the secondary beam size intensity profile on the side "
            "closer to the sample in the horizontal direction."
        ),
        a_nexus_field=NeXusField(
            name="secondary_horizontal_sample_width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    secondary_horizontal_distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-secondary-horizontal-distance-field"
        ],
        description=(
            "Defines the distance between the center of the gauge volume and the "
            "beam shaping device."
        ),
        a_nexus_field=NeXusField(
            name="secondary_horizontal_distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    secondary_horizontal_evaluation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-beam-intensity-profile-secondary-horizontal-evaluation-field"
        ],
        description=(
            "Describes how the beam intensity profile in the secondary "
            "horizontal direction was determined. Examples of valid entries are: "
            "``measured``, ``theoretical``, ``estimated``, ..."
        ),
        a_nexus_field=NeXusField(
            name="secondary_horizontal_evaluation",
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


class StressSampleDescription(Sample):
    """
    This is the recommended location for describing parameters associated with
    the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="SAMPLE_DESCRIPTION",
            name_type="any",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    gauge_volume = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressSampleDescriptionGaugeVolume",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="gauge_volume",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    stress_field__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-stress-field-direction-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="stress_field",
            enumeration=["x", "y", "z"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-depends-on-field"
        ],
        description=(
            "The axis on which the sample position depends may be stored "
            "anywhere, but is normally stored in the NXtransformations group "
            "within the NXsample group."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class StressSampleDescriptionGaugeVolume(Parameters):
    """
    The gauge volume can be described with the following parameters: ..
    figure:: stress/gauge_volume.png :width: 70% :alt: Gauge volume parameters
    and coordinate system.

    Gauge volume parameters and coordinate system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-gauge-volume-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="gauge_volume",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    a = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-gauge-volume-a-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Length of the first diagonal."),
        a_nexus_field=NeXusField(
            name="a",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    b = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-gauge-volume-b-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Length of the second diagonal normal to :ref:`x "
            "</NXstress/ENTRY/sample_description/gauge_volume/a-field>`."
        ),
        a_nexus_field=NeXusField(
            name="b",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    c = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-gauge-volume-c-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Height of the gauge volume."),
        a_nexus_field=NeXusField(
            name="c",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-gauge-volume-depends-on-field"
        ],
        description=(
            "In the local coordinate system, the beam is aligned along the "
            "X-axis, and the Z-axis is oriented in the opposite direction of "
            "gravity. The origin is the center to the gauge volume."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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


class StressFit(Process):
    """
    Zero or more groups to describe the data processing steps to obtain the
    content of this application definition.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="FIT",
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    data_reduction_responsible = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="data_reduction_responsible",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    description = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="DESCRIPTION",
            name_type="any",
            optionality="required",
        ),
    )
    peak_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressFitPeakParameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="peak_parameters",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )
    background_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressFitBackgroundParameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="background_parameters",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )
    diffractogram = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressFitDiffractogram",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="DIFFRACTOGRAM",
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    raw_data_file = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-raw-data-file-field"
        ],
        description=(
            "The raw data file name(s) used during the data reduction process. "
            "This can be a list."
        ),
        a_nexus_field=NeXusField(
            name="raw_data_file",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-date-field"
        ],
        description=(
            "Date when the raw data was reduced and the data in the *NXstress* "
            "file format generated."
        ),
        a_nexus_field=NeXusField(
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    program_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-program-field"
        ],
        description=(
            "Software package used to perform data reduction including the "
            "version number or release date."
        ),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    integration_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-integration-type-field"
        ],
        description=("Describes how the data was integrated."),
        a_nexus_field=NeXusField(
            name="integration_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    bins = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-bins-field"
        ],
        description=("Describes the type of binning used during data reduction."),
        a_nexus_field=NeXusField(
            name="bins",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fit_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-fit-type-field"
        ],
        description=(
            "Describes how the fitting of the peaks was done. For example, "
            "single peak fit, multiple peak fit, Pawley refinement, Rietveld "
            "refinement, …"
        ),
        a_nexus_field=NeXusField(
            name="fit_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fit_range = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-fit-range-field"
        ],
        description=("Describes the data range used for peak fitting."),
        a_nexus_field=NeXusField(
            name="fit_range",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    goodness_of_fit = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-goodness-of-fit-field"
        ],
        description=(
            "Type and value describing the goodness of fit. For example, Rw 0.23."
        ),
        a_nexus_field=NeXusField(
            name="goodness_of_fit",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    normalization = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-normalization-field"
        ],
        description=(
            "Describes whether the data was normalized and if so , how. Examples "
            "of valid entries are: ``None``, ``time``, ``primary monitor``, "
            "``detector``, …"
        ),
        a_nexus_field=NeXusField(
            name="normalization",
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


class StressFitPeakParameters(Parameters):
    """
    This group contains all diffraction peak fit parameters. This information
    is not required for stress and strain calculations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="peak_parameters",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    title = Quantity(
        type=MEnum(
            [
                "gaussian",
                "lorentzian",
                "voigt",
                "pseudo-voigt",
                "split pseudo-voigt",
                "pearson VII",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-title-field"
        ],
        description=("Diffraction peak profile."),
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "gaussian",
                "lorentzian",
                "voigt",
                "pseudo-voigt",
                "split pseudo-voigt",
                "pearson VII",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-area-field"
        ],
        shape=["*"],
        description=(
            "Diffraction peak area (not including the background) in *y_Unit* units."
        ),
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    area__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-area-units-attribute"
        ],
        description=("Specify the *y_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="area",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    area_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-area-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error value(s) asscociated with :ref:`area "
            "</NXstress/ENTRY/fit/peak_parameters/area-field>`"
        ),
        a_nexus_field=NeXusField(
            name="area_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-center-field"
        ],
        shape=["*"],
        description=("Diffraction peak position in *x_Unit* units."),
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    center__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-center-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="center",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    center_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-center-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error value(s) asscociated with :ref:`center "
            "</NXstress/ENTRY/fit/peak_parameters/center-field>`"
        ),
        a_nexus_field=NeXusField(
            name="center_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    height = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-height-field"
        ],
        shape=["*"],
        description=(
            "Diffraction peak height (not including the background) in *y_Unit* units."
        ),
        a_nexus_field=NeXusField(
            name="height",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    height__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-height-units-attribute"
        ],
        description=("Specify the *y_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="height",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    height_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-height-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error value(s) asscociated with :ref:`height "
            "</NXstress/ENTRY/fit/peak_parameters/height-field>`"
        ),
        a_nexus_field=NeXusField(
            name="height_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    fwhm = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-field"
        ],
        shape=["*"],
        description=("Diffraction peak full width at half maximum in *x_Unit* units."),
        a_nexus_field=NeXusField(
            name="fwhm",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    fwhm__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fwhm",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fwhm_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error value(s) asscociated with :ref:`fwhm "
            "</NXstress/ENTRY/fit/peak_parameters/fwhm-field>`"
        ),
        a_nexus_field=NeXusField(
            name="fwhm_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    fwhm_left = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-left-field"
        ],
        shape=["*"],
        description=("Left-side FWHM for split profiles in *x_Unit* units."),
        a_nexus_field=NeXusField(
            name="fwhm_left",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    fwhm_left__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-left-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fwhm_left",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fwhm_left_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-left-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error value(s) asscociated with :ref:`fwhm_left "
            "</NXstress/ENTRY/fit/peak_parameters/fwhm_left-field>`"
        ),
        a_nexus_field=NeXusField(
            name="fwhm_left_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    fwhm_right = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-right-field"
        ],
        shape=["*"],
        description=("Right-side FWHM for split profiles in *x_Unit* units."),
        a_nexus_field=NeXusField(
            name="fwhm_right",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    fwhm_right__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-right-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fwhm_right",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fwhm_right_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-fwhm-right-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error value(s) asscociated with :ref:`fwhm_right "
            "</NXstress/ENTRY/fit/peak_parameters/fwhm_right-field>`"
        ),
        a_nexus_field=NeXusField(
            name="fwhm_right_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    form_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-form-factor-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "- Voigt or Pseudo-Voigt: Lorentzian fraction - Pearson VII: decay "
            "parameter - Other profiles: not applicable"
        ),
        a_nexus_field=NeXusField(
            name="form_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    form_factor_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-form-factor-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error value(s) asscociated with :ref:`form_factor "
            "</NXstress/ENTRY/fit/peak_parameters/form_factor-field>`"
        ),
        a_nexus_field=NeXusField(
            name="form_factor_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    azimuth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-peak-parameters-azimuth-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Angle that defines the position of the integrated sector in the "
            "diffraction cone for angular-dispersive diffraction or the position "
            "of the detector for energy-dispersive diffraction."
        ),
        a_nexus_field=NeXusField(
            name="azimuth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressFitBackgroundParameters(Parameters):
    """
    This group contains all background fit parameters. This information is not
    required for stress and strain calculations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="background_parameters",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-title-field"
        ],
        description=(
            "Diffraction background profile. Required when background parameter "
            "fields are present. Some example values with equations are shown "
            "below: - ``manual`` : No equations nor variables needed to describe "
            "this background. - ``linear`` : \\ :math:`\\small background= A0 + "
            "A1 \\cdot x` - ``5-degree polynomial`` : \\ :math:`\\small "
            "background= A0 + A1 \\cdot x + A2 \\cdot \\mathrm{x}^{2} + A3 "
            "\\cdot \\mathrm{x}^{3} + A4 \\cdot \\mathrm{x}^{4} + A5 \\cdot "
            "\\mathrm{x}^{5}` - ``shape function plus polynomial`` : A shape "
            "function is not a mathematical function, it contains a manual "
            "background obtained from a fit and a polynomial part. This allows "
            "to adapt and modify the fit for subsequent measurements in the same "
            "measurement campaign. The function describing it is the following: "
            "\\ :math:`\\small background= as + b \\cdot SHAPE(x-o)` Where SHAPE "
            "is the name of the variable used to describe the background value "
            "at the position x. x can be e.g. the scattering angle \\ "
            ":math:`2\\theta` in degrees."
        ),
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    A = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-a-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Background parameter(s). For example a second-degree polynomial "
            "will have fields ``A0``, ``A1`` and ``A2``."
        ),
        a_nexus_field=NeXusField(
            name="A",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    as_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-as-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Background parameter *constant* for SHAPE function."),
        a_nexus_field=NeXusField(
            name="as",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    as_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-as-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error associated with background parameter *constant* for SHAPE function."
        ),
        a_nexus_field=NeXusField(
            name="as_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    b = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-b-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Background parameter *amplitude* for SHAPE function."),
        a_nexus_field=NeXusField(
            name="b",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    b_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-b-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error associated with background parameter *amplitude* for SHAPE function."
        ),
        a_nexus_field=NeXusField(
            name="b_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    o = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-o-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Background parameter *offset* for SHAPE function."),
        a_nexus_field=NeXusField(
            name="o",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    o_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-o-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Error associated with background parameter *offset* for SHAPE function."
        ),
        a_nexus_field=NeXusField(
            name="o_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    background_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-background-area-field"
        ],
        shape=["*"],
        description=(
            "The background area in *y_Unit* units, integrated over a confidence "
            "interval around the center (*0.95* by default)."
        ),
        a_nexus_field=NeXusField(
            name="background_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    background_area__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-background-area-units-attribute"
        ],
        description=("Specify the *y_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="background_area",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    background_area_interval = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-background-parameters-background-area-interval-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Confidence interval from which the background counts are "
            "integrated. For example *0.95* means that the background is "
            "integrated over the range in which the integrated peak area is 95% "
            "of the total peak area."
        ),
        a_nexus_field=NeXusField(
            name="background_area_interval",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressFitDiffractogram(Data):
    """
    Diffractogram with fit results in :ref:`peak_parameters
    </NXstress/ENTRY/fit/peak_parameters-group>` and
    :ref:`background_parameters
    </NXstress/ENTRY/fit/background_parameters-group>`. This information is not
    required for stress and strain calculations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="DIFFRACTOGRAM",
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-axes-attribute"
        ],
        shape=["*"],
        description=(
            "List of the one to two axes field name(s) to be used by default. "
            "The axes are further described in the fields DAXIS and XAXIS."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    DAXIS = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-daxis-field"
        ],
        variable=True,
        shape=["*"],
        description=(
            "One or more fields that contain the values for the **n_D** "
            "dimension. For example the azimuthal positions of different "
            "energy-dispersive detectors or the average azimuth of different "
            "azimuthal sections on an area detector."
        ),
        a_nexus_field=NeXusField(
            name="DAXIS",
            type="NX_CHAR_OR_NUMBER",
            name_type="any",
            optionality="optional",
        ),
    )
    XAXIS = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-xaxis-field"
        ],
        variable=True,
        shape=["*"],
        description=(
            "One or more fields that contain the values for the **n_X** "
            "dimension in *x_Unit* units. For example: MCA channels, scattering "
            "angle \\ :math:`2\\theta` in degrees, scattering vector length q in "
            "\\ :math:`\\mathrm{nm}^{-1}`, ..."
        ),
        a_nexus_field=NeXusField(
            name="XAXIS",
            type="NX_NUMBER",
            name_type="any",
            optionality="required",
            units="NX_ANY",
        ),
    )
    XAXIS__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-xaxis-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="XAXIS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    signal = Quantity(
        type=MEnum(["diffractogram"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-signal-attribute"
        ],
        description=("Default field name to be plotted."),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["diffractogram"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="diffractogram",
        ),
    )
    auxiliary_signals = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-auxiliary-signals-attribute"
        ],
        description=(
            "List of additional field names to be plotted. This could be e.g. "
            "fit, background, residuals, …"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="auxiliary_signals",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    diffractogram = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-diffractogram-field"
        ],
        shape=["*", "*"],
        description=("Diffractogram counts in *y_Unit* units (default signal)"),
        a_nexus_field=NeXusField(
            name="diffractogram",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    diffractogram__interpretation = Quantity(
        type=MEnum(["spectrum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-diffractogram-interpretation-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="interpretation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="diffractogram",
            enumeration=["spectrum"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="spectrum",
        ),
    )
    diffractogram__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-diffractogram-units-attribute"
        ],
        description=("Specify the *y_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="diffractogram",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    diffractogram_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-diffractogram-errors-field"
        ],
        shape=["*", "*"],
        description=("Diffractogram counts error in *y_Unit* units (default signal)"),
        a_nexus_field=NeXusField(
            name="diffractogram_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    diffractogram_errors__interpretation = Quantity(
        type=MEnum(["spectrum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-diffractogram-errors-interpretation-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="interpretation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="diffractogram_errors",
            enumeration=["spectrum"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="spectrum",
        ),
    )
    diffractogram_errors__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-diffractogram-errors-units-attribute"
        ],
        description=("Specify the *y_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="diffractogram_errors",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-fit-field"
        ],
        shape=["*", "*"],
        description=("Diffractogram fit counts (auxiliary signal)."),
        a_nexus_field=NeXusField(
            name="fit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    fit__interpretation = Quantity(
        type=MEnum(["spectrum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-fit-interpretation-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="interpretation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fit",
            enumeration=["spectrum"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="spectrum",
        ),
    )
    fit__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-fit-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fit",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fit_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-fit-errors-field"
        ],
        shape=["*", "*"],
        description=("Diffractogram fit counts error (auxiliary signal)."),
        a_nexus_field=NeXusField(
            name="fit_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    fit_errors__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-fit-errors-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fit_errors",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    background = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-background-field"
        ],
        shape=["*", "*"],
        description=(
            "In case the diffraction background was manually determined. "
            "Diffractogram background counts (auxiliary signal)."
        ),
        a_nexus_field=NeXusField(
            name="background",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    background__interpretation = Quantity(
        type=MEnum(["spectrum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-background-interpretation-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="interpretation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="background",
            enumeration=["spectrum"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="spectrum",
        ),
    )
    background__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-background-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="background",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    residuals = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-residuals-field"
        ],
        shape=["*", "*"],
        description=("Difference between diffractogram and fit (auxiliary signal)."),
        a_nexus_field=NeXusField(
            name="residuals",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    residuals__interpretation = Quantity(
        type=MEnum(["spectrum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-residuals-interpretation-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="interpretation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="residuals",
            enumeration=["spectrum"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="spectrum",
        ),
    )
    residuals__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-diffractogram-residuals-units-attribute"
        ],
        description=("Specify the *x_Unit* units"),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="residuals",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressPeaks(Reflections):
    """
    This group contains all diffraction peak parameters that could be needed
    for stress and strain calculations. These parameters are derived from
    :ref:`peak_parameters </NXstress/ENTRY/fit/peak_parameters-group>` and
    additional metadata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXreflections",
            name="peaks",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    h = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-h-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("First Miller index."),
        a_nexus_field=NeXusField(
            name="h",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    k = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-k-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Second Miller index."),
        a_nexus_field=NeXusField(
            name="k",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    l = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-l-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Third Miller index."),
        a_nexus_field=NeXusField(
            name="l",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    lattice = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-lattice-field"
        ],
        shape=["*"],
        description=("Crystal lattice systems (*cubic*, *hexagonal*, ...)"),
        a_nexus_field=NeXusField(
            name="lattice",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    space_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-space-group-field"
        ],
        shape=["*"],
        description=(
            "Crystallographic space group :math:`(Fm\\bar{3}m, Im\\bar{3}m, ...)`"
        ),
        a_nexus_field=NeXusField(
            name="space_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    phase_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-phase-name-field"
        ],
        shape=["*"],
        description=(
            "Name of the crystallographic phase (hematite, goethite, \\ "
            ":math:`\\alpha`-Al\\ :sub:`2`\\ O\\ :sub:`3`\\ , ...)."
        ),
        a_nexus_field=NeXusField(
            name="phase_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    qx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-qx-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "First component of the *normalized* scattering vector *Q* in the "
            "sample reference frame. The sample reference frame is defined by "
            "the :ref:`sample transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_field=NeXusField(
            name="qx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    qy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-qy-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Second component of the *normalized* scattering vector *Q* in the "
            "sample reference frame. The sample reference frame is defined by "
            "the :ref:`sample transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_field=NeXusField(
            name="qy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    qz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-qz-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Third component of the *normalized* scattering vector *Q* in the "
            "sample reference frame. The sample reference frame is defined by "
            "the :ref:`sample transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_field=NeXusField(
            name="qz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-field"
        ],
        shape=["*"],
        description=("Diffraction peak position in *c_Unit* units."),
        a_nexus_field=NeXusField(
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    center__units = Quantity(
        type=MEnum(["degrees", "keV", "1/angstrom", "angstrom", "microseconds", "''"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-units-attribute"
        ],
        description=(
            "Specify the *c_Unit* units (see :ref:`center_type "
            "</NXstress/ENTRY/peaks/center_type-field>`)"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="center",
            enumeration=[
                "degrees",
                "keV",
                "1/angstrom",
                "angstrom",
                "microseconds",
                "''",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    center_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-errors-field"
        ],
        shape=["*"],
        description=(
            "Uncentrainties on :ref:`center "
            "</NXstress/ENTRY/peaks/center-field>` in *c_Unit* units."
        ),
        a_nexus_field=NeXusField(
            name="center_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    center_errors__units = Quantity(
        type=MEnum(["degrees", "keV", "1/angstrom", "angstrom", "microseconds", "''"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-errors-units-attribute"
        ],
        description=(
            "Specify the *c_Unit* units (see :ref:`center_type "
            "</NXstress/ENTRY/peaks/center_type-field>`)"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="center_errors",
            enumeration=[
                "degrees",
                "keV",
                "1/angstrom",
                "angstrom",
                "microseconds",
                "''",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    center_type = Quantity(
        type=MEnum(
            [
                "two-theta",
                "energy",
                "momentum-transfer",
                "d-spacing",
                "channel",
                "time-of-flight",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-type-field"
        ],
        description=(
            "The space in which :ref:`center "
            "</NXstress/ENTRY/peaks/center-field>` is defined. It defines the "
            '*c_Unit* as follows - if *center_type="two-theta"* then *c_Unit* '
            'must have the angle unit *degrees* - if *center_type="energy"* '
            "then *c_Unit* must have the unit *keV* - if "
            '*center_type="momentum-transfer"* then *c_Unit* must have the '
            'unit \\ :math:`Å^{-1}` - if *center_type="d-spacing"* then '
            "*c_Unit* must have the unit \\ :math:`Å` - if "
            '*center_type="channel"* then *c_Unit* must be *dimensioness* - if '
            '*center_type="time-of-flight"* then *c_Unit* must have the unit '
            "\\ :math:`\\mu\\mathrm{s}`"
        ),
        a_nexus_field=NeXusField(
            name="center_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "two-theta",
                "energy",
                "momentum-transfer",
                "d-spacing",
                "channel",
                "time-of-flight",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    sx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-sx-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "First component of the sample position in the sample reference "
            "frame. The sample reference frame is defined by the :ref:`sample "
            "transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_field=NeXusField(
            name="sx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    sy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-sy-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "First component of the sample position in the sample reference "
            "frame. The sample reference frame is defined by the :ref:`sample "
            "transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_field=NeXusField(
            name="sy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    sz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-sz-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "First component of the sample position in the sample reference "
            "frame. The sample reference frame is defined by the :ref:`sample "
            "transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_field=NeXusField(
            name="sz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
