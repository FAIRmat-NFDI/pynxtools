# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXtestBase (see
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
# Run `pynx nomad generate-metainfo --nxdl NXtestBase` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Testbase"]


class Testbase(Object):
    """
    Minimal base class used as a controlled fixture in converter unit tests.
    Not part of the NeXus standard definitions. Covers: NX_CHAR, NX_FLOAT with
    units, NX_INT, NX_BOOLEAN, closed and open enumerations, dimensions,
    flexible and transformation units, named, partial and anonymous groups and
    fields, a field name clashing with a group inherited from NXobject, a link,
    and a group-level attribute — the key structural features exercised by the
    NXDL-to-metainfo converter.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtestBase",
            category="base",
            symbols={"n": "number of points in the sampled fields"},
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("Primary data group (tests group → SubSection mapping)."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="optional",
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=True,
        variable=True,
        description=(
            "An anonymous, variadic subgroup (tests unnamed group → SubSection "
            "mapping)."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sampleID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.Sample",
        repeats=True,
        variable=True,
        description=(
            "A named, partial, variadic subgroup (tests partial nameType on a group)."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sampleID",
            name_type="partial",
            optionality="optional",
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-label-field"
        ],
        description=("A text label field (tests NX_CHAR → str mapping)."),
        a_nexus_field=NeXusField(
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("An energy value (tests NX_FLOAT + unit → np.float64 mapping)."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    count = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-count-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("An integer count (tests NX_INT → np.int64 mapping)."),
        a_nexus_field=NeXusField(
            name="count",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    flag = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-flag-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("A boolean flag (tests NX_BOOLEAN → bool mapping)."),
        a_nexus_field=NeXusField(
            name="flag",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    mode = Quantity(
        type=MEnum(["fast", "slow", "medium"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-mode-field"
        ],
        description=("Operating mode (tests closed enumeration → MEnum mapping)."),
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["fast", "slow", "medium"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    quality = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-quality-field"
        ],
        description=(
            "Quality rating (tests open enumeration → plain type with items kept)."
        ),
        a_nexus_field=NeXusField(
            name="quality",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["good", "poor"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    sampled_values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-sampled-values-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("A one-dimensional field (tests dimensions → shape conversion)."),
        a_nexus_field=NeXusField(
            name="sampled_values",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    scale_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-scale-factor-field"
        ],
        flexible_unit=True,
        description=(
            "A value in any unit (tests NX_ANY → flexible_unit in the schema)."
        ),
        a_nexus_field=NeXusField(
            name="scale_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-offset-field"
        ],
        description=(
            "A transformation value (tests NX_TRANSFORMATION → NX_ANY unit mapping)."
        ),
        a_nexus_field=NeXusField(
            name="offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    collection_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-collection-field"
        ],
        description=(
            "A field whose name collides with the anonymous NXcollection group "
            "inherited from NXobject (tests the field-versus-group rename rule)."
        ),
        a_nexus_field=NeXusField(
            name="collection",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    labelID = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-labelid-field"
        ],
        variable=True,
        description=(
            "A named, partial, variadic field (tests partial nameType on a field)."
        ),
        a_nexus_field=NeXusField(
            name="labelID",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-version-attribute"
        ],
        description=(
            "Schema version string (tests group-level attribute → Quantity mapping)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    energy_link = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtestBase.html#nxtestbase-energy-link-link"
        ],
        description=(
            "A link to another field in this class (tests link → Quantity mapping)."
        ),
        a_nexus_link=NeXusLink(
            name="energy_link",
            target="/NXtestBase/energy",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
