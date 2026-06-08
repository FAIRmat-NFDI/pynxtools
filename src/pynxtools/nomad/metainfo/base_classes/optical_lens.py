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
# Run `pynx nomad generate-metainfo --nxdl NXoptical_lens` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["OpticalLens"]


class OpticalLens(Component):
    """
    Description of an optical lens.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXoptical_lens",
            category="base",
            symbols={
                "N_spectrum": "Size of the wavelength array for which the refractive index of the material\n                is given.",
                "N_spectrum_coating": "Size of the wavelength array for which the refractive index of the coating\n                is given.",
                "N_spectrum_RT": "Size of the wavelength array for which the reflectance or transmission of\n                the lens is given.",
            },
        ),
    )

    substrate = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_lens.OpticalLensSubstrate",
        repeats=False,
        description=(
            "Properties of the substrate material of the lens. If the lens has a "
            "coating specify the coating material and its properties in "
            "'coating'."
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_lens.OpticalLensSample",
        repeats=True,
        variable=True,
        description=(
            "If the lens has a coating describe the material and its properties. "
            "Some basic information can be found e.g. [here] "
            "(https://www.opto-e.com/basics/reflection-transmission-and-coatings). "
            "If the back and front side of the lens are coated with different "
            "materials, use separate COATING(NXsample) fields to describe the "
            "coatings on the front and back side, respectively. For example: "
            "coating_front(NXsample) and coating_back(NXsample)."
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-type-field"
        ],
        description=("Type of the lens (e.g. concave, convex etc.)."),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "biconcave",
                "plano-concave",
                "convexo-concave",
                "biconvex",
                "plano-convex",
                "concavo-convex",
                "Fresnel lens",
            ],
            open_enum=True,
        ),
    )
    chromatic = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-chromatic-field"
        ],
        description=("Is it a chromatic lens?"),
        a_nexus_field=NeXusField(
            name="chromatic",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    lens_diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-lens-diameter-field"
        ],
        dimensionality="[length]",
        description=("Diameter of the lens."),
        a_nexus_field=NeXusField(
            name="lens_diameter",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    reflectance = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-reflectance-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Reflectance of the lens at given spectral values."),
        a_nexus_field=NeXusField(
            name="reflectance",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    transmission = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-transmission-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Transmission of the lens at given spectral values."),
        a_nexus_field=NeXusField(
            name="transmission",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    focal_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-focal-length-field"
        ],
        dimensionality="[length]",
        shape=[2],
        description=(
            "Focal length of the lens on the front side (first value), i.e. "
            "where the beam is incident, and on the back side (second value)."
        ),
        a_nexus_field=NeXusField(
            name="focal_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    curvature_radius_FACE = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-curvature-radius-face-field"
        ],
        variable=True,
        dimensionality="[length]",
        description=(
            "Curvature radius of the lens. Instead of 'FACE' in the name of this "
            "field, the user is advised to specify for which surface (e.g. front "
            "or back) the curvature is provided: e.g. curvature_radius_front or "
            "curvature_radius_back. The front face is the surface on which the "
            "light beam is incident, while the back face is the one from which "
            "the light beam exits the lens."
        ),
        a_nexus_field=NeXusField(
            name="curvature_radius_FACE",
            type="NX_NUMBER",
            name_type="partial",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    Abbe_number = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-abbe-number-field"
        ],
        dimensionality="dimensionless",
        description=("Abbe number (or V-number) of the lens."),
        a_nexus_field=NeXusField(
            name="Abbe_number",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    numerical_aperture = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-numerical-aperture-field"
        ],
        description=("The numerical aperture of the lens."),
        a_nexus_field=NeXusField(
            name="numerical_aperture",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    magnification = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-magnification-field"
        ],
        description=("Magnification of the lens"),
        a_nexus_field=NeXusField(
            name="magnification",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
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


class OpticalLensSubstrate(Sample):
    """
    Properties of the substrate material of the lens. If the lens has a coating
    specify the coating material and its properties in 'coating'.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-substrate-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="substrate",
            name_type="specified",
            optionality="optional",
        ),
    )

    substrate_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-substrate-substrate-material-field"
        ],
        description=("Specify the substrate material of the lens."),
        a_nexus_field=NeXusField(
            name="substrate_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-substrate-substrate-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of the lens substrate at the optical axis."),
        a_nexus_field=NeXusField(
            name="substrate_thickness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    index_of_refraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-substrate-index-of-refraction-field"
        ],
        dimensionality="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the lens material. Specify at given "
            "wavelength (or energy, wavenumber etc.) values."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class OpticalLensSample(Sample):
    """
    If the lens has a coating describe the material and its properties. Some
    basic information can be found e.g. [here]
    (https://www.opto-e.com/basics/reflection-transmission-and-coatings). If
    the back and front side of the lens are coated with different materials,
    use separate COATING(NXsample) fields to describe the coatings on the front
    and back side, respectively. For example: coating_front(NXsample) and
    coating_back(NXsample).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-coating-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    coating_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-coating-coating-type-field"
        ],
        description=(
            "Specify the coating type (e.g. dielectric, anti-reflection (AR), "
            "multilayer coating etc.)."
        ),
        a_nexus_field=NeXusField(
            name="coating_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    coating_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-coating-coating-material-field"
        ],
        description=("Describe the coating material (e.g. MgF2)."),
        a_nexus_field=NeXusField(
            name="coating_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    coating_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-coating-coating-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of the coating."),
        a_nexus_field=NeXusField(
            name="coating_thickness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    index_of_refraction_coating = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXoptical_lens.html#nxoptical_lens-coating-index-of-refraction-coating-field"
        ],
        dimensionality="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the coating. Specify at given "
            "spectral values (wavelength, energy, wavenumber etc.)."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction_coating",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
