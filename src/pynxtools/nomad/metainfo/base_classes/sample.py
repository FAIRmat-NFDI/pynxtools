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
# Run `pynx nomad generate-metainfo --nx-class NXsample` to regenerate.
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

__all__ = ["Sample"]


class Sample(Component, basesections.CompositeSystem):
    """
    Any information on the sample.

    This could include scanned variables that are associated with one of the
    data dimensions, e.g. the magnetic field, or logged data, e.g. monitored
    temperature vs elapsed time.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXsample",
            category="base",
            symbols={
                "n_comp": "number of compositions",
                "n_Temp": "number of temperatures",
                "n_eField": "number of values in applied electric field",
                "n_mField": "number of values in applied magnetic field",
                "n_pField": "number of values in applied pressure field",
                "n_sField": "number of values in applied stress field",
            },
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=False,
        description=(
            "The position and orientation of the center of mass of the sample"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="geometry",
            name_type="specified",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the sample and NXoff_geometry to describe its shape instead",
        ),
    )
    beam = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=True,
        variable=True,
        description=(
            "Details of beam incident on sample - used to calculate sample/beam "
            "interaction point"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sample_component = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample_component.SampleComponent",
        repeats=True,
        variable=True,
        description=(
            "One group per sample component This is the preferred way of "
            "recording per component information over the n_comp arrays"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXsample_component",
            name=None,
            name_type="any",
            optionality="optional",
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
    temperature_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=(
            "temperature_log.value is a link to e.g. "
            "temperature_env.sensor1.value_log.value"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="temperature_log",
            name_type="specified",
            optionality="optional",
            deprecated="use ``temperature``, see: https://github.com/nexusformat/definitions/issues/816",
        ),
    )
    temperature_env = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.environment.Environment",
        repeats=False,
        description=("Additional sample temperature environment information"),
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="temperature_env",
            name_type="specified",
            optionality="optional",
        ),
    )
    magnetic_field = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=(
            "magnetic_field.value is a link to e.g. magnetic_field_env.sensor1.value"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="magnetic_field",
            name_type="specified",
            optionality="optional",
        ),
    )
    magnetic_field_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=(
            "magnetic_field_log.value is a link to e.g. "
            "magnetic_field_env.sensor1.value_log.value"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="magnetic_field_log",
            name_type="specified",
            optionality="optional",
            deprecated="use ``magnetic_field``, see: https://github.com/nexusformat/definitions/issues/816",
        ),
    )
    magnetic_field_env = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.environment.Environment",
        repeats=False,
        description=("Additional sample magnetic environment information"),
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="magnetic_field_env",
            name_type="specified",
            optionality="optional",
        ),
    )
    external_ADC = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=False,
        description=("logged value (or logic state) read from user's setup"),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="external_ADC",
            name_type="specified",
            optionality="optional",
        ),
    )
    positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.positioner.Positioner",
        repeats=True,
        variable=True,
        description=("Any positioner (motor, PZT, ...) used to locate the sample"),
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        repeats=True,
        variable=True,
        description=("This group describes the shape of the sample"),
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.environment.Environment",
        repeats=True,
        variable=True,
        description=(
            "Any environmental or external stimuli/measurements. These can "
            "include, among others: applied pressure, surrounding gas phase and "
            "gas pressure, external electric/magnetic/mechanical fields, "
            "temperature, ..."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    history = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.history.History",
        repeats=False,
        description=(
            "A set of physical processes that occurred to the sample "
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-name-field"
        ],
        description=("Descriptive name of sample"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-chemical-formula-field"
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
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-temperature-field"
        ],
        dimensionality="[temperature]",
        description=("Sample temperature. This could be a scanned variable"),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    electric_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-electric-field-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        shape=["*"],
        description=("Applied electric field"),
        a_nexus_field=NeXusField(
            name="electric_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    electric_field__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-electric-field-direction-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="electric_field",
            enumeration=["x", "y", "z"],
        ),
    )
    magnetic_field_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-magnetic-field-field"
        ],
        shape=["*"],
        description=("Applied magnetic field"),
        a_nexus_field=NeXusField(
            name="magnetic_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    magnetic_field_quantity__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-magnetic-field-direction-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="magnetic_field",
            enumeration=["x", "y", "z"],
        ),
    )
    stress_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-stress-field-field"
        ],
        shape=["*"],
        description=("Applied external stress field"),
        a_nexus_field=NeXusField(
            name="stress_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    stress_field__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-stress-field-direction-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="stress_field",
            enumeration=["x", "y", "z"],
        ),
    )
    pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-pressure-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        shape=["*"],
        description=("Applied pressure"),
        a_nexus_field=NeXusField(
            name="pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PRESSURE",
        ),
    )
    changer_position = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-changer-position-field"
        ],
        dimensionality="dimensionless",
        description=("Sample changer position"),
        a_nexus_field=NeXusField(
            name="changer_position",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    unit_cell_abc = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-unit-cell-abc-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-unit-cell-alphabetagamma-field"
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
    unit_cell = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-unit-cell-field"
        ],
        dimensionality="[length]",
        shape=["*", 6],
        description=("Unit cell parameters (lengths and angles)"),
        a_nexus_field=NeXusField(
            name="unit_cell",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-unit-cell-volume-field"
        ],
        dimensionality="[length] ** 3",
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-sample-orientation-field"
        ],
        dimensionality="[angle]",
        shape=[3],
        description=(
            "This will follow the Busing-Levy convention: W. R. Busing and H. A. "
            "Levy (1967). Acta Cryst. 22, 457-464"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-orientation-matrix-field"
        ],
        shape=["*", 3, 3],
        description=(
            "Orientation matrix of single crystal sample using Busing-Levy "
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
    ub_matrix = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-ub-matrix-field"
        ],
        shape=["*", 3, 3],
        description=(
            "UB matrix of single crystal sample using Busing-Levy convention: W. "
            "R. Busing and H. A. Levy (1967). Acta Cryst. 22, 457-464. This is "
            "the multiplication of the orientation_matrix, given above, with the "
            ":math:`B` matrix which can be derived from the lattice constants."
        ),
        a_nexus_field=NeXusField(
            name="ub_matrix",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-mass-field"
        ],
        dimensionality="[mass]",
        shape=["*"],
        description=("Mass of sample"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-density-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        shape=["*"],
        description=("Density of sample"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-relative-molecular-mass-field"
        ],
        dimensionality="[mass]",
        shape=["*"],
        description=("Relative Molecular Mass of sample"),
        a_nexus_field=NeXusField(
            name="relative_molecular_mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS",
        ),
    )
    type = Quantity(
        type=MEnum(
            [
                "sample",
                "sample+can",
                "can",
                "sample+buffer",
                "buffer",
                "calibration sample",
                "normalisation sample",
                "simulated data",
                "none",
                "sample environment",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "sample",
                "sample+can",
                "can",
                "sample+buffer",
                "buffer",
                "calibration sample",
                "normalisation sample",
                "simulated data",
                "none",
                "sample environment",
            ],
        ),
    )
    situation = Quantity(
        type=MEnum(
            [
                "air",
                "vacuum",
                "inert atmosphere",
                "oxidising atmosphere",
                "reducing atmosphere",
                "sealed can",
                "other",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-situation-field"
        ],
        description=(
            "The atmosphere will be one of the components, which is where its "
            "details will be stored; the relevant components will be indicated "
            "by the entry in the sample_component member."
        ),
        a_nexus_field=NeXusField(
            name="situation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "air",
                "vacuum",
                "inert atmosphere",
                "oxidising atmosphere",
                "reducing atmosphere",
                "sealed can",
                "other",
            ],
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-description-field"
        ],
        description=("Description of the sample"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    preparation_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-preparation-date-field"
        ],
        description=("Date of preparation of the sample"),
        a_nexus_field=NeXusField(
            name="preparation_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    component = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-component-field"
        ],
        shape=["*"],
        description=("Details of the component of the sample and/or can"),
        a_nexus_field=NeXusField(
            name="component",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_component_quantity = Quantity(
        type=MEnum(["sample", "can", "atmosphere", "kit"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-sample-component-field"
        ],
        shape=["*"],
        description=("Type of component"),
        a_nexus_field=NeXusField(
            name="sample_component",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["sample", "can", "atmosphere", "kit"],
        ),
    )
    concentration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-concentration-field"
        ],
        dimensionality="[mass] / [length] ** 3",
        shape=["*"],
        description=("Concentration of each component"),
        a_nexus_field=NeXusField(
            name="concentration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    volume_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-volume-fraction-field"
        ],
        shape=["*"],
        description=("Volume fraction of each component"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-scattering-length-density-field"
        ],
        dimensionality="1 / [length] ** 2",
        shape=["*"],
        description=("Scattering length density of each component"),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-unit-cell-class-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-space-group-field"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-point-group-field"
        ],
        shape=["*"],
        description=("Crystallographic point group, deprecated if space_group present"),
        a_nexus_field=NeXusField(
            name="point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    path_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-path-length-field"
        ],
        dimensionality="[length]",
        description=(
            "Path length through sample/can for simple case when it does not "
            "vary with scattering direction"
        ),
        a_nexus_field=NeXusField(
            name="path_length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    path_length_window = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-path-length-window-field"
        ],
        dimensionality="[length]",
        description=(
            "Thickness of a beam entry/exit window on the can (mm) - assumed "
            "same for entry and exit"
        ),
        a_nexus_field=NeXusField(
            name="path_length_window",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-thickness-field"
        ],
        dimensionality="[length]",
        description=("sample thickness"),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    external_DAC = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-external-dac-field"
        ],
        description=("value sent to user's sample setup"),
        a_nexus_field=NeXusField(
            name="external_DAC",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    short_title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-short-title-field"
        ],
        description=("20 character fixed length sample description for legends"),
        a_nexus_field=NeXusField(
            name="short_title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        description=(
            "Optional rotation angle for the case when the powder diagram has "
            "been obtained through an omega-2theta scan like from a traditional "
            "single detector powder diffractometer. Note, it is recommended to "
            "use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    x_translation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-x-translation-field"
        ],
        dimensionality="[length]",
        description=(
            "Translation of the sample along the X-direction of the laboratory "
            "coordinate system Note, it is recommended to use NXtransformations "
            "instead."
        ),
        a_nexus_field=NeXusField(
            name="x_translation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-distance-field"
        ],
        dimensionality="[length]",
        description=(
            "Translation of the sample along the Z-direction of the laboratory "
            "coordinate system. Note, it is recommended to use NXtransformations "
            "instead."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    physical_form = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXsample.html#nxsample-physical-form-field"
        ],
        description=(
            "Physical form of the sample material. Examples include single "
            "crystal, foil, pellet, powder, thin film, disc, foam, gas, liquid, "
            "amorphous."
        ),
        a_nexus_field=NeXusField(
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
