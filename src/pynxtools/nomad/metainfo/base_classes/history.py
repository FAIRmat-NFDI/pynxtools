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
# Run `pynx nomad generate-metainfo --nxdl NXhistory` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

from nomad.metainfo import Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["History"]


class History(Object):
    """
    A set of activities that occurred to a physical entity prior/during
    experiment.

    Ideally, a full report of the previous operations (or links to a chain of
    operations). Alternatively, notes allow for additional descriptors in any
    format.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXhistory.html#nxhistory"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXhistory",
            category="base",
        ),
    )

    activity = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.activity.Activity",
        repeats=True,
        variable=True,
        description=(
            "Any activity that was performed on the physical entity prior or "
            "during the experiment."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXactivity",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=(
            "A descriptor to keep track of the treatment of the physical entity "
            "before or during the experiment (NXnote allows to add pictures, "
            "audio, movies). Alternatively, a reference to the location or a "
            "unique identifier or other metadata file. In the case these are not "
            "available, free-text description. This should only be used in case "
            "that there is no rigorous description using the base classes above. "
            "This group can also be used to pull in any activities that are not "
            "well described by an existing base class definition. Any number of "
            "instances of NXnote are allowed for describing extra details of "
            "this activity."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    identifierNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXhistory.html#nxhistory-identifiername-field"
        ],
        variable=True,
        description=(
            "An ID or reference to the location or a unique (globally "
            "persistent) identifier of e.g. another file which gives as many as "
            "possible details of the history event."
        ),
        a_nexus_field=NeXusField(
            name="identifierNAME",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
