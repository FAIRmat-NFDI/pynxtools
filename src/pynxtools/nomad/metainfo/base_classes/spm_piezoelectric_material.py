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
# Run `pynx nomad generate-metainfo --nxdl NXspm_piezoelectric_material` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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
from pynxtools.nomad.metainfo.base_classes.crystal import Crystal

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["SpmPiezoelectricMaterial"]


class SpmPiezoelectricMaterial(Crystal):
    """
    Description and properties of the piezoelectric actuator materials. The
    piezoelectric actuator is usually composed of polycrystalline solids and
    attached at the head of the tip or cantilever. The material deforms when
    the external electric field (e.g., electric force) is applied.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspm_piezoelectric_material",
            category="base",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-name-field"
        ],
        description=(
            "The name of the material of the piezo scanner such as Lead "
            "Zirconate Titanates (PZTs)."
        ),
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
    identifier_piezo_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-identifier-piezo-material-field"
        ],
        description=("The identifier of the piezo material."),
        a_nexus_field=NeXusField(
            name="identifier_piezo_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-chemical-formula-field"
        ],
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-type-field"
        ],
        description=(
            "The type of the material of the piezo scanner (e.g. piezoelectric "
            "ceramics, polymer-film piezoelectrics)."
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
    density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-density-field"
        ],
        flexible_unit=True,
        description=("The density of the piezo material."),
        a_nexus_field=NeXusField(
            name="density",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    relative_permittivity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-relative-permittivity-field"
        ],
        flexible_unit=True,
        description=(
            "The relative permittivity (dielectric constant) of the piezo material."
        ),
        a_nexus_field=NeXusField(
            name="relative_permittivity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    D_piezoelectric_constant = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-d-piezoelectric-constant-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "The D_piezoelectric_constant (with substitutable part D) "
            "piezoelectric charge coefficients of the material. The coefficients "
            "describe the electric polarization generated by the applied stress "
            "on the material. Different coefficients correspond to different "
            "relative directions of the polarization and the stress (e.g., d33, "
            "d31)."
        ),
        a_nexus_field=NeXusField(
            name="D_piezoelectric_constant",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    G_voltage_constant = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-g-voltage-constant-field"
        ],
        variable=True,
        flexible_unit=True,
        description=(
            "The constants (with substitutable part G) define the electric field "
            "produced by the external mechanical strain. Different coefficients "
            "correspond to different relative directions of the electric field "
            "and the strain (e.g., g33, g31)."
        ),
        a_nexus_field=NeXusField(
            name="G_voltage_constant",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    K_electromechanical_constant = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-k-electromechanical-constant-field"
        ],
        flexible_unit=True,
        description=(
            "The electromechanical constant measures the efficiency of the "
            "conversion of mechanical energy into electrical energy."
        ),
        a_nexus_field=NeXusField(
            name="K_electromechanical_constant",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    P_pyroelectric_constant = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-p-pyroelectric-constant-field"
        ],
        flexible_unit=True,
        description=(
            "The pyroelectric constant defines the change of the polarization "
            "vector of the piezoelectric material per unit change in "
            "temperature."
        ),
        a_nexus_field=NeXusField(
            name="P_pyroelectric_constant",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    acoustic_impedance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-acoustic-impedance-field"
        ],
        flexible_unit=True,
        description=("The acoustic impedance of the piezo material."),
        a_nexus_field=NeXusField(
            name="acoustic_impedance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    young_modulus = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-young-modulus-field"
        ],
        flexible_unit=True,
        description=("The Young's modulus of the piezo material."),
        a_nexus_field=NeXusField(
            name="young_modulus",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    surface_resistivity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-surface-resistivity-field"
        ],
        flexible_unit=True,
        description=("The surface resistivity of the piezo material."),
        a_nexus_field=NeXusField(
            name="surface_resistivity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    temperature_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-temperature-range-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "The temperature range of the piezo material. This field is "
            "expecting a range of temperatures in an array [min temperature, max "
            "temperature]."
        ),
        a_nexus_field=NeXusField(
            name="temperature_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )
    glass_transition_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXspm_piezoelectric_material.html#nxspm_piezoelectric_material-glass-transition-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "The range of temperature where a piezoelectric hard material "
            "transforms into the viscous state."
        ),
        a_nexus_field=NeXusField(
            name="glass_transition_temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "kelvin"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
