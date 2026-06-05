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
# Run `pynx nomad generate-metainfo --nx-class NXdispersion_function` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
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
        section_def="pynxtools.nomad.metainfo.base_classes.dispersion_repeated_parameter.DispersionRepeatedParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-model-name-field"
        ],
        description=("The name of this dispersion model."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-convention-field"
        ],
        description=("The sign convention being used (n + or - ik)"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["n + ik", "n - ik"],
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="energy_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    energy_min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-energy-min-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("The minimum energy value at which this formula is valid."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="energy_min",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    energy_max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-energy-max-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("The maximum energy value at which this formula is valid."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="energy_max",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    energy_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-energy-unit-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "The energy unit used in the formula. The field value is a scaling "
            "factor for the units attribute. It is recommended to set the field "
            "value to 1 and carry all the unit scaling information in the units "
            "attribute."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="energy_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="wavelength_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    wavelength_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-wavelength-unit-field"
        ],
        dimensionality="[length]",
        description=(
            "The wavelength unit used in the formula. The field value is a "
            "scaling factor for the units attribute. It is recommended to set "
            "the field value to 1 and carry all the unit scaling information in "
            "the units attribute."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="wavelength_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    wavelength_min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-wavelength-min-field"
        ],
        dimensionality="[length]",
        description=("The minimum wavelength value at which this formula is valid."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="wavelength_min",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    wavelength_max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersion_function.html#nxdispersion_function-wavelength-max-field"
        ],
        dimensionality="[length]",
        description=("The maximum wavelength value at which this formula is valid."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="wavelength_max",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["n", "eps"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
