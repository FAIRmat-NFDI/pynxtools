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
# Run `pynx nomad generate-metainfo --nxdl NXspectrum` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Spectrum"]


class Spectrum(Object):
    """
    Base class container for reporting a set of spectra.

    The mostly commonly used scanning methods are supported. That is one-,
    two-, three-dimensional ROIs discretized using regular Euclidean tilings.

    Use stack for all other tilings.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXspectrum",
            category="base",
            symbols={
                "n_spc": "Number of spectra in the stack, for stacks the slowest dimension.",
                "n_k": "Number of image points along the slower dimension (k equivalent to z).",
                "n_j": "Number of image points along the slow dimension (j equivalent to y).",
                "n_i": "Number of image points along the fast dimension (i equivalent to x).",
                "n_energy": "Number of energy bins (always the fastest dimension).",
            },
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumProcess",
        repeats=True,
        variable=True,
        description=("Details how spectra were processed from the detector readings."),
    )
    spectrum_0d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumSpectrum0d",
        repeats=False,
        description=(
            "One spectrum for a point of a 0d ROI. Also known as spot measurement."
        ),
    )
    spectrum_1d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumSpectrum1d",
        repeats=False,
        description=("One spectrum for each point of a 1d ROI."),
    )
    spectrum_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumSpectrum2d",
        repeats=False,
        description=("One spectrum for each scan point of 2d ROI."),
    )
    spectrum_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumSpectrum3d",
        repeats=False,
        description=("One spectrum for point of a 3d ROI."),
    )
    stack_0d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumStack0d",
        repeats=False,
        description=("Multiple instances of spectrum_0d."),
    )
    stack_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumStack2d",
        repeats=False,
        description=("Multiple instances of spectrum_2d."),
    )
    stack_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumStack3d",
        repeats=False,
        description=("Multiple instances of spectrum_3d."),
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


class SpectrumProcess(Process):
    """
    Details how spectra were processed from the detector readings.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    input = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.SpectrumProcessInput",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="optional",
        ),
    )

    mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-process-mode-field"
        ],
        description=(
            "Imaging (data collection) mode of the instrument during acquisition "
            "of the data in this :ref:`NXspectrum` instance."
        ),
        a_nexus_field=NeXusField(
            name="mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    detector_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-process-detector-identifier-field"
        ],
        description=(
            "Link or name of an :ref:`NXdetector` instance with which the data "
            "were collected."
        ),
        a_nexus_field=NeXusField(
            name="detector_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumProcessInput(Note):
    """
    Resolvable data artifact (e.g. filename) from which all values in the
    :ref:`NXdata` instances in this :ref:`NXspectrum` were loaded during
    parsing.

    Possibility to document from which specific other serialized resource as
    the source pieces of information were processed when using NeXus as a
    semantic file format to serialize that information differently.

    The group in combination with an added field *context* therein adds
    context.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-process-input-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="optional",
        ),
    )

    context = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-process-input-context-field"
        ],
        description=(
            "Reference to a location inside the artifact that points to the "
            "specific group of values that were processed if the artifacts "
            "contains several groups of values and thus further resolving of "
            "ambiguities is required."
        ),
        a_nexus_field=NeXusField(
            name="context",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumSpectrum0d(Data):
    """
    One spectrum for a point of a 0d ROI. Also known as spot measurement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-0d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_0d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-0d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-0d-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-0d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-0d-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumSpectrum1d(Data):
    """
    One spectrum for each point of a 1d ROI.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-1d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_1d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-1d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=("Counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-1d-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-1d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the fast dimension"),
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-1d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-1d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-1d-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumSpectrum2d(Data):
    """
    One spectrum for each scan point of 2d ROI.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=("Counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the slow dimension"),
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the slow dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the fast dimension"),
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-2d-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumSpectrum3d(Data):
    """
    One spectrum for point of a 3d ROI.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=("Counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-k-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the slower dimension"),
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-k-long-name-attribute"
        ],
        description=("Point coordinate along the slower dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the slow dimension"),
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the slow dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the fast dimension"),
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-spectrum-3d-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumStack0d(Data):
    """
    Multiple instances of spectrum_0d.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_0d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=("Counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Group identifier"),
        a_nexus_field=NeXusField(
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-indices-group-long-name-attribute"
        ],
        description=("Group identifier"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_group",
        ),
    )
    indices_spectrum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-indices-spectrum-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Spectrum identifier"),
        a_nexus_field=NeXusField(
            name="indices_spectrum",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_spectrum__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-indices-spectrum-long-name-attribute"
        ],
        description=("Spectrum identifier"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_spectrum",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-0d-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumStack2d(Data):
    """
    Multiple instances of spectrum_2d.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=("Counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Group identifier"),
        a_nexus_field=NeXusField(
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-indices-group-long-name-attribute"
        ],
        description=("Group identifier"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_group",
        ),
    )
    indices_spectrum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-indices-spectrum-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Spectrum identifier"),
        a_nexus_field=NeXusField(
            name="indices_spectrum",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_spectrum__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-indices-spectrum-long-name-attribute"
        ],
        description=("Spectrum identifier"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_spectrum",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the slow dimension"),
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the slow dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the fast dimension"),
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-2d-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class SpectrumStack3d(Data):
    """
    Multiple instances of spectrum_3d.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*", "*"],
        description=("Counts"),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-intensity-long-name-attribute"
        ],
        description=("Counts"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="intensity",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Group identifier"),
        a_nexus_field=NeXusField(
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-indices-group-long-name-attribute"
        ],
        description=("Group identifier"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_group",
        ),
    )
    indices_spectrum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-indices-spectrum-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Spectrum identifier"),
        a_nexus_field=NeXusField(
            name="indices_spectrum",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_spectrum__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-indices-spectrum-long-name-attribute"
        ],
        description=("Spectrum identifier"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_spectrum",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-k-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the slower dimension"),
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-k-long-name-attribute"
        ],
        description=("Point coordinate along the slower dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the slow dimension"),
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the slow dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("Point coordinate along the fast dimension"),
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=("Energy axis"),
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXspectrum.html#nxspectrum-stack-3d-axis-energy-long-name-attribute"
        ],
        description=("Energy"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
