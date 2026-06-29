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
# Run `pynx nomad generate-metainfo --nxdl NXsensor_scan` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.environment import Environment
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SensorScan"]


class SensorScan(Entry):
    """
    Application definition for a generic scan using sensors.

    In this application definition, times should be specified always together
    with an UTC offset.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsensor_scan",
            category="application",
            symbols={
                "N_scanpoints": "The number of scan points measured in this scan."
            },
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sensor_scan.SensorScanProcess",
        repeats=True,
        variable=True,
        description=(
            "Define the program that was used to generate the results file(s) "
            "with measured data and metadata."
        ),
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sensor_scan.SensorScanUser",
        repeats=True,
        variable=True,
        description=(
            "Contact information of at least the user of the instrument or the "
            "investigator who performed this experiment. Adding multiple users "
            "if relevant is recommended."
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=(
            "Any additional information or notes (e.g. purpose of the "
            "experiment) that might be useful to understand the experiment."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sensor_scan.SensorScanInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sensor_scan.SensorScanSample",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        description=(
            "A scan specific representation of the measured signals as a "
            "function of the independently controlled environment settings. Plot "
            "of every measured signal as a function of the timestamp of when "
            "they have been acquired is also possible."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-default-attribute"
        ],
        description=(
            ".. index:: plotting Declares which child group contains a path "
            "leading to a :ref:`NXdata` group. It is recommended (as of "
            "NIAC2014) to use this attribute to help define the path to the "
            "default dataset to be visualized upon entry. See "
            "https://www.nexusformat.org/2014_How_to_find_default_data.html for "
            "a summary of the discussion."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition = Quantity(
        type=MEnum(["NXsensor_scan"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsensor_scan"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXsensor_scan",
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-definition-version-attribute"
        ],
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
    identifier_experiment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-identifier-experiment-field"
        ],
        description=(
            "The unique identifier for the entry. The identifier is mainly "
            "lab-defined and can be a combination of the sample name, date and "
            "time, experiment condition (such as temperature) or "
            "instrument-generated unique identifier."
        ),
        a_nexus_field=NeXusField(
            name="identifier_experiment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier_collection = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-identifier-collection-field"
        ],
        description=(
            "The unique identifier for the collection. The identifier is used to "
            "group a number of the experiments run upon the same setup and/or "
            "same sample."
        ),
        a_nexus_field=NeXusField(
            name="identifier_collection",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-experiment-description-field"
        ],
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-start-time-field"
        ],
        description=("The start time of the experiment."),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-end-time-field"
        ],
        description=("The end time of the experiment."),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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


class SensorScanProcess(Process):
    """
    Define the program that was used to generate the results file(s) with
    measured data and metadata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    program_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-process-program-field"
        ],
        description=(
            "Commercial or otherwise defined given name of the program (or a "
            "link to the instrument software)."
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
    program_quantity__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-process-program-version-attribute"
        ],
        description=(
            "Either version with build number, commit hash, or description of an "
            "(online) repository where the source code of the program and build "
            "instructions can be found so that the program can be configured in "
            "such a way that result files can be created ideally in a "
            "deterministic manner."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    program_quantity__program_url = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-process-program-program-url-attribute"
        ],
        description=("Website of the software."),
        a_nexus_attribute=NeXusAttribute(
            name="program_url",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SensorScanUser(User):
    """
    Contact information of at least the user of the instrument or the
    investigator who performed this experiment. Adding multiple users if
    relevant is recommended.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-affiliation-field"
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
    address = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-address-field"
        ],
        description=(
            "Full address (street, street number, ZIP, city, country) of the "
            "user's affiliation."
        ),
        a_nexus_field=NeXusField(
            name="address",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    email = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-email-field"
        ],
        description=("Email address of the user."),
        a_nexus_field=NeXusField(
            name="email",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    orcid = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-orcid-field"
        ],
        description=("Author ID defined by https://orcid.org/."),
        a_nexus_field=NeXusField(
            name="orcid",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    telephone_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-telephone-number-field"
        ],
        description=("Official telephone number of the user."),
        a_nexus_field=NeXusField(
            name="telephone_number",
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


class SensorScanInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sensor_scan.SensorScanInstrumentEnvironment",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SensorScanInstrumentEnvironment(Environment):
    """
    Describes an environment setup for the experiment.

    All the setting values of the independently scanned controllers are listed
    under corresponding NXsensor groups. Similarly, separate NXsensor groups
    are used to store the readings from each measurement sensor.

    For example, in a temperature-dependent IV measurement, the temperature and
    voltage must be present as independently scanned controllers and the
    current sensor must also be present with its readings.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.sensor_scan.SensorScanInstrumentEnvironmentSensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    pid_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pid_controller.PidController",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpid_controller",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    independent_controllers = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-independent-controllers-field"
        ],
        description=(
            "A list of names of NXsensor groups used as independently scanned "
            "controllers."
        ),
        a_nexus_field=NeXusField(
            name="independent_controllers",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    measurement_sensors = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-measurement-sensors-field"
        ],
        description=("A list of names of NXsensor groups used as measurement sensors."),
        a_nexus_field=NeXusField(
            name="measurement_sensors",
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


class SensorScanInstrumentEnvironmentSensor(Sensor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-sensor-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-sensor-value-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "For each point in the scan space, either the nominal setpoint of an "
            "independently scanned controller or a representative average value "
            "of a measurement sensor is registered. The length of each sensor's "
            "data value array stored in this group should be equal to the number "
            "of scan points probed in this scan. For every scan point [N], the "
            "corresponding sensor value can be picked from index [N]. This "
            "allows the scan to be made in any order as the user describes above "
            "in the experiment. We get matching values simply using the index of "
            "the scan point."
        ),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    value_timestamp = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-sensor-value-timestamp-field"
        ],
        description=(
            "Timestamp for when the values provided in the value field were "
            "registered. Individual readings can be stored with their timestamps "
            "under value_log. This is to timestamp the nominal setpoint or "
            "average reading values listed above in the value field."
        ),
        a_nexus_field=NeXusField(
            name="value_timestamp",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    run_control = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-sensor-run-control-field"
        ],
        a_nexus_field=NeXusField(
            name="run_control",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    run_control__description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-sensor-run-control-description-attribute"
        ],
        description=(
            "Free-text describing the data acquisition control: an internal "
            "sweep using the built-in functionality of the controller device, or "
            "a set/wait/read/repeat mechanism."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="run_control",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    calibration_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-instrument-environment-sensor-calibration-time-field"
        ],
        description=(
            "ISO8601 datum when calibration was last performed before this "
            "measurement. UTC offset should be specified."
        ),
        a_nexus_field=NeXusField(
            name="calibration_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SensorScanSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-sample-name-field"
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
