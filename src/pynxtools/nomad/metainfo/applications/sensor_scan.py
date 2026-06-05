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
# Run `pynx nomad generate-metainfo --nx-class NXsensor_scan` to regenerate.
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

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample
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
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
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
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXsensor_scan"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXsensor_scan"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-definition-version-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier_experiment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier_collection",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-experiment-description-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-start-time-field"
        ],
        description=("The start time of the experiment."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-end-time-field"
        ],
        description=("The end time of the experiment."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
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
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )
    program_quantity__program_url = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-process-program-program-url-attribute"
        ],
        description=("Website of the software."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="program_url",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
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

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-name-field"
        ],
        description=("Name of the user."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="affiliation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="address",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    email = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-email-field"
        ],
        description=("Email address of the user."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="email",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    orcid = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-orcid-field"
        ],
        description=("Author ID defined by https://orcid.org/."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="orcid",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    telephone_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-user-telephone-number-field"
        ],
        description=("Official telephone number of the user."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="telephone_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
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

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsensor_scan.html#nxsensor_scan-entry-sample-name-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
