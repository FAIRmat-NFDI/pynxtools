# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXinsertion_device (see
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
# Run `pynx nomad generate-metainfo --nxdl NXinsertion_device` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["InsertionDevice"]


class InsertionDevice(Component):
    """
    An insertion device, as used in a synchrotron light source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXinsertion_device",
            category="base",
        ),
    )

    spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("spectrum of insertion device"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum",
            name_type="specified",
            optionality="optional",
        ),
    )
    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=('"Engineering" position of insertion device'),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the device and NXoff_geometry to describe its shape instead",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the beam line component"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    type = Quantity(
        type=MEnum(["undulator", "wiggler", "wavelength_shifter"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-type-field"
        ],
        description=(
            "It is recommended (effective from 2025) to use the "
            '"wavelength_shifter" choice for 3-pole wigglers, while reserving '
            'the generic "wiggler" designation for extended multipole '
            "wigglers."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["undulator", "wiggler", "wavelength_shifter"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-gap-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("separation between opposing pairs of magnetic poles"),
        a_nexus_field=NeXusField(
            name="gap",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    taper = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-taper-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "angular of gap difference between upstream and downstream ends of "
            "the insertion device"
        ),
        a_nexus_field=NeXusField(
            name="taper",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    phase = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-phase-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="phase",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    poles = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-poles-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("number of poles"),
        a_nexus_field=NeXusField(
            name="poles",
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
    magnetic_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-magnetic-wavelength-field"
        ],
        dimensionality="[length]",
        unit="angstrom",
        a_nexus_field=NeXusField(
            name="magnetic_wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "angstrom"},
    )
    k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-k-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("beam displacement parameter"),
        a_nexus_field=NeXusField(
            name="k",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("length of insertion device"),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        unit="watt",
        description=("total power delivered by insertion device"),
        a_nexus_field=NeXusField(
            name="power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_POWER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "watt"},
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("energy of peak intensity in output spectrum"),
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
    bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-bandwidth-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("bandwidth of peak energy"),
        a_nexus_field=NeXusField(
            name="bandwidth",
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
    harmonic = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-harmonic-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("harmonic number of peak"),
        a_nexus_field=NeXusField(
            name="harmonic",
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
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinsertion_device.html#nxinsertion_device-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a insertion device."
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
