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
# Run `pynx nomad generate-metainfo --nxdl NXem_eels` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

from nomad.metainfo import Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup
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
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        description=(
            "Details about computational steps how the zero-loss peak was threaded."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="zlp_correction",
            name_type="specified",
            optionality="optional",
        ),
    )
    indexing = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        description=(
            "Details about computational steps how peaks were indexed as elements."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
