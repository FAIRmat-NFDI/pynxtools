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
# Run `pynx nomad generate-metainfo --nx-class NXcite` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Cite"]


class Cite(Object):
    """
    A literature reference

    Definition to include references for example for detectors, manuals,
    instruments, acquisition or analysis software used.

    The idea would be to include this in the relevant NeXus object:
    :ref:`NXdetector` for detectors, :ref:`NXinstrument` for instruments, etc.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcite.html#nxcite"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcite",
            category="base",
        ),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcite.html#nxcite-description-field"
        ],
        description=(
            "This should describe the reason for including this reference. For "
            "example: The dataset in this group was normalised using the method "
            "which is described in detail in this reference."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    url = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcite.html#nxcite-url-field"
        ],
        description=("URL referencing the document or data."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="url",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    doi = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcite.html#nxcite-doi-field"
        ],
        description=("DOI referencing the document or data."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="doi",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    endnote = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcite.html#nxcite-endnote-field"
        ],
        description=("Bibliographic reference data in EndNote format."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="endnote",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    bibtex = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcite.html#nxcite-bibtex-field"
        ],
        description=("Bibliographic reference data in BibTeX format."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="bibtex",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
