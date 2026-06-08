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
# Run `pynx nomad generate-metainfo --nx-class NXsubentry` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Subentry"]


class Subentry(Object):
    """
    Group of multiple application definitions for "multi-modal" (e.g.
    SAXS/WAXS) measurements.

    ``NXsubentry`` is a base class virtually identical to :ref:`NXentry` and is
    used as the (overlay) location for application definitions. Use a separate
    ``NXsubentry`` for each application definition.

    To use ``NXsubentry`` with a hypothetical application definition called
    ``NXmyappdef``:

    * Create a group with attribute ``NX_class="NXsubentry"`` * Within that
    group, create a field called ``definition="NXmyappdef"``. * There are two
    optional attributes of definition: ``version`` and ``URL``

    The intended use is to define application definitions for a multi-modal
    (a.k.a. multi-technique) :ref:`NXentry`. Previously, an application
    definition replaced :ref:`NXentry` with its own definition. With the
    increasing popularity of instruments combining multiple techniques for data
    collection (such as SAXS/WAXS instruments), it was recognized the
    application definitions must be entered in the NeXus data file tree as
    children of :ref:`NXentry`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsubentry",
            category="base",
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
        section_def="pynxtools.nomad.metainfo.base_classes.subentry.SubentryThumbnail",
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
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
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

    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-default-attribute"
        ],
        description=(
            ".. index:: find the default plottable data .. index:: plotting .. "
            "index:: default attribute value Declares which :ref:`NXdata` group "
            "contains the data to be shown by default. It is used to resolve "
            "ambiguity when one :ref:`NXdata` group exists. The value "
            ":ref:`names <validItemName>` the default :ref:`NXentry` group. The "
            "value must be the name of a child of the current group. The child "
            "must be a NeXus group or a link to a NeXus group. For more "
            "information about how NeXus identifies the default plottable data, "
            "see the :ref:`Find Plottable Data, v3 <Find-Plottable-Data-v3>` "
            "section."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    IDF_Version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-idf-version-attribute"
        ],
        description=("ISIS Muon IDF_Version"),
        a_nexus_attribute=NeXusAttribute(
            name="IDF_Version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-title-field"
        ],
        description=("Extended title for entry"),
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-experiment-identifier-field"
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
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-experiment-description-field"
        ],
        description=("Brief summary of the experiment, including key objectives."),
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    collection_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-collection-identifier-field"
        ],
        description=(
            "User or Data Acquisition defined group of NeXus files or :ref:`NXentry`"
        ),
        a_nexus_field=NeXusField(
            name="collection_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    collection_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-collection-description-field"
        ],
        description=("Brief summary of the collection, including grouping criteria."),
        a_nexus_field=NeXusField(
            name="collection_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    entry_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-entry-identifier-field"
        ],
        description=("unique identifier for the measurement, defined by the facility."),
        a_nexus_field=NeXusField(
            name="entry_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this subentry conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-definition-version-attribute"
        ],
        description=("NXDL version number"),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-definition-url-attribute"
        ],
        description=("URL of NXDL file"),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
    )
    definition_local = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-definition-local-field"
        ],
        description=(
            "Local NXDL schema extended from the subentry specified in the "
            "``definition`` field. This contains any locally-defined, additional "
            "fields in the subentry."
        ),
        a_nexus_field=NeXusField(
            name="definition_local",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition_local__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-definition-local-version-attribute"
        ],
        description=("NXDL version number"),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition_local",
        ),
    )
    definition_local__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-definition-local-url-attribute"
        ],
        description=("URL of NXDL file"),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition_local",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-start-time-field"
        ],
        description=("Starting time of measurement"),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-end-time-field"
        ],
        description=("Ending time of measurement"),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    duration = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-duration-field"
        ],
        dimensionality="[time]",
        description=("Duration of measurement"),
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    collection_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-collection-time-field"
        ],
        dimensionality="[time]",
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
    )
    run_cycle = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-run-cycle-field"
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
    )
    program_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-program-name-field"
        ],
        description=("Name of program used to generate this file"),
        a_nexus_field=NeXusField(
            name="program_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    program_name__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-program-name-version-attribute"
        ],
        description=("Program version number"),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="program_name",
        ),
    )
    program_name__configuration = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-program-name-configuration-attribute"
        ],
        description=("configuration of the program"),
        a_nexus_attribute=NeXusAttribute(
            name="configuration",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="program_name",
        ),
    )
    revision = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-revision-field"
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
    )
    revision__comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-revision-comment-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="revision",
        ),
    )
    pre_sample_flightpath = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-pre-sample-flightpath-field"
        ],
        dimensionality="[length]",
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


class SubentryThumbnail(Note):
    """
    A small image that is representative of the entry. An example of this is a
    640x480 jpeg image automatically produced by a low resolution plot of the
    NXdata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-thumbnail-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="thumbnail",
            name_type="specified",
            optionality="optional",
        ),
    )

    mime_type = Quantity(
        type=MEnum(["image/*"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsubentry.html#nxsubentry-thumbnail-mime-type-attribute"
        ],
        description=("The value should be an ``image/*``"),
        a_nexus_attribute=NeXusAttribute(
            name="mime_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["image/*"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
