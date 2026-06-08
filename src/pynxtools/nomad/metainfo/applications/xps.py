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
# Run `pynx nomad generate-metainfo --nxdl NXxps` to regenerate.
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
from pynxtools.nomad.metainfo.applications.mpes import Mpes
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.fit import Fit
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xps"]


class Xps(Mpes):
    """
    This is the application definition for X-ray photoelectron spectroscopy.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxps",
            category="application",
        ),
    )

    xps_coordinate_system = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsXpsCoordinateSystem",
        repeats=False,
        description=(
            "In traditional surface science, a left-handed coordinate system is "
            "used such that the positive z-axis points along the normal of the "
            "sample stage, and the x- and y-axes lie in the plane of the sample "
            "stage. However, in NeXus, a coordinate system that is the same as "
            "`McStas`_ is used. `xps_coordinate_system` gives the user the "
            "opportunity to work in the traditional base coordinate system. .. "
            "_McStas: http://mcstas.org/ .. image:: xps/xps_cs.png :width: 40%"
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=True,
        variable=True,
        description=(
            "Description of the XPS spectrometer and its individual parts. This "
            "concept is related to term `12.58`_ of the ISO 18115-1:2023 "
            "standard. .. _12.58: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.58"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    energy_referencing = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsEnergyReferencing",
        repeats=False,
    )
    transmission_correction = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="transmission_correction",
            name_type="specified",
            optionality="recommended",
        ),
    )
    fit = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFit",
        repeats=True,
        variable=True,
        description=(
            "Peak model for XPS fitting. Each `NXfit` instance shall be used for "
            "the description of _one_ peak fit in _one_ XPS region. As an "
            "example, this could be used to describe the fitting of one measured "
            "C 1s spectrum. This concept is related to term `3.29`_ of the ISO "
            "18115-1:2023 standard. .. _3.29: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:3.29"
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsSample",
        repeats=True,
        variable=True,
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsData",
        repeats=True,
        variable=True,
    )

    definition = Quantity(
        type=MEnum(["NXxps"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxps"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )
    method = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-method-field"
        ],
        description=(
            "A name of the experimental method according to `Clause 11`_ of the "
            "`ISO 18115-1:2023`_ specification. Examples for XPS-related "
            "experiments include: * X-ray photoelectron spectroscopy (XPS) * "
            "angle-resolved X-ray photoelectron spectroscopy (ARXPS) * "
            "ultraviolet photoelectron spectroscopy (UPS) * hard X-ray "
            "photoemission spectroscopy (HAXPES) * near ambient pressure X-ray "
            "photoelectron spectroscopy (NAPXPS) * electron spectroscopy for "
            "chemical analysis (ESCA) .. _ISO 18115-1:2023: "
            "https://www.iso.org/standard/74811.html .. _Clause 11: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:sec:11"
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    transitions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-transitions-field"
        ],
        a_nexus_field=NeXusField(
            name="transitions",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-start-time-field"
        ],
        description=(
            "Datetime of the start of the measurement. Should be an ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise the local time zone is assumed per ISO8601."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-end-time-field"
        ],
        description=(
            "Datetime of the end of the measurement. Should be a ISO8601 "
            "date/time stamp. It is recommended to add an explicit time zone, "
            "otherwise the local time zone is assumed per ISO8601."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
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


class XpsXpsCoordinateSystem(CoordinateSystem):
    """
    In traditional surface science, a left-handed coordinate system is used
    such that the positive z-axis points along the normal of the sample stage,
    and the x- and y-axes lie in the plane of the sample stage. However, in
    NeXus, a coordinate system that is the same as `McStas`_ is used.
    `xps_coordinate_system` gives the user the opportunity to work in the
    traditional base coordinate system.

    .. _McStas: http://mcstas.org/

    .. image:: xps/xps_cs.png :width: 40%
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="xps_coordinate_system",
            name_type="specified",
            optionality="recommended",
        ),
    )

    origin = Quantity(
        type=MEnum(["sample stage"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-origin-field"
        ],
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["sample stage"],
        ),
    )
    z_direction = Quantity(
        type=MEnum(["sample stage normal"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-z-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["sample stage normal"],
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-x-field"
        ],
        dimensionality="[length]",
        shape=[3],
        a_nexus_field=NeXusField(
            name="x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-y-field"
        ],
        dimensionality="[length]",
        shape=[3],
        a_nexus_field=NeXusField(
            name="y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-z-field"
        ],
        dimensionality="[length]",
        shape=[3],
        a_nexus_field=NeXusField(
            name="z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-depends-on-field"
        ],
        description=(
            "Link to transformations defining the XPS base coordinate system, "
            "which is defined such that the positive z-axis points along the "
            "sample stage normal, and the x- and y-axes lie in the plane of the "
            "sample stage."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsEnergyReferencing(Calibration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-energy-referencing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="energy_referencing",
            name_type="specified",
            optionality="recommended",
        ),
    )

    physical_quantity = Quantity(
        type=MEnum(["energy"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["energy"],
        ),
    )
    level = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-level-field"
        ],
        description=(
            "Electronic core or valence level that was used for the calibration. "
            "This should be single string defining the core or valence level "
            "that was used for energy referencing. The notation should be the "
            "same as the one described in the :ref:`NXmpes/ENTRY/transitions "
            "</NXmpes/ENTRY/transitions-field>` field."
        ),
        a_nexus_field=NeXusField(
            name="level",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    reference_peak = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-reference-peak-field"
        ],
        description=(
            "Reference peak that was used for the calibration. For example: "
            "adventitious carbon | C-C | metallic Au | elemental Si | Fermi edge "
            "| vacuum level"
        ),
        a_nexus_field=NeXusField(
            name="reference_peak",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    binding_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-binding-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "The binding energy (in units of eV) that the specified emission "
            "line appeared at, after adjusting the binding energy scale. This "
            "concept is related to term `12.16`_ of the ISO 18115-1:2023 "
            "standard. .. _12.16: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.16"
        ),
        a_nexus_field=NeXusField(
            name="binding_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-offset-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "Offset between measured binding energy and calibrated binding "
            "energy of the emission line."
        ),
        a_nexus_field=NeXusField(
            name="offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )
    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-energy-referencing-calibrated-axis-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        description=(
            "This is the calibrated energy axis to be used for data plotting. "
            "This could be a link to /entry/data/energy."
        ),
        a_nexus_field=NeXusField(
            name="calibrated_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFit(Fit):
    """
    Peak model for XPS fitting. Each `NXfit` instance shall be used for the
    description of _one_ peak fit in _one_ XPS region. As an example, this
    could be used to describe the fitting of one measured C 1s spectrum.

    This concept is related to term `3.29`_ of the ISO 18115-1:2023 standard.

    .. _3.29:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:3.29
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfit",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-label-field"
        ],
        a_nexus_field=NeXusField(
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    figure_of_meritMETRIC = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-figure-of-meritmetric-field"
        ],
        variable=True,
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="figure_of_meritMETRIC",
            type="NX_NUMBER",
            name_type="partial",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    figure_of_meritMETRIC__metric = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-figure-of-meritmetric-metric-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="metric",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="figure_of_meritMETRIC",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-depends-on-field"
        ],
        description=(
            "Reference to the transformation describing the orientation of the "
            "sample relative to a defined coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-chemical-formula-field"
        ],
        a_nexus_field=NeXusField(
            name="chemical_formula",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-atom-types-field"
        ],
        description=(
            "Array of comma-separated elements from the periodic table that are "
            "contained in the sample. If the sample substance has multiple "
            "components, all elements from each component must be included in "
            "`atom_types`."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    physical_form = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-physical-form-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    situation = Quantity(
        type=MEnum(
            [
                "vacuum",
                "inert atmosphere",
                "oxidizing atmosphere",
                "reducing atmosphere",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-sample-situation-field"
        ],
        a_nexus_field=NeXusField(
            name="situation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "vacuum",
                "inert atmosphere",
                "oxidizing atmosphere",
                "reducing atmosphere",
            ],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-data-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    energy__type = Quantity(
        type=MEnum(["kinetic", "binding"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-energy-type-attribute"
        ],
        description=(
            "The energy can be either stored as kinetic or as binding energy."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="energy",
            enumeration=["kinetic", "binding"],
        ),
    )
    energy_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-data-energy-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="energy_indices",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    signal = Quantity(
        type=MEnum(["data"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["data"],
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-data-field"
        ],
        description=(
            "Represents a measure of one- or more-dimensional photoemission "
            "counts, where the varied axis may be for example energy, momentum, "
            "spatial coordinate, pump-probe delay, spin index, temperature, etc. "
            "The axes traces should be linked to the actual encoder position in "
            "NXinstrument or calibrated axes in NXprocess (or classes inheriting "
            "from NXprocess)."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    photon_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-photon-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=(
            "Calibrated photon energy of the incoming probe beam. Could be a "
            "link to /entry/instrument/beam_probe/incident_energy."
        ),
        a_nexus_field=NeXusField(
            name="photon_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    kx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-kx-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated k-space coordinate in x direction. It is envisioned that "
            "the axes in momentum space are named ``kx``, ``ky``, and ``kz``. "
            "Typically, the vectors in momentum space are defined such that "
            "``kx`` and ``ky`` comprise the parallel component, while ``kz`` is "
            "the perpendicular component. It is also possible to define "
            "``k_parallel`` and ``k_perp`` for the parallel and perpendicular "
            "momenta, respectively. Units are typically 1/angstrom."
        ),
        a_nexus_field=NeXusField(
            name="kx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    ky = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-ky-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated k-space coordinate in y direction. For more information, "
            "see the definition of the :ref:`kx </NXmpes/ENTRY/DATA/kx-field>` "
            "axis."
        ),
        a_nexus_field=NeXusField(
            name="ky",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    kz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-kz-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated k-space coordinate in z direction. For more information, "
            "see the definition of the :ref:`kx </NXmpes/ENTRY/DATA/kx-field>` "
            "axis."
        ),
        a_nexus_field=NeXusField(
            name="kz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    k_parallel = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-k-parallel-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated parallel component in k-space. ``k_parallel`` and "
            ":ref:`k_perpendicular </NXmpes/ENTRY/DATA/k_perpendicular-field>` "
            "describe how the electron's wave vector ``k`` is split into "
            "components relative to the surface. ``k_parallel`` is the component "
            "of the electron's wave vector that is parallel to the surface. It "
            "is conserved during the photoemission process. This means that the "
            "electron's momentum along the surface inside the material is "
            "directly related to its measured momentum outside the material. "
            "Units are typically 1/angstrom."
        ),
        a_nexus_field=NeXusField(
            name="k_parallel",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    k_perpendicular = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-k-perpendicular-field"
        ],
        dimensionality="1 / [length]",
        description=(
            "Calibrated perpendicular component in k-space. ``k_perpendicular`` "
            "is the component that is normal (perpendicular) to the surface. It "
            "is not conserved during photoemission because the electron "
            "experiences a potential change when it exits the material into "
            "vacuum. To determine ``k_perpendicular`` inside the material, one "
            "typically needs to estimate the inner potential :math:`V_0`, which "
            "accounts for the energy shift due to the material's work function "
            "and electronic structure. Units are typically 1/angstrom."
        ),
        a_nexus_field=NeXusField(
            name="k_perpendicular",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVENUMBER",
        ),
    )
    angular0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-angular0-field"
        ],
        dimensionality="[angle]",
        description=(
            "First calibrated angular coordinate. It is envisioned that the axes "
            "in angular space are named ``angular0`` and ``angular1``. The "
            "angular axes should be named in order of decreasing speed, i.e., "
            "``angular0`` should be the fastest scan axis and ``angular1`` "
            "should be the slow-axis angular coordinate. However, ``angular0`` "
            "may also be second slow axis if the measurement is angularly "
            "integrated and ``angular1`` could also be the second fast axis in "
            "the case of simultaneous dispersion in two angular dimensions."
        ),
        a_nexus_field=NeXusField(
            name="angular0",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angular1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-angular1-field"
        ],
        dimensionality="[angle]",
        description=(
            "Second calibrated angular coordinate. For more information, see the "
            "definition of the :ref:`angular0 "
            "</NXmpes/ENTRY/DATA/angular0-field>` axis. This is typically the "
            "slower scan axis compared to ``angular0``."
        ),
        a_nexus_field=NeXusField(
            name="angular1",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    spatial0 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-spatial0-field"
        ],
        dimensionality="[length]",
        description=(
            "First calibrated spatial coordinate. It is envisioned that the axes "
            "in angular space are named ``spatial0`` and ``spatial1``. The "
            "spatial axes should be named in order of decreasing speed, i.e., "
            "``spatial0`` should be the fastest scan axis and `spatial1`` should "
            "be the slow-axis spatial coordinate. However, ``spatial`` may also "
            "be second slow axis if the measurement is spatially integrated and "
            "``spatial1`` could also be the second fast axis in the case of "
            "simultaneous dispersion in two spatial dimensions."
        ),
        a_nexus_field=NeXusField(
            name="spatial0",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    spatial1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-spatial1-field"
        ],
        dimensionality="[length]",
        description=(
            "Second calibrated spatial coordinate. For more information, see the "
            "definition of the :ref:`spatial0 "
            "</NXmpes/ENTRY/DATA/spatial0-field>` axis. This is typically the "
            "slower scan axis compared to ``spatial0``."
        ),
        a_nexus_field=NeXusField(
            name="spatial1",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    delay = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-delay-field"
        ],
        dimensionality="[time]",
        description=(
            "Calibrated pump-probe delay time. Could be a link to "
            "/entry/instrument/beam_pump/pulse_delay."
        ),
        a_nexus_field=NeXusField(
            name="delay",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmpes.html#nxmpes-entry-data-temperature-field"
        ],
        dimensionality="[time]",
        description=(
            "Calibrated temperature axis in case of experiments where the "
            "temperature was scanned. This is typically the sample temperature "
            "and could be linked from "
            "/entry/sample/temperature_env/temperature_sensor/value."
        ),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
