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
# Run `pynx nomad generate-metainfo --nxdl NXfilter` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import MEnum, Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.component import Component

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Filter"]


class Filter(Component):
    """
    For band pass beam filters.

    If uncertain whether to use :ref:`NXfilter` (band-pass filter) or
    :ref:`NXattenuator` (reduces beam intensity), then use :ref:`NXattenuator`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXfilter",
            category="base",
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=("Geometry of the filter"),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to filter the beamstop and NXoff_geometry to describe its shape instead",
        ),
    )
    transmission = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("Wavelength transmission profile of filter"),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission",
            name_type="specified",
            optionality="optional",
        ),
    )
    temperature_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("Linked temperature_log for the filter"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="temperature_log",
            name_type="specified",
            optionality="optional",
        ),
    )
    sensor_type = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=False,
        description=("Sensor(s)used to monitor the filter temperature"),
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sensor_type",
            name_type="specified",
            optionality="optional",
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

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-description-field"
        ],
        description=(
            "Composition of the filter. Chemical formula can be specified "
            "separately. This field was changed (2010-11-17) from an enumeration "
            "to a string since common usage showed a wider variety of use than a "
            "simple list. These are the items in the list at the time of the "
            "change: Beryllium | Pyrolytic Graphite | Graphite | Sapphire | "
            "Silicon | Supermirror."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    status = Quantity(
        type=MEnum(["in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-status-field"
        ],
        description=(
            "position with respect to in or out of the beam (choice of only "
            '"in" or "out")'
        ),
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["in", "out"],
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-temperature-field"
        ],
        dimensionality="[temperature]",
        description=("average/nominal filter temperature"),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-thickness-field"
        ],
        dimensionality="[length]",
        description=("Thickness of the filter"),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        description=("mass density of the filter"),
        a_nexus_field=NeXusField(
            name="density",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-chemical-formula-field"
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
            "carbon is present, the order should be: * C, then H, then the other "
            "elements in alphabetical order of their symbol. * If carbon is not "
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
    unit_cell_a = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-unit-cell-a-field"
        ],
        dimensionality="[length]",
        description=("Unit cell lattice parameter: length of side a"),
        a_nexus_field=NeXusField(
            name="unit_cell_a",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_b = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-unit-cell-b-field"
        ],
        dimensionality="[length]",
        description=("Unit cell lattice parameter: length of side b"),
        a_nexus_field=NeXusField(
            name="unit_cell_b",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_c = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-unit-cell-c-field"
        ],
        dimensionality="[length]",
        description=("Unit cell lattice parameter: length of side c"),
        a_nexus_field=NeXusField(
            name="unit_cell_c",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-unit-cell-alpha-field"
        ],
        dimensionality="[angle]",
        description=("Unit cell lattice parameter: angle alpha"),
        a_nexus_field=NeXusField(
            name="unit_cell_alpha",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell_beta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-unit-cell-beta-field"
        ],
        dimensionality="[angle]",
        description=("Unit cell lattice parameter: angle beta"),
        a_nexus_field=NeXusField(
            name="unit_cell_beta",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell_gamma = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-unit-cell-gamma-field"
        ],
        dimensionality="[angle]",
        description=("Unit cell lattice parameter: angle gamma"),
        a_nexus_field=NeXusField(
            name="unit_cell_gamma",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell_volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-unit-cell-volume-field"
        ],
        dimensionality="[length] ** 3",
        shape=["*"],
        description=("Unit cell"),
        a_nexus_field=NeXusField(
            name="unit_cell_volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )
    orientation_matrix = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-orientation-matrix-field"
        ],
        shape=["*", 3, 3],
        description=(
            "Orientation matrix of single crystal filter using Busing-Levy "
            "convention: W. R. Busing and H. A. Levy (1967). Acta Cryst. 22, "
            "457-464"
        ),
        a_nexus_field=NeXusField(
            name="orientation_matrix",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    m_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-m-value-field"
        ],
        dimensionality="dimensionless",
        description=("m value of supermirror filter"),
        a_nexus_field=NeXusField(
            name="m_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    substrate_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-substrate-material-field"
        ],
        description=("substrate material of supermirror filter"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-substrate-thickness-field"
        ],
        dimensionality="[length]",
        description=("substrate thickness of supermirror filter"),
        a_nexus_field=NeXusField(
            name="substrate_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    coating_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-coating-material-field"
        ],
        description=("coating material of supermirror filter"),
        a_nexus_field=NeXusField(
            name="coating_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate_roughness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-substrate-roughness-field"
        ],
        dimensionality="[length]",
        description=("substrate roughness (RMS) of supermirror filter"),
        a_nexus_field=NeXusField(
            name="substrate_roughness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    coating_roughness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-coating-roughness-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=("coating roughness (RMS) of supermirror filter"),
        a_nexus_field=NeXusField(
            name="coating_roughness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfilter.html#nxfilter-depends-on-field"
        ],
        description=(".. todo:: Add a definition for the reference point of a filter."),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
