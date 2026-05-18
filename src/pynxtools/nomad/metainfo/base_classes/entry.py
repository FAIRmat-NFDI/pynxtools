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
# Run `pynx nomad generate-metainfo --nx-class NXentry` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.basesections import Measurement
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.subentry import Subentry
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Entry"]


class Entry(Measurement):
    """
    (**required**) :ref:`NXentry` describes the measurement.

    The top-level NeXus group which contains all the data and associated
    information that comprise a single measurement. It is mandatory that there
    is at least one group of this type in the NeXus file.
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXentry",
            category="base",
            optionality="optional",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryData",
        repeats=True,
        variable=True,
    )
    experiment_documentation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryExperimentDocumentation",
        repeats=True,
    )
    notes = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryNotes",
        repeats=True,
    )
    thumbnail = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryThumbnail",
        repeats=True,
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryUser",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntrySample",
        repeats=True,
        variable=True,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryInstrument",
        repeats=True,
        variable=True,
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryCollection",
        repeats=True,
        variable=True,
    )
    monitor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryMonitor",
        repeats=True,
        variable=True,
    )
    parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryParameters",
        repeats=True,
        variable=True,
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryProcess",
        repeats=True,
        variable=True,
    )
    subentry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntrySubentry",
        repeats=True,
        variable=True,
    )

    default = Quantity(
        type=str,
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
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    IDF_Version = Quantity(
        type=str,
        description=("ISIS Muon IDF_Version"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="IDF_Version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    title = Quantity(
        type=str,
        description=("Extended title for entry"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_identifier = Quantity(
        type=str,
        description=(
            "Unique identifier for the experiment, defined by the facility, "
            "possibly linked to the proposals"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_description = Quantity(
        type=str,
        description=("Brief summary of the experiment, including key objectives."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    collection_identifier = Quantity(
        type=str,
        description=(
            "User or Data Acquisition defined group of NeXus files or NXentry"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="collection_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    collection_description = Quantity(
        type=str,
        description=("Brief summary of the collection, including grouping criteria."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="collection_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    entry_identifier = Quantity(
        type=str,
        description=("Unique identifier for the measurement, defined by the facility."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="entry_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    entry_identifier_uuid = Quantity(
        type=str,
        description=("UUID identifier for the measurement."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="entry_identifier_uuid",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    entry_identifier_uuid__version = Quantity(
        type=str,
        description=("Version of UUID used"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="entry_identifier_uuid",
        ),
    )
    experiment_location = Quantity(
        type=str,
        description=("City and country where the experiment took place"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_location",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_start_date = Quantity(
        type=Datetime,
        description=(
            "Start time of experimental run that includes the current "
            "measurement, for example a beam time."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_start_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_end_date = Quantity(
        type=Datetime,
        description=(
            "End time of experimental run that includes the current measurement, "
            "for example a beam time."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_end_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_institution = Quantity(
        type=str,
        description=("Name of the institution hosting the facility"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_institution",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_facility = Quantity(
        type=str,
        description=("Name of the experimental facility"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_facility",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_laboratory = Quantity(
        type=str,
        description=("Name of the laboratory or beamline"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_laboratory",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    features = Quantity(
        type=str,
        description=(
            "Reserved for future use by NIAC. See "
            "https://github.com/nexusformat/definitions/issues/382"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="features",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition = Quantity(
        type=str,
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    definition__version = Quantity(
        type=str,
        description=("NXDL version number"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
    )
    definition__URL = Quantity(
        type=str,
        description=("URL of NXDL file"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
    )
    definition_local = Quantity(
        type=str,
        description=(
            "Local NXDL schema extended from the entry specified in the "
            "``definition`` field. This contains any locally-defined, additional "
            "fields in the entry."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition_local",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            deprecated="see same field in :ref:`NXsubentry` for preferred use",
        ),
    )
    definition_local__version = Quantity(
        type=str,
        description=("NXDL version number"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition_local",
        ),
    )
    definition_local__URL = Quantity(
        type=str,
        description=("URL of NXDL file"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition_local",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        description=("Starting time of measurement"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        description=("Ending time of measurement"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    duration = Quantity(
        type=np.int64,
        dimensionality="[time]",
        description=("Duration of measurement"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="duration",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    collection_time = Quantity(
        type=np.float64,
        dimensionality="[time]",
        description=(
            "Time transpired actually collecting data i.e. taking out time when "
            "collection was suspended due to e.g. temperature out of range"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="collection_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    run_cycle = Quantity(
        type=str,
        description=(
            'Such as "2007-3". Some user facilities organize their beam time '
            "into run cycles."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="run_cycle",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    program_name = Quantity(
        type=str,
        description=("Name of program used to generate this file"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="program_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    program_name__version = Quantity(
        type=str,
        description=("Program version number"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="program_name",
        ),
    )
    program_name__configuration = Quantity(
        type=str,
        description=("configuration of the program"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="configuration",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="program_name",
        ),
    )
    revision = Quantity(
        type=str,
        description=(
            "Revision id of the file due to re-calibration, reprocessing, new "
            "analysis, new instrument definition format, ..."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="revision",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    revision__comment = Quantity(
        type=str,
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="revision",
        ),
    )
    pre_sample_flightpath = Quantity(
        type=np.float64,
        dimensionality="[length]",
        description=(
            "This is the flightpath before the sample position. This can be "
            "determined by a chopper, by the moderator or the source itself. In "
            "other words: it the distance to the component which gives the T0 "
            "signal to the detector electronics. If another component in the "
            "NXinstrument hierarchy provides this information, this should be a "
            "link."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
# Named concept groups — one Section class per group defined in NXentry.
# These are referenced by the SubSections above via string FQNs and resolved
# lazily by NOMAD at __init_metainfo__() time.
# =============================================================================


class EntryData(Data):
    """
    The data group

    .. note:: Before the NIAC2016 meeting [#]_, at least one :ref:`NXdata`
    group was required in each :ref:`NXentry` group. At the NIAC2016 meeting,
    it was decided to make :ref:`NXdata` an optional group in :ref:`NXentry`
    groups for data files that do not use an application definition. It is
    recommended strongly that all NeXus data files provide a NXdata group. It
    is permissible to omit the NXdata group only when defining the default plot
    is not practical or possible from the available data.

    For example, neutron event data may not have anything that makes a useful
    plot without extensive processing.

    Certain application definitions override this decision and require an
    :ref:`NXdata` group in the :ref:`NXentry` group. The ``minOccurs=0``
    attribute in the application definition will indicate the :ref:`NXdata`
    group is optional, otherwise, it is required.

    .. [#] NIAC2016: https://www.nexusformat.org/NIAC2016.html,
    https://github.com/nexusformat/NIAC/issues/16
    """

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntryExperimentDocumentation(Note):
    """
    Description of the full experiment (document in pdf, latex, ...)
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="experiment_documentation",
            name_type="specified",
            optionality="optional",
        ),
    )


class EntryNotes(Note):
    """
    Notes describing entry
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="notes",
            name_type="specified",
            optionality="optional",
        ),
    )


class EntryThumbnail(Note):
    """
    A small image that is representative of the entry. An example of this is a
    640x480 jpeg image automatically produced by a low resolution plot of the
    NXdata.
    """

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="thumbnail",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["image/*"]),
        description=("The mime type should be an ``image/*``"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["image/*"],
            deprecated="Use the `type` field instead",
        ),
    )


class EntryUser(User):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntrySample(Sample):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntryInstrument(Instrument):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntryCollection(Collection):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntryMonitor(Monitor):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntryParameters(Parameters):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntryProcess(Process):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class EntrySubentry(Subentry):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsubentry",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
