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
# Run `pynx nomad generate-metainfo --nx-class NXresolution` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Resolution"]


class Resolution(Object):
    """
    Describes the resolution of a physical quantity.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXresolution",
            category="base",
        ),
    )

    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "Additional details of the estimate or description of the "
            "calibration procedure"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="note",
            name_type="specified",
            optionality="optional",
        ),
    )
    response_function = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=(
            "The response of the instrument or part of the instrument to a "
            "infinitesimally sharp input signal along the physical quantity of "
            "this group. This is also sometimes called instrument response "
            "function for time resolution or point spread function for spatial "
            "response. The resolution is typically determined by taking the full "
            "width at half maximum (FWHM) of the response function. This could "
            "have an AXISNAME field ```input``` (the input axis or grid of the "
            "response function) and a ``DATA`` field ```magnitude```. Both of "
            "these should have the same unit. The dimensions should match those "
            "of the :ref:`resolution </NXresolution/resolution-field>` field."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="response_function",
            name_type="specified",
            optionality="optional",
        ),
    )
    formula_symbols = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=False,
        description=(
            "Symbols linking to another path in the NeXus tree to be referred to "
            "from the `resolution_formula_description` field. The ``TERM`` "
            "should be a valid path inside this application definition, i.e., of "
            "the form /entry/instrument/my_part/my_field."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="formula_symbols",
            name_type="specified",
            optionality="optional",
        ),
    )
    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
        repeats=True,
        variable=True,
        description=(
            "For storing details and data of a calibration to derive a "
            "resolution from data."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution-physical-quantity-field"
        ],
        description=(
            "The physical quantity of the resolution, e.g., energy, momentum, "
            "time, area, etc."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    type = Quantity(
        type=MEnum(["estimated", "derived", "calibrated", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution-type-field"
        ],
        description=("The process by which the resolution was determined."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["estimated", "derived", "calibrated", "other"],
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution-resolution-field"
        ],
        description=("The resolution of the physical quantity."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    resolution_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution-resolution-errors-field"
        ],
        description=("Standard deviation of the resolution of the physical quantity."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    relative_resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution-relative-resolution-field"
        ],
        description=(
            "Ratio of the resolution at a specified measurand value to that "
            "measurand value."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="relative_resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    relative_resolution_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution-relative-resolution-errors-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Standard deviation of the relative resolution of the physical quantity."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="relative_resolution_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    resolution_formula_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXresolution.html#nxresolution-resolution-formula-description-field"
        ],
        description=(
            "A description of the resolution formula to determine the resolution "
            "from a set of symbols as entered by the `formula_...` fields. This "
            "should be an english description of the math used."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="resolution_formula_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
