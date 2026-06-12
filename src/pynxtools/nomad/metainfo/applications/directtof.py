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
# Run `pynx nomad generate-metainfo --nxdl NXdirecttof` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.applications.tofraw import Tofraw
from pynxtools.nomad.metainfo.base_classes.disk_chopper import DiskChopper
from pynxtools.nomad.metainfo.base_classes.fermi_chopper import FermiChopper
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Directtof"]


class Directtof(Tofraw):
    """
    This is a application definition for raw data from a direct geometry TOF
    spectrometer
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdirecttof",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.directtof.DirecttofInstrument",
        repeats=True,
        variable=True,
        description=(
            "We definitely want the rotation_speed and energy of the chopper. "
            "Thus either a fermi_chopper or a disk_chopper group is required."
        ),
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-start-time-field"
        ],
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXdirecttof"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXdirecttof"],
        ),
    )
    duration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-duration-field"
        ],
        a_nexus_field=NeXusField(
            name="duration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    run_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-run-number-field"
        ],
        a_nexus_field=NeXusField(
            name="run_number",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    pre_sample_flightpath = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtofraw.html#nxtofraw-entry-pre-sample-flightpath-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the flight path before the sample position. This can be "
            "determined by a chopper, by the moderator, or the source itself. In "
            "other words: it is the distance to the component which gives the T0 "
            "signal to the detector electronics. If another component in the "
            "NXinstrument hierarchy provides this information, this should be a "
            "link."
        ),
        a_nexus_field=NeXusField(
            name="pre_sample_flightpath",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
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


class DirecttofInstrument(Instrument):
    """
    We definitely want the rotation_speed and energy of the chopper. Thus
    either a fermi_chopper or a disk_chopper group is required.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    fermi_chopper = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.directtof.DirecttofInstrumentFermiChopper",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfermi_chopper",
            name="fermi_chopper",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )
    disk_chopper = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.directtof.DirecttofInstrumentDiskChopper",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdisk_chopper",
            name="disk_chopper",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DirecttofInstrumentFermiChopper(FermiChopper):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-instrument-fermi-chopper-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfermi_chopper",
            name="fermi_chopper",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )

    rotation_speed = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-instrument-fermi-chopper-rotation-speed-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("chopper rotation speed"),
        a_nexus_field=NeXusField(
            name="rotation_speed",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_FREQUENCY",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-instrument-fermi-chopper-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("energy selected"),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DirecttofInstrumentDiskChopper(DiskChopper):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-instrument-disk-chopper-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdisk_chopper",
            name="disk_chopper",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )

    rotation_speed = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-instrument-disk-chopper-rotation-speed-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        description=("chopper rotation speed"),
        a_nexus_field=NeXusField(
            name="rotation_speed",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_FREQUENCY",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXdirecttof.html#nxdirecttof-entry-instrument-disk-chopper-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("energy selected"),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
