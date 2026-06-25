# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXxasproc (see
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
# Run `pynx nomad generate-metainfo --nxdl NXxasproc` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xasproc"]


class Xasproc(Entry):
    """
    Processed data from XAS. This is energy versus I(incoming)/I(absorbed).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxasproc",
            category="application",
            symbols={"nP": "Number of points"},
        ),
    )

    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xasproc.XasprocSample",
        repeats=True,
        variable=True,
    )
    XAS_data_reduction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xasproc.XasprocXasDataReduction",
        repeats=False,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xasproc.XasprocData",
        repeats=True,
        variable=True,
    )

    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition = Quantity(
        type=MEnum(["NXxasproc"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxasproc"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxasproc",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class XasprocSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-sample-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasprocXasDataReduction(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-xas-data-reduction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="XAS_data_reduction",
            name_type="specified",
            optionality="required",
        ),
    )

    parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xasproc.XasprocXasDataReductionParameters",
        repeats=False,
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-xas-data-reduction-program-field"
        ],
        description=("Name of the program used for reconstruction"),
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-xas-data-reduction-version-field"
        ],
        description=("Version of the program used"),
        a_nexus_field=NeXusField(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-xas-data-reduction-date-field"
        ],
        description=("Date and time of reconstruction processing."),
        a_nexus_field=NeXusField(
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasprocXasDataReductionParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-xas-data-reduction-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="parameters",
            name_type="specified",
            optionality="required",
        ),
    )

    raw_file = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-xas-data-reduction-parameters-raw-file-field"
        ],
        description=("Original raw data file this data was derived from"),
        a_nexus_field=NeXusField(
            name="raw_file",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasprocData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-data-energy-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    energy__min = Quantity(
        type=np.float64,
        description="Minimum of energy, computed over the full array at parse time.",
    )
    energy__max = Quantity(
        type=np.float64,
        description="Maximum of energy, computed over the full array at parse time.",
    )
    energy__size = Quantity(
        type=np.int64,
        description="Number of elements of energy in the HDF5 file.",
    )
    energy__ndim = Quantity(
        type=np.int8,
        description="Number of dimensions of energy in the HDF5 file.",
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxasproc.html#nxxasproc-entry-data-data-field"
        ],
        shape=["*"],
        description=(
            "This is corrected and calibrated I(incoming)/I(absorbed). So it is "
            "the absorption. Expect attribute ``signal=1``"
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    data_quantity__min = Quantity(
        type=np.float64,
        description="Minimum of data_quantity, computed over the full array at parse time.",
    )
    data_quantity__max = Quantity(
        type=np.float64,
        description="Maximum of data_quantity, computed over the full array at parse time.",
    )
    data_quantity__size = Quantity(
        type=np.int64,
        description="Number of elements of data_quantity in the HDF5 file.",
    )
    data_quantity__ndim = Quantity(
        type=np.int8,
        description="Number of dimensions of data_quantity in the HDF5 file.",
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
