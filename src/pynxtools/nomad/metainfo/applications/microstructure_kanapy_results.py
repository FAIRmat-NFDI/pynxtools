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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_kanapy_results` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.program import Program

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructureKanapyResults"]


class MicrostructureKanapyResults(Entry):
    """
    Application definition for the microstructure generator kanapy from ICAMS
    Bochum.

    * `A. Hartmeier et al.
    <https://joss.theoj.org/papers/10.21105/joss.01732>`_

    A draft application definition to support discussion within the
    infrastructure use case IUC07 of the NFDI-MatWerk consortium of the German
    NFDI working on a data model for documenting simulations of spatiotemporal
    microstructure evolution with scientific software from this community.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_kanapy_results",
            category="application",
            symbols={
                "n_z": "Number of material points along the z axis of the domain.",
                "n_y": "Number of material points along the y axis of the domain.",
                "n_x": "Number of material points along the x axis of the domain.",
                "c": "Number of crystals.",
            },
        ),
    )

    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cs_profiling.CsProfiling",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="optional",
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
            min_occurs=0,
        ),
    )
    program1 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_kanapy_results.MicrostructureKanapyResultsProgram1",
        repeats=False,
    )
    program2 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_kanapy_results.MicrostructureKanapyResultsProgram2",
        repeats=False,
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.microstructure_kanapy_results.MicrostructureKanapyResultsEnvironment",
        repeats=False,
        description=(
            "Programs and libraries representing the computational environment"
        ),
    )
    microstructureID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.Microstructure",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="microstructureID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    definition = Quantity(
        type=MEnum(["NXmicrostructure_kanapy_results"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXmicrostructure_kanapy_results"],
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-description-field"
        ],
        description=(
            "Discouraged free-text field to add further details to the computation."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-start-time-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
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


class MicrostructureKanapyResultsProgram1(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program1-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="program1",
            name_type="specified",
            optionality="required",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program1-program-field"
        ],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program1-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )
    program__url = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program1-program-url-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="url",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureKanapyResultsProgram2(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program2-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="program2",
            name_type="specified",
            optionality="required",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program2-program-field"
        ],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program2-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )
    program__url = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-program2-program-url-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="url",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureKanapyResultsEnvironment(Collection):
    """
    Programs and libraries representing the computational environment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_kanapy_results.html#nxmicrostructure_kanapy_results-entry-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="optional",
        ),
    )

    program = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
