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
# Run `pynx nomad generate-metainfo --nxdl NXmx` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Mx"]


class Mx(Entry):
    """
    functional application definition for macromolecular crystallography
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmx",
            category="application",
            symbols={
                "dataRank": "Rank of the ``data`` field",
                "nP": "Number of scan points",
                "i": "Number of detector pixels in the slowest direction",
                "j": "Number of detector pixels in the second slowest direction",
                "k": "Number of detector pixels in the third slowest direction",
                "m": "Number of channels in the incident beam spectrum, if known",
                "groupIndex": "An array of the hierarchical levels of the parents of detector\n                    elements or groupings of detector elements.\n                    A top-level element or grouping has parent level -1.",
            },
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxData",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxSample",
        repeats=True,
        variable=True,
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxInstrument",
        repeats=True,
        variable=True,
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxSource",
        repeats=True,
        variable=True,
        description=(
            "The neutron or x-ray storage ring/facility. Note, the NXsource base "
            "class has many more fields available, but at present we only "
            "require the name."
        ),
    )

    version = Quantity(
        type=MEnum(["1.0"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-version-attribute"
        ],
        description=(
            "Describes the version of the NXmx definition used to write this "
            "data. This must be a text (not numerical) representation. Such as:: "
            '@version="1.0"'
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["1.0"],
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-start-time-field"
        ],
        description=(
            "ISO 8601 time/date of the first data point collected in UTC, using "
            "the Z suffix to avoid confusion with local time. Note that the time "
            "zone of the beamline should be provided in "
            "NXentry/NXinstrument/time_zone."
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-end-time-field"
        ],
        description=(
            "ISO 8601 time/date of the last data point collected in UTC, using "
            "the Z suffix to avoid confusion with local time. Note that the time "
            "zone of the beamline should be provided in "
            "NXentry/NXinstrument/time_zone. This field should only be filled "
            "when the value is accurately observed. If the data collection "
            "aborts or otherwise prevents accurate recording of the end_time, "
            "this field should be omitted."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time_estimated = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-end-time-estimated-field"
        ],
        description=(
            "ISO 8601 time/date of the last data point collected in UTC, using "
            "the Z suffix to avoid confusion with local time. Note that the time "
            "zone of the beamline should be provided in "
            "NXentry/NXinstrument/time_zone. This field may be filled with a "
            "value estimated before an observed value is available."
        ),
        a_nexus_field=NeXusField(
            name="end_time_estimated",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXmx"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-definition-field"
        ],
        description=("NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmx"],
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


class MxData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-data-data-field"
        ],
        description=(
            "For a dimension-2 detector, the rank of the data array will be 3. "
            "For a dimension-3 detector, the rank of the data array will be 4. "
            "This allows for the introduction of the frame number as the first "
            "index."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )
    data_scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-data-data-scaling-factor-field"
        ],
        description=(
            "An optional scaling factor to apply to the values in ``data``. The "
            "elements in ``data`` are often stored as integers for efficiency "
            "reasons and need further correction, generating floats. The two "
            "fields data_scaling_factor and data_offset allow linear corrections "
            "using the following convention: .. code-block:: corrected_data = "
            "(data + offset) * scaling_factor This formula will derive the "
            "corrected value, when necessary. data_scaling_factor is sometimes "
            "known as gain and data_offset is sometimes known as pedestal or "
            "background, depending on the community. Use these fields to specify "
            "constants that need to be applied to the data to correct it to "
            "physical values. For example, if the detector gain is 10 counts per "
            "photon and a constant background of 400 needs to be subtracted off "
            "the pixels, specify data_scaling_factor as 0.1 and data_offset as "
            "-400 to specify the required conversion from raw counts to "
            "corrected photons. It is implied processing software will apply "
            "these corrections on-the-fly during processing. The rank of these "
            "fields should either be a single value for the full dataset, a "
            "single per-pixel array applied to every image (dimensions (i, j) or "
            "(i, j, k)), or a per-image correction specified with an array whose "
            "slowest rank is nP (dimensions (np, 1), (np, i, j) or (np, i, j, "
            "k)). When omitted, the scaling factor is assumed to be 1."
        ),
        a_nexus_field=NeXusField(
            name="data_scaling_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    data_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-data-data-offset-field"
        ],
        description=(
            "An optional offset to apply to the values in data. When omitted, "
            "the offset is assumed to be 0. See :ref:`data_scaling_factor "
            "</NXmx/ENTRY/DATA/data_scaling_factor-field>` for more information."
        ),
        a_nexus_field=NeXusField(
            name="data_offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
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
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-sample-depends-on-field"
        ],
        description=(
            "This is a requirement to describe for any scan experiment. The axis "
            "on which the sample position depends may be stored anywhere, but is "
            "normally stored in the NXtransformations group within the NXsample "
            "group. If there is no goniometer, e.g. with a jet, depends_on "
            'should be set to "."'
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-sample-temperature-field"
        ],
        dimensionality="[temperature]",
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-name-field"
        ],
        description=(
            "Name of instrument. Consistency with the controlled vocabulary "
            "beamline naming in "
            "https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_diffrn_source.pdbx_synchrotron_beamline.html "
            "and "
            "https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_diffrn_source.type.html "
            "is highly recommended."
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity__short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-name-short-name-attribute"
        ],
        description=("Short name for instrument, perhaps the acronym."),
        a_nexus_attribute=NeXusAttribute(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
    )
    time_zone = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-time-zone-field"
        ],
        description=("ISO 8601 time_zone offset from UTC."),
        a_nexus_field=NeXusField(
            name="time_zone",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxSource(Source):
    """
    The neutron or x-ray storage ring/facility. Note, the NXsource base class
    has many more fields available, but at present we only require the name.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-source-name-field"
        ],
        description=(
            "Name of source. Consistency with the naming in "
            "https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_diffrn_source.pdbx_synchrotron_site.html "
            "controlled vocabulary is highly recommended."
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity__short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-source-name-short-name-attribute"
        ],
        description=("short name for source, perhaps the acronym"),
        a_nexus_attribute=NeXusAttribute(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
