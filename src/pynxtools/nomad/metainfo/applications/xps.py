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
from pynxtools.nomad.metainfo.applications.mpes import (
    Mpes,
    MpesData,
    MpesInstrument,
    MpesSample,
)
from pynxtools.nomad.metainfo.base_classes.beam import Beam
from pynxtools.nomad.metainfo.base_classes.collectioncolumn import Collectioncolumn
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.electronanalyzer import Electronanalyzer
from pynxtools.nomad.metainfo.base_classes.energydispersion import Energydispersion
from pynxtools.nomad.metainfo.base_classes.fit import Fit
from pynxtools.nomad.metainfo.base_classes.fit_function import FitFunction
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.peak import Peak
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.transformations import Transformations

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
        categories=[ExperimentCategory],
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxps",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="sample stage",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="sample stage normal",
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-xps-coordinate-system-x-field"
        ],
        dimensionality="[length]",
        unit="m",
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
        unit="m",
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
        unit="m",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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

    source_probe = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrumentSourceProbe",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_probe",
            name_type="specified",
            optionality="recommended",
        ),
    )
    beam_probe = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrumentBeamProbe",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_probe",
            name_type="specified",
            optionality="required",
        ),
    )
    electronanalyzer = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrumentElectronanalyzer",
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


class XpsInstrumentSourceProbe(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-source-probe-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="source_probe",
            name_type="specified",
            optionality="recommended",
        ),
    )

    power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-source-probe-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        unit="watt",
        a_nexus_field=NeXusField(
            name="power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_POWER",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "watt"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsInstrumentBeamProbe(Beam):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beam_probe",
            name_type="specified",
            optionality="required",
        ),
    )

    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrumentBeamProbeTransformations",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-depends-on-field"
        ],
        description=(
            "Reference to the transformation describing the direction of the "
            "beam relative to a defined coordinate system. Should point to "
            "/entry/instrument/beam_probe/transformations/beam_direction."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsInstrumentBeamProbeTransformations(Transformations):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="recommended",
        ),
    )

    beam_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-direction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Beam direction in the XPS coordinate system after rotation."),
        a_nexus_field=NeXusField(
            name="beam_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    beam_direction__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-direction-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="beam_direction",
        ),
    )
    beam_direction__depends_on = Quantity(
        type=MEnum(["beam_polar_angle_of_incidence"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-direction-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="beam_direction",
            enumeration=["beam_polar_angle_of_incidence"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="beam_polar_angle_of_incidence",
        ),
    )
    beam_polar_angle_of_incidence = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-polar-angle-of-incidence-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Incidence angle of the beam with respect to the upward z-direction, "
            "defined by the sample stage."
        ),
        a_nexus_field=NeXusField(
            name="beam_polar_angle_of_incidence",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    beam_polar_angle_of_incidence__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-polar-angle-of-incidence-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="beam_polar_angle_of_incidence",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    beam_polar_angle_of_incidence__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-polar-angle-of-incidence-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="beam_polar_angle_of_incidence",
        ),
    )
    beam_polar_angle_of_incidence__depends_on = Quantity(
        type=MEnum(["beam_azimuth_angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-polar-angle-of-incidence-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="beam_polar_angle_of_incidence",
            enumeration=["beam_azimuth_angle"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="beam_azimuth_angle",
        ),
    )
    beam_azimuth_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-azimuth-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Azimuthal rotation of the beam from the y-direction defined by the "
            "sample stage."
        ),
        a_nexus_field=NeXusField(
            name="beam_azimuth_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    beam_azimuth_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-azimuth-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="beam_azimuth_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    beam_azimuth_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-azimuth-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="beam_azimuth_angle",
        ),
    )
    beam_azimuth_angle__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-beam-probe-transformations-beam-azimuth-angle-depends-on-attribute"
        ],
        description=(
            "This should point to the coordinate system defined in "
            "/entry/xps_coordinate_system."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="beam_azimuth_angle",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsInstrumentElectronanalyzer(Electronanalyzer):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectronanalyzer",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    collectioncolumn = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrumentElectronanalyzerCollectioncolumn",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollectioncolumn",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    energydispersion = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrumentElectronanalyzerEnergydispersion",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenergydispersion",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    transformations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsInstrumentElectronanalyzerTransformations",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="recommended",
        ),
    )

    work_function = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-work-function-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="work_function",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-depends-on-field"
        ],
        description=(
            "Reference to the transformation describing the orientation of the "
            "analyzer relative to a defined coordinate system."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsInstrumentElectronanalyzerCollectioncolumn(Collectioncolumn):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-collectioncolumn-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollectioncolumn",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    magnification = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-collectioncolumn-magnification-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="magnification",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsInstrumentElectronanalyzerEnergydispersion(Energydispersion):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-energydispersion-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXenergydispersion",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-energydispersion-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="radius",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    energy_scan_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-energydispersion-energy-scan-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="energy_scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "fixed_analyzer_transmission",
                "fixed_retardation_ratio",
                "fixed_energy",
                "snapshot",
                "dither",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsInstrumentElectronanalyzerTransformations(Transformations):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="recommended",
        ),
    )

    analyzer_take_off_polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Polar tilt of the analyzer with respect to the upward z-direction, "
            "defined by the sample stage. The angle between the incoming beam "
            "and the analyzer is given by beam_analyzer_angle = "
            "beam_polar_angle_of_incidence + analyzer_take_off_polar_angle. In "
            "practice, the analyzer axis is often set as the z axis "
            "(analyzer_take_off_polar_angle = 0), so that beam_analyzer_angle = "
            "beam_polar_angle_of_incidence. For magic angle configurations, this "
            "angle is 54.5°."
        ),
        a_nexus_field=NeXusField(
            name="analyzer_take_off_polar_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    analyzer_take_off_polar_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-polar-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_take_off_polar_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    analyzer_take_off_polar_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-polar-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_take_off_polar_angle",
        ),
    )
    analyzer_take_off_polar_angle__depends_on = Quantity(
        type=MEnum(["analyzer_take_off_azimuth_angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-polar-angle-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_take_off_polar_angle",
            enumeration=["analyzer_take_off_azimuth_angle"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="analyzer_take_off_azimuth_angle",
        ),
    )
    analyzer_take_off_azimuth_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-azimuth-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Azimuthal rotation of the analyzer from the y-direction defined by "
            "the sample stage."
        ),
        a_nexus_field=NeXusField(
            name="analyzer_take_off_azimuth_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    analyzer_take_off_azimuth_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-azimuth-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_take_off_azimuth_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    analyzer_take_off_azimuth_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-azimuth-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_take_off_azimuth_angle",
        ),
    )
    analyzer_take_off_azimuth_angle__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-instrument-electronanalyzer-transformations-analyzer-take-off-azimuth-angle-depends-on-attribute"
        ],
        description=(
            "This should point to the coordinate system defined in "
            "/entry/xps_coordinate_system."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="analyzer_take_off_azimuth_angle",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitData",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )
    peakPEAK = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitPeakPEAK",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="peakPEAK",
            name_type="partial",
            optionality="required",
        ),
    )
    backgroundBACKGROUND = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitBackgroundBACKGROUND",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="backgroundBACKGROUND",
            name_type="partial",
            optionality="required",
        ),
    )
    global_fit_function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitGlobalFitFunction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="global_fit_function",
            name_type="specified",
            optionality="recommended",
        ),
    )
    error_function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitErrorFunction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="error_function",
            name_type="specified",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    figure_of_meritMETRIC = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-figure-of-meritmetric-field"
        ],
        variable=True,
        dimensionality="dimensionless",
        unit="dimensionless",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitData(Data):
    """
    Input data and results of the fit.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    input_dependent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-data-input-dependent-field"
        ],
        description=(
            "Dependent variable for this fit procedure. This could be a link to "
            "entry/data/data."
        ),
        a_nexus_field=NeXusField(
            name="input_dependent",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    input_independent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-data-input-independent-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Independent variable for this fit procedure. This could be a link "
            "to entry/data/energy."
        ),
        a_nexus_field=NeXusField(
            name="input_independent",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    fit_sum = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-data-fit-sum-field"
        ],
        a_nexus_field=NeXusField(
            name="fit_sum",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    residual = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-data-residual-field"
        ],
        a_nexus_field=NeXusField(
            name="residual",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitPeakPEAK(Peak):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="peakPEAK",
            name_type="partial",
            optionality="required",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitPeakPEAKData",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )
    function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitPeakPEAKFunction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-label-field"
        ],
        a_nexus_field=NeXusField(
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    total_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-total-area-field"
        ],
        description=(
            "Total area under the peak after background removal. This concept is "
            "related to term `3.16`_ of the ISO 18115-1:2023 standard. .. _3.16: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:3.16"
        ),
        a_nexus_field=NeXusField(
            name="total_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    relative_atomic_concentration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-relative-atomic-concentration-field"
        ],
        description=(
            "Atomic concentration of the species defined by this peak. This "
            "should be a value between 0 and 1."
        ),
        a_nexus_field=NeXusField(
            name="relative_atomic_concentration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitPeakPEAKData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-data-position-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("This could be a link to entry/data/energy."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-data-intensity-field"
        ],
        description=(
            "Intensity values of the fitted function at each energy in the "
            "position field. This concept is related to term `3.15`_ of the ISO "
            "18115-1:2023 standard. .. _3.15: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:3.15"
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitPeakPEAKFunction(FitFunction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    fit_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitPeakPEAKFunctionFitParameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="fit_parameters",
            name_type="specified",
            optionality="recommended",
        ),
    )

    function_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-function-type-field"
        ],
        description=(
            "Type of fit function used. The user is encouraged to use one of the "
            "options defined in the enumeration, but in case none of these fit "
            "(e.g., in the case of very complex line shapes), a different value "
            "for the ``function_type`` field can be used. In that case in "
            "particular, but also if one of the suggested values is used, the "
            "functional form of the peak should be given by the "
            "``formula_description`` field. The user is also encouraged to use "
            "the ``description`` field for describing the fit function in a "
            "human-readable way."
        ),
        a_nexus_field=NeXusField(
            name="function_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "Gaussian",
                "Lorentzian",
                "Voigt",
                "Gaussian-Lorentzian Sum",
                "Gaussian-Lorentzian Product",
                "Asymmetric Lorentzian",
                "Doniach-Sunjic",
                "Asymmetric Finite",
            ],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-description-field"
        ],
        description=("Human-readable description of the peak fit function."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    formula_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-formula-description-field"
        ],
        a_nexus_field=NeXusField(
            name="formula_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitPeakPEAKFunctionFitParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-fit-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="fit_parameters",
            name_type="specified",
            optionality="recommended",
        ),
    )

    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-fit-parameters-area-field"
        ],
        description=("Area of the peak."),
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    width = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-fit-parameters-width-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Width of a peak at a defined fraction of the peak height. Usually, "
            "this will be the Full Width at Half Maximum of the peak (FWHM). For "
            "asymmetric peaks, convenient measures of peak width are the "
            "half-widths of each side of the peak at half maximum intensity. "
            "This concept is related to term `3.28`_ of the ISO 18115-1:2023 "
            "standard. .. _3.28: "
            "https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:3.28"
        ),
        a_nexus_field=NeXusField(
            name="width",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-peakpeak-function-fit-parameters-position-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=("Position of the peak on the energy axis."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitBackgroundBACKGROUND(Peak):
    """
    Functional form of one of the fitted XPS backgrounds.

    This concept is related to term `3.21`_ of the ISO 18115-1:2023 standard.

    .. _3.21:
    https://www.iso.org/obp/ui/en/#iso:std:iso:18115:-1:ed-3:v1:en:term:3.21
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="backgroundBACKGROUND",
            name_type="partial",
            optionality="required",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitBackgroundBACKGROUNDData",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )
    function = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsFitBackgroundBACKGROUNDFunction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-label-field"
        ],
        a_nexus_field=NeXusField(
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitBackgroundBACKGROUNDData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-data-position-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-data-intensity-field"
        ],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitBackgroundBACKGROUNDFunction(FitFunction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-function-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    function_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-function-function-type-field"
        ],
        description=(
            "Type of fit function used. The user is encouraged to use one of the "
            "options defined in the enumeration, but in case none of these fit "
            "(e.g., in the case of very complex line shapes), a different value "
            "for the ``function_type`` field can be used. In that case in "
            "particular, but also if one of the suggested values is used, the "
            "functional form of the background should be given by the "
            "``formula_description`` field. The user is also encouraged to use "
            "the ``description`` field for describing the fit function in a "
            "human-readable way."
        ),
        a_nexus_field=NeXusField(
            name="function_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["Linear", "Shirley", "Tougaard", "Step Down", "Step Up"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-function-description-field"
        ],
        description=("Human-readable description of the background fit function."),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    formula_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-backgroundbackground-function-formula-description-field"
        ],
        a_nexus_field=NeXusField(
            name="formula_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitGlobalFitFunction(FitFunction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-global-fit-function-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="global_fit_function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    function_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-global-fit-function-function-type-field"
        ],
        a_nexus_field=NeXusField(
            name="function_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-global-fit-function-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    formula_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-global-fit-function-formula-description-field"
        ],
        a_nexus_field=NeXusField(
            name="formula_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsFitErrorFunction(FitFunction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-error-function-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="error_function",
            name_type="specified",
            optionality="recommended",
        ),
    )

    function_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-error-function-function-type-field"
        ],
        a_nexus_field=NeXusField(
            name="function_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-error-function-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    formula_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-fit-error-function-formula-description-field"
        ],
        a_nexus_field=NeXusField(
            name="formula_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        section_def="pynxtools.nomad.metainfo.applications.xps.XpsSampleTransformations",
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpsSampleTransformations(Transformations):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="transformations",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sample_rotation_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-rotation-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation about the sample normal."),
        a_nexus_field=NeXusField(
            name="sample_rotation_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    sample_rotation_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-rotation-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_rotation_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    sample_rotation_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-rotation-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="sample_rotation_angle",
        ),
    )
    sample_rotation_angle__depends_on = Quantity(
        type=MEnum(["sample_normal_polar_angle_of_tilt"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-rotation-angle-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_rotation_angle",
            enumeration=["sample_normal_polar_angle_of_tilt"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="sample_normal_polar_angle_of_tilt",
        ),
    )
    sample_normal_polar_angle_of_tilt = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-polar-angle-of-tilt-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Polar tilt of the sample with respect to the upward z-direction, "
            "defined by the sample stage."
        ),
        a_nexus_field=NeXusField(
            name="sample_normal_polar_angle_of_tilt",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    sample_normal_polar_angle_of_tilt__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-polar-angle-of-tilt-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_normal_polar_angle_of_tilt",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    sample_normal_polar_angle_of_tilt__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-polar-angle-of-tilt-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="sample_normal_polar_angle_of_tilt",
        ),
    )
    sample_normal_polar_angle_of_tilt__depends_on = Quantity(
        type=MEnum(["sample_normal_tilt_azimuth_angle"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-polar-angle-of-tilt-depends-on-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_normal_polar_angle_of_tilt",
            enumeration=["sample_normal_tilt_azimuth_angle"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="sample_normal_tilt_azimuth_angle",
        ),
    )
    sample_normal_tilt_azimuth_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-tilt-azimuth-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Azimuthal rotation of the sample from the y-direction defined by "
            "the sample stage."
        ),
        a_nexus_field=NeXusField(
            name="sample_normal_tilt_azimuth_angle",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    sample_normal_tilt_azimuth_angle__transformation_type = Quantity(
        type=MEnum(["rotation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-tilt-azimuth-angle-transformation-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="transformation_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_normal_tilt_azimuth_angle",
            enumeration=["rotation"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="rotation",
        ),
    )
    sample_normal_tilt_azimuth_angle__vector = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-tilt-azimuth-angle-vector-attribute"
        ],
        shape=[3],
        a_nexus_attribute=NeXusAttribute(
            name="vector",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            parent_field="sample_normal_tilt_azimuth_angle",
        ),
    )
    sample_normal_tilt_azimuth_angle__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXxps.html#nxxps-entry-sample-transformations-sample-normal-tilt-azimuth-angle-depends-on-attribute"
        ],
        description=(
            "This should point to the coordinate system defined in "
            "/entry/xps_coordinate_system."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="sample_normal_tilt_azimuth_angle",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
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
        unit="joule",
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
