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
# Run `pynx nomad generate-metainfo --nxdl NXbeam_splitter` to regenerate.
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

from pynxtools.nomad.annotations import (
    NeXusAttribute,
    NeXusChoice,
    NeXusDefinition,
    NeXusField,
    NeXusGroup,
    NeXusLink,
)
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.shape import Shape

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["BeamSplitter"]


class BeamSplitter(Component):
    """
    A beam splitter, i.e. a device splitting the light into two or more beams.

    Information about types and properties of beam splitters is provided e.g.
    [here](https://www.rp-photonics.com/beam_splitters.html).

    Use two or more instances of NXbeam to describe the beam paths after the
    beam splitter. In the dependency chain of the new beam paths, the first
    elements each point to this beam splitter, as this is the previous element.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXbeam_splitter",
            category="base",
            symbols={
                "N_spectrum": "Length of the spectrum vector (e.g. wavelength or energy) for which the\n                refractive index of the beam splitter material and/or coating is defined.",
                "N_spectrum_RT": "Length of the spectrum vector (e.g. wavelength or energy) for which the\n                reflectance or transmission of the beam splitter is given.",
                "N_shapepar": "Number of parameters needed do describe the shape of the beam splitter.",
                "N_objects": "Number of objects the beam splitter is made up of.",
                "N_outputs": "Number of outputs, i.e. number of paths the beam takes after being split by\n                the beam splitter.",
            },
        ),
    )

    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam_splitter.BeamSplitterShape",
        repeats=True,
        variable=True,
        description=(
            "Describe the geometry (shape, dimension etc.) of the beam splitter. "
            "Specify the dimensions in 'SHAPE/size'. A sketch of the device "
            "should be provided in the 'sketch(NXdata)' field to clarify (i) the "
            "shape and dimensions of the device, and (ii) the input and outputs "
            "(i.e. the direction of the incoming and outcoming (split) beams)."
        ),
    )
    substrate = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam_splitter.BeamSplitterSubstrate",
        repeats=False,
        description=(
            "Substrate of the beam splitter. Describe the material of the "
            "substrate in substrate/substrate_material and provide its index of "
            "refraction in substrate/index_of_refraction_substrate, if known."
        ),
    )
    coating = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam_splitter.BeamSplitterCoating",
        repeats=False,
        description=(
            "Is the beam splitter coated? If yes, specify the type and material "
            "of the coating and the spectral range for which it is designed. If "
            "known, you may also provide its index of refraction. For a beam "
            "splitter cube consisting of two prisms which are glued together, "
            "you may want to specify the the glue and the coatings of each "
            "prism."
        ),
    )

    type = Quantity(
        type=MEnum(
            [
                "dichroic mirror",
                "dielectric mirror",
                "metal-coated mirror",
                "Nicol prism",
                "Glan-Thompson prism",
                "pellicle mirror",
                "Polka dot beam splitter",
                "fiber optic splitter",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-type-field"
        ],
        description=(
            "Specify the beam splitter type (e.g. dielectric mirror, pellicle, "
            "dichroic mirror etc.). Shape (e.g. prism, plate, cube) and "
            "dimension should be described in 'geometry'. Define if the beam "
            "splitter is polarizing or not in the field "
            "'polarizing(NX_BOOLEAN)'."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "dichroic mirror",
                "dielectric mirror",
                "metal-coated mirror",
                "Nicol prism",
                "Glan-Thompson prism",
                "pellicle mirror",
                "Polka dot beam splitter",
                "fiber optic splitter",
            ],
        ),
    )
    polarizing = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-polarizing-field"
        ],
        description=("Is the beam splitter polarizing?"),
        a_nexus_field=NeXusField(
            name="polarizing",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    multiple_outputs = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-multiple-outputs-field"
        ],
        description=(
            "Does the beam splitter have multiple outputs (diffractive optical "
            "element), i.e. more than two outputs?"
        ),
        a_nexus_field=NeXusField(
            name="multiple_outputs",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    splitting_ratio = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-splitting-ratio-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Beam splitting ratio(s) for the various outputs (i.e. the paths of "
            "the beam after being split by the beam splitter). The order of the "
            "ratios must be consistent with the labels 1, 2, ... N_outputs "
            "defined by the sketch in 'SHAPE/sketch', starting with 1."
        ),
        a_nexus_field=NeXusField(
            name="splitting_ratio",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    clear_aperture = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-clear-aperture-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Clear aperture of the device (e.g. 90% of diameter for a disc, or "
            "90% of length and height for square geometry)."
        ),
        a_nexus_field=NeXusField(
            name="clear_aperture",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    wavelength_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-wavelength-range-field"
        ],
        dimensionality="[length]",
        shape=[2],
        description=(
            "Wavelength range for which the beam splitter is designed. Enter the "
            "minimum and maximum values of the wavelength range. Alternatively, "
            "or additionally, you may define the wavelength range for the "
            "coating in coating/wavelength_range_coating."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_WAVELENGTH",
        ),
    )
    optical_loss = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-optical-loss-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Optical loss of the beam splitter for the various outputs (i.e. the "
            "paths of the beam after being split by the beam splitter). The "
            "order of the ratios must be consistent with the labels 1, 2, ... "
            "N_outputs defined by the sketch in 'SHAPE/sketch', starting with 1."
        ),
        a_nexus_field=NeXusField(
            name="optical_loss",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    incident_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-incident-angle-field"
        ],
        dimensionality="[angle]",
        description=("Optimized angle of incidence for the desired splitting ratio."),
        a_nexus_field=NeXusField(
            name="incident_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    deflection_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-deflection-angle-field"
        ],
        dimensionality="[angle]",
        description=(
            "Angle of deflection corresponding to the optimized angle of "
            "incidence defined in incident_angle."
        ),
        a_nexus_field=NeXusField(
            name="deflection_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    AOI_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-aoi-range-field"
        ],
        variable=True,
        dimensionality="[angle]",
        shape=[2],
        description=(
            "Range of the angles of incidence (AOI) for which the beam splitter "
            "can be operated. Specify the minimum and maximum angles of the "
            "range."
        ),
        a_nexus_field=NeXusField(
            name="AOI_range",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    reflectance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-reflectance-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Reflectance of the beam splitter at given spectral values."),
        a_nexus_field=NeXusField(
            name="reflectance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    transmission = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-transmission-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Transmission at given spectral values for the various outputs (i.e. "
            "the paths of the beam after being split by the beam splitter). The "
            "order of the ratios must be consistent with the labels 1, 2, ... "
            "N_outputs defined by the sketch in 'SHAPE/sketch', starting with 1."
        ),
        a_nexus_field=NeXusField(
            name="transmission",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
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


class BeamSplitterShape(Shape):
    """
    Describe the geometry (shape, dimension etc.) of the beam splitter. Specify
    the dimensions in 'SHAPE/size'. A sketch of the device should be provided
    in the 'sketch(NXdata)' field to clarify (i) the shape and dimensions of
    the device, and (ii) the input and outputs (i.e. the direction of the
    incoming and outcoming (split) beams).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-shape-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    shape = Quantity(
        type=MEnum(["cube", "cylinder", "plate", "prism", "wedged", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-shape-shape-field"
        ],
        description=("Describe the shape (plate, cube, wedged, prism etc.)."),
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["cube", "cylinder", "plate", "prism", "wedged", "other"],
        ),
    )
    size = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-shape-size-field"
        ],
        shape=["*", "*"],
        description=(
            "Physical extent of the beam splitter device. The beam splitter "
            "might be made up of one or more objects (NX_objects). The meaning "
            "and location of the axes used will vary according to the value of "
            "the 'shape' variable. 'N_shapepar' defines how many parameters: * "
            "For 'cube' the parameters are (width, length). * For 'cylinder' the "
            "parameters are (diameter, length). * For 'plate' the parameters are "
            "(width, height, length). * For 'prism' the parameters are (width, "
            "height, length). * For 'wedged' the parameters are (width, height, "
            "shortest length). The wedge angle should be provided in "
            "'SHAPE/wedge_angle'. * For 'other' the parameters may be (A, B, C, "
            "...) with the labels defined in the sketch plotted in "
            "'SHAPE/sketch'."
        ),
        a_nexus_field=NeXusField(
            name="size",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    wedge_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-shape-wedge-angle-field"
        ],
        dimensionality="[angle]",
        description=("Wedge angle if 'shape' is 'wedged'."),
        a_nexus_field=NeXusField(
            name="wedge_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class BeamSplitterSubstrate(Sample):
    """
    Substrate of the beam splitter. Describe the material of the substrate in
    substrate/substrate_material and provide its index of refraction in
    substrate/index_of_refraction_substrate, if known.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-substrate-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-substrate-substrate-material-field"
        ],
        description=(
            "Specify the material of the beam splitter. If the device has a "
            "coating it should be described in coating/coating_material. Is the "
            "material birefringent?"
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-substrate-substrate-thickness-field"
        ],
        dimensionality="[length]",
        shape=[2],
        description=(
            "Thickness of the beam splitter substrate. Define the minimum and "
            "maximum thickness (for a wedged geometry). For a homogeneous "
            "thickness (e.g. as in plate beam splitters) the minimum and maximum "
            "values are equal."
        ),
        a_nexus_field=NeXusField(
            name="substrate_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    index_of_refraction_substrate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-substrate-index-of-refraction-substrate-field"
        ],
        dimensionality="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the beam splitter substrate. Specify "
            "at given spectral values (e.g. wavelength, energy, wavenumber "
            "etc.)."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction_substrate",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class BeamSplitterCoating(Sample):
    """
    Is the beam splitter coated? If yes, specify the type and material of the
    coating and the spectral range for which it is designed. If known, you may
    also provide its index of refraction. For a beam splitter cube consisting
    of two prisms which are glued together, you may want to specify the the
    glue and the coatings of each prism.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-coating-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="coating",
            name_type="specified",
            optionality="optional",
        ),
    )

    coating_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-coating-coating-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-coating-coating-material-field"
        ],
        description=("Specify the coating material."),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-coating-coating-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of the coating."),
        a_nexus_field=NeXusField(
            name="coating_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    wavelength_range_coating = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-coating-wavelength-range-coating-field"
        ],
        dimensionality="[length]",
        shape=[2],
        description=(
            "Wavelength range for which the coating is designed. Enter the "
            "minimum and maximum values of the wavelength range."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_range_coating",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_WAVELENGTH",
        ),
    )
    index_of_refraction_coating = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXbeam_splitter.html#nxbeam_splitter-coating-index-of-refraction-coating-field"
        ],
        dimensionality="dimensionless",
        shape=[2, "*"],
        description=(
            "Complex index of refraction of the coating. Specify at given "
            "spectral values (e.g. wavelength, energy, wavenumber etc.)."
        ),
        a_nexus_field=NeXusField(
            name="index_of_refraction_coating",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
