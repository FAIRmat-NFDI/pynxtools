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
# Run `pynx nomad generate-metainfo --nxdl NXtransmission` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.attenuator import Attenuator
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.grating import Grating
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.resolution import Resolution
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.slit import Slit
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Transmission"]


class Transmission(Entry):
    """
    Application definition for transmission experiments
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtransmission",
            category="application",
            symbols={
                "N_wavelengths": "Number of wavelength points",
                "N_scans": "Number of scans",
            },
        ),
    )

    acquisition_program = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionAcquisitionProgram",
        repeats=False,
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionUser",
        repeats=True,
        variable=True,
        description=(
            "Contact information of at least the user of the instrument or the "
            "investigator who performed this experiment. Adding multiple users "
            "if relevant is recommended."
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionSample",
        repeats=True,
        variable=True,
        description=("Properties of the sample measured"),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionData",
        repeats=False,
        description=(
            "A default view of the data emitted intensity vs. wavelength. From "
            "measured_data plot intensity and wavelength."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXtransmission"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXtransmission"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXtransmission",
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-definition-version-attribute"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-definition-url-attribute"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-start-time-field"
        ],
        description=("Start time of the experiment."),
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
    experiment_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-experiment-identifier-field"
        ],
        description=(
            "Unique identifier of the experiment, such as a (globally "
            "persistent) unique identifier. * The identifier is usually defined "
            "by the facility or principle investigator. * The identifier enables "
            "to link experiments to e.g. proposals."
        ),
        a_nexus_field=NeXusField(
            name="experiment_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-experiment-description-field"
        ],
        description=(
            "An optional free-text description of the experiment. However, "
            "details of the experiment should be defined in the specific fields "
            "of this application definition rather than in this experiment "
            "description."
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class TransmissionAcquisitionProgram(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="acquisition_program",
            name_type="specified",
            optionality="optional",
        ),
    )

    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-model-field"
        ],
        description=(
            "Commercial or otherwise defined given name to the program that was "
            "used to generate the result file(s) with measured data and "
            "metadata."
        ),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-identifier-field"
        ],
        description=(
            "Version number of the program that was used to generate the result "
            "file(s) with measured data and metadata."
        ),
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    url = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-url-attribute"
        ],
        description=("Website of the software"),
        a_nexus_attribute=NeXusAttribute(
            name="url",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionUser(User):
    """
    Contact information of at least the user of the instrument or the
    investigator who performed this experiment. Adding multiple users if
    relevant is recommended.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-user-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-user-name-field"
        ],
        description=("Name of the user."),
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
    affiliation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-user-affiliation-field"
        ],
        description=(
            "Name of the affiliation of the user at the point in time when the "
            "experiment was performed."
        ),
        a_nexus_field=NeXusField(
            name="affiliation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    manufacturer = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="manufacturer",
            name_type="specified",
            optionality="recommended",
        ),
    )
    common_beam_mask = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentCommonBeamMask",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXslit",
            name="common_beam_mask",
            name_type="specified",
            optionality="required",
        ),
    )
    ref_attenuator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentRefAttenuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name="ref_attenuator",
            name_type="specified",
            optionality="required",
        ),
    )
    sample_attenuator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentSampleAttenuator",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name="sample_attenuator",
            name_type="specified",
            optionality="required",
        ),
    )
    spectrometer = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentSpectrometer",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="spectrometer",
            name_type="specified",
            optionality="required",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    common_beam_depolarizer = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-common-beam-depolarizer-field"
        ],
        description=("If true, the incident beam is depolarized."),
        a_nexus_field=NeXusField(
            name="common_beam_depolarizer",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    polarizer_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-polarizer-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Polarizer value inside the beam path"),
        a_nexus_field=NeXusField(
            name="polarizer",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    time_points = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-time-points-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=("An array of relative scan start time points."),
        a_nexus_field=NeXusField(
            name="time_points",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    measured_data = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-measured-data-field"
        ],
        shape=["*", "*"],
        description=(
            "Resulting data from the measurement. The length of the 2nd "
            "dimension is the number of time points. If it has length one the "
            "time_points may be empty."
        ),
        a_nexus_field=NeXusField(
            name="measured_data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentCommonBeamMask(Slit):
    """
    Common beam mask to shape the incident beam
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-common-beam-mask-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXslit",
            name="common_beam_mask",
            name_type="specified",
            optionality="required",
        ),
    )

    y_gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-common-beam-mask-y-gap-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The height of the common beam in percentage of the beam"),
        a_nexus_field=NeXusField(
            name="y_gap",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentRefAttenuator(Attenuator):
    """
    Attenuator in the reference beam
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-ref-attenuator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name="ref_attenuator",
            name_type="specified",
            optionality="required",
        ),
    )

    attenuator_transmission = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-ref-attenuator-attenuator-transmission-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="attenuator_transmission",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentSampleAttenuator(Attenuator):
    """
    Attenuator in the sample beam
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-sample-attenuator-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name="sample_attenuator",
            name_type="specified",
            optionality="required",
        ),
    )

    attenuator_transmission = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-sample-attenuator-attenuator-transmission-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="attenuator_transmission",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentSpectrometer(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="spectrometer",
            name_type="specified",
            optionality="required",
        ),
    )

    spectral_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentSpectrometerSpectralResolution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="spectral_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )
    grating = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentSpectrometerGrating",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXgrating",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "Wavelength value(s) used for the measurement. An array of 1 or more "
            "elements. Length defines N_wavelenghts"
        ),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentSpectrometerSpectralResolution(Resolution):
    """
    Overall spectral resolution of this spectrometer. If several gratings are
    employed the spectral resolution should rather be specified for each
    grating inside the NXgrating group of this spectrometer.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-spectral-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="spectral_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-spectral-resolution-resolution-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentSpectrometerGrating(Grating):
    """
    Diffraction grating, as could be used in a monochromator. If two or more
    gratings were used, define the angular dispersion and the wavelength range
    (min/max wavelength) for each grating and make sure that the wavelength
    ranges do not overlap. The dispersion should be defined for the entire
    wavelength range of the experiment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-grating-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXgrating",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    spectral_resolution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentSpectrometerGratingSpectralResolution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="spectral_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    angular_dispersion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-grating-angular-dispersion-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Dispersion of the grating in nm/mm used."),
        a_nexus_field=NeXusField(
            name="angular_dispersion",
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
    blaze_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-grating-blaze-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The blaze wavelength of the grating used."),
        a_nexus_field=NeXusField(
            name="blaze_wavelength",
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
    wavelength_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-grating-wavelength-range-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[2],
        description=("Wavelength range in which this grating was used"),
        a_nexus_field=NeXusField(
            name="wavelength_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentSpectrometerGratingSpectralResolution(Resolution):
    """
    Overall spectral resolution of the instrument when this grating is used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-grating-spectral-resolution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXresolution",
            name="spectral_resolution",
            name_type="specified",
            optionality="optional",
        ),
    )

    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-spectrometer-grating-spectral-resolution-resolution-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_WAVENUMBER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    slit = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrumentDetectorSlit",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXslit",
            name="slit",
            name_type="specified",
            optionality="required",
        ),
    )

    wavelength_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-detector-wavelength-range-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[2],
        description=("Wavelength range in which this detector was used"),
        a_nexus_field=NeXusField(
            name="wavelength_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    type = Quantity(
        type=MEnum(["PMT", "PbS", "InGaAs"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-detector-type-field"
        ],
        description=("Detector type"),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["PMT", "PbS", "InGaAs"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    response_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-detector-response-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Response time of the detector"),
        a_nexus_field=NeXusField(
            name="response_time",
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
    gain = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-detector-gain-field"
        ],
        description=("Detector gain"),
        a_nexus_field=NeXusField(
            name="gain",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentDetectorSlit(Slit):
    """
    Slit setting used for measurement with this detector
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-detector-slit-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXslit",
            name="slit",
            name_type="specified",
            optionality="required",
        ),
    )

    type = Quantity(
        type=MEnum(["fixed", "servo"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-detector-slit-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["fixed", "servo"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrumentSource(Source):
    """
    The lamp used for illumination
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-source-type-field"
        ],
        description=("The type of lamp, e.g. halogen, D2 etc."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["halogen", "D2"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    spectrum = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-source-spectrum-field"
        ],
        shape=["*"],
        description=("The spectrum of the lamp used"),
        a_nexus_field=NeXusField(
            name="spectrum",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    wavelength_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-source-wavelength-range-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[2],
        description=("Wavelength range in which the lamp was used"),
        a_nexus_field=NeXusField(
            name="wavelength_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionSample(Sample):
    """
    Properties of the sample measured
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-sample-name-field"
        ],
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionData(Data):
    """
    A default view of the data emitted intensity vs. wavelength. From
    measured_data plot intensity and wavelength.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-data-axes-attribute"
        ],
        shape=["*"],
        description=(
            "We recommend to use wavelength as a default attribute, but it can "
            "be replaced by any suitable parameter along the X-axis."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
