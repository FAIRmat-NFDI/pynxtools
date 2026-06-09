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
# Run `pynx nomad generate-metainfo --nxdl NXarchive` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Archive"]


class Archive(Entry):
    """
    This is a definition for data to be archived by ICAT
    (http://www.icatproject.org/).

    .. text from the icatproject.org site

    the database (with supporting software) that provides an interface to all
    ISIS experimental data and will provide a mechanism to link all aspects of
    ISIS research from proposal through to publication.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXarchive",
            category="application",
        ),
    )

    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.archive.ArchiveUser",
        repeats=False,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.archive.ArchiveInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.archive.ArchiveSample",
        repeats=False,
    )

    index = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-index-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="index",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    experiment_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-experiment-identifier-field"
        ],
        description=("unique identifier for the experiment"),
        a_nexus_field=NeXusField(
            name="experiment_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-experiment-description-field"
        ],
        description=("Brief description of the experiment and its objectives"),
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    collection_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-collection-identifier-field"
        ],
        description=("ID of user or DAQ define group of data files"),
        a_nexus_field=NeXusField(
            name="collection_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    collection_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-collection-description-field"
        ],
        description=("Brief summary of the collection, including grouping criteria"),
        a_nexus_field=NeXusField(
            name="collection_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    entry_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-entry-identifier-field"
        ],
        description=(
            "unique identifier for this measurement as provided by the facility"
        ),
        a_nexus_field=NeXusField(
            name="entry_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-duration-field"
        ],
        dimensionality="[time]",
        description=("TODO: needs documentation"),
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    collection_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-collection-time-field"
        ],
        dimensionality="[time]",
        description=("TODO: needs documentation"),
        a_nexus_field=NeXusField(
            name="collection_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    run_cycle = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-run-cycle-field"
        ],
        description=("TODO: needs documentation"),
        a_nexus_field=NeXusField(
            name="run_cycle",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    revision = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-revision-field"
        ],
        description=(
            "revision ID of this file, may be after recalibration, reprocessing etc."
        ),
        a_nexus_field=NeXusField(
            name="revision",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXarchive"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXarchive"],
        ),
    )
    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-program-field"
        ],
        description=("The program and version used for generating this file"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )
    release_date = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-release-date-field"
        ],
        dimensionality="[time]",
        description=("when this file is to be released into PD"),
        a_nexus_field=NeXusField(
            name="release_date",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
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


class ArchiveUser(User):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-user-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="user",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-user-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    role = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-user-role-field"
        ],
        description=("role of the user"),
        a_nexus_field=NeXusField(
            name="role",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    facility_user_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-user-facility-user-id-field"
        ],
        description=("ID of the user in the facility bureaucracy database"),
        a_nexus_field=NeXusField(
            name="facility_user_id",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ArchiveInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-instrument-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-instrument-description-field"
        ],
        description=("Brief description of the instrument"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ArchiveSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-sample-id-field"
        ],
        description=("Unique database id of the sample"),
        a_nexus_field=NeXusField(
            name="sample_id",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    type = Quantity(
        type=MEnum(
            [
                "sample",
                "sample+can",
                "calibration sample",
                "normalisation sample",
                "simulated data",
                "none",
                "sample_environment",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "sample",
                "sample+can",
                "calibration sample",
                "normalisation sample",
                "simulated data",
                "none",
                "sample_environment",
            ],
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-chemical-formula-field"
        ],
        description=("Chemical formula formatted according to CIF conventions"),
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    preparation_date = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-preparation-date-field"
        ],
        dimensionality="[time]",
        a_nexus_field=NeXusField(
            name="preparation_date",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    situation = Quantity(
        type=MEnum(
            [
                "air",
                "vacuum",
                "inert atmosphere",
                "oxidising atmosphere",
                "reducing atmosphere",
                "sealed can",
                "other",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-situation-field"
        ],
        description=(
            "Description of the environment the sample is in: air, vacuum, "
            "oxidizing atmosphere, dehydrated, etc."
        ),
        a_nexus_field=NeXusField(
            name="situation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "air",
                "vacuum",
                "inert atmosphere",
                "oxidising atmosphere",
                "reducing atmosphere",
                "sealed can",
                "other",
            ],
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-temperature-field"
        ],
        dimensionality="[temperature]",
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )
    magnetic_field_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-magnetic-field-field"
        ],
        dimensionality="[current]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="magnetic_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_CURRENT",
        ),
    )
    electric_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-electric-field-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="electric_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
    )
    stress_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-stress-field-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="stress_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXarchive.html#nxarchive-entry-sample-pressure-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_PRESSURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
