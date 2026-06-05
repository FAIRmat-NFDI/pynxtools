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
# Run `pynx nomad generate-metainfo --nx-class NXdispersion` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Dispersion"]


class Dispersion(Object):
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
