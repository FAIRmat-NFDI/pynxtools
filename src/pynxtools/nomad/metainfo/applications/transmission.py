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
# Run `pynx nomad generate-metainfo --nx-class NXtransmission` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Transmission"]


class Transmission(Entry):
    """
    Application definition for transmission experiments
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtransmission",
            category="application",
            symbols={
                "N_wavelengths": "Number of wavelength points",
                "N_scans": "Number of scans",
            },
        ),
    )

    acquisition_program = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionAcquisitionProgram",
        repeats=False,
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionUser",
        repeats=True,
        variable=True,
        description=(
            "Contact information of at least the user of the instrument or the "
            "investigator who performed this experiment. Adding multiple users "
            "if relevant is recommended."
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionSample",
        repeats=True,
        variable=True,
        description=("Properties of the sample measured"),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.transmission.TransmissionData",
        repeats=False,
        description=(
            "A default view of the data emitted intensity vs. wavelength. From "
            "measured_data plot intensity and wavelength."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXtransmission"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-definition-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXtransmission"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-definition-version-attribute"
        ],
        description=(
            "Version number to identify which definition of this application "
            "definition was used for this entry/data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-definition-url-attribute"
        ],
        description=(
            "URL where to find further material (documentation, examples) "
            "relevant to the application definition."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-start-time-field"
        ],
        description=("Start time of the experiment."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    experiment_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-experiment-identifier-field"
        ],
        description=(
            "Unique identifier of the experiment, such as a (globally "
            "persistent) unique identifier. * The identifier is usually defined "
            "by the facility or principle investigator. * The identifier enables "
            "to link experiments to e.g. proposals."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-experiment-description-field"
        ],
        description=(
            "An optional free-text description of the experiment. However, "
            "details of the experiment should be defined in the specific fields "
            "of this application definition rather than in this experiment "
            "description."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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


class TransmissionAcquisitionProgram(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="acquisition_program",
            name_type="specified",
            optionality="optional",
        ),
    )

    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-model-field"
        ],
        description=(
            "Commercial or otherwise defined given name to the program that was "
            "used to generate the result file(s) with measured data and "
            "metadata."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-identifier-field"
        ],
        description=(
            "Version number of the program that was used to generate the result "
            "file(s) with measured data and metadata."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    url = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-acquisition-program-url-attribute"
        ],
        description=("Website of the software"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="url",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionUser(User):
    """
    Contact information of at least the user of the instrument or the
    investigator who performed this experiment. Adding multiple users if
    relevant is recommended.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-user-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-user-name-field"
        ],
        description=("Name of the user."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    affiliation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-user-affiliation-field"
        ],
        description=(
            "Name of the affiliation of the user at the point in time when the "
            "experiment was performed."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="affiliation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    common_beam_depolarizer = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-common-beam-depolarizer-field"
        ],
        description=("If true, the incident beam is depolarized."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="common_beam_depolarizer",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    polarizer_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-polarizer-field"
        ],
        dimensionality="[angle]",
        description=("Polarizer value inside the beam path"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="polarizer",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    time_points = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-time-points-field"
        ],
        dimensionality="[time]",
        shape=["*"],
        description=("An array of relative scan start time points."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="time_points",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    measured_data = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-instrument-measured-data-field"
        ],
        shape=["*", "*"],
        description=(
            "Resulting data from the measurement. The length of the 2nd "
            "dimension is the number of time points. If it has length one the "
            "time_points may be empty."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="measured_data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionSample(Sample):
    """
    Properties of the sample measured
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-sample-name-field"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TransmissionData(Data):
    """
    A default view of the data emitted intensity vs. wavelength. From
    measured_data plot intensity and wavelength.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXtransmission.html#nxtransmission-entry-data-axes-attribute"
        ],
        shape=["*"],
        description=(
            "We recommend to use wavelength as a default attribute, but it can "
            "be replaced by any suitable parameter along the X-axis."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
