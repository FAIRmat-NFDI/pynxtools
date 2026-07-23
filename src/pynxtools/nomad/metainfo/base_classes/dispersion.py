# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXdispersion (see
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
# Run `pynx nomad generate-metainfo --nxdl NXdispersion` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.data import ArchiveSection
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

__all__ = ["Dispersion"]


class Dispersion(Object, ArchiveSection):
    """
    A dispersion denoting a sum of different dispersions. All
    NXdispersion_table and NXdispersion_function groups will be added together
    to form a single dispersion.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion.html#nxdispersion"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdispersion",
            category="base",
        ),
    )

    dispersion_table = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.dispersion_table.DispersionTable",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_table",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    dispersion_function = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.dispersion_function.DispersionFunction",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_function",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion.html#nxdispersion-model-name-field"
        ],
        description=("The name of the composite model."),
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
