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
# Run `pynx nomad generate-metainfo --nxdl NXraman` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.applications.optical_spectroscopy import (
    OpticalSpectroscopy,
    OpticalSpectroscopyInstrument,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Raman"]


class Raman(OpticalSpectroscopy):
    """
    An application definition for Raman spectroscopy experiments.

    This application definition supports a wide range of Raman spectroscopy
    experiments. These may be as simple as acquiring a single Raman spectrum
    from spontaneous Raman scattering, or as complex as Raman imaging with a
    Raman spectrometer. The scope also includes surface- and tip-enhanced Raman
    techniques, X-ray Raman scattering, resonant Raman scattering, and
    multidimensional Raman spectra collected under varying conditions such as
    temperature, pressure, or electric field.

    The application definition comprises two main components:

    1. Structures defined in NXoptical_spectroscopy: * Instrument configuration
    and data calibration * Sensors monitoring sample or beam conditions

    2. Structures specified and extended in NXraman: * Description of the
    experiment type * Metadata and configuration of the optical setup (e.g.,
    source, monochromator, detector, waveplate, lens) * Detailed description of
    beam properties and their interaction with the sample * Sample-specific
    information

    Information on Raman spectroscopy are provided in:

    General

    * Lewis, Ian R.; Edwards, Howell G. M. Handbook of Raman Spectroscopy ISBN
    0-8247-0557-2

    Raman scattering selection rules

    * Dresselhaus, M. S.; Dresselhaus, G.; Jorio, A. Group Theory - Application
    to the Physics ofCondensed Matter ISBN 3540328971

    Semiconductors

    * Manuel Cardona Light Scattering in Solids I eBook ISBN: 978-3-540-37568-5
    DOI: https://doi.org/10.1007/978-3-540-37568-5

    * Manuel Cardona, Gernot Güntherodt Light Scattering in Solids II eBook
    ISBN: 978-3-540-39075-6 DOI: https://doi.org/10.1007/3-540-11380-0

    * See as well other Books from the "Light Scattering in Solids" series:
    III: Recent Results IV: Electronic Scattering, Spin Effects, SERS, and
    Morphic Effects V: Superlattices and Other Microstructures VI: Recent
    Results, Including High-Tc Superconductivity VII: Crystal-Field and
    Magnetic Excitations VIII: Fullerenes, Semiconductor Surfaces, Coherent
    Phonons IX: Novel Materials and Techniques

    Glasses, Liquids, Gasses, ...

    Review articles: Stimulated Raman scattering, Coherent anti-Stokes Raman
    scattering, Surface-enhanced Raman scattering, Tip-enhanced Raman
    scattering * https://doi.org/10.1186/s11671-019-3039-2
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXraman",
            category="application",
            symbols={
                "N_scattering_configurations": "Number of scattering configurations used in the measurement.\n                It is 1 for only parallel polarization measurement, 2 for parallel and cross\n                polarization measurement or larger, if i.e. the incident and scattered photon\n                direction is varied."
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.raman.RamanInstrument",
        repeats=True,
        variable=True,
        description=(
            "Metadata of the setup, its optical elements and physical properties "
            "which defines the Raman measurement."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXraman"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-definition-field"
        ],
        description=("An application definition for Raman spectroscopy."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXraman"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXraman",
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-definition-version-attribute"
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-definition-url-attribute"
        ],
        description=(
            "URL where to find further material (documentation, examples) "
            "relevant to the application definition."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="URL",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_type = Quantity(
        type=MEnum(["Raman spectroscopy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-experiment-type-field"
        ],
        description=(
            "Specify the type of the optical experiment. You may specify "
            "fundamental characteristics or properties in the experimental "
            "sub-type."
        ),
        a_nexus_field=NeXusField(
            name="experiment_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["Raman spectroscopy"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="Raman spectroscopy",
        ),
    )
    raman_experiment_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-raman-experiment-type-field"
        ],
        description=("Specify the type of Raman experiment."),
        a_nexus_field=NeXusField(
            name="raman_experiment_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "in situ Raman spectroscopy",
                "resonant Raman spectroscopy",
                "non-resonant Raman spectroscopy",
                "Raman imaging",
                "tip-enhanced Raman spectroscopy (TERS)",
                "surface-enhanced Raman spectroscopy (SERS)",
                "surface plasmon polariton enhanced Raman scattering (SPPERS)",
                "hyper Raman spectroscopy (HRS)",
                "stimulated Raman spectroscopy (SRS)",
                "inverse Raman spectroscopy (IRS)",
                "coherent anti-Stokes Raman spectroscopy (CARS)",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-start-time-field"
        ],
        description=(
            "Datetime of the start of the measurement. Should be a ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise, the local time zone is assumed per ISO8601. It is "
            "required to enter at least one of both measurement times, either "
            '"start_time" or "end_time".'
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-end-time-field"
        ],
        description=(
            "Datetime of the end of the measurement. Should be a ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise the local time zone is assumed per ISO8601. It is "
            "required to enter at least one of both measurement times, either "
            '"start_time" or "end_time".'
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    identifier_experiment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-identifier-experiment-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier_experiment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-experiment-description-field"
        ],
        description=(
            "An optional free-text description of the experiment. Users are "
            "strongly advised to parameterize the description of their "
            "experiment by using respective groups and fields and base classes "
            "instead of writing prose into this field. The reason is that such a "
            "free-text field is difficult to machine-interpret. The motivation "
            "behind keeping this field for now is to learn how far the current "
            "base classes need extension based on user feedback."
        ),
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    experiment_sub_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-experiment-sub-type-field"
        ],
        description=(
            "Specify a special property or characteristic of the experiment, "
            "which specifies the generic experiment type."
        ),
        a_nexus_field=NeXusField(
            name="experiment_sub_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["time resolved", "imaging", "pump-probe"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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


class RamanInstrument(OpticalSpectroscopyInstrument):
    """
    Metadata of the setup, its optical elements and physical properties which
    defines the Raman measurement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    scattering_configuration = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-instrument-scattering-configuration-field"
        ],
        description=(
            "Scattering configuration as defined by the porto notation by three "
            "states, which are orthogonal to each other. Example: z(xx)z for "
            "parallel polarized backscattering configuration. See: "
            "https://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-doc-raman "
            "A(BC)D A = The propagation direction of the incident light (k_i) B "
            "= The polarization direction of the incident light (E_i) C = The "
            "polarization direction of the scattered light (E_s) D = The "
            "propagation direction of the scattered light (k_s) An orthogonal "
            "base is assumed. Linear polarized light is displayed by e.g. "
            '"x","y" or "z" Unpolarized light is displayed by "." For '
            "non-orthogonal vectors, use the attribute porto_notation_vectors."
        ),
        a_nexus_field=NeXusField(
            name="scattering_configuration",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    scattering_configuration__porto_notation_vectors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXraman.html#nxraman-entry-instrument-scattering-configuration-porto-notation-vectors-attribute"
        ],
        shape=[4, 3, "*"],
        description=(
            "Scattering configuration as defined by the porto notation given by "
            "respective vectors. Vectors in the porto notation are defined as "
            "for A, B, C, D above. Linear light polarization is assumed."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="porto_notation_vectors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            parent_field="scattering_configuration",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
