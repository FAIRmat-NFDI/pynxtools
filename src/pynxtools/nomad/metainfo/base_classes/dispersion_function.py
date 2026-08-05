# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXdispersion_function (see
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
# Run `pynx nomad generate-metainfo --nxdl NXdispersion_function` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.dispersion_repeated_parameter import (
    DispersionRepeatedParameter,
)
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["DispersionFunction"]


class DispersionFunction(Object):
    """
    This describes a dispersion function for a material or layer
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdispersion_function",
            category="base",
            symbols={
                "n_repetitions": "The number of repetitions for the repeated parameters"
            },
        ),
    )

    dispersion_single_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.dispersion_single_parameter.DispersionSingleParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_single_parameter",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    dispersion_repeated_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.dispersion_function.DispersionFunctionDispersionRepeatedParameter",
        repeats=True,
        variable=True,
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-model-name-field"
        ],
        description=("The name of this dispersion model."),
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-formula-field"
        ],
        description=(
            "This should be a python parsable function. Here we should provide "
            "which keywords are available and a BNF of valid grammar."
        ),
        a_nexus_field=NeXusField(
            name="formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-convention-field"
        ],
        description=("The sign convention being used (n + or - ik)"),
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["n + ik", "n - ik"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    energy_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-energy-identifier-field"
        ],
        description=(
            "The identifier used to represent energy in the formula. It is "
            "recommended to use `E`."
        ),
        a_nexus_field=NeXusField(
            name="energy_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    energy_min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-energy-min-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("The minimum energy value at which this formula is valid."),
        a_nexus_field=NeXusField(
            name="energy_min",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    energy_max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-energy-max-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("The maximum energy value at which this formula is valid."),
        a_nexus_field=NeXusField(
            name="energy_max",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    energy_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-energy-unit-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=(
            "The energy unit used in the formula. The field value is a scaling "
            "factor for the units attribute. It is recommended to set the field "
            "value to 1 and carry all the unit scaling information in the units "
            "attribute."
        ),
        a_nexus_field=NeXusField(
            name="energy_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    wavelength_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-wavelength-identifier-field"
        ],
        description=(
            "The identifier used to represent wavelength in the formula. It is "
            "recommended to use `lambda`."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    wavelength_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-wavelength-unit-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "The wavelength unit used in the formula. The field value is a "
            "scaling factor for the units attribute. It is recommended to set "
            "the field value to 1 and carry all the unit scaling information in "
            "the units attribute."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    wavelength_min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-wavelength-min-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The minimum wavelength value at which this formula is valid."),
        a_nexus_field=NeXusField(
            name="wavelength_min",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    wavelength_max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-wavelength-max-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The maximum wavelength value at which this formula is valid."),
        a_nexus_field=NeXusField(
            name="wavelength_max",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    representation = Quantity(
        type=MEnum(["n", "eps"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-representation-field"
        ],
        description=(
            "Which representation does the formula evaluate to. This may either "
            "be n for refractive index or eps for dielectric function. The "
            "appropriate token is then to be used inside the formula."
        ),
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["n", "eps"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
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


class DispersionFunctionDispersionRepeatedParameter(DispersionRepeatedParameter):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-dispersion-repeated-parameter-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    parameter_units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-dispersion-repeated-parameter-parameter-units-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="parameter_units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-dispersion-repeated-parameter-values-field"
        ],
        flexible_unit=True,
        shape=["*"],
        a_nexus_field=NeXusField(
            name="values",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
