# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXcomponent (see
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
# Run `pynx nomad generate-metainfo --nxdl NXcomponent` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
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

__all__ = ["Component"]


class Component(Object, ArchiveSection):
    """
    Base class for components of an instrument - real ones or simulated ones.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcomponent",
            category="base",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    program = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=True,
        variable=True,
        description=(
            "Collection of axis-based translations and rotations to describe the "
            "location and geometry of the component in the instrument. The "
            "dependency chain may however traverse similar groups in other "
            "component groups."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-applied-field"
        ],
        description=("Was the component used?"),
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-name-field"
        ],
        description=("Name of the component."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-description-field"
        ],
        description=(
            "Ideally, use instances of ``identifierNAME`` to point to a resource "
            "that provides further details. If such a resource does not exist or "
            "should not be used, use this free text, although it is not "
            "recommended."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.RichTextEditQuantity,
        ),
    )
    inputs = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-inputs-field"
        ],
        description=(
            "Instance or list of instances of ``NXcomponent`` (or base classes "
            "extending ``NXcomponent``) or ``NXbeam`` that act as input(s) to "
            "this component. Each input should point to the path of the group "
            "acting as input. An example usage would be to chain components "
            "and/or beams together to describe the beam path in an experiment."
        ),
        a_nexus_field=NeXusField(
            name="inputs",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    outputs = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-outputs-field"
        ],
        description=(
            "Instance or list of instances of ``NXcomponent`` (or base classes "
            "extending ``NXcomponent``) or ``NXbeam`` that act as output(s) of "
            "this component. For more information, see :ref:`inputs "
            "</NXcomponent/inputs-field>`."
        ),
        a_nexus_field=NeXusField(
            name="outputs",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcomponent.html#nxcomponent-depends-on-field"
        ],
        description=(
            "Specifies the position of the component by pointing to the last "
            "transformation in the transformation chain that is defined via the "
            "NXtransformations group. NeXus positions components by applying a "
            "set of translations and rotations to apply to the component "
            "starting from 0, 0, 0. The order of these operations is critical "
            "and forms what NeXus calls a dependency chain. The depends_on field "
            "defines the path to the top most operation of the dependency chain "
            'or the string "." if located in the origin. Usually these '
            "operations are stored in a NXtransformations group. But NeXus "
            "allows them to be stored anywhere."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
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
