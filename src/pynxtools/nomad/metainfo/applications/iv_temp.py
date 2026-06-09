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
# Run `pynx nomad generate-metainfo --nxdl NXiv_temp` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.applications.sensor_scan import SensorScan
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["IvTemp"]


class IvTemp(SensorScan):
    """
    Application definition for temperature-dependent IV curve measurements.

    In this application definition, times should be specified always together
    with an UTC offset.

    This is the application definition describing temperature dependent IV
    curve measurements. For this a temperature is set. After reaching the
    temperature, a voltage sweep is performed. For each voltage a current is
    measured. Then, the next desired temperature is set and an IV measurement
    is performed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXiv_temp",
            category="application",
            symbols={
                "n_different_temperatures": "Number of different temperature setpoints used in the experiment.",
                "n_different_voltages": "Number of different voltage setpoints used in the experiment.",
            },
        ),
    )

    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.iv_temp.IvTempSample",
        repeats=True,
        variable=True,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.iv_temp.IvTempInstrument",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.iv_temp.IvTempData",
        repeats=True,
        variable=True,
        description=(
            "This NXdata should contain separate fields for the current values "
            "at different temperature setpoints, for example current_at_100C. "
            "There should also be two more fields called temperature and voltage "
            "containing the setpoint values. There should also be a field with "
            "an array of rank equal to the number of different temperature "
            "setpoints and each child's dimension equal to the number of voltage "
            "setpoints."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXiv_temp"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXiv_temp"],
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


class IvTempSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-sample-name-field"
        ],
        description=(
            "Descriptive name or ideally (globally) unique persistent identifier."
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-sample-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the sample. If the sample substance has multiple "
            "components, all elements from each component must be included in "
            "`atom_types`. The purpose of the field is to offer materials "
            "database systems an opportunity to parse the relevant elements "
            "without having to interpret these from the sample history or from "
            "other data sources."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class IvTempInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.environment.Environment",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class IvTempData(Data):
    """
    This NXdata should contain separate fields for the current values at
    different temperature setpoints, for example current_at_100C. There should
    also be two more fields called temperature and voltage containing the
    setpoint values. There should also be a field with an array of rank equal
    to the number of different temperature setpoints and each child's dimension
    equal to the number of voltage setpoints.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-data-temperature-field"
        ],
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-data-voltage-field"
        ],
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html#nxiv_temp-entry-data-current-field"
        ],
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
