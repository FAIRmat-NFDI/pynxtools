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
# Run `pynx nomad generate-metainfo --nxdl NXellipsometry` to regenerate.
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
from pynxtools.nomad.metainfo.applications.optical_spectroscopy import (
    OpticalSpectroscopy,
)
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Ellipsometry"]


class Ellipsometry(OpticalSpectroscopy):
    """
    This is the application definition describing ellipsometry experiments.

    Such experiments may be as simple as identifying how a reflected beam of
    light with a single wavelength changes its polarization state, to a
    variable angle spectroscopic ellipsometry experiment.

    The application definition specializes :ref:`NXoptical_spectroscopy` by
    extending the terms and setting specific requirements.

    Information on ellipsometry is provided, e.g. in:

    * H. Fujiwara, Spectroscopic ellipsometry: principles and applications,
    John Wiley & Sons, 2007. * R. M. A. Azzam and N. M. Bashara, Ellipsometry
    and Polarized Light, North-Holland Publishing Company, 1977. * H. G.
    Tompkins and E. A. Irene, Handbook of Ellipsometry, William Andrew, 2005.

    Open access sources:

    * https://www.angstromadvanced.com/resource.asp *
    https://pypolar.readthedocs.io/en/latest/

    Review articles:

    * T. E. Jenkins, "Multiple-angle-of-incidence ellipsometry", J. Phys. D:
    Appl. Phys. 32, R45 (1999), https://doi.org/10.1088/0022-3727/32/9/201 * D.
    E. Aspnes, "Spectroscopic ellipsometry - Past, present, and future", Thin
    Solid Films 571, 334-344 (2014), https://doi.org/10.1016/j.tsf.2014.03.056
    * R. M. A. Azzam, "Mueller-matrix ellipsometry: a review", Proc. SPIE 3121,
    Polarization: Measurement, Analysis, and Remote Sensing, (3 October 1997),
    https://doi.org/10.1117/12.283870 * E. A. Irene, "Applications of
    spectroscopic ellipsometry to microelectronics", Thin Solid Films 233,
    96-111 (1993), https://doi.org/10.1016/0040-6090(93)90069-2 * S. Zollner et
    al., "Spectroscopic ellipsometry from 10 to 700 K", Adv. Opt. Techn.,
    (2022), https://doi.org/10.1515/aot-2022-0016
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXellipsometry",
            category="application",
            symbols={
                "N_spectrum": "Length of the spectrum array (e.g. wavelength or energy) of the measured\n                data.",
                "N_measurements": "Number of measurements (1st dimension of measured_data array). This is\n                equal to the number of parameters scanned. For example, if the experiment\n                was performed at three different temperatures and two different pressures\n                N_measurements = 2*3 = 6.",
                "N_detection_angles": "Number of detection angles of the beam reflected or scattered off the\n                sample.",
                "N_incident_angles": "Number of angles of incidence of the incident beam.",
            },
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.ellipsometry.EllipsometryInstrument",
        repeats=True,
        variable=True,
        description=("Properties of the ellipsometry equipment."),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.ellipsometry.EllipsometrySample",
        repeats=True,
        variable=True,
    )
    data_collection = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.ellipsometry.EllipsometryDataCollection",
        repeats=False,
        description=(
            "Measured data, data errors, and varied parameters. This may be used "
            "to describe indirectly derived data or data transformed between "
            "different descriptions, such as: Raw Data --> Psi Delta Psi, Delta "
            "--> N,C,S Mueller matrix --> N,C,S Mueller matrix --> Psi, Delta "
            "etc. Other types of data, such as temperature or sample location, "
            "may be saved in a generic (NXdata) concept from "
            ":ref:`NXoptical_spectroscopy`, or better directly in the location "
            "of the sample positioner or temperature sensor."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXellipsometry"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-definition-field"
        ],
        description=("An application definition for ellipsometry."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXellipsometry"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-definition-version-attribute"
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
    )
    definition__URL = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-definition-url-attribute"
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
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    experiment_type = Quantity(
        type=MEnum(["ellipsometry"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-experiment-type-field"
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
            enumeration=["ellipsometry"],
        ),
    )
    ellipsometry_experiment_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-ellipsometry-experiment-type-field"
        ],
        description=("Specify the type of ellipsometry."),
        a_nexus_field=NeXusField(
            name="ellipsometry_experiment_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "in situ spectroscopic ellipsometry",
                "THz spectroscopic ellipsometry",
                "infrared spectroscopic ellipsometry",
                "ultraviolet spectroscopic ellipsometry",
                "uv-vis spectroscopic ellipsometry",
                "NIR-Vis-UV spectroscopic ellipsometry",
            ],
            open_enum=True,
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


class EllipsometryInstrument(Instrument):
    """
    Properties of the ellipsometry equipment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    ellipsometer_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-instrument-ellipsometer-type-field"
        ],
        description=("What type of ellipsometry was used? See Fujiwara Table 4.2."),
        a_nexus_field=NeXusField(
            name="ellipsometer_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "rotating analyzer",
                "rotating analyzer with analyzer compensator",
                "rotating analyzer with polarizer compensator",
                "rotating polarizer",
                "rotating compensator on polarizer side",
                "rotating compensator on analyzer side",
                "modulator on polarizer side",
                "modulator on analyzer side",
                "dual compensator",
                "phase modulation",
                "imaging ellipsometry",
                "null ellipsometry",
            ],
            open_enum=True,
        ),
    )
    angle_reference_frame = Quantity(
        type=MEnum(["beam centered", "sample-normal centered"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-reference-frame-field"
        ],
        description=(
            "Defines the reference frame which is used to describe the sample "
            "orientation with respect to the beam directions. A beam centered "
            "description is the default and uses 4 angles(similar to XRD): - "
            "Omega (angle between sample surface and incident beam) - 2Theta "
            "(angle between the transmitted beam and the detection beam) - Chi "
            "(sample tilt angle, angle between plane#1 and the surface normal, "
            "plane#1 = spanned by incidence beam and detection and detection. If "
            "Chi=0°, then plane#1 is the plane of incidence in reflection "
            "setups) - Phi (inplane rotation of sample, rotation axis is the "
            "samples surface normal) A sample normal centered description is "
            "possible as well: - angle of incidence (angle between incident beam "
            "and sample surface) - angle of detection (angle between detection "
            "beam and sample surface) - angle of incident and detection beam - "
            "angle of in-plane sample rotation (direction along the sample's "
            "surface normal)"
        ),
        a_nexus_field=NeXusField(
            name="angle_reference_frame",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["beam centered", "sample-normal centered"],
        ),
    )
    omega = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-omega-field"
        ],
        dimensionality="[angle]",
        description=("Angle between sample incident beam and sample surface."),
        a_nexus_field=NeXusField(
            name="omega",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    twotheta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-twotheta-field"
        ],
        dimensionality="[angle]",
        description=("Angle between incident and detection beam"),
        a_nexus_field=NeXusField(
            name="twotheta",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    chi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-chi-field"
        ],
        dimensionality="[angle]",
        description=(
            "Sample tilt between sample normal, and the plane spanned by "
            "detection and incident beam."
        ),
        a_nexus_field=NeXusField(
            name="chi",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-phi-field"
        ],
        dimensionality="[angle]",
        description=(
            "Inplane rotation of the sample, with rotation axis along sample normal."
        ),
        a_nexus_field=NeXusField(
            name="phi",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_incidence = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-incidence-field"
        ],
        dimensionality="[angle]",
        description=(
            "Angle(s) of the incident beam vs. the normal of the bottom "
            "reflective (substrate) surface in the sample. These two directions "
            "span the plane of incidence."
        ),
        a_nexus_field=NeXusField(
            name="angle_of_incidence",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_detection = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-detection-field"
        ],
        dimensionality="[angle]",
        description=(
            "Detection angle(s) of the beam reflected or scattered off the "
            "sample vs. the normal of the bottom reflective (substrate) surface "
            "in the sample if not equal to the angle(s) of incidence. These two "
            "directions span the plane of detection."
        ),
        a_nexus_field=NeXusField(
            name="angle_of_detection",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_incident_and_detection_beam = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-incident-and-detection-beam-field"
        ],
        dimensionality="[angle]",
        description=(
            "Angle between the incident and detection beam. If "
            "angle_of_detection + angle_of_incidence = "
            "angle_of_incident_and_detection_beam, then the setup is a "
            "reflection setup. If angle_of_detection + angle_of_incidence != "
            "angle_of_incident_and_detection_beam then the setup may be a light "
            "scattering setup. (i.e. 90° + 90° != 90°, i.e. incident and "
            "detection beam in the sample surface, but the angle "
            "source-sample-detector is 90°)"
        ),
        a_nexus_field=NeXusField(
            name="angle_of_incident_and_detection_beam",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    angle_of_in_plane_sample_rotation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-angle-of-in-plane-sample-rotation-field"
        ],
        dimensionality="[angle]",
        description=(
            "Angle of the inplane orientation of the sample. This might be an "
            "arbitrary, angle without specific relation to the sample symmetry, "
            "of the angle to a specific sample property (i.e. crystallographic "
            "axis or sample shape such as wafer flat)"
        ),
        a_nexus_field=NeXusField(
            name="angle_of_in_plane_sample_rotation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    lateral_focal_point_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-instrument-lateral-focal-point-offset-field"
        ],
        dimensionality="[length]",
        description=(
            "Specify if there is a lateral offset on the sample surface, between "
            "the focal points of the incident beam and the detection beam."
        ),
        a_nexus_field=NeXusField(
            name="lateral_focal_point_offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EllipsometrySample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    backside_roughness = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-sample-backside-roughness-field"
        ],
        description=(
            "Was the backside of the sample roughened? Relevant for infrared "
            "ellipsometry."
        ),
        a_nexus_field=NeXusField(
            name="backside_roughness",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    sample_id = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-sample-id-field"
        ],
        description=(
            "Locally unique ID of the sample, used in the research institute or group."
        ),
        a_nexus_field=NeXusField(
            name="sample_id",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    physical_form = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-physical-form-field"
        ],
        description=(
            "State the form of the sample, examples are: thin film, single "
            "crystal, poly crystal, amorphous, single layer, multi layer, "
            "liquid, gas, pellet, powder. Generic properties of liquids or gases "
            "see NXsample properties."
        ),
        a_nexus_field=NeXusField(
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    chemical_formula = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-chemical-formula-field"
        ],
        description=(
            "Chemical formula of the sample. Use the Hill system (explained "
            "here: https://en.wikipedia.org/wiki/Chemical_formula#Hill_system) "
            "to write the chemical formula. In case the sample consists of "
            "several layers, this should be a list of the chemical formulas of "
            "the individual layers, where the first entry is the chemical "
            "formula of the top layer (the one on the front surface, on which "
            "the light incident). The order must be consistent with "
            "layer_structure"
        ),
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the sample. If the sample substance has multiple "
            "components, all elements from each component must be included in "
            "'atom_types'."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    preparation_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-preparation-date-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "when the specimen was prepared. Ideally, report the end of the "
            "preparation, i.e. the last known timestamp when the measured "
            "specimen surface was actively prepared."
        ),
        a_nexus_field=NeXusField(
            name="preparation_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-thickness-field"
        ],
        dimensionality="[length]",
        description=(
            "(Measured) sample thickness. The information is recorded to qualify "
            "if the light used was likely able to shine through the sample. In "
            "this case the value should be set to the actual thickness of the "
            "specimen viewed for an illumination situation where the nominal "
            "surface normal of the specimen is parallel to the optical axis."
        ),
        a_nexus_field=NeXusField(
            name="thickness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    thickness_determination = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-thickness-determination-field"
        ],
        description=(
            "If a thickness if given, please specify how this thickness was "
            "estimated or determined."
        ),
        a_nexus_field=NeXusField(
            name="thickness_determination",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    layer_structure = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-layer-structure-field"
        ],
        description=(
            "Qualitative description of the layer structure for the sample, "
            "starting with the top layer (i.e. the one on the front surface, on "
            "which the light incident), e.g. native oxide/bulk substrate, or "
            "Si/native oxide/thermal oxide/polymer/peptide."
        ),
        a_nexus_field=NeXusField(
            name="layer_structure",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    sample_orientation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-sample-orientation-field"
        ],
        description=(
            "Specify the sample orientation, how is its sample normal oriented "
            "relative in the laboratory reference frame, incident beam reference "
            "frame."
        ),
        a_nexus_field=NeXusField(
            name="sample_orientation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    substrate = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-sample-substrate-field"
        ],
        description=(
            "If the sample is grown or fixed on a substrate, specify this here "
            "by a free text description."
        ),
        a_nexus_field=NeXusField(
            name="substrate",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EllipsometryDataCollection(Data):
    """
    Measured data, data errors, and varied parameters. This may be used to
    describe indirectly derived data or data transformed between different
    descriptions, such as: Raw Data --> Psi Delta Psi, Delta --> N,C,S Mueller
    matrix --> N,C,S Mueller matrix --> Psi, Delta etc.

    Other types of data, such as temperature or sample location, may be saved
    in a generic (NXdata) concept from :ref:`NXoptical_spectroscopy`, or better
    directly in the location of the sample positioner or temperature sensor.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data_collection",
            name_type="specified",
            optionality="optional",
        ),
    )

    data_identifier = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-data-identifier-field"
        ],
        description=(
            "An identifier to correlate data to the experimental conditions, if "
            "several were used in this measurement; typically an index of 0-N."
        ),
        a_nexus_field=NeXusField(
            name="data_identifier",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )
    data_type = Quantity(
        type=MEnum(
            [
                "intensity",
                "reflectivity",
                "transmittance",
                "Psi/Delta",
                "tan(Psi)/cos(Delta)",
                "Mueller matrix",
                "Jones matrix",
                "N/C/S",
                "raw data",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-data-type-field"
        ],
        description=(
            "Select which type of data was recorded, for example intensity, "
            "reflectivity, transmittance, Psi and Delta etc. It is possible to "
            "have multiple selections. The enumeration list depends on the type "
            "of experiment and may differ for different application definitions."
        ),
        a_nexus_field=NeXusField(
            name="data_type",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "intensity",
                "reflectivity",
                "transmittance",
                "Psi/Delta",
                "tan(Psi)/cos(Delta)",
                "Mueller matrix",
                "Jones matrix",
                "N/C/S",
                "raw data",
            ],
        ),
    )
    NAME_spectrum = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-name-spectrum-field"
        ],
        variable=True,
        shape=["*"],
        description=(
            "Spectral values (e.g. wavelength or energy) used for the "
            "measurement. An array of 1 or more elements. Length defines "
            "N_spectrum. Replace 'NAME' by the physical quantity that is used, "
            "e.g. wavelength."
        ),
        a_nexus_field=NeXusField(
            name="NAME_spectrum",
            type="NX_FLOAT",
            name_type="partial",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    NAME_spectrum__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-name-spectrum-units-attribute"
        ],
        description=(
            "If applicable, change 'unit: NX_ANY' to the appropriate NXDL unit. "
            "If the unit of the measured data is not covered by NXDL units state "
            "here which unit was used."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="NAME_spectrum",
        ),
    )
    measured_data = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-measured-data-field"
        ],
        shape=["*", "*", "*"],
        description=(
            "Resulting data from the measurement, described by 'data_type'. The "
            "first dimension is defined by the number of measurements taken, "
            "(N_measurements). The instructions on how to order the values "
            "contained in the parameter vectors given in the doc string of "
            "INSTRUMENT/sample_stage/environment_conditions/PARAMETER/values, "
            "define the N_measurements parameter sets. For example, if the "
            "experiment was performed at three different temperatures (T1, T2, "
            "T3), two different pressures (p1, p2) and two different angles of "
            "incidence (a1, a2), the first measurement was taken at the "
            "parameters {a1,p1,T1}, the second measurement at {a1,p1,T2} etc."
        ),
        a_nexus_field=NeXusField(
            name="measured_data",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    measured_data__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-measured-data-units-attribute"
        ],
        description=(
            "If applicable, change 'unit: NX_ANY' to the appropriate NXDL unit. "
            "If the unit of the measured data is not covered by NXDL units state "
            "here which unit was used."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="measured_data",
        ),
    )
    measured_data_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-measured-data-errors-field"
        ],
        shape=["*", "*", "*"],
        description=(
            "Specified uncertainties (errors) of the data described by "
            "'data_type' and provided in 'measured_data'."
        ),
        a_nexus_field=NeXusField(
            name="measured_data_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    measured_data_errors__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-measured-data-errors-units-attribute"
        ],
        description=(
            "If applicable, change 'unit: NX_ANY' to the appropriate NXDL unit. "
            "If the unit of the measured data is not covered by NXDL units state "
            "here which unit was used."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="measured_data_errors",
        ),
    )
    varied_parameter_link = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-varied-parameter-link-field"
        ],
        shape=["*"],
        description=(
            "List of links to the values of the sensors. Add a link for each "
            "varied parameter (i.e. for each sensor)."
        ),
        a_nexus_field=NeXusField(
            name="varied_parameter_link",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    reference_data_link = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXellipsometry.html#nxellipsometry-entry-data-collection-reference-data-link-field"
        ],
        description=(
            ":ref:`External link <Design-Links>` to the data field in the NeXus "
            "file which describes the reference data if a reference measurement "
            "was performed. Ideally, the reference measurement was performed "
            "using the same conditions as the actual measurement and should be "
            "as close in time to the actual measurement as possible. Ideally, "
            "the link uses the relative path with respect to the actual NeXus "
            "file."
        ),
        a_nexus_field=NeXusField(
            name="reference_data_link",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-data-collection-axes-attribute"
        ],
        shape=["*"],
        description=(
            "Spectrum, i.e. x-axis of the data (e.g. wavelength, energy etc.)"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXoptical_spectroscopy.html#nxoptical_spectroscopy-entry-data-collection-signal-attribute"
        ],
        description=("Spectrum, i.e. y-axis of the data (e.g. counts, intensity)"),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
