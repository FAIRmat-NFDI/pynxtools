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
# Run `pynx nomad generate-metainfo --nxdl NXdispersive_material` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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
from pynxtools.nomad.metainfo.base_classes.cite import Cite
from pynxtools.nomad.metainfo.base_classes.dispersion import Dispersion
from pynxtools.nomad.metainfo.base_classes.dispersion_function import DispersionFunction
from pynxtools.nomad.metainfo.base_classes.dispersion_repeated_parameter import (
    DispersionRepeatedParameter,
)
from pynxtools.nomad.metainfo.base_classes.dispersion_single_parameter import (
    DispersionSingleParameter,
)
from pynxtools.nomad.metainfo.base_classes.dispersion_table import DispersionTable
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["DispersiveMaterial"]


class DispersiveMaterial(Entry):
    """
    An application definition for describing a dispersive material.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdispersive_material",
            category="application",
        ),
    )

    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialSample",
        repeats=False,
    )
    cite = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialCite",
        repeats=True,
        variable=True,
    )
    dispersion_x = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionX",
        repeats=False,
        description=(
            "The dispersion along the optical axis of the material. This should "
            "be the only dispersion available for isotropic materials. For "
            "uniaxial materials this denotes the ordinary axis. For biaxial "
            "materials this denotes the x axis or epsilon 11 tensor element of "
            "the diagonalized permittivity tensor."
        ),
    )
    dispersion_y = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionY",
        repeats=False,
        description=(
            "This should only be filled for biaxial materials. It denotes the "
            "epsilon 22 direction of the diagonalized permittivity tensor."
        ),
    )
    dispersion_z = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionZ",
        repeats=False,
        description=(
            "This should only be filled for uniaxial or biaxial materials. For "
            "uniaxial materials this denotes the extraordinary axis. For biaxial "
            "materials this denotes the epsilon 33 tensor element of the "
            "diagonalized permittivity tensor."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXdispersive_material"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXdispersive_material"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-definition-version-attribute"
        ],
        description=(
            "Version number to identify which definition of this application "
            "definition was used for this entry/data."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-definition-url-attribute"
        ],
        description=(
            "URL where to find further material (documentation, examples) "
            "relevant to the application definition"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    dispersion_type = Quantity(
        type=MEnum(["measured", "simulated"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-type-field"
        ],
        description=(
            "Denotes whether the dispersion is calculated or derived from an experiment"
        ),
        a_nexus_field=NeXusField(
            name="dispersion_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["measured", "simulated"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class DispersiveMaterialSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="required",
        ),
    )

    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-sample-chemical-formula-field"
        ],
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-sample-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the sample. If the sample substance has multiple "
            "components, all elements from each component must be included in "
            "`atom_types`."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    colloquial_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-sample-colloquial-name-field"
        ],
        description=(
            "The colloquial name of the material, e.g. graphite or diamond for carbon."
        ),
        a_nexus_field=NeXusField(
            name="colloquial_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    material_phase = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-sample-material-phase-field"
        ],
        description=("The phase of the material"),
        a_nexus_field=NeXusField(
            name="material_phase",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["gas", "liquid", "solid"],
            open_enum=True,
        ),
    )
    material_phase_comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-sample-material-phase-comment-field"
        ],
        description=(
            "Additional information about the phase if the material phase is not "
            "from the enumerated list."
        ),
        a_nexus_field=NeXusField(
            name="material_phase_comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    additional_phase_information = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-sample-additional-phase-information-field"
        ],
        description=(
            "This field may be used to denote additional phase information, such "
            "as crystalline phase of a crystal (e.g. 4H or 6H for SiC) or if a "
            "measurement was done on a thin film or bulk material."
        ),
        a_nexus_field=NeXusField(
            name="additional_phase_information",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialCite(Cite):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-references-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcite",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    text = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-references-text-field"
        ],
        description=(
            "A text description of this reference, e.g. `E. Example et al, The "
            "mighty example, An example journal 50 (2023), 100`"
        ),
        a_nexus_field=NeXusField(
            name="text",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    doi = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-references-doi-field"
        ],
        a_nexus_field=NeXusField(
            name="doi",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionX(Dispersion):
    """
    The dispersion along the optical axis of the material. This should be the
    only dispersion available for isotropic materials. For uniaxial materials
    this denotes the ordinary axis. For biaxial materials this denotes the x
    axis or epsilon 11 tensor element of the diagonalized permittivity tensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion",
            name="dispersion_x",
            name_type="specified",
            optionality="required",
        ),
    )

    dispersion_table = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionXDispersionTable",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_table",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    dispersion_function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionXDispersionFunction",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_function",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    plot = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="plot",
            name_type="specified",
            optionality="recommended",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-model-name-field"
        ],
        description=("The name of this dispersion model."),
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionXDispersionTable(DispersionTable):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-table-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_table",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-table-model-name-field"
        ],
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-table-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n + ik", "n - ik"],
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-table-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    dielectric_function = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-table-dielectric-function-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="dielectric_function",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )
    refractive_index = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-table-refractive-index-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="refractive_index",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionXDispersionFunction(DispersionFunction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_function",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    dispersion_single_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionXDispersionFunctionDispersionSingleParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_single_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    dispersion_repeated_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionXDispersionFunctionDispersionRepeatedParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-model-name-field"
        ],
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-formula-field"
        ],
        a_nexus_field=NeXusField(
            name="formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n + ik", "n - ik"],
        ),
    )
    energy_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-energy-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="energy_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    energy_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-energy-unit-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="energy_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    wavelength_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-wavelength-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="wavelength_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wavelength_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-wavelength-unit-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="wavelength_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    representation = Quantity(
        type=MEnum(["n", "eps"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n", "eps"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionXDispersionFunctionDispersionSingleParameter(
    DispersionSingleParameter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-dispersion-single-parameter-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_single_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-dispersion-single-parameter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-dispersion-single-parameter-value-field"
        ],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionXDispersionFunctionDispersionRepeatedParameter(
    DispersionRepeatedParameter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-dispersion-repeated-parameter-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-dispersion-repeated-parameter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-x-dispersion-function-dispersion-repeated-parameter-values-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="values",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionY(Dispersion):
    """
    This should only be filled for biaxial materials. It denotes the epsilon 22
    direction of the diagonalized permittivity tensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion",
            name="dispersion_y",
            name_type="specified",
            optionality="optional",
        ),
    )

    dispersion_table = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionYDispersionTable",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_table",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    dispersion_function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionYDispersionFunction",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_function",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    plot = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="plot",
            name_type="specified",
            optionality="recommended",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-model-name-field"
        ],
        description=("The name of this dispersion model."),
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionYDispersionTable(DispersionTable):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-table-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_table",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-table-model-name-field"
        ],
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-table-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n + ik", "n - ik"],
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-table-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    dielectric_function = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-table-dielectric-function-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="dielectric_function",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )
    refractive_index = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-table-refractive-index-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="refractive_index",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionYDispersionFunction(DispersionFunction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_function",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    dispersion_single_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionYDispersionFunctionDispersionSingleParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_single_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    dispersion_repeated_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionYDispersionFunctionDispersionRepeatedParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-model-name-field"
        ],
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-formula-field"
        ],
        a_nexus_field=NeXusField(
            name="formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n + ik", "n - ik"],
        ),
    )
    energy_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-energy-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="energy_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    energy_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-energy-unit-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="energy_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    wavelength_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-wavelength-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="wavelength_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wavelength_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-wavelength-unit-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="wavelength_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    representation = Quantity(
        type=MEnum(["n", "eps"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n", "eps"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionYDispersionFunctionDispersionSingleParameter(
    DispersionSingleParameter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-dispersion-single-parameter-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_single_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-dispersion-single-parameter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-dispersion-single-parameter-value-field"
        ],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionYDispersionFunctionDispersionRepeatedParameter(
    DispersionRepeatedParameter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-dispersion-repeated-parameter-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-dispersion-repeated-parameter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-y-dispersion-function-dispersion-repeated-parameter-values-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="values",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionZ(Dispersion):
    """
    This should only be filled for uniaxial or biaxial materials. For uniaxial
    materials this denotes the extraordinary axis. For biaxial materials this
    denotes the epsilon 33 tensor element of the diagonalized permittivity
    tensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion",
            name="dispersion_z",
            name_type="specified",
            optionality="optional",
        ),
    )

    dispersion_table = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionZDispersionTable",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_table",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    dispersion_function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionZDispersionFunction",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_function",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    plot = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="plot",
            name_type="specified",
            optionality="recommended",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-model-name-field"
        ],
        description=("The name of this dispersion model."),
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionZDispersionTable(DispersionTable):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-table-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_table",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-table-model-name-field"
        ],
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-table-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n + ik", "n - ik"],
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-table-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    dielectric_function = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-table-dielectric-function-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="dielectric_function",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )
    refractive_index = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-table-refractive-index-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="refractive_index",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionZDispersionFunction(DispersionFunction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_function",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    dispersion_single_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionZDispersionFunctionDispersionSingleParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_single_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    dispersion_repeated_parameter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.dispersive_material.DispersiveMaterialDispersionZDispersionFunctionDispersionRepeatedParameter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    model_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-model-name-field"
        ],
        a_nexus_field=NeXusField(
            name="model_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-formula-field"
        ],
        a_nexus_field=NeXusField(
            name="formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    convention = Quantity(
        type=MEnum(["n + ik", "n - ik"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n + ik", "n - ik"],
        ),
    )
    energy_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-energy-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="energy_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    energy_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-energy-unit-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="energy_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    wavelength_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-wavelength-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="wavelength_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    wavelength_unit = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-wavelength-unit-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="wavelength_unit",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    representation = Quantity(
        type=MEnum(["n", "eps"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["n", "eps"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionZDispersionFunctionDispersionSingleParameter(
    DispersionSingleParameter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-dispersion-single-parameter-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_single_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-dispersion-single-parameter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-dispersion-single-parameter-value-field"
        ],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class DispersiveMaterialDispersionZDispersionFunctionDispersionRepeatedParameter(
    DispersionRepeatedParameter
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-dispersion-repeated-parameter-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdispersion_repeated_parameter",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-dispersion-repeated-parameter-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    values = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXdispersive_material.html#nxdispersive_material-entry-dispersion-z-dispersion-function-dispersion-repeated-parameter-values-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="values",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
