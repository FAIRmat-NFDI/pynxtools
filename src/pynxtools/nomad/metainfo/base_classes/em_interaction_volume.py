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
# Run `pynx nomad generate-metainfo --nxdl NXem_interaction_volume` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmInteractionVolume"]


class EmInteractionVolume(Object):
    """
    Base class to describe the volume of interaction for particle-matter
    interaction.

    Computer models like Monte Carlo or molecular dynamics / electron- or
    ion-beam interaction simulations can be used to qualify and (or) quantify
    the shape of the interaction volume. Results of such simulations can be
    summary statistics or single-particle-resolved sets of trajectories.

    Explicit or implicit descriptions of the geometry of this interaction
    volume are possible:

    * An implicit description is via a set of electron/specimen interactions
    represented ideally as trajectory data from the computer simulation. * An
    explicit description is via iso-contour surface using either a simulation
    grid or a triangulated surface mesh of the approximated iso-contour surface
    evaluated at specific threshold values. Iso-contours could be computed from
    electron or particle flux through an imaginary control surface (the
    iso-surface) or energy-levels (e.g. the case of X-rays). Details depend on
    the model. * Another explicit description is via theoretical models which
    may be relevant e.g. for X-ray spectroscopy

    Further details on how the interaction volume can be quantified is
    available in the literature for example:

    * `S. Richter et al. <https://doi.org/10.1088/1757-899X/109/1/012014>`_ *
    `J. Bünger et al. <https://doi.org/10.1017/S1431927622000083>`_ * `J. F.
    Ziegler et al. <https://doi.org/10.1007/978-3-642-68779-2_5>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_interaction_volume.html#nxem_interaction_volume"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_interaction_volume",
            category="base",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
