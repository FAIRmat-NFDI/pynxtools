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
# Run `pynx nomad generate-metainfo --nxdl NXmonochromator` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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

__all__ = ["Monochromator"]


class Monochromator(Component):
    """
    A wavelength defining device.

    This is a base class for everything which selects a wavelength or energy,
    be it a monochromator crystal, a velocity selector, an undulator or
    whatever.

    The expected units are:

    * wavelength: angstrom * energy: eV
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmonochromator",
            category="base",
        ),
    )

    entrance_slit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=False,
        description=(
            "Size, position and shape of the entrance slit of the monochromator."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="entrance_slit",
            name_type="specified",
            optionality="optional",
        ),
    )
    exit_slit = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=False,
        description=("Size, position and shape of the exit slit of the monochromator."),
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="exit_slit",
            name_type="specified",
            optionality="optional",
        ),
    )
    distribution = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="distribution",
            name_type="specified",
            optionality="optional",
        ),
    )
    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="geometry",
            name_type="specified",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the monochromator and NXoff_geometry to describe its shape instead",
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
    crystal = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.crystal.Crystal",
        repeats=True,
        variable=True,
        description=("Use as many crystals as necessary to describe"),
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    velocity_selector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.velocity_selector.VelocitySelector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXvelocity_selector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    grating = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.grating.Grating",
        repeats=True,
        variable=True,
        description=("For diffraction grating based monochromators"),
        a_nexus_group=NeXusGroup(
            nx_class="NXgrating",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("wavelength selected"),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    wavelength_error = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-wavelength-error-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("wavelength standard deviation"),
        a_nexus_field=NeXusField(
            name="wavelength_error",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
            deprecated="see https://github.com/nexusformat/definitions/issues/820",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    wavelength_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-wavelength-errors-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("wavelength standard deviation"),
        a_nexus_field=NeXusField(
            name="wavelength_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("energy selected"),
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
        a_display={"unit": "joule"},
    )
    energy_error = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-energy-error-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("energy standard deviation"),
        a_nexus_field=NeXusField(
            name="energy_error",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
            deprecated="see https://github.com/nexusformat/definitions/issues/820",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    energy_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-energy-errors-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("energy standard deviation"),
        a_nexus_field=NeXusField(
            name="energy_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    energy_dispersion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-energy-dispersion-field"
        ],
        dimensionality="[mass] * [length] / [time] ** 2",
        unit="eV/mm",
        description=("Energy dispersion at the exit slit."),
        a_nexus_field=NeXusField(
            name="energy_dispersion",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="eV/mm",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV/mm"},
    )
    wavelength_dispersion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-wavelength-dispersion-field"
        ],
        dimensionality="dimensionless",
        unit="nm/mm",
        description=("Wavelength dispersion at the exit slit."),
        a_nexus_field=NeXusField(
            name="wavelength_dispersion",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="nm/mm",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "nm/mm"},
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXmonochromator.html#nxmonochromator-depends-on-field"
        ],
        description=(
            ".. todo:: Add a definition for the reference point of a monochromator."
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
