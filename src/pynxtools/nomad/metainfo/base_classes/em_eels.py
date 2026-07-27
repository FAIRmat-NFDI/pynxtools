# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXem_eels (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXem_eels` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
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
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmEels"]


class EmEels(Process):
    """
    Base class method-specific for Electron Energy Loss Spectroscopy (EELS).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eels.html#nxem_eels"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_eels",
            category="base",
        ),
    )

    zlp_correction = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eels.EmEelsZlpCorrection",
        repeats=False,
    )
    indexing = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eels.EmEelsIndexing",
        repeats=False,
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class EmEelsZlpCorrection(Process):
    """
    Details about computational steps how the zero-loss peak was threaded.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eels.html#nxem_eels-zlp-correction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="zlp_correction",
            name_type="specified",
            optionality="optional",
        ),
    )

    program_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        description=(
            "The program with which the zero-loss peak correction was performed."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEelsIndexing(Process):
    """
    Details about computational steps how peaks were indexed as elements.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eels.html#nxem_eels-indexing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="optional",
        ),
    )

    program_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        description=("The program with which the indexing was performed."),
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    peak = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.peak.Peak",
        repeats=True,
        variable=True,
        description=(
            "Name and location of each peak in the spectrum considered to be of "
            "relevance."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.Spectrum",
        repeats=True,
        variable=True,
        description=("NXspectrum specialized for EELS."),
        a_nexus_group=NeXusGroup(
            nx_class="NXspectrum",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
