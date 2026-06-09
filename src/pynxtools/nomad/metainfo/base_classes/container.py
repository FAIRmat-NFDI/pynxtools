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
# Run `pynx nomad generate-metainfo --nxdl NXcontainer` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Container"]


class Container(Component):
    """
    State of a container holding the sample under investigation.

    A container is any object in the beam path which absorbs the beam and whose
    contribution to the overall attenuation/scattering needs to be determined
    to process the experimental data. Examples of containers include glass
    capillary tubes, vanadium cans, windows in furnaces or diamonds in a
    Diamond Anvil Cell. The following figures show a complex example of a
    container:

    .. figure:: container/ComplexExampleContainer.png

    A hypothetical capillary furnace. The beam passes from left to right (blue
    dashes), passing through window 1, then window 2, before passing through
    the downstream wall of the capillary. It is then scattered by the sample
    with scattered beams passing through the upstream wall of the capillary,
    then windows 4 and 5. As part of the corrections for a PDF experiment it is
    necessary to subtract the PDF of the empty container (i.e. each of the
    windows and the capillary). To calculate the PDF of the empty container it
    is necessary to have the measured scattering data and to know the nature
    (e.g. density, elemental composition, etc.) of the portion of the container
    which the beam passed through.

    .. figure:: container/ComplexContainerBeampath.png

    A complete description of the shapes of the container elements with their
    orientation relative to the beam and also information on whether they are
    upstream or downstream of the sample is also therefore important. For
    example, although the windows 2 and 4 have the same shape, the path taken
    through them by the beam is very different and this needs to be modelled.
    Furthermore, it is not inconceivable that windows might move during an
    experiment and thus the changes to the beampath would need to be accounted
    for.

    This class encodes the position of the container with respect to the sample
    and allows the calculation of the beampath through the container. It also
    includes sufficient data to model beam absorption of the container and a
    link to a dataset containing a measurement of the container with nothing
    inside, to allow data corrections (at a specific beam energy/measurement
    time) to be made.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcontainer",
            category="base",
        ),
    )

    beam = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=False,
        description=(
            "Details of beam incident on container, including the position "
            "relative to the sample (to determine whether the container is "
            "upstream or downstream of the sample)."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam",
            name_type="specified",
            optionality="optional",
        ),
    )
    shape = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.shape.Shape",
        repeats=False,
        description=(
            "Shape of the container. In combination with orientation this should "
            "allow the beampath through the container to be modelled to allow "
            "the adsorption to be calculated."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXshape",
            name="shape",
            name_type="specified",
            optionality="optional",
        ),
    )
    orientation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=False,
        description=(
            "The angle the container makes to the beam and how it may change "
            "during the experiment.In combination with shape this should allow "
            "the beampath through the container to be modelled to allow the "
            "adsorption of the container to be calculated."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="orientation",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer-name-field"
        ],
        description=("Descriptive name of container."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer-description-field"
        ],
        description=(
            "Verbose description of container and how it fits into the wider "
            "experimental set up."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer-chemical-formula-field"
        ],
        description=(
            "Chemical composition of the material the container is made from. "
            "Specified using CIF conventions. Abbreviated version of CIF "
            "standard: * Only recognized element symbols may be used. * Each "
            "element symbol is followed by a 'count' number. A count of '1' may "
            "be omitted. * A space or parenthesis must separate each cluster of "
            "(element symbol + count). * Where a group of elements is enclosed "
            "in parentheses, the multiplier for the group must follow the "
            "closing parentheses. That is, all element and group multipliers are "
            "assumed to be printed as subscripted numbers. * Unless the elements "
            "are ordered in a manner that corresponds to their chemical "
            "structure, the order of the elements within any group or moiety "
            "depends on whether or not carbon is present. * If carbon is "
            "present, the order should be: - C, then H, then the other elements "
            "in alphabetical order of their symbol. - If carbon is not present, "
            "the elements are listed purely in alphabetic order of their symbol. "
            "* This is the *Hill* system used by Chemical Abstracts."
        ),
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        shape=["*"],
        description=("Density of the material the container is made from."),
        a_nexus_field=NeXusField(
            name="density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    packing_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer-packing-fraction-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Fraction of the volume of the container occupied by the material "
            "forming the container."
        ),
        a_nexus_field=NeXusField(
            name="packing_fraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    relative_molecular_mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer-relative-molecular-mass-field"
        ],
        dimensionality="[mass]",
        shape=["*"],
        description=("Relative molecular mass of container."),
        a_nexus_field=NeXusField(
            name="relative_molecular_mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS",
        ),
    )

    reference_measurement = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcontainer.html#nxcontainer-reference-measurement-link"
        ],
        description=(
            "A link to a full data collection which contains the actual measured "
            "data for this container within the experimental set up (with no "
            "sample or inner container(s)). This data set will also include the "
            "wavelength/energy, measurement time and intensity for which these "
            "data are valid."
        ),
        a_nexus_link=NeXusLink(
            name="reference_measurement",
            target="/NXentry",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
