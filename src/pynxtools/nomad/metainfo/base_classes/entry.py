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
# Run `pynx nomad generate-metainfo --nxdl NXentry` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo import basesections
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
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Entry"]


class Entry(Object, basesections.Measurement, EntryData):
    """
    (**required**) :ref:`NXentry` describes the measurement.

    The top-level NeXus group which contains all the data and associated
    information that comprise a single measurement. It is mandatory that there
    is at least one group of this type in the NeXus file.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry"
        ],
        categories=[ExperimentCategory],
        a_schema=SchemaAnnotation(enabled=False),
        a_nexus_definition=NeXusDefinition(
            nx_class="NXentry",
            category="base",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        description=(
            "The data group .. note:: Before the NIAC2016 meeting [#]_, at least "
            "one :ref:`NXdata` group was required in each :ref:`NXentry` group. "
            "At the NIAC2016 meeting, it was decided to make :ref:`NXdata` an "
            "optional group in :ref:`NXentry` groups for data files that do not "
            "use an application definition. It is recommended strongly that all "
            "NeXus data files provide a NXdata group. It is permissible to omit "
            "the NXdata group only when defining the default plot is not "
            "practical or possible from the available data. For example, neutron "
            "event data may not have anything that makes a useful plot without "
            "extensive processing. Certain application definitions override this "
            "decision and require an :ref:`NXdata` group in the :ref:`NXentry` "
            "group. The ``minOccurs=0`` attribute in the application definition "
            "will indicate the :ref:`NXdata` group is optional, otherwise, it is "
            "required. .. [#] NIAC2016: "
            "https://www.nexusformat.org/NIAC2016.html, "
            "https://github.com/nexusformat/NIAC/issues/16"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    experiment_documentation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "Description of the full experiment (document in pdf, latex, ...)"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="experiment_documentation",
            name_type="specified",
            optionality="optional",
        ),
    )
    notes = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=("Notes describing entry"),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="notes",
            name_type="specified",
            optionality="optional",
        ),
    )
    thumbnail = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryThumbnail",
        repeats=False,
        description=(
            "A small image that is representative of the entry. An example of "
            "this is a 640x480 jpeg image automatically produced by a low "
            "resolution plot of the NXdata."
        ),
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.Sample",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
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
            optionality="optional",
        ),
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.monitor.Monitor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    subentry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.subentry.Subentry",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsubentry",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-default-attribute"
        ],
        description=(
            ".. index:: find the default plottable data .. index:: plotting .. "
            "index:: default attribute value Declares which :ref:`NXdata` group "
            "contains the data to be shown by default. It is used to resolve "
            "ambiguity when one :ref:`NXdata` group exists. The value "
            ":ref:`names <validItemName>` a child group. If that group itself "
            "has a ``default`` attribute, continue this chain until an "
            ":ref:`NXdata` group is reached. For more information about how "
            "NeXus identifies the default plottable data, see the :ref:`Find "
            "Plottable Data, v3 <Find-Plottable-Data-v3>` section."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    IDF_Version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-idf-version-attribute"
        ],
        description=("ISIS Muon IDF_Version"),
        a_nexus_attribute=NeXusAttribute(
            name="IDF_Version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-title-field"
        ],
        description=("Extended title for entry"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-identifier-field"
        ],
        description=(
            "Unique identifier for the experiment, defined by the facility, "
            "possibly linked to the proposals"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-description-field"
        ],
        description=("Brief summary of the experiment, including key objectives."),
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
    collection_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-collection-identifier-field"
        ],
        description=(
            "User or Data Acquisition defined group of NeXus files or NXentry"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-collection-description-field"
        ],
        description=("Brief summary of the collection, including grouping criteria."),
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
    entry_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-entry-identifier-field"
        ],
        description=("Unique identifier for the measurement, defined by the facility."),
        a_nexus_field=NeXusField(
            name="entry_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    entry_identifier_uuid = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-entry-identifier-uuid-field"
        ],
        description=("UUID identifier for the measurement."),
        a_nexus_field=NeXusField(
            name="entry_identifier_uuid",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    entry_identifier_uuid__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-entry-identifier-uuid-version-attribute"
        ],
        description=("Version of UUID used"),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="entry_identifier_uuid",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_location = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-location-field"
        ],
        description=("City and country where the experiment took place"),
        a_nexus_field=NeXusField(
            name="experiment_location",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_start_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-start-date-field"
        ],
        description=(
            "Start time of experimental run that includes the current "
            "measurement, for example a beam time."
        ),
        a_nexus_field=NeXusField(
            name="experiment_start_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    experiment_end_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-end-date-field"
        ],
        description=(
            "End time of experimental run that includes the current measurement, "
            "for example a beam time."
        ),
        a_nexus_field=NeXusField(
            name="experiment_end_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    experiment_institution = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-institution-field"
        ],
        description=("Name of the institution hosting the facility"),
        a_nexus_field=NeXusField(
            name="experiment_institution",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_facility = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-facility-field"
        ],
        description=("Name of the experimental facility"),
        a_nexus_field=NeXusField(
            name="experiment_facility",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_laboratory = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-experiment-laboratory-field"
        ],
        description=("Name of the laboratory or beamline"),
        a_nexus_field=NeXusField(
            name="experiment_laboratory",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    features = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-features-field"
        ],
        description=(
            "Reserved for future use by NIAC. See "
            "https://github.com/nexusformat/definitions/issues/382"
        ),
        a_nexus_field=NeXusField(
            name="features",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-field"
        ],
        description=(
            "(alternate use: see same field in :ref:`NXsubentry` for preferred) "
            "Official NeXus NXDL schema to which this entry conforms which must "
            "be the name of the NXDL file (case sensitive without the file "
            "extension) that the NXDL schema is defined in. For example the "
            "``definition`` field for a file that conformed to the "
            "*NXarpes.nxdl.xml* definition must contain the string **NXarpes**. "
            "This field is provided so that :ref:`NXentry` can be the overlay "
            "position in a NeXus data file for an application definition and its "
            "set of groups, fields, and attributes. *It is advised* to use "
            ":ref:`NXsubentry`, instead, as the overlay position."
        ),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-version-attribute"
        ],
        description=("NXDL version number"),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-url-attribute"
        ],
        description=("URL of NXDL file"),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition_local = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-local-field"
        ],
        description=(
            "Local NXDL schema extended from the entry specified in the "
            "``definition`` field. This contains any locally-defined, additional "
            "fields in the entry."
        ),
        a_nexus_field=NeXusField(
            name="definition_local",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            deprecated="see same field in :ref:`NXsubentry` for preferred use",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition_local__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-local-version-attribute"
        ],
        description=("NXDL version number"),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition_local",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition_local__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-local-url-attribute"
        ],
        description=("URL of NXDL file"),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition_local",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-start-time-field"
        ],
        description=("Starting time of measurement"),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-end-time-field"
        ],
        description=("Ending time of measurement"),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    duration = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-duration-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Duration of measurement"),
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    collection_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-collection-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Time transpired actually collecting data i.e. taking out time when "
            "collection was suspended due to e.g. temperature out of range"
        ),
        a_nexus_field=NeXusField(
            name="collection_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    run_cycle = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-run-cycle-field"
        ],
        description=(
            'Such as "2007-3". Some user facilities organize their beam time '
            "into run cycles."
        ),
        a_nexus_field=NeXusField(
            name="run_cycle",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    program_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-program-name-field"
        ],
        description=("Name of program used to generate this file"),
        a_nexus_field=NeXusField(
            name="program_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    program_name__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-program-name-version-attribute"
        ],
        description=("Program version number"),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="program_name",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    program_name__configuration = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-program-name-configuration-attribute"
        ],
        description=("configuration of the program"),
        a_nexus_attribute=NeXusAttribute(
            name="configuration",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="program_name",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    revision = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-revision-field"
        ],
        description=(
            "Revision id of the file due to re-calibration, reprocessing, new "
            "analysis, new instrument definition format, ..."
        ),
        a_nexus_field=NeXusField(
            name="revision",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    revision__comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-revision-comment-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="revision",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    pre_sample_flightpath = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-pre-sample-flightpath-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the flightpath before the sample position. This can be "
            "determined by a chopper, by the moderator or the source itself. In "
            "other words: it the distance to the component which gives the T0 "
            "signal to the detector electronics. If another component in the "
            "NXinstrument hierarchy provides this information, this should be a "
            "link."
        ),
        a_nexus_field=NeXusField(
            name="pre_sample_flightpath",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class EntryThumbnail(Note):
    """
    A small image that is representative of the entry. An example of this is a
    640x480 jpeg image automatically produced by a low resolution plot of the
    NXdata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-thumbnail-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="thumbnail",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["image/*"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-thumbnail-type-attribute"
        ],
        description=("The mime type should be an ``image/*``"),
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["image/*"],
            deprecated="Use the `type` field instead",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="image/*",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
