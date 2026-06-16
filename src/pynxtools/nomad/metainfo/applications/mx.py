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
from pynxtools.nomad.metainfo.base_classes.beam import Beam
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.detector_group import DetectorGroup
from pynxtools.nomad.metainfo.base_classes.detector_module import DetectorModule
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
        categories=[ExperimentCategory],
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="1.0",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXmx",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-sample-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
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

    attenuator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxInstrumentAttenuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    detector_group = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxInstrumentDetectorGroup",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector_group",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    beam = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxInstrumentBeam",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxInstrumentAttenuator(Attenuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-attenuator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    attenuator_transmission = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-attenuator-attenuator-transmission-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="attenuator_transmission",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxInstrumentDetectorGroup(DetectorGroup):
    """
    Optional logical grouping of detectors.

    Each detector is represented as an NXdetector with its own detector data
    array. Each detector data array may be further decomposed into array
    sections by use of NXdetector_module groups. Detectors can be grouped
    logically together using NXdetector_group. Groups can be further grouped
    hierarchically in a single NXdetector_group (for example, if there are
    multiple detectors at an endstation or multiple endstations at a facility).
    Alternatively, multiple NXdetector_groups can be provided.

    The groups are defined hierarchically, with names given in the group_names
    field, unique identifying indices given in the field group_index, and the
    level in the hierarchy given in the group_parent field. For example if an
    x-ray detector group, DET, consists of four detectors in a rectangular
    array::

    DTL DTR DLL DLR

    We could have::

    group_names: ["DET", "DTL", "DTR", "DLL", "DLR"] group_index: [1, 2, 3, 4,
    5] group_parent: [-1, 1, 1, 1, 1]
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-group-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector_group",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    group_names = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-group-group-names-field"
        ],
        description=(
            "An array of the names of the detectors or the names of hierarchical "
            "groupings of detectors."
        ),
        a_nexus_field=NeXusField(
            name="group_names",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    group_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-group-group-index-field"
        ],
        shape=["*"],
        description=(
            "An array of unique identifiers for detectors or groupings of "
            "detectors. Each ID is a unique ID for the corresponding detector or "
            "group named in the field group_names. The IDs are positive integers "
            "starting with 1."
        ),
        a_nexus_field=NeXusField(
            name="group_index",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    group_parent = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-group-group-parent-field"
        ],
        shape=["*"],
        description=(
            "An array of the hierarchical levels of the parents of detectors or "
            "groupings of detectors. A top-level grouping has parent level -1."
        ),
        a_nexus_field=NeXusField(
            name="group_parent",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxInstrumentDetector(Detector):
    """
    Normally the detector group will have the name ``detector``. However, in
    the case of multiple detectors, each detector needs a uniquely named
    NXdetector.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
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
    detector_module = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.mx.MxInstrumentDetectorDetectorModule",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector_module",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-data-field"
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
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-description-field"
        ],
        description=("name/manufacturer/model/etc. information."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    time_per_channel = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-time-per-channel-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "For a time-of-flight detector this is the scaling factor to convert "
            "from the numeric value reported to the flight time for a given "
            "measurement."
        ),
        a_nexus_field=NeXusField(
            name="time_per_channel",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*", "*"],
        description=(
            "Distance from the sample to the beam center. Normally this value is "
            "for guidance only, the proper geometry can be found following the "
            "depends_on axis chain, But in appropriate cases where the detector "
            "distance to the sample is observable independent of the axis chain, "
            "that may take precedence over the axis chain calculation."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    distance_derived = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-distance-derived-field"
        ],
        description=(
            "Boolean to indicate if the distance is a derived, rather than a "
            "primary observation. If distance_derived true or is not specified, "
            "the distance is assumed to be derived from detector axis "
            "specifications."
        ),
        a_nexus_field=NeXusField(
            name="distance_derived",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    count_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-count-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=("Elapsed actual counting time."),
        a_nexus_field=NeXusField(
            name="count_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_TIME",
        ),
    )
    beam_center_derived = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-beam-center-derived-field"
        ],
        description=(
            "Boolean to indicate if the distance is a derived, rather than a "
            "primary observation. If true or not provided, that value of "
            "beam_center_derived is assumed to be true."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_derived",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    beam_center_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-beam-center-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the x position where the direct beam would hit the "
            "detector. This is a length and can be outside of the actual "
            "detector. The length can be in physical units or pixels as "
            "documented by the units attribute. Normally, this should be derived "
            "from the axis chain, but the direct specification may take "
            "precedence if it is not a derived quantity."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    beam_center_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-beam-center-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the y position where the direct beam would hit the "
            "detector. This is a length and can be outside of the actual "
            "detector. The length can be in physical units or pixels as "
            "documented by the units attribute. Normally, this should be derived "
            "from the axis chain, but the direct specification may take "
            "precedence if it is not a derived quantity."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    flatfield = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-flatfield-field"
        ],
        description=(
            "Flat field correction data. If provided, it is recommended that it "
            "be compressed."
        ),
        a_nexus_field=NeXusField(
            name="flatfield",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    flatfield_error = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-flatfield-error-field"
        ],
        description=(
            "*** Deprecated form. Use plural form *** Errors of the flat field "
            "correction data. If provided, it is recommended that it be "
            "compressed."
        ),
        a_nexus_field=NeXusField(
            name="flatfield_error",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    flatfield_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-flatfield-errors-field"
        ],
        description=(
            "Errors of the flat field correction data. If provided, it is "
            "recommended that it be compressed."
        ),
        a_nexus_field=NeXusField(
            name="flatfield_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    pixel_mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-pixel-mask-field"
        ],
        shape=["*", "*"],
        description=(
            "The 32-bit pixel mask for the detector. Can be either one mask for "
            "the whole dataset (i.e. an array with indices i, j) or each frame "
            "can have its own mask (in which case it would be an array with "
            "indices nP, i, j). Contains a bit field for each pixel to signal "
            "dead, blind, high or otherwise unwanted or undesirable pixels. They "
            "have the following meaning: * bit 0: gap (pixel with no sensor) * "
            "bit 1: dead * bit 2: under-responding * bit 3: over-responding * "
            "bit 4: noisy * bit 5: -undefined- * bit 6: pixel is part of a "
            "cluster of problematic pixels (bit set in addition to others) * bit "
            "7: -undefined- * bit 8: user defined mask (e.g. around beamstop) * "
            "bits 9-30: -undefined- * bit 31: virtual pixel (corner pixel with "
            "interpolated value) Normal data analysis software would not take "
            "pixels into account when a bit in (mask & 0x0000FFFF) is set. Tag "
            "bit in the upper two bytes would indicate special pixel properties "
            "that normally would not be a sole reason to reject the intensity "
            "value (unless lower bits are set. If the full bit depths is not "
            "required, providing a mask with fewer bits is permissible. If "
            "needed, additional pixel masks can be specified by including "
            "additional entries named pixel_mask_N, where N is an integer. For "
            "example, a general bad pixel mask could be specified in pixel_mask "
            "that indicates noisy and dead pixels, and an additional pixel mask "
            "from experiment-specific shadowing could be specified in "
            "pixel_mask_2. The cumulative mask is the bitwise OR of pixel_mask "
            "and any pixel_mask_N entries. If provided, it is recommended that "
            "it be compressed."
        ),
        a_nexus_field=NeXusField(
            name="pixel_mask",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    bit_depth_readout = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-bit-depth-readout-field"
        ],
        description=("How many bits the electronics record per pixel."),
        a_nexus_field=NeXusField(
            name="bit_depth_readout",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    sensor_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-sensor-material-field"
        ],
        description=(
            "At times, radiation is not directly sensed by the detector. Rather, "
            "the detector might sense the output from some converter like a "
            "scintillator. This is the name of this converter material."
        ),
        a_nexus_field=NeXusField(
            name="sensor_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    sensor_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-sensor-thickness-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "At times, radiation is not directly sensed by the detector. Rather, "
            "the detector might sense the output from some converter like a "
            "scintillator. This is the thickness of this converter material."
        ),
        a_nexus_field=NeXusField(
            name="sensor_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxInstrumentDetectorDetectorModule(DetectorModule):
    """
    Many detectors consist of multiple smaller modules that are operated in
    sync and store their data in a common dataset. To allow consistent parsing
    of the experimental geometry, this application definition requires all
    detectors to define a detector module, even if there is only one.

    This group specifies the hyperslab of data in the data array associated
    with the detector that contains the data for this module. If the module is
    associated with a full data array, rather than with a hyperslab within a
    larger array, then a single module should be defined, spanning the entire
    array.

    Note, the pixel size is given as values in the array fast_pixel_direction
    and slow_pixel_direction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector_module",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    data_origin = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-data-origin-field"
        ],
        description=(
            "A dimension-2 or dimension-3 field which gives the indices of the "
            "origin of the hyperslab of data for this module in the main area "
            "detector image in the parent NXdetector module. The data_origin is "
            "0-based. The frame number dimension (nP) is omitted. Thus the "
            "data_origin field for a dimension-2 dataset with indices (nP, i, j) "
            "will be an array with indices (i, j), and for a dimension-3 dataset "
            "with indices (nP, i, j, k) will be an array with indices (i, j, k). "
            "The :ref:`order <Design-ArrayStorageOrder>` of indices (i, j or i, "
            "j, k) is slow to fast."
        ),
        a_nexus_field=NeXusField(
            name="data_origin",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    data_size = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-data-size-field"
        ],
        description=(
            "Two or three values for the size of the module in pixels in each "
            "direction. Dimensionality and order of indices is the same as for "
            "data_origin."
        ),
        a_nexus_field=NeXusField(
            name="data_size",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    data_stride = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-data-stride-field"
        ],
        description=(
            "Two or three values for the stride of the module in pixels in each "
            "direction. By default the stride is [1,1] or [1,1,1], and this is "
            "the most likely case. This optional field is included for "
            "completeness."
        ),
        a_nexus_field=NeXusField(
            name="data_stride",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    module_offset__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-module-offset-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="module_offset",
            enumeration=["translation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="translation",
        ),
    )
    module_offset__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-module-offset-vector-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="module_offset",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    module_offset__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-module-offset-offset-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="module_offset",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    module_offset__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-module-offset-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="module_offset",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    fast_pixel_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-fast-pixel-direction-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Values along the direction of :ref:`fastest varying "
            "<Design-ArrayStorageOrder>` pixel direction. The direction itself "
            "is given through the vector attribute."
        ),
        a_nexus_field=NeXusField(
            name="fast_pixel_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    fast_pixel_direction__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-fast-pixel-direction-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fast_pixel_direction",
            enumeration=["translation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="translation",
        ),
    )
    fast_pixel_direction__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-fast-pixel-direction-vector-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="fast_pixel_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    fast_pixel_direction__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-fast-pixel-direction-offset-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="fast_pixel_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    fast_pixel_direction__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-fast-pixel-direction-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="fast_pixel_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    slow_pixel_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-slow-pixel-direction-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Values along the direction of :ref:`slowest varying "
            "<Design-ArrayStorageOrder>` pixel direction. The direction itself "
            "is given through the vector attribute."
        ),
        a_nexus_field=NeXusField(
            name="slow_pixel_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    slow_pixel_direction__transformation_type = Quantity(
        type=MEnum(["translation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-slow-pixel-direction-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="slow_pixel_direction",
            enumeration=["translation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="translation",
        ),
    )
    slow_pixel_direction__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-slow-pixel-direction-vector-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="slow_pixel_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    slow_pixel_direction__offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-slow-pixel-direction-offset-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="slow_pixel_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    slow_pixel_direction__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-detector-detector-module-slow-pixel-direction-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="slow_pixel_direction",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MxInstrumentBeam(Beam):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    incident_wavelength_spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="incident_wavelength_spectrum",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )

    flux = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-flux-attribute"
        ],
        description=(
            "Which field contains the measured flux. One of ``flux``, "
            "``total_flux``, ``flux_integrated``, or ``total_flux_integrated``. "
            "Alternatively, the name being indicated could be a link to a "
            "dataset in an NXmonitor group that records per shot beam data."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="flux",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    incident_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-incident-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "In the case of a monochromatic beam this is the scalar wavelength. "
            "Several other use cases are permitted, depending on the presence or "
            "absence of other incident_wavelength_X fields. In the case of a "
            "polychromatic beam this is an array of length **m** of wavelengths, "
            "with the relative weights in ``incident_wavelength_weights``. In "
            "the case of a monochromatic beam that varies shot- to-shot, this is "
            "an array of wavelengths, one for each recorded shot. Here, "
            "``incident_wavelength_weights`` and incident_wavelength_spread are "
            "not set. In the case of a polychromatic beam that varies shot-to- "
            "shot, this is an array of length **m** with the relative weights in "
            "``incident_wavelength_weights`` as a 2D array. In the case of a "
            "polychromatic beam that varies shot-to- shot and where the channels "
            "also vary, this is a 2D array of dimensions **nP** by **m** (slow "
            "to fast) with the relative weights in "
            "``incident_wavelength_weights`` as a 2D array. Note, :ref:`variants "
            "<Design-Variants>` are a good way to represent several of these use "
            "cases in a single dataset, e.g. if a calibrated, single-value "
            "wavelength value is available along with the original spectrum from "
            "which it was calibrated."
        ),
        a_nexus_field=NeXusField(
            name="incident_wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    incident_wavelength_weight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-incident-wavelength-weight-field"
        ],
        description=(
            "In the case of a polychromatic beam this is an array of length "
            "**m** of the relative weights of the corresponding wavelengths in "
            "incident_wavelength. In the case of a polychromatic beam that "
            "varies shot-to- shot, this is a 2D array of dimensions **nP** by "
            "**m** (slow to fast) of the relative weights of the corresponding "
            "wavelengths in incident_wavelength."
        ),
        a_nexus_field=NeXusField(
            name="incident_wavelength_weight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            deprecated="use incident_wavelength_weights, see https://github.com/nexusformat/definitions/issues/837",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    total_flux = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-total-flux-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=(
            "Flux incident on beam plane in photons per second. In other words "
            "this is the :ref:`flux </NXmx/ENTRY/INSTRUMENT/BEAM/flux-field>` "
            "integrated over area. Useful where spatial beam profiles are not "
            "known. In the case of a beam that varies in total flux "
            "shot-to-shot, this is an array of values, one for each recorded "
            "shot."
        ),
        a_nexus_field=NeXusField(
            name="total_flux",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_FREQUENCY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "hertz"},
    )
    flux_integrated = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-flux-integrated-field"
        ],
        dimensionality="1 / [length] ** 2",
        unit="1 / m ** 2",
        description=(
            "Flux density incident on beam plane area in photons per unit area. "
            "In other words this is the :ref:`flux "
            "</NXmx/ENTRY/INSTRUMENT/BEAM/flux-field>` integrated over time. "
            "Useful where temporal beam profiles of flux are not known. In the "
            "case of a beam that varies in flux shot-to-shot, this is an array "
            "of values, one for each recorded shot."
        ),
        a_nexus_field=NeXusField(
            name="flux_integrated",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PER_AREA",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "1 / m ** 2"},
    )
    total_flux_integrated = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-total-flux-integrated-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Flux incident on beam plane in photons. In other words this is the "
            ":ref:`flux </NXmx/ENTRY/INSTRUMENT/BEAM/flux-field>` integrated "
            "over time and area. Useful where temporal beam profiles of flux are "
            "not known. In the case of a beam that varies in total flux "
            "shot-to-shot, this is an array of values, one for each recorded "
            "shot."
        ),
        a_nexus_field=NeXusField(
            name="total_flux_integrated",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    incident_beam_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-incident-beam-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=[2],
        description=(
            "Two-element array of FWHM (if Gaussian or Airy function) or "
            "diameters (if top hat) or widths (if rectangular) of the beam in "
            "the order x, y"
        ),
        a_nexus_field=NeXusField(
            name="incident_beam_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    profile = Quantity(
        type=MEnum(["Gaussian", "Airy", "top-hat", "rectangular"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-profile-field"
        ],
        description=(
            "The beam profile, Gaussian, Airy function, top-hat or rectangular. "
            "The profile is given in the plane of incidence of the beam on the "
            "sample."
        ),
        a_nexus_field=NeXusField(
            name="profile",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["Gaussian", "Airy", "top-hat", "rectangular"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    incident_polarisation_stokes = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-incident-polarisation-stokes-field"
        ],
        shape=["*", 4],
        description=(
            "Polarization vector on entering beamline component using Stokes notation"
        ),
        a_nexus_field=NeXusField(
            name="incident_polarisation_stokes",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            deprecated="use incident_polarization_stokes, see https://github.com/nexusformat/definitions/issues/708",
        ),
    )
    incident_polarization_stokes = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmx.html#nxmx-entry-instrument-beam-incident-polarization-stokes-field"
        ],
        shape=["*", 4],
        description=(
            "Polarization vector on entering beamline component using Stokes "
            "notation. See incident_polarization_stokes in :ref:`NXbeam`"
        ),
        a_nexus_field=NeXusField(
            name="incident_polarization_stokes",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
