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
# Run `pynx nomad generate-metainfo --nxdl NXstxm` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.monitor import Monitor
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Stxm"]


class Stxm(Entry):
    """
    Application definition for a STXM instrument.

    The interferometer position measurements, monochromator photon energy
    values and detector measurements are all treated as NXdetectors and stored
    within the NXinstrument group as lists of values stored in chronological
    order. The NXdata group then holds another version of the data in a regular
    3D array (NumE by NumY by NumX, for a total of nP points in a sample image
    stack type scan). The former data values should be stored with a minimum
    loss of precision, while the latter values can be simplified and/or
    approximated in order to fit the constraints of a regular 3D array. 'Line
    scans' and 'point spectra' are just sample_image scan types with reduced
    dimensions in the same way as single images have reduced E dimensions
    compared to image 'stacks'.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXstxm",
            category="application",
            symbols={
                "nP": "Total number of scan points",
                "nE": "Number of photon energies scanned",
                "nX": "Number of pixels in X direction",
                "nY": "Number of pixels in Y direction",
                "detectorRank": "Rank of data array provided by the detector for a single measurement",
            },
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
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stxm.StxmSample",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stxm.StxmData",
        repeats=True,
        variable=True,
    )
    control = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stxm.StxmControl",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-start-time-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXstxm"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXstxm"],
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


class StxmSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-sample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StxmData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    stxm_scan_type = Quantity(
        type=MEnum(
            [
                "sample point spectrum",
                "sample line spectrum",
                "sample image",
                "sample image stack",
                "sample focus",
                "osa image",
                "osa focus",
                "detector image",
                "generic scan",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-data-stxm-scan-type-field"
        ],
        description=(
            "Label for typical scan types as a convenience for humans. Each "
            "label corresponds to a specific set of axes being scanned to "
            "produce a data array of shape: * sample point spectrum: "
            "(photon_energy,) * sample line spectrum: (photon_energy, "
            "sample_y/sample_x) * sample image: (sample_y, sample_x) * sample "
            "image stack: (photon_energy, sample_y, sample_x) * sample focus: "
            "(zoneplate_z, sample_y/sample_x) * osa image: (osa_y, osa_x) * osa "
            "focus: (zoneplate_z, osa_y/osa_x) * detector image: (detector_y, "
            'detector_x) The "generic scan" string is to be used when none of '
            "the other choices are appropriate."
        ),
        a_nexus_field=NeXusField(
            name="stxm_scan_type",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
            enumeration=[
                "sample point spectrum",
                "sample line spectrum",
                "sample image",
                "sample image stack",
                "sample focus",
                "osa image",
                "osa focus",
                "detector image",
                "generic scan",
            ],
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-data-data-field"
        ],
        description=(
            "Detectors that provide more than one value per scan point should be "
            "summarised to a single value per scan point for this array in order "
            "to simplify plotting. Note that 'Line scans' and focus type scans "
            "measure along one spatial dimension but are not restricted to being "
            "parallel to the X or Y axes. Such scans should therefore use a "
            "single dimension for the positions along the spatial line. The "
            "'sample_x' and 'sample_y' fields should then contain lists of the "
            "x- and y-positions and should both have the 'axis' attribute "
            "pointing to the same dimension."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-data-energy-field"
        ],
        shape=["*"],
        description=(
            "List of photon energies of the X-ray beam. If scanned through "
            "multiple values, then an 'axis' attribute will be required to link "
            "the field to the appropriate data array dimension."
        ),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    sample_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-data-sample-y-field"
        ],
        shape=["*"],
        description=(
            "List of Y positions on the sample. If scanned through multiple "
            "values, then an 'axis' attribute will be required to link the field "
            "to the appropriate data array dimension."
        ),
        a_nexus_field=NeXusField(
            name="sample_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    sample_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-data-sample-x-field"
        ],
        shape=["*"],
        description=(
            "List of X positions on the sample. If scanned through multiple "
            "values, then an 'axis' attribute will be required to link the field "
            "to the appropriate data array dimension."
        ),
        a_nexus_field=NeXusField(
            name="sample_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StxmControl(Monitor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-control-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmonitor",
            name="control",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstxm.html#nxstxm-entry-control-data-field"
        ],
        description=(
            "Values to use to normalise for time-variations in photon flux. "
            "Typically, the synchrotron storage ring electron beam current is "
            "used as a proxy for the X-ray beam intensity. Array must have same "
            "shape as the NXdata groups."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
