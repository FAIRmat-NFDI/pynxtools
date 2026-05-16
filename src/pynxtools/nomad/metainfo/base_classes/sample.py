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
from nomad.datamodel.metainfo.basesections import CompositeSystem
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.beam import Beam
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.environment import Environment
from pynxtools.nomad.metainfo.base_classes.geometry import Geometry
from pynxtools.nomad.metainfo.base_classes.history import History
from pynxtools.nomad.metainfo.base_classes.log import Log
from pynxtools.nomad.metainfo.base_classes.off_geometry import OffGeometry
from pynxtools.nomad.metainfo.base_classes.positioner import Positioner
from pynxtools.nomad.metainfo.base_classes.sample_component import SampleComponent

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Sample"]


class Sample(CompositeSystem):
    """Any information on the sample.

    This could include scanned variables that
    are associated with one of the data dimensions, e.g. the magnetic field, or
    logged data, e.g. monitored temperature vs elapsed time."""

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            category="base",
            optionality="optional",
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
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleGeometry",
        repeats=True,
    )
    beam = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleBeam",
        repeats=True,
        variable=True,
    )
    sample_component = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleSampleComponent",
        repeats=True,
        variable=True,
    )
    transmission = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleTransmission",
        repeats=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleData",
        repeats=True,
        variable=True,
    )
    temperature_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleTemperatureLog",
        repeats=True,
    )
    log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleLog",
        repeats=True,
        variable=True,
    )
    temperature_env = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleTemperatureEnv",
        repeats=True,
    )
    magnetic_field = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleMagneticField",
        repeats=True,
    )
    magnetic_field_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleMagneticFieldLog",
        repeats=True,
    )
    magnetic_field_env = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleMagneticFieldEnv",
        repeats=True,
    )
    external_ADC = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleExternalAdc",
        repeats=True,
    )
    positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SamplePositioner",
        repeats=True,
        variable=True,
    )
    off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleOffGeometry",
        repeats=True,
        variable=True,
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleEnvironment",
        repeats=True,
        variable=True,
    )
    history = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sample.SampleHistory",
        repeats=True,
    )

    name_field = Quantity(
        type=str,
        description="Descriptive name of sample",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        description="The chemical formula specified using CIF conventions. Abbreviated version of CIF standard: * Only recognized element symbols may be used. * Each element symbol is followed by a 'count' number. A count of '1' may be omitted. * A space or parenthesis must separate each cluster of (element symbol + count). * Where a group of elements is enclosed in parentheses, the multiplier for the group must follow the closing parentheses. That is, all element and group multipliers are assumed to be printed as subscripted numbers. * Unless the elements are ordered in a manner that corresponds to their chemical structure, the order of the elements within any group or moiety depends on whether or not carbon is present. * If carbon is present, the order should be: - C, then H, then the other elements in alphabetical order of their symbol. - If carbon is not present, the elements are listed purely in alphabetic order of their symbol. * This is the *Hill* system used by Chemical Abstracts.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        dimensionality="[temperature]",
        description="Sample temperature. This could be a scanned variable",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    electric_field = Quantity(
        type=np.float64,
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        shape=["*"],
        description="Applied electric field",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="electric_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    electric_field__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["x", "y", "z"],
            parent_field="electric_field",
        ),
    )
    magnetic_field = Quantity(
        type=np.float64,
        shape=["*"],
        description="Applied magnetic field",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="magnetic_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    magnetic_field__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["x", "y", "z"],
            parent_field="magnetic_field",
        ),
    )
    stress_field = Quantity(
        type=np.float64,
        shape=["*"],
        description="Applied external stress field",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="stress_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    stress_field__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["x", "y", "z"],
            parent_field="stress_field",
        ),
    )
    pressure = Quantity(
        type=np.float64,
        dimensionality="[mass] / [length] / [time] ** 2",
        shape=["*"],
        description="Applied pressure",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PRESSURE",
        ),
    )
    changer_position = Quantity(
        type=np.int64,
        dimensionality="dimensionless",
        description="Sample changer position",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="changer_position",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    unit_cell_abc = Quantity(
        type=np.float64,
        dimensionality="[length]",
        shape=[3],
        description="Crystallography unit cell parameters a, b, and c",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="unit_cell_abc",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_alphabetagamma = Quantity(
        type=np.float64,
        dimensionality="[angle]",
        shape=[3],
        description="Crystallography unit cell parameters alpha, beta, and gamma",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="unit_cell_alphabetagamma",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    unit_cell = Quantity(
        type=np.float64,
        dimensionality="[length]",
        shape=["*", 6],
        description="Unit cell parameters (lengths and angles)",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="unit_cell",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    unit_cell_volume = Quantity(
        type=np.float64,
        dimensionality="[length] ** 3",
        shape=["*"],
        description="Volume of the unit cell",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="unit_cell_volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )
    sample_orientation = Quantity(
        type=np.float64,
        dimensionality="[angle]",
        shape=[3],
        description="This will follow the Busing-Levy convention: W. R. Busing and H. A. Levy (1967). Acta Cryst. 22, 457-464",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sample_orientation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    orientation_matrix = Quantity(
        type=np.float64,
        shape=["*", 3, 3],
        description="Orientation matrix of single crystal sample using Busing-Levy convention: W. R. Busing and H. A. Levy (1967). Acta Cryst. 22, 457-464",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="orientation_matrix",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    ub_matrix = Quantity(
        type=np.float64,
        shape=["*", 3, 3],
        description="UB matrix of single crystal sample using Busing-Levy convention: W. R. Busing and H. A. Levy (1967). Acta Cryst. 22, 457-464. This is the multiplication of the orientation_matrix, given above, with the :math:`B` matrix which can be derived from the lattice constants.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="ub_matrix",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    mass = Quantity(
        type=np.float64,
        dimensionality="[mass]",
        shape=["*"],
        description="Mass of sample",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS",
        ),
    )
    density = Quantity(
        type=np.float64,
        dimensionality="[mass] / [length] ** 3",
        shape=["*"],
        description="Density of sample",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="density",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    relative_molecular_mass = Quantity(
        type=np.float64,
        dimensionality="[mass]",
        shape=["*"],
        description="Relative Molecular Mass of sample",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        description="The atmosphere will be one of the components, which is where its details will be stored; the relevant components will be indicated by the entry in the sample_component member.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
    description_field = Quantity(
        type=str,
        description="Description of the sample",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    preparation_date = Quantity(
        type=Datetime,
        description="Date of preparation of the sample",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="preparation_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    component = Quantity(
        type=str,
        shape=["*"],
        description="Details of the component of the sample and/or can",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="component",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_component = Quantity(
        type=MEnum(["sample", "can", "atmosphere", "kit"]),
        shape=["*"],
        description="Type of component",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sample_component",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["sample", "can", "atmosphere", "kit"],
        ),
    )
    concentration = Quantity(
        type=np.float64,
        dimensionality="[mass] / [length] ** 3",
        shape=["*"],
        description="Concentration of each component",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="concentration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_MASS_DENSITY",
        ),
    )
    volume_fraction = Quantity(
        type=np.float64,
        shape=["*"],
        description="Volume fraction of each component",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="volume_fraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    scattering_length_density = Quantity(
        type=np.float64,
        dimensionality="1 / [length] ** 2",
        shape=["*"],
        description="Scattering length density of each component",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        description="In case it is all we know and we want to record/document it",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
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
        shape=["*"],
        description="Crystallographic space group",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="space_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    point_group = Quantity(
        type=str,
        shape=["*"],
        description="Crystallographic point group, deprecated if space_group present",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    path_length = Quantity(
        type=np.float64,
        dimensionality="[length]",
        description="Path length through sample/can for simple case when it does not vary with scattering direction",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="path_length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    path_length_window = Quantity(
        type=np.float64,
        dimensionality="[length]",
        description="Thickness of a beam entry/exit window on the can (mm) - assumed same for entry and exit",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="path_length_window",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        dimensionality="[length]",
        description="sample thickness",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    external_DAC = Quantity(
        type=np.float64,
        description="value sent to user's sample setup",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="external_DAC",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    short_title = Quantity(
        type=str,
        description="20 character fixed length sample description for legends",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="short_title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    rotation_angle = Quantity(
        type=np.float64,
        dimensionality="[angle]",
        description="Optional rotation angle for the case when the powder diagram has been obtained through an omega-2theta scan like from a traditional single detector powder diffractometer. Note, it is recommended to use NXtransformations instead.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="rotation_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    x_translation = Quantity(
        type=np.float64,
        dimensionality="[length]",
        description="Translation of the sample along the X-direction of the laboratory coordinate system Note, it is recommended to use NXtransformations instead.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="x_translation",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    distance = Quantity(
        type=np.float64,
        dimensionality="[length]",
        description="Translation of the sample along the Z-direction of the laboratory coordinate system. Note, it is recommended to use NXtransformations instead.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    physical_form = Quantity(
        type=str,
        description="Physical form of the sample material. Examples include single crystal, foil, pellet, powder, thin film, disc, foam, gas, liquid, amorphous.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — one Section class per group defined in NXsample.
# These are referenced by the SubSections above via string FQNs and resolved
# lazily by NOMAD at __init_metainfo__() time.
# =============================================================================


class SampleGeometry(Geometry):
    "The position and orientation of the center of mass of the sample"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name="geometry",
            name_type="specified",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the sample and NXoff_geometry to describe its shape instead",
        ),
    )


class SampleBeam(Beam):
    "Details of beam incident on sample - used to calculate sample/beam interaction point"

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class SampleSampleComponent(SampleComponent):
    "One group per sample component This is the preferred way of recording per component information over the n_comp arrays"

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample_component",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class SampleTransmission(Data):
    "As a function of Wavelength"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="transmission",
            name_type="specified",
            optionality="optional",
        ),
    )


class SampleData(Data):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )


class SampleTemperatureLog(Log):
    "temperature_log.value is a link to e.g. temperature_env.sensor1.value_log.value"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="temperature_log",
            name_type="specified",
            optionality="optional",
            deprecated="use ``temperature``, see: https://github.com/nexusformat/definitions/issues/816",
        ),
    )


class SampleLog(Log):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )


class SampleTemperatureEnv(Environment):
    "Additional sample temperature environment information"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="temperature_env",
            name_type="specified",
            optionality="optional",
        ),
    )


class SampleMagneticField(Log):
    "magnetic_field.value is a link to e.g. magnetic_field_env.sensor1.value"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="magnetic_field",
            name_type="specified",
            optionality="optional",
        ),
    )


class SampleMagneticFieldLog(Log):
    "magnetic_field_log.value is a link to e.g. magnetic_field_env.sensor1.value_log.value"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="magnetic_field_log",
            name_type="specified",
            optionality="optional",
            deprecated="use ``magnetic_field``, see: https://github.com/nexusformat/definitions/issues/816",
        ),
    )


class SampleMagneticFieldEnv(Environment):
    "Additional sample magnetic environment information"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name="magnetic_field_env",
            name_type="specified",
            optionality="optional",
        ),
    )


class SampleExternalAdc(Log):
    "logged value (or logic state) read from user's setup"

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="external_ADC",
            name_type="specified",
            optionality="optional",
        ),
    )


class SamplePositioner(Positioner):
    "Any positioner (motor, PZT, ...) used to locate the sample"

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class SampleOffGeometry(OffGeometry):
    "This group describes the shape of the sample"

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXoff_geometry",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )


class SampleEnvironment(Environment):
    "Any environmental or external stimuli/measurements. These can include, among others: applied pressure, surrounding gas phase and gas pressure, external electric/magnetic/mechanical fields, temperature, ..."

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenvironment",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )


class SampleHistory(History):
    "A set of physical processes that occurred to the sample prior/during experiment."

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXhistory",
            name="history",
            name_type="specified",
            optionality="optional",
        ),
    )
