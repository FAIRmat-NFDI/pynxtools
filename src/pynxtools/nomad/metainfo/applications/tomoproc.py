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
# Run `pynx nomad generate-metainfo --nxdl NXtomoproc` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Tomoproc"]


class Tomoproc(Entry):
    """
    This is an application definition for the final result of a tomography
    experiment: a 3D construction of some volume of physical properties.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtomoproc",
            category="application",
            symbols={
                "nX": "Number of voxels in X direction",
                "nY": "Number of voxels in Y direction",
                "nZ": "Number of voxels in Z direction",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomoproc.TomoprocInstrument",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomoproc.TomoprocSample",
        repeats=True,
        variable=True,
    )
    reconstruction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomoproc.TomoprocReconstruction",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomoproc.TomoprocData",
        repeats=False,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition = Quantity(
        type=MEnum(["NXtomoproc"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXtomoproc"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXtomoproc",
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


class TomoprocInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomoproc.TomoprocInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomoprocInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-instrument-source-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "Spallation Neutron Source",
                "Pulsed Reactor Neutron Source",
                "Reactor Neutron Source",
                "Synchrotron X-ray Source",
                "Pulsed Muon Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "UV Laser",
                "Free-Electron Laser",
                "Optical Laser",
                "Ion Source",
                "UV Plasma Source",
                "Metal Jet X-ray",
                "Laser",
                "Dye Laser",
                "Broadband Tunable Light Source",
                "Halogen Lamp",
                "LED",
                "Mercury Cadmium Telluride Lamp",
                "Deuterium Lamp",
                "Xenon Lamp",
                "Globar",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-instrument-source-name-field"
        ],
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
    probe = Quantity(
        type=MEnum(["neutron", "x-ray", "electron"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-instrument-source-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["neutron", "x-ray", "electron"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomoprocSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-sample-name-field"
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomoprocReconstruction(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-reconstruction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="reconstruction",
            name_type="specified",
            optionality="required",
        ),
    )

    parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.tomoproc.TomoprocReconstructionParameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="parameters",
            name_type="specified",
            optionality="required",
        ),
    )

    program_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-reconstruction-program-field"
        ],
        description=("Name of the program used for reconstruction"),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-reconstruction-version-field"
        ],
        description=("Version of the program used"),
        a_nexus_field=NeXusField(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-reconstruction-date-field"
        ],
        description=("Date and time of reconstruction processing."),
        a_nexus_field=NeXusField(
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomoprocReconstructionParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-reconstruction-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="parameters",
            name_type="specified",
            optionality="required",
        ),
    )

    raw_file = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-reconstruction-parameters-raw-file-field"
        ],
        description=("Original raw data file this data was derived from"),
        a_nexus_field=NeXusField(
            name="raw_file",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TomoprocData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-data-field"
        ],
        shape=["*", "*", "*"],
        description=(
            "This is the reconstructed volume. This can be different things. "
            "Please indicate in the unit attribute what physical quantity this "
            "really is."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    data_quantity__transform = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-data-transform-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transform",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="data",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    data_quantity__offset = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-data-offset-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="offset",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="data",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    data_quantity__scaling = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-data-scaling-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="scaling",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="data",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-x-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "This is an array holding the values to use for the x-axis of data. "
            "The units must be appropriate for the measurement."
        ),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-y-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "This is an array holding the values to use for the y-axis of data. "
            "The units must be appropriate for the measurement."
        ),
        a_nexus_field=NeXusField(
            name="y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXtomoproc.html#nxtomoproc-entry-data-z-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=(
            "This is an array holding the values to use for the z-axis of data. "
            "The units must be appropriate for the measurement."
        ),
        a_nexus_field=NeXusField(
            name="z",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
