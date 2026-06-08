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
# Run `pynx nomad generate-metainfo --nxdl NXspm_cantilever` to regenerate.
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
