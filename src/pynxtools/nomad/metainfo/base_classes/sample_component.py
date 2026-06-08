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
# Run `pynx nomad generate-metainfo --nxdl NXsample_component` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
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

__all__ = ["SampleComponent"]


class SampleComponent(Component, basesections.Component):
    """
    One group like this per component can be recorded for a sample consisting
    of multiple components.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsample_component",
            category="base",
            symbols={
                "n_Temp": "number of temperatures",
                "n_eField": "number of values in applied electric field",
                "n_mField": "number of values in applied magnetic field",
                "n_pField": "number of values in applied pressure field",
                "n_sField": "number of values in applied stress field",
            },
        ),
    )

    transmission = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("As a function of Wavelength"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission",
            name_type="specified",
            optionality="optional",
        ),
    )
    history = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.history.History",
        repeats=False,
        description=(
            "A set of physical processes that occurred to the sample component "
            "prior/during experiment."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXhistory",
            name="history",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-name-field"
        ],
        description=("Descriptive name of sample component"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-chemical-formula-field"
        ],
        description=(
            "The chemical formula specified using CIF conventions. Abbreviated "
            "version of CIF standard: * Only recognized element symbols may be "
            "used. * Each element symbol is followed by a 'count' number. A "
            "count of '1' may be omitted. * A space or parenthesis must separate "
            "each cluster of (element symbol + count). * Where a group of "
            "elements is enclosed in parentheses, the multiplier for the group "
            "must follow the closing parentheses. That is, all element and group "
            "multipliers are assumed to be printed as subscripted numbers. * "
            "Unless the elements are ordered in a manner that corresponds to "
            "their chemical structure, the order of the elements within any "
            "group or moiety depends on whether or not carbon is present. * If "
            "carbon is present, the order should be: - C, then H, then the other "
            "elements in alphabetical order of their symbol. - If carbon is not "
            "present, the elements are listed purely in alphabetic order of "
            "their symbol. * This is the *Hill* system used by Chemical "
            "Abstracts."
        ),
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    unit_cell_abc = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-unit-cell-abc-field"
        ],
        dimensionality="[length]",
        shape=[3],
        description=("Crystallography unit cell parameters a, b, and c"),
        a_nexus_field=NeXusField(
            name="unit_cell_abc",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_alphabetagamma = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-unit-cell-alphabetagamma-field"
        ],
        dimensionality="[angle]",
        shape=[3],
        description=("Crystallography unit cell parameters alpha, beta, and gamma"),
        a_nexus_field=NeXusField(
            name="unit_cell_alphabetagamma",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell_volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-unit-cell-volume-field"
        ],
        dimensionality="[length] ** 3",
        description=("Volume of the unit cell"),
        a_nexus_field=NeXusField(
            name="unit_cell_volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )
    sample_orientation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-sample-orientation-field"
        ],
        dimensionality="[angle]",
        shape=[3],
        description=(
            "This will follow the Busing and Levy convention from Acta.Crysta "
            "v22, p457 (1967)"
        ),
        a_nexus_field=NeXusField(
            name="sample_orientation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    orientation_matrix = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-orientation-matrix-field"
        ],
        shape=[3, 3],
        description=(
            "Orientation matrix of single crystal sample component. This will "
            "follow the Busing and Levy convention from Acta.Crysta v22, p457 "
            "(1967)"
        ),
        a_nexus_field=NeXusField(
            name="orientation_matrix",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-mass-field"
        ],
        dimensionality="[mass]",
        description=("Mass of sample component"),
        a_nexus_field=NeXusField(
            name="mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS",
        ),
    )
    density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        description=("Density of sample component"),
        a_nexus_field=NeXusField(
            name="density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    relative_molecular_mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-relative-molecular-mass-field"
        ],
        dimensionality="[mass]",
        description=("Relative Molecular Mass of sample component"),
        a_nexus_field=NeXusField(
            name="relative_molecular_mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-description-field"
        ],
        description=("Description of the sample component"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    volume_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-volume-fraction-field"
        ],
        description=("Volume fraction of component"),
        a_nexus_field=NeXusField(
            name="volume_fraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    scattering_length_density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-scattering-length-density-field"
        ],
        dimensionality="1 / [length] ** 2",
        description=("Scattering length density of component"),
        a_nexus_field=NeXusField(
            name="scattering_length_density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_SCATTERING_LENGTH_DENSITY",
        ),
    )
    unit_cell_class = Quantity(
        type=MEnum(
            [
                "triclinic",
                "monoclinic",
                "orthorhombic",
                "tetragonal",
                "rhombohedral",
                "hexagonal",
                "cubic",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-unit-cell-class-field"
        ],
        description=("In case it is all we know and we want to record/document it"),
        a_nexus_field=NeXusField(
            name="unit_cell_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "triclinic",
                "monoclinic",
                "orthorhombic",
                "tetragonal",
                "rhombohedral",
                "hexagonal",
                "cubic",
            ],
        ),
    )
    space_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-space-group-field"
        ],
        description=("Crystallographic space group"),
        a_nexus_field=NeXusField(
            name="space_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    point_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample_component.html#nxsample_component-point-group-field"
        ],
        description=("Crystallographic point group, deprecated if space_group present"),
        a_nexus_field=NeXusField(
            name="point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
