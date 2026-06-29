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
# Run `pynx nomad generate-metainfo --nxdl NXxrd_pan` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.applications.xrd import Xrd, XrdData
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["XrdPan"]


class XrdPan(Xrd):
    """
    NXxrd_pan is a specialization of NXxrd with extra properties for the
    PANalytical XRD data format.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxrd_pan",
            category="application",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanInstrument",
        repeats=True,
        variable=True,
    )
    experiment_config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanExperimentConfig",
        repeats=False,
        description=("Collect user inputs e.g. name or path of the input file."),
    )
    experiment_result = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanExperimentResult",
        repeats=False,
        description=(
            "All experiment results data such as scattering angle (2theta), "
            "intensity, incident angle, scattering vector, etc will be stored "
            "here."
        ),
    )
    q_data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanQData",
        repeats=False,
        description=("The desired view for scattering vectors."),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanSample",
        repeats=True,
        variable=True,
        description=("Description on sample."),
    )

    data_file = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-data-file-field"
        ],
        description=("Name of the data file."),
        a_nexus_field=NeXusField(
            name="data_file",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    measurement_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-measurement-type-field"
        ],
        description=("Type of measurement."),
        a_nexus_field=NeXusField(
            name="measurement_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition = Quantity(
        type=MEnum(["NXxrd_pan"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxrd_pan"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="NXxrd_pan",
        ),
    )
    method = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-method-field"
        ],
        description=(
            "Method used to collect the data default='X-Ray Diffraction (XRD)'"
        ),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["X-Ray Diffraction (XRD)"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXmonopd.html#nxmonopd-entry-start-time-field"
        ],
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class XrdPanInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrdPanInstrumentSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    xray_tube_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-xray-tube-material-field"
        ],
        description=("Type of the X-ray tube."),
        a_nexus_field=NeXusField(
            name="xray_tube_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["Cu", "Cr", "Mo", "Fe", "Ag", "In", "Ga"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    xray_tube_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-xray-tube-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("Current of the X-ray tube."),
        a_nexus_field=NeXusField(
            name="xray_tube_current",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    xray_tube_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-xray-tube-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=("Voltage of the X-ray tube."),
        a_nexus_field=NeXusField(
            name="xray_tube_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    k_alpha_one = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-k-alpha-one-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Wavelength of the K\\u03b1 1 line."),
        a_nexus_field=NeXusField(
            name="k_alpha_one",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    k_alpha_one__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-k-alpha-one-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="k_alpha_one",
            enumeration=["angstrom"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    k_alpha_two = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-k-alpha-two-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Wavelength of the K\\u03b1 2 line."),
        a_nexus_field=NeXusField(
            name="k_alpha_two",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    k_alpha_two__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-k-alpha-two-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="k_alpha_two",
            enumeration=["angstrom"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    ratio_k_alphatwo_k_alphaone = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-ratio-k-alphatwo-k-alphaone-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("K\\u03b1 2/K\\u03b1 1 intensity ratio."),
        a_nexus_field=NeXusField(
            name="ratio_k_alphatwo_k_alphaone",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    kbeta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-kbeta-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Wavelength of the K\\u00df line."),
        a_nexus_field=NeXusField(
            name="kbeta",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    kbeta__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-kbeta-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="kbeta",
            enumeration=["angstrom"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    source_peak_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-source-source-peak-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Wavelength of the X-ray source. Used to convert from 2-theta to Q."
        ),
        a_nexus_field=NeXusField(
            name="source_peak_wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrdPanInstrumentDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    scan_axis = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-detector-scan-axis-field"
        ],
        description=("Axis scanned."),
        a_nexus_field=NeXusField(
            name="scan_axis",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    scan_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-detector-scan-mode-field"
        ],
        description=("Mode of scan."),
        a_nexus_field=NeXusField(
            name="scan_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    integration_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-instrument-detector-integration-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Integration time per channel."),
        a_nexus_field=NeXusField(
            name="integration_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrdPanExperimentConfig(Object):
    """
    Collect user inputs e.g. name or path of the input file.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXobject",
            name="experiment_config",
            name_type="specified",
            optionality="optional",
        ),
    )

    two_theta = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanExperimentConfigTwoTheta",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXobject",
            name="two_theta",
            name_type="specified",
            optionality="required",
        ),
    )
    omega = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xrd_pan.XrdPanExperimentConfigOmega",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXobject",
            name="omega",
            name_type="specified",
            optionality="required",
        ),
    )

    beam_attenuation_factors = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-beam-attenuation-factors-field"
        ],
        description=("Beam attenuation factors over the path."),
        a_nexus_field=NeXusField(
            name="beam_attenuation_factors",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    goniometer_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-goniometer-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Goniometer position X."),
        a_nexus_field=NeXusField(
            name="goniometer_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    goniometer_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-goniometer-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Goniometer position Y."),
        a_nexus_field=NeXusField(
            name="goniometer_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    goniometer_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-goniometer-z-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Goniometer position Z"),
        a_nexus_field=NeXusField(
            name="goniometer_z",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    count_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-count-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("Total time of count."),
        a_nexus_field=NeXusField(
            name="count_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrdPanExperimentConfigTwoTheta(Object):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-two-theta-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXobject",
            name="two_theta",
            name_type="specified",
            optionality="required",
        ),
    )

    start = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-two-theta-start-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Starting value of the diffraction angle."),
        a_nexus_field=NeXusField(
            name="start",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    end = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-two-theta-end-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Ending value of the diffraction angle."),
        a_nexus_field=NeXusField(
            name="end",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    step = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-two-theta-step-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Minimum step size in-between two diffraction angles."),
        a_nexus_field=NeXusField(
            name="step",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrdPanExperimentConfigOmega(Object):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-omega-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXobject",
            name="omega",
            name_type="specified",
            optionality="required",
        ),
    )

    start = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-omega-start-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Starting value of the incident angle."),
        a_nexus_field=NeXusField(
            name="start",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    end = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-omega-end-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Ending value of the incident angle."),
        a_nexus_field=NeXusField(
            name="end",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )
    step = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-config-omega-step-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Minimum step size in the between two incident angles."),
        a_nexus_field=NeXusField(
            name="step",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "radian"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrdPanExperimentResult(XrdData):
    """
    All experiment results data such as scattering angle (2theta), intensity,
    incident angle, scattering vector, etc will be stored here.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="experiment_result",
            name_type="specified",
            optionality="required",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-intensity-field"
        ],
        shape=["*"],
        description=("Number of scattered electrons per unit time."),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    two_theta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-two-theta-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("Two-theta (scattering angle) of the diffractogram."),
        a_nexus_field=NeXusField(
            name="two_theta",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    omega = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-omega-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("Incident angle of the diffractogram."),
        a_nexus_field=NeXusField(
            name="omega",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-phi-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("The phi range of the diffractogram."),
        a_nexus_field=NeXusField(
            name="phi",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    chi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-chi-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=("The chi range of the diffractogram"),
        a_nexus_field=NeXusField(
            name="chi",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    q_parallel = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-q-parallel-field"
        ],
        flexible_unit=True,
        description=(
            "The scattering vector component, which is parallel to the sample surface."
        ),
        a_nexus_field=NeXusField(
            name="q_parallel",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    q_perpendicular = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-q-perpendicular-field"
        ],
        flexible_unit=True,
        description=(
            "The scattering vector component, which is perpendicular to the "
            "sample surface."
        ),
        a_nexus_field=NeXusField(
            name="q_perpendicular",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    q_norm = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-experiment-result-q-norm-field"
        ],
        flexible_unit=True,
        description=(
            "The norm value of the scattering vector, q. The scattering vector "
            "is defined as a difference between the incident and scattered wave "
            "vectors. For details: "
            "https://en.wikipedia.org/wiki/Powder_diffraction and "
            "https://theory.labster.com/scattering-vector/"
        ),
        a_nexus_field=NeXusField(
            name="q_norm",
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


class XrdPanQData(XrdData):
    """
    The desired view for scattering vectors.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-q-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="q_data",
            name_type="specified",
            optionality="optional",
        ),
    )

    q = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-q-data-q-field"
        ],
        description=(
            "This concept corresponds to the norm value of the scattering "
            "vector(q). The concept is the same as 'q_norm' of "
            "'experiment_result' and should be linked to "
            "/entry[ENTRY]/experiment_result/q_norm."
        ),
        a_nexus_field=NeXusField(
            name="q",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-q-data-intensity-field"
        ],
        description=(
            "Number of scattered electrons per unit time at each scattering "
            "vector (q) value. The concept is the same as the 'intensity' of "
            "experiment_result and should be linked to "
            "/entry[ENTRY]/experiment_result/intensity."
        ),
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    q_parallel = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-q-data-q-parallel-field"
        ],
        description=(
            "The scattering vector (q) component, which is parallel to the "
            "sample surface. This component is used in the Reciprocal Space "
            "Mapping (RSM) technique of X-ray diffraction method. The concept is "
            "the same as 'q_parallel' of experiment_result, and should be linked "
            "to /entry[ENTRY]/experiment_result/q_parallel."
        ),
        a_nexus_field=NeXusField(
            name="q_parallel",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    q_perpendicular = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-q-data-q-perpendicular-field"
        ],
        description=(
            "The scattering vector component, which is perpendicular to the "
            "sample surface. The concept is the same as 'q_perpendicular' of "
            "experiment_result, and should be linked to "
            "/entry[ENTRY]/experiment_result/q_perpendicular."
        ),
        a_nexus_field=NeXusField(
            name="q_perpendicular",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XrdPanSample(Sample):
    """
    Description on sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    sample_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-sample-sample-mode-field"
        ],
        description=("Mode of sample."),
        a_nexus_field=NeXusField(
            name="sample_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    sample_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-sample-sample-id-field"
        ],
        description=("Id of sample."),
        a_nexus_field=NeXusField(
            name="sample_id",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    sample_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxrd_pan.html#nxxrd_pan-entry-sample-sample-name-field"
        ],
        description=(
            "Usually in xrd sample are being analyzed, but sample might be "
            "identified by assumed name or given name."
        ),
        a_nexus_field=NeXusField(
            name="sample_name",
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
