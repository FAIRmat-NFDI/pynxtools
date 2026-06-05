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
# Run `pynx nomad generate-metainfo --nx-class NXstress` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.reflections import Reflections
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Stress"]


class Stress(Entry):
    """
    Application definition for stress and strain analysis of crystalline
    material defined by the `EASI-STRESS consortium <https://easi-stress.eu>`_.

    When a crystal is loaded (applied or residual stress) its crystallographic
    parameters change.

    Stress and strain analysis calculates deformation (strain) and the
    associated force (stress) from diffraction data.

    This application definition essentially standardizes the result of
    diffraction pattern analysis from different types of diffraction
    experiments for the purpose of stress and strain analysis. The analysis is
    typically some form of diffraction peak indexing and fitting. The
    experiments are for example

    - energy-dispersive X-ray powder diffraction - angular-dispersive X-ray
    powder diffraction - angular-dispersive neutron powder diffraction -
    time-of-flight (TOF) neutron powder diffraction.

    In addition, the application definition guarantees that the information
    about instrumental setups, measurement conditions, and data analysis
    workflows are described. This ensures not only the reproducability and
    tracability of the measured data, but also the metadata. Since not all
    participating beamlines or instruments can provide an input to all the
    NeXus fields listed in this application definition, not all of them are
    "required".

    However, when possible and technically feasible, the instrument using the
    NXstress application definition is expected to provide the type of
    information outlined below.

    Sample and detector positions can be defined with :ref:`NXtransformations`.
    If you don't specify the direction of gravity and the direction of the beam
    then the standard NeXus Coordinate System is used.

    It is highly recommended that when certain parameters or values are the
    same for all the measurements (acquistions) in the same file, they are
    stored only in one location and then linked in the other instances. For
    example, if during an acquisition all

    instrumental parameters but one stay the same and only the sample table
    moves in one direction (e.g. Xtranslation), then all the static
    instrumental parameters should be saved just once (e.g. in just one NXentry
    or in a *Shared_Information group*) and their values linked to every
    *instrument group* under all the other acquisitions. The value for the
    variable that changes, Xtranslation in this example, is suggested to be
    saved only at every instrument group under each acquistion but not in the
    *Shared_Information group*.

    It is not always necessary to link each field. In case all the fields with
    an entire group are the same, the entire group can be linked.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXstress",
            category="application",
            symbols={
                "n_X": "Number of diffractogram channels.",
                "n_D": "Number of diffractograms. For example the number of energy-dispersive detectors or the number of azimuthal sections in an area detector.",
                "n_Peaks": "Number of reflections.",
                "x_Unit": "Diffractogram X units.",
                "y_Unit": "Diffractogram Y units.",
                "c_Unit": "Converted diffractogram X units (could be the same as *x_Unit*).",
                "n_Temp": "number of temperatures",
                "n_sField": "number of values in applied stress field",
                "nP": "number of scan points (only present in scanning measurements)",
                "i": "number of detector pixels in the first (slowest) direction",
                "j": "number of detector pixels in the second (faster) direction",
            },
        ),
    )

    experiment_responsible = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=False,
        description=("Information about the person who performed the experiment."),
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="experiment_responsible",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressInstrument",
        repeats=False,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressSample",
        repeats=True,
        variable=True,
        description=(
            "This is the recommended location for describing parameters "
            "associated with the sample."
        ),
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressProcess",
        repeats=True,
        variable=True,
        description=(
            "Zero or more groups to describe the data processing steps to obtain "
            "the content of this application definition."
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        description=(
            "User description of the data acquisitions. A description of data "
            "analysis goes in the :ref:`fit descriptions "
            "</NXstress/ENTRY/FIT/DESCRIPTION-group>`."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    peaks = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.stress.StressPeaks",
        repeats=False,
        description=(
            "This group contains all diffraction peak parameters that could be "
            "needed for stress and strain calculations. These parameters are "
            "derived from :ref:`peak_parameters "
            "</NXstress/ENTRY/fit/peak_parameters-group>` and additional "
            "metadata."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXstress"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXstress"],
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-title-field"
        ],
        description=("Extended title for the entry."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-experiment-identifier-field"
        ],
        description=(
            "Unique identifier for the experiment as defined by the facility "
            "(e.g. DOI, proposal id, ...). At ILL, this could be, for example, "
            "``exp_1-02-286``, ``exp_INDU-229``, or ``exp_INTER-569``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-experiment-description-field"
        ],
        description=(
            "Brief summary of the experiment, including key objectives. At least "
            "one of the following information should be provided: * "
            "``energy-dispersive X-ray powder diffraction`` * "
            "``angular-dispersive X-ray powder diffraction`` * "
            "``angular-dispersive neutron powder diffraction`` * "
            "``time-of-flight (TOF) neutron powder diffraction``"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-start-time-field"
        ],
        description=(
            "The starting time(s) of measurement(s) which can be provided in "
            "form of a list if multiple measurements are included in the same "
            "NXentry."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-end-time-field"
        ],
        description=(
            "The end time(s) of measurement(s) which can be provided in form of "
            "a list if multiple measurements are included in the same NXentry."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    collection_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-collection-identifier-field"
        ],
        description=(
            "User or Data Acquisition defined identifier from which the content "
            "of this application definition is derived. This can be freely "
            "chosen by the user or the instrument scientist and could be, for "
            "example, ``05_DA_650_AX_B3P5``, ``SENB-14``, ``Quartz``,...."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="collection_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    collection_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-collection-description-field"
        ],
        description=(
            "Brief summary of the collection, including grouping criteria. The "
            "information provided in this field can highlight, for example, the "
            "measurement setup or information about experimental conditions."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="collection_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    processing_type = Quantity(
        type=MEnum(["two-theta", "energy", "d-spacing", "time-of-flight", "sin2psi"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-processing-type-field"
        ],
        description=(
            "Describes the way strain :math:`\\varepsilon` can be calculated "
            "from the :ref:`center </NXstress/ENTRY/peaks/center-field>` peak "
            "parameter."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="processing_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "two-theta",
                "energy",
                "d-spacing",
                "time-of-flight",
                "sin2psi",
            ],
        ),
    )
    measurement_direction = Quantity(
        type=MEnum(["radial", "longitudinal", "normal", "tangential", "multiple"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-measurement-direction-field"
        ],
        description=(
            "Describes the specific measurement direction covered by the data in "
            "this file."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="measurement_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["radial", "longitudinal", "normal", "tangential", "multiple"],
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


class StressInstrument(Instrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-name-field"
        ],
        description=(
            "Name of the diffractometer, instrument, or beamline used for the "
            "experiment. This could be, for example, *Strain Analyser for Large "
            "and Small scale engineering Applications*."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity__short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-instrument-name-short-name-attribute"
        ],
        description=(
            "Short name for the instrument, perhaps the acronym, which would be "
            "for the the example above ``SALSA``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressSample(Sample):
    """
    This is the recommended location for describing parameters associated with
    the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-name-field"
        ],
        description=("Descriptive name of sample"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    stress_field__direction = Quantity(
        type=MEnum(["x", "y", "z"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-stress-field-direction-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["x", "y", "z"],
            parent_field="stress_field",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-sample-description-depends-on-field"
        ],
        description=(
            "The axis on which the sample position depends may be stored "
            "anywhere, but is normally stored in the NXtransformations group "
            "within the NXsample group."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressProcess(Process):
    """
    Zero or more groups to describe the data processing steps to obtain the
    content of this application definition.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    raw_data_file = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-raw-data-file-field"
        ],
        description=(
            "The raw data file name(s) used during the data reduction process. "
            "This can be a list."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="raw_data_file",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-date-field"
        ],
        description=(
            "Date when the raw data was reduced and the data in the *NXstress* "
            "file format generated."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    program_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-program-field"
        ],
        description=(
            "Software package used to perform data reduction including the "
            "version number or release date."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    integration_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-integration-type-field"
        ],
        description=("Describes how the data was integrated."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="integration_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    bins = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-bins-field"
        ],
        description=("Describes the type of binning used during data reduction."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="bins",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    fit_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-fit-type-field"
        ],
        description=(
            "Describes how the fitting of the peaks was done. For example, "
            "single peak fit, multiple peak fit, Pawley refinement, Rietveld "
            "refinement, …"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="fit_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    fit_range = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-fit-range-field"
        ],
        description=("Describes the data range used for peak fitting."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="fit_range",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    goodness_of_fit = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-goodness-of-fit-field"
        ],
        description=(
            "Type and value describing the goodness of fit. For example, Rw 0.23."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="goodness_of_fit",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    normalization = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-fit-normalization-field"
        ],
        description=(
            "Describes whether the data was normalized and if so , how. Examples "
            "of valid entries are: ``None``, ``time``, ``primary monitor``, "
            "``detector``, …"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="normalization",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class StressPeaks(Reflections):
    """
    This group contains all diffraction peak parameters that could be needed
    for stress and strain calculations. These parameters are derived from
    :ref:`peak_parameters </NXstress/ENTRY/fit/peak_parameters-group>` and
    additional metadata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXreflections",
            name="peaks",
            name_type="specified",
            optionality="required",
            min_occurs=1,
            max_occurs=1,
        ),
    )

    h = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-h-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("First Miller index."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="h",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    k = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-k-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Second Miller index."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="k",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    l = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-l-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Third Miller index."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="l",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    lattice = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-lattice-field"
        ],
        shape=["*"],
        description=("Crystal lattice systems (*cubic*, *hexagonal*, ...)"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="lattice",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    space_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-space-group-field"
        ],
        shape=["*"],
        description=(
            "Crystallographic space group :math:`(Fm\\bar{3}m, Im\\bar{3}m, ...)`"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="space_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    phase_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-phase-name-field"
        ],
        shape=["*"],
        description=(
            "Name of the crystallographic phase (hematite, goethite, \\ "
            ":math:`\\alpha`-Al\\ :sub:`2`\\ O\\ :sub:`3`\\ , ...)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="phase_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    qx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-qx-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "First component of the *normalized* scattering vector *Q* in the "
            "sample reference frame. The sample reference frame is defined by "
            "the :ref:`sample transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="qx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    qy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-qy-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Second component of the *normalized* scattering vector *Q* in the "
            "sample reference frame. The sample reference frame is defined by "
            "the :ref:`sample transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="qy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    qz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-qz-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Third component of the *normalized* scattering vector *Q* in the "
            "sample reference frame. The sample reference frame is defined by "
            "the :ref:`sample transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="qz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    center = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-field"
        ],
        shape=["*"],
        description=("Diffraction peak position in *c_Unit* units."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="center",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    center__units = Quantity(
        type=MEnum(["degrees", "keV", "1/angstrom", "angstrom", "microseconds", "''"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-units-attribute"
        ],
        description=(
            "Specify the *c_Unit* units (see :ref:`center_type "
            "</NXstress/ENTRY/peaks/center_type-field>`)"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "degrees",
                "keV",
                "1/angstrom",
                "angstrom",
                "microseconds",
                "''",
            ],
            parent_field="center",
        ),
    )
    center_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-errors-field"
        ],
        shape=["*"],
        description=(
            "Uncentrainties on :ref:`center "
            "</NXstress/ENTRY/peaks/center-field>` in *c_Unit* units."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="center_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    center_errors__units = Quantity(
        type=MEnum(["degrees", "keV", "1/angstrom", "angstrom", "microseconds", "''"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-errors-units-attribute"
        ],
        description=(
            "Specify the *c_Unit* units (see :ref:`center_type "
            "</NXstress/ENTRY/peaks/center_type-field>`)"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "degrees",
                "keV",
                "1/angstrom",
                "angstrom",
                "microseconds",
                "''",
            ],
            parent_field="center_errors",
        ),
    )
    center_type = Quantity(
        type=MEnum(
            [
                "two-theta",
                "energy",
                "momentum-transfer",
                "d-spacing",
                "channel",
                "time-of-flight",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-center-type-field"
        ],
        description=(
            "The space in which :ref:`center "
            "</NXstress/ENTRY/peaks/center-field>` is defined. It defines the "
            '*c_Unit* as follows - if *center_type="two-theta"* then *c_Unit* '
            'must have the angle unit *degrees* - if *center_type="energy"* '
            "then *c_Unit* must have the unit *keV* - if "
            '*center_type="momentum-transfer"* then *c_Unit* must have the '
            'unit \\ :math:`Å^{-1}` - if *center_type="d-spacing"* then '
            "*c_Unit* must have the unit \\ :math:`Å` - if "
            '*center_type="channel"* then *c_Unit* must be *dimensioness* - if '
            '*center_type="time-of-flight"* then *c_Unit* must have the unit '
            "\\ :math:`\\mu\\mathrm{s}`"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="center_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "two-theta",
                "energy",
                "momentum-transfer",
                "d-spacing",
                "channel",
                "time-of-flight",
            ],
        ),
    )
    sx = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-sx-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "First component of the sample position in the sample reference "
            "frame. The sample reference frame is defined by the :ref:`sample "
            "transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sx",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    sy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-sy-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "First component of the sample position in the sample reference "
            "frame. The sample reference frame is defined by the :ref:`sample "
            "transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    sz = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXstress.html#nxstress-entry-peaks-sz-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        description=(
            "First component of the sample position in the sample reference "
            "frame. The sample reference frame is defined by the :ref:`sample "
            "transformations "
            "</NXstress/ENTRY/sample_description/TRANSFORMATIONS-group>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="sz",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
