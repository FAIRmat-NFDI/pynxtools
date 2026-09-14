# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXxas (see
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
# Run `pynx nomad generate-metainfo --nxdl NXxas` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.hdf5 import HDF5Reference
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
from pynxtools.nomad.metainfo.base_classes.element import Element
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xas"]


class Xas(Entry):
    """
    This is a generic application definition for X-ray absorption spectroscopy.
    Technique-specific application definitions extend this base definition.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxas",
            category="application",
            symbols={
                "nP": "Number of stacked spectra (scan points). This is the growable\n                first dimension: data could be appended along it during acquisition.\n                It is absent when a single spectrum is stored.",
                "nEnergy": "Number of energy data points",
                "dataRank": "Rank of the ``intensity`` field: 1 for a single spectrum\n                ``[nEnergy]`` or 2 for a stack of spectra ``[nP, nEnergy]``.",
            },
        ),
    )

    element = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas.XasElement",
        repeats=False,
    )
    edge = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.absorption_edge.AbsorptionEdge",
        repeats=False,
        description=(
            "The absorption edge being probed, defined by the principal quantum "
            "number and orbital symmetry of the photoionized electron (e.g. K, "
            "L1, L2, L3, L2,3). Together with the element uniquely identifies "
            "probed electronic transition."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXabsorption_edge",
            name="edge",
            name_type="specified",
            optionality="required",
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas.XasSample",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xas.XasData",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXxas"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxas"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxas",
        ),
    )
    is_experimental = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-is-experimental-field"
        ],
        description=(
            "Specify if the data comes from an experiment. Use ``true`` for data "
            "acquired at a beamline or laboratory instrument, and ``false`` for "
            "spectra calculated/simulated using a computational tool, "
            "reconstructed from a linear combination of reference components, "
            "etc."
        ),
        a_nexus_field=NeXusField(
            name="is_experimental",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    energy = Quantity(
        type=HDF5Reference,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-energy-field"
        ],
        description=("The energy axis of the spectrum."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-intensity-field"
        ],
        flexible_unit=True,
        description=(
            "The intensity of the spectrum. The precise definition of what is "
            "meant by intensity depends on the acquisition mode, and will be "
            "specified by each subclass application definition."
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    intensity_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-intensity-errors-field"
        ],
        flexible_unit=True,
        description=("The errors associated with the intensity of the spectrum."),
        a_nexus_field=NeXusField(
            name="intensity_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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


class XasElement(Element):
    """
    The element being probed by the incident X-rays.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-element-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXelement",
            name="element",
            name_type="specified",
            optionality="required",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-element-name-field"
        ],
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


class XasSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-sample-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-sample-name-field"
        ],
        description=("Descriptive name of the sample"),
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
    temperature = Quantity(
        type=HDF5Reference,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-sample-temperature-field"
        ],
        description=("Sample temperature."),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XasData(Data):
    """
    Plot of the X-ray absorption intensity versus energy.

    When several spectra are stacked along ``nP`` (a time series, a spatial
    map, an operando series, ...), the quantity that varies across the stack is
    stored in its standard NeXus location (for example
    ``NXsample/temperature``, ``NXsample/electric_field``, an
    ``NXsample/NXtransformations`` axis, or an ``NXbeam`` polarization field)
    and linked here as an additional axis with its ``AXISNAME_indices`` set to
    0, the ``nP`` dimension. The application definition does not enumerate
    these coordinates: any of them, including ones not listed here, is declared
    simply by adding the field in its base-class location and wiring it into
    this group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    energy = Quantity(
        type=HDF5Reference,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-data-energy-link"
        ],
        a_nexus_link=NeXusLink(
            name="energy",
            target="/NXentry/energy",
            optionality="required",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxas.html#nxxas-entry-data-intensity-link"
        ],
        flexible_unit=True,
        a_nexus_link=NeXusLink(
            name="intensity",
            target="/NXentry/intensity",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
