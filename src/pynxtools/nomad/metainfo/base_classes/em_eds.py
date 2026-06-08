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
# Run `pynx nomad generate-metainfo --nxdl NXem_eds` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

from nomad.metainfo import Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmEds"]


class EmEds(Process):
    """
    Base class method-specific for energy-dispersive X-ray spectroscopy
    (EDS/EDXS).

    `IUPAC instead of Siegbahn notation
    <https://doi.org/10.1002/xrs.1300200308>`_ should be used.

    X-ray spectroscopy is a surface-sensitive technique. Therefore,
    three-dimensional elemental characterization requires typically a sequence
    of characterization and preparation of the surface to expose new surface
    layer that can be characterized in the next acquisition. In effect, the
    resulting three-dimensional elemental information mappings are truly the
    result of a correlation and post-processing of several measurements which
    is the field of correlative tomographic usage of electron microscopy.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_eds",
            category="base",
            symbols={
                "n_photon_energy": "Number of X-ray photon energy (bins)",
                "n_elements": "Number of identified elements",
                "n_peaks": "Number of peaks detected",
                "n_iupac_line_names": "Number of IUPAC line names",
            },
        ),
    )

    indexing = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEdsIndexing",
        repeats=False,
        description=(
            "Details about computational steps how peaks were indexed as elements."
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


class EmEdsIndexing(Process):
    """
    Details about computational steps how peaks were indexed as elements.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="optional",
        ),
    )

    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_eds.html#nxem_eds-indexing-atom-types-field"
        ],
        description=(
            "Comma-separated list of symbols for elements from the periodic "
            "table that have been confirmed present by the here reported EDS "
            "analysis. This field can be used when creating instances of "
            ":ref:`NXpeak` is not desired. However, a collection of instances of "
            "NXpeak with individual NXatom can be used to add isotopic "
            "information and other relevant context."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
