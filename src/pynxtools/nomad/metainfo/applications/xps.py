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
from pynxtools.nomad.metainfo.applications.mpes import (
    Mpes,
    MpesData,
    MpesInstrument,
    MpesSample,
)
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.fit import Fit

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
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsCoordinateSystem",
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
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrument",
        repeats=True,
        variable=True,
        description=(
            "Description of the XPS spectrometer and its individual parts. This "
            "concept is related to term `12.58`_ of the ISO 18115-1:2023 "
            "standard. .. _12.58: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.58"
        ),
    )
    energy_referencing = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.Calibration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="energy_referencing",
            name_type="specified",
            optionality="recommended",
        ),
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


class XpsCoordinateSystem(CoordinateSystem):
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


class XpsInstrument(MpesInstrument):
    """
    Description of the XPS spectrometer and its individual parts.

    This concept is related to term `12.58`_ of the ISO 18115-1:2023 standard.

    .. _12.58:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:12.58
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    electronanalyzer = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electronanalyzer.Electronanalyzer",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectronanalyzer",
            name=None,
            name_type="any",
            optionality="required",
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


class XpsSample(MpesSample):
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

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="recommended",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsData(MpesData):
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
