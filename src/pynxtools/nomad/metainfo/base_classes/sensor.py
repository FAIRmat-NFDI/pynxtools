# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXsensor (see
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
# Run `pynx nomad generate-metainfo --nxdl NXsensor` to regenerate.
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

__all__ = ["Sensor"]


class Sensor(Component):
    """
    A sensor used to monitor an external condition

    The condition itself is described in :ref:`NXenvironment`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsensor",
            category="base",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=False,
        description=(
            "Defines the axes for logged vector quantities if they are not the "
            "global instrument axes."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="geometry",
            name_type="specified",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the beamstop and NXoff_geometry to describe its shape instead",
        ),
    )
    value_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("Time history of sensor readings"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="value_log",
            name_type="specified",
            optionality="optional",
        ),
    )
    value_deriv1_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("Time history of first derivative of sensor readings"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="value_deriv1_log",
            name_type="specified",
            optionality="optional",
        ),
    )
    value_deriv2_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("Time history of second derivative of sensor readings"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="value_deriv2_log",
            name_type="specified",
            optionality="optional",
        ),
    )
    external_field_full = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.orientation.Orientation",
        repeats=False,
        description=(
            "For complex external fields not satisfied by External_field_brief"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXorientation",
            name="external_field_full",
            name_type="specified",
            optionality="optional",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the sensor when necessary."),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-model-field"
        ],
        description=("Sensor identification code/model number"),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-name-field"
        ],
        description=("Name for the sensor"),
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
    short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-short-name-field"
        ],
        description=("Short name of sensor used e.g. on monitor display program"),
        a_nexus_field=NeXusField(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    attached_to = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-attached-to-field"
        ],
        description=('where sensor is attached to ("sample" | "can")'),
        a_nexus_field=NeXusField(
            name="attached_to",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    measurement = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-measurement-field"
        ],
        description=("name for measured signal"),
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "temperature",
                "pH",
                "magnetic_field",
                "electric_field",
                "current",
                "conductivity",
                "resistance",
                "voltage",
                "pressure",
                "flow",
                "stress",
                "strain",
                "shear",
                "surface_pressure",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-type-field"
        ],
        description=(
            "The type of hardware used for the measurement. Examples "
            "(suggestions but not restrictions): :Temperature: J | K | T | E | R "
            "| S | Pt100 | Rh/Fe :pH: Hg/Hg2Cl2 | Ag/AgCl | ISFET :Ion selective "
            "electrode: specify species; e.g. Ca2+ :Magnetic field: Hall "
            ":Surface pressure: wilhelmy plate"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    run_control = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-run-control-field"
        ],
        description=(
            "Is data collection controlled or synchronised to this quantity: "
            '1=no, 0=to "value", 1=to "value_deriv1", etc.'
        ),
        a_nexus_field=NeXusField(
            name="run_control",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    high_trip_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-high-trip-value-field"
        ],
        flexible_unit=True,
        description=("Upper control bound of sensor reading if using run_control"),
        a_nexus_field=NeXusField(
            name="high_trip_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    low_trip_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-low-trip-value-field"
        ],
        flexible_unit=True,
        description=("Lower control bound of sensor reading if using run_control"),
        a_nexus_field=NeXusField(
            name="low_trip_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-value-field"
        ],
        flexible_unit=True,
        shape=["*"],
        description=("nominal setpoint or average value - need [n] as may be a vector"),
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    value_deriv1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-value-deriv1-field"
        ],
        flexible_unit=True,
        description=(
            "Nominal/average first derivative of value e.g. strain rate - same "
            'dimensions as "value" (may be a vector)'
        ),
        a_nexus_field=NeXusField(
            name="value_deriv1",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    value_deriv2 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-value-deriv2-field"
        ],
        flexible_unit=True,
        description=(
            "Nominal/average second derivative of value - same dimensions as "
            '"value" (may be a vector)'
        ),
        a_nexus_field=NeXusField(
            name="value_deriv2",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    external_field_brief = Quantity(
        type=MEnum(
            [
                "along beam",
                "across beam",
                "transverse",
                "solenoidal",
                "flow shear gradient",
                "flow vorticity",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-external-field-brief-field"
        ],
        a_nexus_field=NeXusField(
            name="external_field_brief",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "along beam",
                "across beam",
                "transverse",
                "solenoidal",
                "flow shear gradient",
                "flow vorticity",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsensor.html#nxsensor-depends-on-field"
        ],
        description=(".. todo:: Add a definition for the reference point of a sensor."),
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
