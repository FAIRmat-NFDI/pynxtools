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
# Run `pynx nomad generate-metainfo --nxdl NXcorrector_cs` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CorrectorCs"]


class CorrectorCs(Component):
    """
    Base class for a corrector reducing (spherical) aberrations of an electron
    optical setup.

    Different technology partners use different conventions and models for
    quantifying the aberration coefficients.

    Aberration correction components are especially important for (scanning)
    transmission electron microscopy. Composed of multiple lenses and multipole
    stigmators, their technical details are specific for the technology partner
    as well as the microscope and instrument. Most technical details are
    proprietary knowledge.

    If one component corrects for multiple types of aberrations (like it is the
    case reported here `CEOS
    <https://www.ceos-gmbh.de/en/research/electrostat>`_) follow this design
    when using corrector and monochromator in an application definition:

    * Use :ref:`NXcorrector_cs` for spherical aberration * Use
    :ref:`NXmonochromator` for energy filtering or chromatic aberration * Use
    the group corrector_ax in :ref:`NXem` for axial astigmatism aberration

    Although this base class currently provides concepts that are foremost used
    in the field of electron microscopy using this base class is not restricted
    to this research field. NXcorrector_cs can also serve as a container to
    detail, in combination with :ref:`NXaberration`, about measured aberrations
    in classical optics. In optics, though, the difference is that the design
    of the :ref:`NXoptical_lens` itself (e.g., using aspheric lenses or
    combinations of lenses) enables to reduce spherical aberrations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcorrector_cs",
            category="base",
            symbols={"n_img": "Number of images taken, at least one."},
        ),
    )

    tableauID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.corrector_cs.CorrectorCsTableauID",
        repeats=True,
        variable=True,
        description=(
            "Specific information about the alignment procedure. This is a "
            "process during which the corrector is configured to enable "
            "calibrated usage of the instrument. This :ref:`NXprocess` group "
            "should also be used when one describes in a computer simulation the "
            "specific details about the modeled or assumed aberrations."
        ),
    )
    electromagnetic_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electromagnetic_lens.ElectromagneticLens",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    optical_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.optical_lens.OpticalLens",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXoptical_lens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs-applied-field"
        ],
        description=("Was the corrector used?"),
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
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


class CorrectorCsTableauID(Process):
    """
    Specific information about the alignment procedure. This is a process
    during which the corrector is configured to enable calibrated usage of the
    instrument.

    This :ref:`NXprocess` group should also be used when one describes in a
    computer simulation the specific details about the modeled or assumed
    aberrations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs-tableauid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="tableauID",
            name_type="partial",
            optionality="optional",
        ),
    )

    imageID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.Image",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="imageID",
            name_type="partial",
            optionality="optional",
        ),
    )
    c_1 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_1 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_1",
            name_type="specified",
            optionality="optional",
        ),
    )
    b_2 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="b_2",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_2 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_2",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3",
            name_type="specified",
            optionality="optional",
        ),
    )
    s_3 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="s_3",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_3 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_3",
            name_type="specified",
            optionality="optional",
        ),
    )
    b_4 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="b_4",
            name_type="specified",
            optionality="optional",
        ),
    )
    d_4 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="d_4",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_4 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_4",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5",
            name_type="specified",
            optionality="optional",
        ),
    )
    s_5 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="s_5",
            name_type="specified",
            optionality="optional",
        ),
    )
    r_5 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="r_5",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_6 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_6",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_1_0 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_0",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_1_2_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_1_2_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_1_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_1_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_1_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_1_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_3_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_3_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_3_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_3_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_0 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_0",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_2_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_2_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_4_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_4_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_4_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_4_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_1_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_1_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_1_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_1_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_3_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_3_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_3_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_3_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_5_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_5_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_5_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_5_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_0 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_0",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_2_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_2_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_4_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_4_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_4_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_4_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_6_a = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_6_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_6_b = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aberration.Aberration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_6_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs-tableauid-description-field"
        ],
        description=(
            "Discouraged free-text field to add further details about the "
            "alignment procedure."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    tilt_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs-tableauid-tilt-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "The outer tilt angle of the beam in tableau acquisition. TODO: The "
            "relevant axes which span the tilt_angle need a cleaner description. "
            "Suggestions from the community are welcome here for guiding an "
            "improvement of this base class."
        ),
        a_nexus_field=NeXusField(
            name="tilt_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    exposure_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs-tableauid-exposure-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=("The exposure time of single tilt images."),
        a_nexus_field=NeXusField(
            name="exposure_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    magnification = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs-tableauid-magnification-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The factor of enlargement of the apparent size, not the physical "
            "size, of an object."
        ),
        a_nexus_field=NeXusField(
            name="magnification",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    model = Quantity(
        type=MEnum(["ceos", "nion"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcorrector_cs.html#nxcorrector_cs-tableauid-model-field"
        ],
        description=(
            "Convention used for storing measured or estimated aberrations (for "
            "each or the final image) via fields c_1, a_1, c_1_0, c_1_2_a, and "
            "so on and so forth. See `S. J. Pennycock and P. D. Nellist "
            "<https://doi.org/10.1007/978-1-4419-7200-2>`_ (page 44ff, and page "
            "118ff) for different definitions available and further details. "
            "Table 7-2 of Ibid. publication (page 305ff) documents how to "
            "convert from the Nion to the CEOS definitions. Conversion tables "
            "are also summarized by `Y. Liao "
            "<https://www.globalsino.com/EM/page3740.html>`_."
        ),
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["ceos", "nion"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
