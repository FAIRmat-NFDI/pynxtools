# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXspm_cantilever (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add or
# adjust project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXspm_cantilever` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmCantilever"]


class SpmCantilever(Object):
    """
    A base class to describe the cantilever used in Atomic Force Microscopy
    (AFM).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_cantilever.html#nxspm_cantilever"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_cantilever",
            category="base",
        ),
    )

    cantilever_oscillator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_cantilever_oscillator.SpmCantileverOscillator",
        repeats=False,
        description=("The oscillator of the cantilever."),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_cantilever_oscillator",
            name="cantilever_oscillator",
            name_type="specified",
            optionality="optional",
        ),
    )
    cantilever_config = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spm_cantilever_config.SpmCantileverConfig",
        repeats=False,
        description=(
            "The configuration parameters of the cantilever used in scanning "
            "probe microscopy."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXspm_cantilever_config",
            name="cantilever_config",
            name_type="specified",
            optionality="optional",
        ),
    )
    phase_positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.positioner.Positioner",
        repeats=False,
        description=("The phase positioner of the cantilever."),
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name="phase_positioner",
            name_type="specified",
            optionality="optional",
        ),
    )
    amplitude_positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.positioner.Positioner",
        repeats=False,
        description=("The amplitude positioner of the cantilever."),
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name="amplitude_positioner",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
