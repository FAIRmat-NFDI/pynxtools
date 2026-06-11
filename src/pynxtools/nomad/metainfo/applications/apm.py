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
# Run `pynx nomad generate-metainfo --nxdl NXapm` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.apm_charge_state_analysis import (
    ApmChargeStateAnalysis,
)
from pynxtools.nomad.metainfo.base_classes.apm_event_data import ApmEventData
from pynxtools.nomad.metainfo.base_classes.apm_instrument import ApmInstrument
from pynxtools.nomad.metainfo.base_classes.apm_measurement import ApmMeasurement
from pynxtools.nomad.metainfo.base_classes.apm_ranging import ApmRanging
from pynxtools.nomad.metainfo.base_classes.apm_reconstruction import ApmReconstruction
from pynxtools.nomad.metainfo.base_classes.atom import Atom
from pynxtools.nomad.metainfo.base_classes.chemical_composition import (
    ChemicalComposition,
)
from pynxtools.nomad.metainfo.base_classes.cite import Cite
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.cs_filter_boolean_mask import (
    CsFilterBooleanMask,
)
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.electromagnetic_lens import (
    ElectromagneticLens,
)
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.image import Image
from pynxtools.nomad.metainfo.base_classes.manipulator import Manipulator
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.peak import Peak
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.project import Project
from pynxtools.nomad.metainfo.base_classes.pump import Pump
from pynxtools.nomad.metainfo.base_classes.roi_process import RoiProcess
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.sensor import Sensor
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Apm"]


class Apm(Entry):
    """
    Application definition for real or simulated atom probe and field-ion
    microscopy experiments.

    Atom probe tomography and field-ion microscopy are methods for
    characterizing materials through induced controlled extraction of
    individual atoms as ions and molecular ions from a sharp needle-shaped
    specimen.

    Offering isotopic and nanometer-scale resolution, atom probe data enable
    quantification of local chemical composition and computing of volumetric
    reconstructions which are models for the atomic architecture of the small
    specimen volume analyzed. These reconstructions provide input for
    characterization of atomic segregation at crystal defects. The term
    microstructural features is considered as a narrow synonym for crystal
    defects.

    The aim of the NXapm application definition is to provide a general yet
    specific enough solution to serialize artifacts for virtually all atom
    probe and field-ion microscopy experiments.

    Before summarizing the design of the base classes and the parts of the
    NXapm application definition, it is worthwhile to recall and distinguish
    concepts that are related to atom extraction events and the molecular ions
    that are frequently generated by the sequence of events:

    * An atom probe instrument uses laser or voltage pulsing events to trigger
    ion extraction events. * These ions are accelerated in an electric field
    towards a position-sensitive detector system. Physical events and
    corresponding signal on this detector is triggered by an ion hitting the
    detector. Some of these events are not necessarily caused by or directly
    correlated with an identifiable pulsing event. * Note that only a part the
    specimen volume can be measured and finite detection efficiency means that
    not all atoms in the measured volume will be detected. Neutral atoms can
    escape detection. Some ions escape detection because they hit into walls of
    the analysis_chamber.

    Raw data are typically processed as follows:

    * Detector pulses and their timing are processed and discriminated into
    signal events of different quality levels. High quality events might be
    considered in further processing to identify the corresponding molecular
    ion and its original position in the reconstructed volume. * Signal
    calibration and filtering steps are applied to convert raw time-of-flight
    data to calibrated mass-to-charge state ratio values and obtain calibrated
    impact positions on the detector. * Ranging and identifying an ion that
    corresponds to each detector event. Isotopic abundance and theoretical
    models inform these ranging algorithms. * Finally, such selected ion impact
    positions and iontypes are used to compute a reconstructed volume of the
    specimen using backprojection algorithms. In effect, an atom probe
    measurement is a combination of a data acquisition and a data analysis
    workflow.

    Not only in AMETEK/Cameca's APSuite/IVAS software, which the majority of
    atom probers use, these concepts are well distinguished. However, the
    algorithms used to transform correlations between pulses and physical
    events into actual events, the so-called detector hits of ions, is a
    proprietary one. This algorithm is also referred to as the hit finding
    algorithm.

    Due to this practical inaccessibility of details, virtually all atom probe
    studies currently use a reporting schema where the course of the specimen
    evaporation is documented such that quantities are a function of
    evaporation_id i.e. actual event/ion, i.e. after having the hit finding
    algorithm and correlations applied. That is the evaporation_id values take
    the role of an implicit time and course of the experiment given that ion
    extraction physically is a sequential process.

    This application definition includes fields that the atom probe community
    has decided to represent best practices for reporting atom probe
    measurements. Exemplar mapping tables are provided for documents that
    reported these best practices to translate technical term into concepts of
    the NXapm application definition.

    *The NeXus application definition NXapm defines a hierarchical data model
    with ten building blocks:*

    The data model represents a tree of concepts. The tree is constructed from
    groups of concepts representing the branches, together with fields and
    attributes representing leaves. NXapm is defined by composing and
    specializing base classes into the following ten categories:

    - The field ``definition`` specifies that the data schema is NXapm. In
    combination with administrative metadata such as the attribute
    ``NeXus_version`` provided by :ref:`NXroot` this specifies which version of
    NXapm the instance data in a NeXus/HDF5 file are compliant with. - The
    fields ``run_number``, ``experiment_alias``, ``experiment_description`` and
    the group ``userID`` provide concepts for storing organizational metadata
    that contextualize the work within the research workflow and humans
    involved in this. - The fields ``start_time``, ``end_time`` provide
    concepts for framing a temporal context for the research. - The groups
    ``citeID``, ``noteID`` provide concepts for adding contextual details such
    as citations or notes that are associated with the data, i.e. other
    artifacts that are deemed relevant when reporting about a measurement or
    simulation. These groups are useful when NXapm is used as a serialization
    format for technology-partner-agnostic archival of data and metadata that
    have been collected during a session with an atom probe instrument. The
    terms run and session are understood as exact synonyms that refer to an
    uninterrupted period of measurement. Resuming measurement on a specimen
    after an interruption is viewed as a new run and the new data should not be
    appended to the previous run, but written to either a new NXentry, or a new
    file. Removing the specimen from the instrument is an interruption.
    Changing evaporation conditions while the specimen is remains in the
    analysis_chamber and resuming thereafter the measurement is not considered
    as an interruption. It is a common strategy to probe the evaporation
    process for different instrument parameters. Each individual collection
    should then though be stored in an own NXapm_event_data group. Parking the
    specimen to the buffer_chamber and resuming the measurement at a later
    stage is an interruption. During a run, the microscope is used for a
    certain amount of time to characterize a single specimen. - The groups
    ``sample`` and ``specimen`` provide concepts for storing metadata about the
    sample and the specimen, i.e. the smaller part that was removed from the
    sample to be measured in the atom probe session. The term "tip" in the
    context of atom probe research is considered jargon. Specimen is an exact
    synonym for tip. - The field ``operation_mode`` and group ``measurement``
    provides concepts that are useful for describing a measurement during a
    session with an atom probe or field-ion microscope. This includes the chain
    of events of data and metadata that were collected during such a session. -
    The group ``simulation`` provides concepts that are useful for describing a
    simulation of an atom extraction, ionization, and ion trajectory
    simulation. Combined with ``measurement`` this provides a data schema for
    defining a digital twin of the instrument and its setup. - The groups
    ``consistent_rotations``, and ``NAMED_reference_frame`` provide concepts
    for reporting coordinate systems (frames of reference) and rotation
    conventions that clarify how data should be interpreted specifying the
    rotation of orientable objects in the microscope, its components, or of
    crystals and crystal defects in the material analyzed. - The group
    ``atom_probeID`` provides concepts for the computational workflows that
    were used to convert raw detector data into reconstructed ion positions and
    documentation of ranging definitions made. - The group ``profiling``
    provides concepts for reporting computational details such as programs and
    libraries used, for documenting the libraries of virtual environments such
    as those used by conda or python virtual environment, including details
    about the computing hardware used, and documenting capabilities for
    performance analyses and benchmarking of the software or its parts.

    *Design choices:*

    Given that most atom probe instruments across the globe were built by
    AMETEK/Cameca and are delivered with the AP Suite/IVAS software there is
    some homogeneity in how a measurement is performed and which data artifacts
    and algorithms used for data processing. Complementary use of open-source
    software specifically for the reconstruction, ranging, and later data
    processing stages contributes to a landscape of multiple tools in use.
    Therefore, communication of atom probe research differs between user
    groups. This holds even more so true for the sub community in atom probe
    which study physical mechanisms involved during ionization to the point
    that here that almost each research work defines different simulation tools
    with different types of data artifacts.

    NXapm defines constraints on the existence and cardinality of concepts and
    its concept branches but seeks to offer a compromise. The key design
    pattern followed is that most branches are made optional or at most
    recommended but their child concepts are conditionally required. Thereby,
    NXapm can cover a variety of simple but also complex use cases. An example
    of this parent-optional-but-children-stronger-restricted design is the
    combination of the optional group ``measurement`` with its required child
    ``measurement/instrument``: Users which report simulations are not forced
    to document the instrument but users which have characterized a specimen
    are motivated to report about the instrument. They are though not
    necessarily required to report all the details of the instruments'
    components because the design pattern is applied recursively.

    *NXapm distinguishes and stores instance data based on how long they remain
    unchanged:*

    ``measurement`` provides two groups ``measurement/instrument`` and
    ``measurement/eventID``. The first group is designed for storing metadata
    about the instrument that do not change over the course of the session.
    Examples are the name of the technology partner who built the microscope or
    whether a laser or voltage pulser and reflectron exists or not. The second
    group is designed for metadata and data that are collected during the
    session with the instrument. These, are stored as instances of
    ``measurement/eventID``, events that can be time-stamped individually. Each
    instance of a group ``measurement/eventID`` contains
    ``measurement/instrument`` whose purpose is to store those specific state
    and settings of the instrument that was present during the collection of
    the event. Thereby, changing conditions such as campaigns with different
    target detection rate can be stored.

    Noteworthy, such an approach of the atom probe detecting groups of events
    and storing these as groups has also been in use in the proprietary
    software via CamecaRoot, a set of customized data structures and file
    formats that use the CernRoot library. By virtue of design this reduces
    unnecessary repetition of metadata stored in the first group.

    ``atom_probeID`` offer classes for the each task relevant task in the data
    processing pipeline that converts raw detector event data to calibrated
    mass-to-charge-state-ratio values and hit_position on the detector. These
    include ``initial_specimen``, and ``final_specimen`` locations for storing
    images of the specimen prior/after the measurement as considered best
    practice by AMETEK/Cameca, ``raw_data`` for delay-line timing data,
    ``hit_finding`` for details of the hit finding algorithm,
    ``hit_spatial_filtering`` a process that filters hits of too low quality
    and those laying outside the about to be computed reconstruction volume.
    Furthermore, group ``voltage_and_bowl`` offers a place for documenting
    calibrations and processing nonlinearities. Group
    ``mass_to_charge_conversion`` is used to document the mass calibration and
    the conversion from time-of-flight to mass-to-charge-state-ratio values.

    Finally, the groups ``reconstruction`` and ``ranging`` were designed to
    match and document the classical approaches how from all the previous
    sources of input one can compute a reconstructed volume, and apply peak
    fitting routines on the mass-to-charge-state-ratio histogram to label ions,
    i.e. range them for their isotopic identity. Group
    ``atom_probeID/reconstruction/naive_discretization`` offers a standardized
    way to report simple three-dimensional histograms. Group
    ``atom_probeID/ranging/peak_identification/ionID`` and its complementing
    group
    ``atom_probeID/ranging/peak_identification/ionID/charge_state_analysis``
    solves the issue that the ranging definitions in classical file formats are
    not reported for always for their isotopic identity and charge state. The
    field ``atom_probeID/ranging/peak_identification/iontypes`` provides a
    place for storing a compact representation of the results of each ranging
    definition made at the level of each ion.

    *The compatibility of NXapm and NXem:**

    The design of NXapm mirrors that of :ref:`NXem`. This was an intentional
    choice to support the increasingly stronger connection between these two
    materials characterization methods, especially in light of recent advances
    in the direct coupling of atom probe and transmission electron microscopes
    and scanning transmission electron microscopes.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm",
            category="application",
            symbols={
                "n_ht": "Number of hit qualities, the so-called hit types, distinguished.",
                "n_dld": "Number of delay-line-detector (DLD) wires of the detector.",
                "n_bins": "Number of bins used in the mass-to-charge-state-ratio spectrum.",
                "p": "Number of pulses collected in between start_time and end_time resolved by an\n                instance of :ref:`NXapm_event_data`. If this is not defined, p is the number of\n                ions included in the reconstructed volume if the application definition is used\n                to store results of an already reconstructed dataset.",
                "p_out": "Number of pulses returned by the hit_finding algorithm.\n                Neither necessarily equal to p nor to n.",
                "n": "Number of ions spatially filtered from results of the hit_finding algorithm\n                from which an instance of a reconstructed volume has been generated.\n                These ions get new identifier assigned in the process, the so-called\n                evaporation_id. This identifier must not be confused with the pulse_id.\n                This value is typically smaller than both p and p_out.",
                "m_r": "Number of mass resolution values.",
            },
        ),
    )

    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmProfiling",
        repeats=False,
        description=(
            "The configuration of the software that was used to generate this "
            "NeXus file."
        ),
    )
    citeID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmCiteID",
        repeats=True,
        variable=True,
    )
    noteID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmNoteID",
        repeats=True,
        variable=True,
    )
    project = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmProject",
        repeats=False,
    )
    userID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmUserID",
        repeats=True,
        variable=True,
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmSample",
        repeats=False,
        description=(
            "Description of the sample from which the specimen was prepared or "
            "site-specifically cut out using e.g. a focused-ion beam instrument. "
            "In NXapm, a measurement is performed on a specimen. Since APM "
            "specimens are very small, they are typically cut from a larger "
            "object with some scientific significance, which NXapm refers to as "
            "a sample."
        ),
    )
    specimen = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmSpecimen",
        repeats=False,
        description=(
            "Description of the specimen that was cut off from the sample. In "
            "atom probe jargon this is typically referred to as the tip."
        ),
    )
    consistent_rotations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmConsistentRotations",
        repeats=False,
        description=(
            "The conventions used when reporting crystal orientations. We follow "
            "the best practices of the Material Science community that are "
            "defined in reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_."
        ),
    )
    NAMED_reference_frameID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmNAMED_reference_frameID",
        repeats=True,
        variable=True,
        description=(
            "A coordinate system. Multiple instances require unique names. "
            "Several Euclidean coordinate systems (CS) are used in the field of "
            "atom probe: * World space; a CS specifying a local coordinate "
            "system of the planet earth which identifies into which direction "
            "gravity is pointing such that the laboratory space CS can be "
            "rotated into this world CS. * The laboratory space; a CS specifying "
            "the room where the instrument is located in or a physical landmark "
            "on the instrument, e.g. the direction of the transfer rod where "
            "positive is the direction how the rod has to be pushed during "
            "loading a specimen into the instrument. In summary, this CS is "
            "defined by the chassis of the instrument. Suggested name of the "
            "group ``laboratory_reference_frame``. * The specimen space; a CS "
            "affixed to either the base or the initial apex of the specimen, "
            "whose z axis points towards the detector. Suggested name of the "
            "group ``specimen_reference_frame``. * The detector space; a CS "
            "affixed to the detector plane whose xy plane is usually in the "
            "detector and whose z axis points towards the specimen. This is a "
            "distorted space with respect to the reconstructed ion positions. "
            "Suggested name of the group ``detector_reference_frame``. * The "
            "reconstruction space; a CS in which the reconstructed ion positions "
            "are defined. The orientation depends on the analysis software used. "
            "* Eventually further coordinate systems attached to the flight path "
            "of individual ions might be defined. Suggested name of the group "
            "``reconstruction_reference_frame``. To achieve unique names, the "
            'prefix "NAMED" should be replaced to with something derived from '
            'an alias for the coordinate system, or the value of the "alias" '
            "field. Use the suffix _reference_frame when creating specific "
            "instances of NXcoordinate_system e.g. laboratory_reference_frame, "
            "reconstruction_reference_frame and so on and so forth. In atom "
            "probe microscopy a frequently used choice for the detector space "
            "(CS) is discussed with the so-called detector space image stack. "
            "This is a stack of two-dimensional histograms of detected ions "
            "within a predefined evaporation identifier interval. Typically, the "
            "set of ion evaporation sequence identifiers is grouped into chunks. "
            "For each chunk a histogram of the ion hit positions on the detector "
            "is computed. This leaves the possibility for inconsistency between "
            "the so-called detector space and the e.g. specimen space. To avoid "
            "these ambiguities, instances of :ref:`NXtransformations` should be "
            "used."
        ),
    )
    measurement = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmApmMeasurement",
        repeats=False,
    )
    simulation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_simulation.ApmSimulation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_simulation",
            name="simulation",
            name_type="specified",
            optionality="optional",
        ),
    )
    atom_probeID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeID",
        repeats=True,
        variable=True,
        description=(
            "A region-of-interest analyzed either during or after the session "
            "for which specific processed data of the measured or simulated data "
            "are available. If a single instance is required the group should be "
            "named atom_probe. If multiple groups are required these should be "
            "named atom_probe1, atom_probe2, and so on and so forth."
        ),
    )

    definition = Quantity(
        type=MEnum(["NXapm"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXapm"],
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
    )
    run_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-run-number-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The identifier whereby the experiment is referred to in the control "
            "software. It is common practice in atom probe research to refer to "
            "a measurement on a single specimen as a run. When working with "
            "AMETEK/Cameca instruments it is a common practice also to store all "
            "data associated with such a run in files whose name is composed "
            "from a prefix that details the type of instrument (e.g. R5076) "
            "followed by the run_number. These filenames are often used as the "
            "specimen_name or experiment_identifier. The terms run and session "
            "are understood as exact synonyms. For other instruments, such as "
            "the one from Stuttgart or Oxcart from Erlangen, or the instruments "
            "at GPM in Rouen, use the identifier which matches best conceptually "
            "to the LEAP run number. The field does not have to be required, if "
            "the information is recoverable in the dataset which for LEAP "
            "instruments is the case; provided these RHIT or HITS files "
            "respectively are stored alongside a data artifact. With NXapm the "
            "RHIT or HITS can be stored via NXnote in the hit_finding algorithm "
            "section. As a destructive microscopy technique, a run can be "
            "performed only once. It is possible, however, to interrupt a run "
            "and restart data acquisition while still using the same specimen. "
            "In this case, each evaporation run needs to be distinguished with "
            "different run numbers. We follow this habit of most atom probe "
            "groups. Such interrupted runs should be stored as individual "
            ":ref:`NXentry` instances in one NeXus file."
        ),
        a_nexus_field=NeXusField(
            name="run_number",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    experiment_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-experiment-alias-field"
        ],
        description=(
            "Alias or short name which scientists can use to refer to this experiment."
        ),
        a_nexus_field=NeXusField(
            name="experiment_alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-experiment-description-field"
        ],
        description=(
            "Free-text description about the experiment. Users are strongly "
            "advised to parameterize the description of their experiment by "
            "using respective groups and fields and base classes instead of "
            "writing prose into the field."
        ),
        a_nexus_field=NeXusField(
            name="experiment_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the atom probe session started. If the exact duration "
            "of the measurement is not relevant, start_time only should be used. "
            "The start_time is required in order to ensure that at least one "
            "point in time is provided for full temporal context to a "
            "measurement and simulation when writing instance data using NXapm. "
            "Otherwise, the instance data can not be sorted in order or even "
            "placed in a logical sequence to other steps of the research "
            "workflow, which would disallow using functionalities in research "
            "data management systems that rely on temporal context. Specifying "
            "start_time and end_time is useful for capturing more detailed "
            "bookkeeping of the experiment. The user should be aware that even "
            "with having both dates specified, it may not be possible to infer "
            "how long the experiment took or for how long data were collected. "
            "More detailed timing data over the course of the experiment have to "
            "be collected to compute this event chain during the experiment. For "
            "this purpose the :ref:`NXapm_event_data` instance should be used."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-end-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC included when "
            "the atom probe session ended. Writing the end_time can be a tricky "
            "in practice. If written at the start of the experiment, it can only "
            "be an estimate. If written at the end, there is the risk for having "
            "the computer crash or lose power. The absence of end_time should "
            "not be interpreted as that the experiment was aborted. Only, the "
            "field ``status`` should be used for communicating such abortion."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-elapsed-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "How long did the measurement take e.g. use "
            "CRunHeader.CAnalysis.fElapsedTime"
        ),
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_TIME",
        ),
    )
    operation_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-operation-mode-field"
        ],
        description=(
            "What type of atom probe experiment is performed to inform research "
            "data management systems and allow filtering: * apt are experiments "
            "where the analysis_chamber has no imaging gas. Experiments with "
            "LEAP instruments are typically with this operation_mode. * fim are "
            "experiments where the analysis_chamber has an imaging gas, which "
            "should be specified with the atmosphere in the analysis_chamber "
            "group. * apt_fim should be used for combinations of the two imaging "
            "modes. Few experiments of this type have been performed, as it can "
            "be detrimental to LEAP systems (see `S. Katnagallu et al. "
            "<https://doi.org/10.1017/S1431927621012381>`_)."
        ),
        a_nexus_field=NeXusField(
            name="operation_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["apt", "fim", "apt_fim"],
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


class ApmProfiling(CsProfiling):
    """
    The configuration of the software that was used to generate this NeXus
    file.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="optional",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmProfilingProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmProfilingEnvironment",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmProfilingProgramID(Program):
    """
    A collection of all programs and libraries which are considered relevant to
    understand with which software tools this NeXus file instance was
    generated. Ideally, to enable a binary recreation from the input data.

    Examples include the name and version of the libraries used to write the
    instance. Ideally, the software which writes these NXprogram instances also
    includes the version of the set of NeXus classes i.e. the specific set of
    base classes, application definitions, and contributed definitions with
    which the here described concepts can be resolved.

    For the `pynxtools library <https://github.com/FAIRmat-NFDI/pynxtools>`_
    which is used by the `NOMAD <https://nomad-lab.eu/nomad-lab>`_ research
    data management system, it makes sense to store e.g. the GitHub repository
    commit and respective submodule references used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmProfilingEnvironment(Collection):
    """
    Programs and libraries representing the computational environment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )

    program = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmProfilingEnvironmentProgram",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmProfilingEnvironmentProgram(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-environment-program-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-environment-program-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-profiling-environment-program-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmCiteID(Cite):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-citeid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcite",
            name="citeID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    author = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-citeid-author-field"
        ],
        description=("The author(s) of that reference."),
        a_nexus_field=NeXusField(
            name="author",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    doi = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-citeid-doi-field"
        ],
        a_nexus_field=NeXusField(
            name="doi",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmNoteID(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-noteid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="noteID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-noteid-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-noteid-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-noteid-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-noteid-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmProject(Project):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-project-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXproject",
            name="project",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-project-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmUserID(User):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-userid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="userID",
            name_type="partial",
            optionality="recommended",
        ),
    )

    identifierNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-userid-identifiername-field"
        ],
        variable=True,
        a_nexus_field=NeXusField(
            name="identifierNAME",
            type="NX_CHAR",
            name_type="partial",
            optionality="recommended",
        ),
    )
    identifierNAME__type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-userid-identifiername-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="identifierNAME",
            enumeration=[
                "ARK",
                "DOI",
                "Hdl",
                "IGSN",
                "ISNI",
                "ISSN",
                "ISSN-L",
                "ORCID",
                "PURL",
                "ROR",
                "URL",
                "URN",
            ],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmSample(Sample):
    """
    Description of the sample from which the specimen was prepared or
    site-specifically cut out using e.g. a focused-ion beam instrument.

    In NXapm, a measurement is performed on a specimen. Since APM specimens are
    very small, they are typically cut from a larger object with some
    scientific significance, which NXapm refers to as a sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="recommended",
        ),
    )

    chemical_composition = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmSampleChemicalComposition",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXchemical_composition",
            name="chemical_composition",
            name_type="specified",
            optionality="recommended",
        ),
    )

    identifierNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-identifiername-field"
        ],
        variable=True,
        a_nexus_field=NeXusField(
            name="identifierNAME",
            type="NX_CHAR",
            name_type="partial",
            optionality="recommended",
        ),
    )
    is_simulation = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-is-simulation-field"
        ],
        description=(
            "False, if the sample is a real one. True, if the sample is a virtual one."
        ),
        a_nexus_field=NeXusField(
            name="is_simulation",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-alias-field"
        ],
        description=("Given name/alias for the sample."),
        a_nexus_field=NeXusField(
            name="alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    grain_diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-grain-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Qualitative information about the grain size, here specifically "
            "described as the equivalent spherical diameter of an assumed "
            "average grain size for the crystal ensemble. If the specimen does "
            "not contain many crystals average values might be an unreliable "
            "descriptor. Reporting a grain size may be useful though as it "
            "allows judging if specific features are expected to be found in the "
            "detector hit map."
        ),
        a_nexus_field=NeXusField(
            name="grain_diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    grain_diameter_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-grain-diameter-errors-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Magnitude of the standard deviation of the grain_diameter."),
        a_nexus_field=NeXusField(
            name="grain_diameter_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    heat_treatment_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-heat-treatment-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "An array of elapsed time, the independent axis, of a "
            "time-temperature curve. This field can be used in combination with "
            "heat_treatment_temperature and heat_treatment_temperature_errors as "
            "well as heat_treatment_quenching_rate and "
            "heat_treatment_quenching_rate_errors respectively. In this case, "
            "these fields should also be stored as an array with the same "
            "dimensions as heat_treatment_time to store the dependant axes of a "
            "time-temperature curve as well as its first derivative."
        ),
        a_nexus_field=NeXusField(
            name="heat_treatment_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    heat_treatment_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-heat-treatment-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "If heat_treatment_time is absent, the temperature of the last heat "
            "treatment step before quenching. Knowledge about this value can "
            "give an idea how the sample was heat treated. However, if a "
            "documentation of the annealing treatment as a function of time is "
            "available one should better rely on this information and have it "
            "stored alongside the NeXus file. If heat_treatment_time is "
            "provided, the temperature. Consult the docstring of "
            "heat_treatment_time."
        ),
        a_nexus_field=NeXusField(
            name="heat_treatment_temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    heat_treatment_temperature_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-heat-treatment-temperature-errors-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=(
            "Magnitude of the standard deviation of the "
            "heat_treatment_temperature. If heat_treatment_time is provided, the "
            "magnitude of the standard derivation of the temperature. Consult "
            "the docstring of heat_treatment_time."
        ),
        a_nexus_field=NeXusField(
            name="heat_treatment_temperature_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    heat_treatment_quenching_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-heat-treatment-quenching-rate-field"
        ],
        description=(
            "If heat_treatment_time is absent, the rate of the last quenching "
            "step. Knowledge about this value can give an idea how the sample "
            "was heat treated. However, there are many situations where one can "
            "imagine that the scalar value for just the quenching rate is "
            "insufficient. If heat_treatment_time is provided, the first "
            "derivative of the time-temperature curve. Consult the docstring of "
            "heat_treatment_time for further details."
        ),
        a_nexus_field=NeXusField(
            name="heat_treatment_quenching_rate",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    heat_treatment_quenching_rate_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-heat-treatment-quenching-rate-errors-field"
        ],
        description=(
            "Magnitude of the standard deviation of the "
            "heat_treatment_quenching_rate. If heat_treatment_time is provided, "
            "the magnitude of the standard deviation of the first derivative of "
            "the time-temperature curve. Consult the docstring of "
            "heat_treatment_time for further details."
        ),
        a_nexus_field=NeXusField(
            name="heat_treatment_quenching_rate_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmSampleChemicalComposition(ChemicalComposition):
    """
    The chemical composition of the sample.

    Typically, it is assumed that this more macroscopic composition is
    representative for the material so that the composition of the typically
    substantially less voluminous specimen probes from the more voluminous
    sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-chemical-composition-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXchemical_composition",
            name="chemical_composition",
            name_type="specified",
            optionality="recommended",
        ),
    )

    atom = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmSampleChemicalCompositionAtom",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
            max_occurs=118,
        ),
    )

    normalization = Quantity(
        type=MEnum(["atom_percent", "weight_percent"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-chemical-composition-normalization-field"
        ],
        a_nexus_field=NeXusField(
            name="normalization",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["atom_percent", "weight_percent"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmSampleChemicalCompositionAtom(Atom):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-chemical-composition-element-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
            max_occurs=118,
        ),
    )

    chemical_symbol = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-chemical-composition-element-chemical-symbol-field"
        ],
        a_nexus_field=NeXusField(
            name="chemical_symbol",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    composition = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-chemical-composition-element-composition-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="composition",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    composition_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-sample-chemical-composition-element-composition-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="composition_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmSpecimen(Sample):
    """
    Description of the specimen that was cut off from the sample.

    In atom probe jargon this is typically referred to as the tip.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="specimen",
            name_type="specified",
            optionality="required",
        ),
    )

    identifierNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-identifiername-field"
        ],
        variable=True,
        a_nexus_field=NeXusField(
            name="identifierNAME",
            type="NX_CHAR",
            name_type="partial",
            optionality="recommended",
        ),
    )
    is_simulation = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-is-simulation-field"
        ],
        description=(
            "False, if the specimen is a real one. True, if the specimen is a "
            "virtual one."
        ),
        a_nexus_field=NeXusField(
            name="is_simulation",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-alias-field"
        ],
        description=(
            "Given name or an alias. Better use identifierNAME and "
            "identifier_parent instead. A single NXentry should be used only for "
            "the characterization of a single specimen."
        ),
        a_nexus_field=NeXusField(
            name="alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier_parent = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-identifier-parent-field"
        ],
        description=(
            "Identifier of the sample from which the specimen was cut or the "
            'string "n/a". The purpose of this field is to support '
            "functionalities for tracking sample provenance via a research data "
            "management system."
        ),
        a_nexus_field=NeXusField(
            name="identifier_parent",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    preparation_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-preparation-date-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "when the specimen was prepared. Ideally, report the end of the "
            "preparation, i.e. the last known time the measured specimen surface "
            "was actively prepared. Ideally, this matches the last timestamp "
            "that is mentioned in the digital resource pointed to by "
            "identifier_parent. Knowing when the specimen was exposed to e.g. "
            "specific atmosphere is especially required for environmentally "
            "sensitive material such as hydrogen charged specimens or "
            "experiments including tracers with a short half time."
        ),
        a_nexus_field=NeXusField(
            name="preparation_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the IUPAC periodic table that "
            "are contained in the specimen. If the specimen substance has "
            "multiple components, all elements from each component must be "
            "included in `atom_types`. The purpose of the field is to offer "
            "research data management systems an opportunity to parse the "
            "relevant elements without having to interpret these from the "
            "resources pointed to by identifier_parent or walk through "
            "eventually deeply nested groups in data instances."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    is_polycrystalline = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-is-polycrystalline-field"
        ],
        description=(
            "True, if the specimen contains a grain or phase boundary. False, if "
            "the specimen is a single crystal."
        ),
        a_nexus_field=NeXusField(
            name="is_polycrystalline",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="recommended",
        ),
    )
    is_amorphous = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-is-amorphous-field"
        ],
        description=(
            "True, if the specimen is amorphous. False, if the specimen is not."
        ),
        a_nexus_field=NeXusField(
            name="is_amorphous",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="recommended",
        ),
    )
    initial_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-initial-radius-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Ideally measured otherwise best elaborated guess of the initial "
            "radius of the specimen."
        ),
        a_nexus_field=NeXusField(
            name="initial_radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    shank_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-specimen-shank-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Ideally measured, otherwise best estimate, of the initial shank "
            "angle. This is a measure of the specimen taper. Define it in such a "
            "way that the base of the specimen is modelled as a conical frustrum "
            "so that the shank angle is the smallest angle between the specimen "
            "space z-axis and a vector on the lateral surface of the cone."
        ),
        a_nexus_field=NeXusField(
            name="shank_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmConsistentRotations(Parameters):
    """
    The conventions used when reporting crystal orientations. We follow the
    best practices of the Material Science community that are defined in
    reference `<https://doi.org/10.1088/0965-0393/23/8/083501>`_.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-consistent-rotations-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="consistent_rotations",
            name_type="specified",
            optionality="recommended",
        ),
    )

    rotation_handedness = Quantity(
        type=MEnum(["counter_clockwise", "clockwise"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-consistent-rotations-rotation-handedness-field"
        ],
        description=(
            "Convention how a positive rotation angle is defined when viewing "
            "from the end of the rotation unit vector towards its origin. This "
            "is in accordance with convention 2 of reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_. "
            "Counter_clockwise is equivalent to a right-handed choice. Clockwise "
            "is equivalent to a left-handed choice."
        ),
        a_nexus_field=NeXusField(
            name="rotation_handedness",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["counter_clockwise", "clockwise"],
        ),
    )
    rotation_convention = Quantity(
        type=MEnum(["passive", "active"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-consistent-rotations-rotation-convention-field"
        ],
        description=(
            "How are rotations interpreted into an orientation according to "
            "convention 3 of reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_."
        ),
        a_nexus_field=NeXusField(
            name="rotation_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["passive", "active"],
        ),
    )
    euler_angle_convention = Quantity(
        type=MEnum(
            [
                "zxz",
                "xyx",
                "yzy",
                "zyz",
                "xzx",
                "yxy",
                "xyz",
                "yzx",
                "zxy",
                "xzy",
                "zyx",
                "yxz",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-consistent-rotations-euler-angle-convention-field"
        ],
        description=(
            "How are Euler angles interpreted given that there are several "
            "choices e.g. zxz, xyz according to convention 4 of reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_. The most "
            "frequently used convention in Materials Science is zxz, which is "
            "based on the work of H.-J. Bunge but using other conventions is "
            "possible. Proper Euler angles are distinguished from Tait-Bryan "
            "angles."
        ),
        a_nexus_field=NeXusField(
            name="euler_angle_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "zxz",
                "xyx",
                "yzy",
                "zyz",
                "xzx",
                "yxy",
                "xyz",
                "yzx",
                "zxy",
                "xzy",
                "zyx",
                "yxz",
            ],
        ),
    )
    axis_angle_convention = Quantity(
        type=MEnum(["rotation_angle_on_interval_zero_to_pi"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-consistent-rotations-axis-angle-convention-field"
        ],
        description=(
            "To which angular range is the rotation angle argument of an "
            "axis-angle pair parameterization constrained according to "
            "convention 5 of reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_."
        ),
        a_nexus_field=NeXusField(
            name="axis_angle_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["rotation_angle_on_interval_zero_to_pi"],
        ),
    )
    sign_convention = Quantity(
        type=MEnum(["p_plus_one", "p_minus_one"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-consistent-rotations-sign-convention-field"
        ],
        description=(
            "Which sign convention is followed when converting orientations "
            "between different parametrizations/representations according to "
            "convention 6 of reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_."
        ),
        a_nexus_field=NeXusField(
            name="sign_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["p_plus_one", "p_minus_one"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmNAMED_reference_frameID(CoordinateSystem):
    """
    A coordinate system. Multiple instances require unique names.

    Several Euclidean coordinate systems (CS) are used in the field of atom
    probe:

    * World space; a CS specifying a local coordinate system of the planet
    earth which identifies into which direction gravity is pointing such that
    the laboratory space CS can be rotated into this world CS. * The laboratory
    space; a CS specifying the room where the instrument is located in or a
    physical landmark on the instrument, e.g. the direction of the transfer rod
    where positive is the direction how the rod has to be pushed during loading
    a specimen into the instrument. In summary, this CS is defined by the
    chassis of the instrument. Suggested name of the group
    ``laboratory_reference_frame``. * The specimen space; a CS affixed to
    either the base or the initial apex of the specimen, whose z axis points
    towards the detector. Suggested name of the group
    ``specimen_reference_frame``. * The detector space; a CS affixed to the
    detector plane whose xy plane is usually in the detector and whose z axis
    points towards the specimen. This is a distorted space with respect to the
    reconstructed ion positions. Suggested name of the group
    ``detector_reference_frame``. * The reconstruction space; a CS in which the
    reconstructed ion positions are defined. The orientation depends on the
    analysis software used. * Eventually further coordinate systems attached to
    the flight path of individual ions might be defined. Suggested name of the
    group ``reconstruction_reference_frame``.

    To achieve unique names, the prefix "NAMED" should be replaced to with
    something derived from an alias for the coordinate system, or the value of
    the "alias" field.

    Use the suffix _reference_frame when creating specific instances of
    NXcoordinate_system e.g. laboratory_reference_frame,
    reconstruction_reference_frame and so on and so forth.

    In atom probe microscopy a frequently used choice for the detector space
    (CS) is discussed with the so-called detector space image stack. This is a
    stack of two-dimensional histograms of detected ions within a predefined
    evaporation identifier interval. Typically, the set of ion evaporation
    sequence identifiers is grouped into chunks.

    For each chunk a histogram of the ion hit positions on the detector is
    computed. This leaves the possibility for inconsistency between the
    so-called detector space and the e.g. specimen space.

    To avoid these ambiguities, instances of :ref:`NXtransformations` should be
    used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="NAMED_reference_frameID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-alias-field"
        ],
        a_nexus_field=NeXusField(
            name="alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["undefined", "cartesian"],
            open_enum=True,
        ),
    )
    origin = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-origin-field"
        ],
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-x-field"
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
    x_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-x-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-y-field"
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
    y_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-y-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-z-field"
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
    z_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-named-reference-frameid-z-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmApmMeasurement(ApmMeasurement):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_measurement",
            name="measurement",
            name_type="specified",
            optionality="optional",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrument",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_instrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )
    eventID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_event_data",
            name="eventID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    standing_voltage_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementStandingVoltageTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="standing_voltage_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    pulse_frequency_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementPulseFrequencyTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pulse_frequency_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    detection_rate_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementDetectionRateTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    detection_rate_set_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementDetectionRateSetTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_set_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    pressure_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementPressureTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pressure_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    specimen_voltage_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementSpecimenVoltageTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_voltage_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    specimen_temperature_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementSpecimenTemperatureTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_temperature_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    ambient_temperature_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementAmbientTemperatureTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ambient_temperature_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    reflectron_voltage_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementReflectronVoltageTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="reflectron_voltage_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    xstage_position_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementXstagePositionTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="xstage_position_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    ystage_position_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementYstagePositionTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ystage_position_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    zstage_position_time = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementZstagePositionTime",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="zstage_position_time",
            name_type="specified",
            optionality="optional",
        ),
    )
    standing_voltage_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementStandingVoltageSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="standing_voltage_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    pulse_frequency_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementPulseFrequencySequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pulse_frequency_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    detection_rate_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementDetectionRateSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    detection_rate_set_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementDetectionRateSetSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_set_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    pressure_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementPressureSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pressure_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    specimen_voltage_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementSpecimenVoltageSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_voltage_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    specimen_temperature_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementSpecimenTemperatureSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_temperature_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    ambient_temperature_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementAmbientTemperatureSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ambient_temperature_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    reflectron_voltage_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementReflectronVoltageSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="reflectron_voltage_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    xstage_position_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementXstagePositionSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="xstage_position_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    ystage_position_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementYstagePositionSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ystage_position_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )
    zstage_position_sequence = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementZstagePositionSequence",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="zstage_position_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    status = Quantity(
        type=MEnum(["success", "aborted"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-status-field"
        ],
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["success", "aborted"],
        ),
    )
    quality = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-quality-field"
        ],
        a_nexus_field=NeXusField(
            name="quality",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrument(ApmInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_instrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )
    reflectron = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentReflectron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="reflectron",
            name_type="specified",
            optionality="optional",
        ),
    )
    local_electrode = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentLocalElectrode",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="local_electrode",
            name_type="specified",
            optionality="recommended",
        ),
    )
    ion_detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentIonDetector",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="ion_detector",
            name_type="specified",
            optionality="recommended",
        ),
    )
    pulser = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentPulser",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="pulser",
            name_type="specified",
            optionality="recommended",
        ),
    )
    stage = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentStage",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stage",
            name_type="specified",
            optionality="optional",
        ),
    )
    analysis_chamber = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentAnalysisChamber",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="analysis_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )
    buffer_chamber = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentBufferChamber",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="buffer_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )
    load_lock_chamber = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentLoadLockChamber",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="load_lock_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )
    getter_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentGetterPump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="getter_pump",
            name_type="specified",
            optionality="optional",
        ),
    )
    roughening_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentRougheningPump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="roughening_pump",
            name_type="specified",
            optionality="optional",
        ),
    )
    turbomolecular_pump = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentTurbomolecularPump",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="turbomolecular_pump",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "Inspico",
                "3DAP",
                "LAWATAP",
                "LEAP 3000 Si",
                "LEAP 3000X Si",
                "LEAP 3000 HR",
                "LEAP 3000X HR",
                "LEAP 4000 Si",
                "LEAP 4000X Si",
                "LEAP 4000 HR",
                "LEAP 4000X HR",
                "LEAP 5000 XS",
                "LEAP 5000 XR",
                "LEAP 5000 R",
                "EIKOS",
                "EIKOS-UV",
                "LEAP 6000 XR",
                "LEAP INVIZO",
                "Photonic AP",
                "TeraSAT",
                "TAPHR",
                "Modular AP",
                "Titanium APT",
                "Extreme UV APT",
            ],
            open_enum=True,
        ),
    )
    location = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-location-field"
        ],
        a_nexus_field=NeXusField(
            name="location",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    flight_path = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-flight-path-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="flight_path",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentReflectron(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-reflectron-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="reflectron",
            name_type="specified",
            optionality="optional",
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-reflectron-applied-field"
        ],
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentLocalElectrode(ElectromagneticLens):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-local-electrode-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="local_electrode",
            name_type="specified",
            optionality="recommended",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentLocalElectrodeFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-local-electrode-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    aperture_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-local-electrode-aperture-type-field"
        ],
        a_nexus_field=NeXusField(
            name="aperture_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentLocalElectrodeFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-local-electrode-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-local-electrode-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-local-electrode-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-local-electrode-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentIonDetector(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-ion-detector-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="ion_detector",
            name_type="specified",
            optionality="recommended",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentIonDetectorFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentIonDetectorFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-ion-detector-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-ion-detector-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-ion-detector-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-ion-detector-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentPulser(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="pulser",
            name_type="specified",
            optionality="recommended",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentPulserFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )
    sourceID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentPulserSourceID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="sourceID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=2,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentPulserFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentPulserSourceID(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-sourceid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="sourceID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=2,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentPulserSourceIDFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentPulserSourceIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-sourceid-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-sourceid-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-sourceid-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-pulser-sourceid-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentStage(Manipulator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-stage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stage",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentStageFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentStageFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-stage-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-stage-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-stage-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-stage-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentAnalysisChamber(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-analysis-chamber-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="analysis_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentAnalysisChamberFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentAnalysisChamberFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-analysis-chamber-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-analysis-chamber-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-analysis-chamber-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-analysis-chamber-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentBufferChamber(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-buffer-chamber-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="buffer_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentBufferChamberFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentBufferChamberFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-buffer-chamber-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-buffer-chamber-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-buffer-chamber-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-buffer-chamber-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentLoadLockChamber(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-load-lock-chamber-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="load_lock_chamber",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentLoadLockChamberFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentLoadLockChamberFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-load-lock-chamber-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-load-lock-chamber-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-load-lock-chamber-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-load-lock-chamber-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentGetterPump(Pump):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-getter-pump-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="getter_pump",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentGetterPumpFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentGetterPumpFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-getter-pump-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-getter-pump-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-getter-pump-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-getter-pump-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentRougheningPump(Pump):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-roughening-pump-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="roughening_pump",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentRougheningPumpFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentRougheningPumpFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-roughening-pump-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-roughening-pump-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-roughening-pump-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-roughening-pump-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentTurbomolecularPump(Pump):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-turbomolecular-pump-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="turbomolecular_pump",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementInstrumentTurbomolecularPumpFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementInstrumentTurbomolecularPumpFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-turbomolecular-pump-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-turbomolecular-pump-fabrication-vendor-field"
        ],
        a_nexus_field=NeXusField(
            name="vendor",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-turbomolecular-pump-fabrication-model-field"
        ],
        a_nexus_field=NeXusField(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-instrument-turbomolecular-pump-fabrication-serial-number-field"
        ],
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventID(ApmEventData):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_event_data",
            name="eventID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrument",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_instrument",
            name="instrument",
            name_type="specified",
            optionality="recommended",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-start-time-field"
        ],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrument(ApmInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_instrument",
            name="instrument",
            name_type="specified",
            optionality="recommended",
        ),
    )

    reflectron = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentReflectron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="reflectron",
            name_type="specified",
            optionality="recommended",
        ),
    )
    local_electrode = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentLocalElectrode",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="local_electrode",
            name_type="specified",
            optionality="recommended",
        ),
    )
    pulser = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentPulser",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="pulser",
            name_type="specified",
            optionality="recommended",
        ),
    )
    stage = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentStage",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stage",
            name_type="specified",
            optionality="required",
        ),
    )
    analysis_chamber = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentAnalysisChamber",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="analysis_chamber",
            name_type="specified",
            optionality="required",
        ),
    )
    control = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentControl",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="control",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentReflectron(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-reflectron-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="reflectron",
            name_type="specified",
            optionality="recommended",
        ),
    )

    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-reflectron-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentLocalElectrode(ElectromagneticLens):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-local-electrode-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="local_electrode",
            name_type="specified",
            optionality="recommended",
        ),
    )

    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-local-electrode-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentPulser(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="pulser",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sourceID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentPulserSourceID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="sourceID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=2,
        ),
    )

    pulse_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-pulse-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="pulse_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["laser", "voltage", "laser_and_voltage"],
            open_enum=True,
        ),
    )
    pulse_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-pulse-frequency-field"
        ],
        dimensionality="1 / [time]",
        unit="hertz",
        a_nexus_field=NeXusField(
            name="pulse_frequency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_FREQUENCY",
        ),
    )
    pulse_fraction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-pulse-fraction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="pulse_fraction",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    pulse_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-pulse-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="pulse_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    pulse_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-pulse-number-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="pulse_number",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    standing_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-standing-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="standing_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentPulserSourceID(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-sourceid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="sourceID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
            max_occurs=2,
        ),
    )

    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-sourceid-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_WAVELENGTH",
        ),
    )
    power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-sourceid-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        unit="watt",
        a_nexus_field=NeXusField(
            name="power",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_POWER",
        ),
    )
    pulse_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-pulser-sourceid-pulse-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="pulse_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentStage(Manipulator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-stage-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stage",
            name_type="specified",
            optionality="required",
        ),
    )

    temperature_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentStageTemperatureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentStageTemperatureSensor(Sensor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-stage-temperature-sensor-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="temperature_sensor",
            name_type="specified",
            optionality="required",
        ),
    )

    measurement = Quantity(
        type=MEnum(["temperature"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-stage-temperature-sensor-measurement-field"
        ],
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["temperature"],
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-stage-temperature-sensor-value-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentAnalysisChamber(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-analysis-chamber-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="analysis_chamber",
            name_type="specified",
            optionality="required",
        ),
    )

    pressure_sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmMeasurementEventIDInstrumentAnalysisChamberPressureSensor",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="pressure_sensor",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentAnalysisChamberPressureSensor(Sensor):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-analysis-chamber-pressure-sensor-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="pressure_sensor",
            name_type="specified",
            optionality="required",
        ),
    )

    measurement = Quantity(
        type=MEnum(["pressure"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-analysis-chamber-pressure-sensor-measurement-field"
        ],
        a_nexus_field=NeXusField(
            name="measurement",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["pressure"],
        ),
    )
    value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-analysis-chamber-pressure-sensor-value-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_PRESSURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementEventIDInstrumentControl(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-control-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="control",
            name_type="specified",
            optionality="recommended",
        ),
    )

    evaporation_control = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-control-evaporation-control-field"
        ],
        a_nexus_field=NeXusField(
            name="evaporation_control",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    target_detection_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-eventid-instrument-control-target-detection-rate-field"
        ],
        a_nexus_field=NeXusField(
            name="target_detection_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementStandingVoltageTime(Data):
    """
    Monitoring standing_voltage as a function of elapsed time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="standing_voltage_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    standing_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-standing-voltage-field"
        ],
        a_nexus_field=NeXusField(
            name="standing_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    standing_voltage__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-standing-voltage-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="standing_voltage",
        ),
    )
    standing_voltage__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-time-standing-voltage-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="standing_voltage",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementPulseFrequencyTime(Data):
    """
    Monitoring pulse_frequency as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pulse_frequency_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    pulse_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-pulse-frequency-field"
        ],
        a_nexus_field=NeXusField(
            name="pulse_frequency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    pulse_frequency__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-pulse-frequency-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="pulse_frequency",
        ),
    )
    pulse_frequency__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-time-pulse-frequency-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="pulse_frequency",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementDetectionRateTime(Data):
    """
    Monitoring detection_rate as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    detection_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-detection-rate-field"
        ],
        a_nexus_field=NeXusField(
            name="detection_rate",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    detection_rate__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-detection-rate-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="detection_rate",
        ),
    )
    detection_rate__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-time-detection-rate-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="detection_rate",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementDetectionRateSetTime(Data):
    """
    Monitoring detection_rate_set as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_set_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    detection_rate_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-detection-rate-set-field"
        ],
        a_nexus_field=NeXusField(
            name="detection_rate_set",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    detection_rate_set__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-detection-rate-set-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="detection_rate_set",
        ),
    )
    detection_rate_set__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-time-detection-rate-set-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="detection_rate_set",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementPressureTime(Data):
    """
    Monitoring pressure as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pressure_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-pressure-field"
        ],
        a_nexus_field=NeXusField(
            name="pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    pressure__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-pressure-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="pressure",
        ),
    )
    pressure__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-time-pressure-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="pressure",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementSpecimenVoltageTime(Data):
    """
    Monitoring specimen_voltage as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_voltage_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    specimen_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-specimen-voltage-field"
        ],
        a_nexus_field=NeXusField(
            name="specimen_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    specimen_voltage__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-specimen-voltage-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="specimen_voltage",
        ),
    )
    specimen_voltage__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-time-specimen-voltage-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="specimen_voltage",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementSpecimenTemperatureTime(Data):
    """
    Monitoring specimen_temperature as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_temperature_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    specimen_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-specimen-temperature-field"
        ],
        a_nexus_field=NeXusField(
            name="specimen_temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    specimen_temperature__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-specimen-temperature-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="specimen_temperature",
        ),
    )
    specimen_temperature__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-time-specimen-temperature-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="specimen_temperature",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementAmbientTemperatureTime(Data):
    """
    Monitoring ambient_temperature as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ambient_temperature_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    ambient_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-ambient-temperature-field"
        ],
        a_nexus_field=NeXusField(
            name="ambient_temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    ambient_temperature__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-ambient-temperature-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="ambient_temperature",
        ),
    )
    ambient_temperature__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-time-ambient-temperature-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="ambient_temperature",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementReflectronVoltageTime(Data):
    """
    Monitoring reflectron_voltage as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="reflectron_voltage_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    reflectron_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-reflectron-voltage-field"
        ],
        a_nexus_field=NeXusField(
            name="reflectron_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    reflectron_voltage__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-reflectron-voltage-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="reflectron_voltage",
        ),
    )
    reflectron_voltage__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-time-reflectron-voltage-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="reflectron_voltage",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementXstagePositionTime(Data):
    """
    Monitoring xstage_position as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="xstage_position_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    xstage_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-xstage-position-field"
        ],
        a_nexus_field=NeXusField(
            name="xstage_position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    xstage_position__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-xstage-position-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="xstage_position",
        ),
    )
    xstage_position__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-time-xstage-position-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="xstage_position",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementYstagePositionTime(Data):
    """
    Monitoring ystage_position as a function of elapsed_time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ystage_position_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    ystage_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-ystage-position-field"
        ],
        a_nexus_field=NeXusField(
            name="ystage_position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    ystage_position__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-ystage-position-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="ystage_position",
        ),
    )
    ystage_position__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-time-ystage-position-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="ystage_position",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementZstagePositionTime(Data):
    """
    Monitoring zstage_position as a function of elapsed time

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="zstage_position_time",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-elapsed-time-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="elapsed_time_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-elapsed-time-field"
        ],
        a_nexus_field=NeXusField(
            name="elapsed_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    elapsed_time__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-elapsed-time-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="elapsed_time",
        ),
    )
    elapsed_time__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-elapsed-time-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="elapsed_time",
        ),
    )
    zstage_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-zstage-position-field"
        ],
        a_nexus_field=NeXusField(
            name="zstage_position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    zstage_position__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-zstage-position-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="zstage_position",
        ),
    )
    zstage_position__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-time-zstage-position-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="zstage_position",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementStandingVoltageSequence(Data):
    """
    Monitoring standing_voltage as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="standing_voltage_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    standing_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-standing-voltage-field"
        ],
        a_nexus_field=NeXusField(
            name="standing_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    standing_voltage__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-standing-voltage-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="standing_voltage",
        ),
    )
    standing_voltage__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-standing-voltage-sequence-standing-voltage-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="standing_voltage",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementPulseFrequencySequence(Data):
    """
    Monitoring pulse_frequency as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pulse_frequency_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    pulse_frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-pulse-frequency-field"
        ],
        a_nexus_field=NeXusField(
            name="pulse_frequency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    pulse_frequency__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-pulse-frequency-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="pulse_frequency",
        ),
    )
    pulse_frequency__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pulse-frequency-sequence-pulse-frequency-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="pulse_frequency",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementDetectionRateSequence(Data):
    """
    Monitoring detection_rate as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    detection_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-detection-rate-field"
        ],
        a_nexus_field=NeXusField(
            name="detection_rate",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    detection_rate__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-detection-rate-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="detection_rate",
        ),
    )
    detection_rate__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-sequence-detection-rate-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="detection_rate",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementDetectionRateSetSequence(Data):
    """
    Monitoring detection_rate_set as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="detection_rate_set_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    detection_rate_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-detection-rate-set-field"
        ],
        a_nexus_field=NeXusField(
            name="detection_rate_set",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    detection_rate_set__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-detection-rate-set-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="detection_rate_set",
        ),
    )
    detection_rate_set__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-detection-rate-set-sequence-detection-rate-set-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="detection_rate_set",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementPressureSequence(Data):
    """
    Monitoring pressure as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="pressure_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-pressure-field"
        ],
        a_nexus_field=NeXusField(
            name="pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    pressure__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-pressure-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="pressure",
        ),
    )
    pressure__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-pressure-sequence-pressure-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="pressure",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementSpecimenVoltageSequence(Data):
    """
    Monitoring specimen_voltage as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_voltage_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    specimen_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-specimen-voltage-field"
        ],
        a_nexus_field=NeXusField(
            name="specimen_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    specimen_voltage__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-specimen-voltage-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="specimen_voltage",
        ),
    )
    specimen_voltage__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-voltage-sequence-specimen-voltage-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="specimen_voltage",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementSpecimenTemperatureSequence(Data):
    """
    Monitoring specimen_temperature as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specimen_temperature_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    specimen_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-specimen-temperature-field"
        ],
        a_nexus_field=NeXusField(
            name="specimen_temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    specimen_temperature__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-specimen-temperature-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="specimen_temperature",
        ),
    )
    specimen_temperature__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-specimen-temperature-sequence-specimen-temperature-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="specimen_temperature",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementAmbientTemperatureSequence(Data):
    """
    Monitoring ambient_temperature as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ambient_temperature_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    ambient_temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-ambient-temperature-field"
        ],
        a_nexus_field=NeXusField(
            name="ambient_temperature",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    ambient_temperature__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-ambient-temperature-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="ambient_temperature",
        ),
    )
    ambient_temperature__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ambient-temperature-sequence-ambient-temperature-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="ambient_temperature",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementReflectronVoltageSequence(Data):
    """
    Monitoring reflectron_voltage as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="reflectron_voltage_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    reflectron_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-reflectron-voltage-field"
        ],
        a_nexus_field=NeXusField(
            name="reflectron_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    reflectron_voltage__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-reflectron-voltage-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="reflectron_voltage",
        ),
    )
    reflectron_voltage__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-reflectron-voltage-sequence-reflectron-voltage-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="reflectron_voltage",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementXstagePositionSequence(Data):
    """
    Monitoring xstage_position as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="xstage_position_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    xstage_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-xstage-position-field"
        ],
        a_nexus_field=NeXusField(
            name="xstage_position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    xstage_position__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-xstage-position-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="xstage_position",
        ),
    )
    xstage_position__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-xstage-position-sequence-xstage-position-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="xstage_position",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementYstagePositionSequence(Data):
    """
    Monitoring ystage_position as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="ystage_position_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    ystage_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-ystage-position-field"
        ],
        a_nexus_field=NeXusField(
            name="ystage_position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    ystage_position__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-ystage-position-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="ystage_position",
        ),
    )
    ystage_position__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-ystage-position-sequence-ystage-position-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="ystage_position",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmMeasurementZstagePositionSequence(Data):
    """
    Monitoring zstage_position as a function of event_id

    Sub-sampling should be used for practical purposes. For HITS, ntf TTree
    objects are used as values for each event are not reliably accessible
    because these are binarily encoded with a proprietary structure that is not
    documented publicly. For RHIT, nth TBranch objects are used. Values for
    each event are available but sub-sampling should still be used.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="zstage_position_sequence",
            name_type="specified",
            optionality="optional",
        ),
    )

    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-axes-attribute"
        ],
        shape=["*"],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-event-id-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="event_id_indices",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-event-id-field"
        ],
        a_nexus_field=NeXusField(
            name="event_id",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
        ),
    )
    event_id__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-event-id-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="event_id",
        ),
    )
    event_id__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-event-id-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="event_id",
        ),
    )
    zstage_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-zstage-position-field"
        ],
        a_nexus_field=NeXusField(
            name="zstage_position",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    zstage_position__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-zstage-position-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="zstage_position",
        ),
    )
    zstage_position__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-measurement-zstage-position-sequence-zstage-position-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="zstage_position",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeID(RoiProcess):
    """
    A region-of-interest analyzed either during or after the session for which
    specific processed data of the measured or simulated data are available.

    If a single instance is required the group should be named atom_probe. If
    multiple groups are required these should be named atom_probe1,
    atom_probe2, and so on and so forth.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXroi_process",
            name="atom_probeID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    initial_specimen = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDInitialSpecimen",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="initial_specimen",
            name_type="specified",
            optionality="recommended",
        ),
    )
    final_specimen = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDFinalSpecimen",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="final_specimen",
            name_type="specified",
            optionality="recommended",
        ),
    )
    raw_data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRawData",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="raw_data",
            name_type="specified",
            optionality="optional",
        ),
    )
    hit_finding = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDHitFinding",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="hit_finding",
            name_type="specified",
            optionality="recommended",
        ),
    )
    hit_spatial_filtering = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDHitSpatialFiltering",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="hit_spatial_filtering",
            name_type="specified",
            optionality="recommended",
        ),
    )
    voltage_and_bowl = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDVoltageAndBowl",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="voltage_and_bowl",
            name_type="specified",
            optionality="recommended",
        ),
    )
    mass_to_charge_conversion = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDMassToChargeConversion",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="mass_to_charge_conversion",
            name_type="specified",
            optionality="recommended",
        ),
    )
    reconstruction = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstruction",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_reconstruction",
            name="reconstruction",
            name_type="specified",
            optionality="recommended",
        ),
    )
    ranging = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRanging",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_ranging",
            name="ranging",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDInitialSpecimen(Image):
    """
    SEM or TEM image of the initial specimen taken before the measurement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="initial_specimen",
            name_type="specified",
            optionality="recommended",
        ),
    )

    image_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDInitialSpecimenImage2d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDInitialSpecimenImage2d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-real-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axis-j-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_j__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axis-j-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axis-i-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_i__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axis-i-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-initial-specimen-image-2d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDFinalSpecimen(Image):
    """
    SEM or TEM image of the final specimen taken after completion of the
    measurement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="final_specimen",
            name_type="specified",
            optionality="recommended",
        ),
    )

    image_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDFinalSpecimenImage2d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDFinalSpecimenImage2d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-real-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axis-j-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_j__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axis-j-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axis-i-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_i__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axis-i-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-final-specimen-image-2d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRawData(Process):
    """
    Document the control software that was used on the instrument with which
    raw data were collected.

    For almost all atom probe instruments, the recorded raw data and metadata
    follow proprietary semantics. Therefore, this group can currently often not
    be filled with more than the control software and some pointing to digital
    artifacts (e.g. proprietary files) that have been collected during the
    measurement in an effort to document as best as possible all steps of an
    analysis workflow.

    The physical quantities measured in an atom probe experiment are
    time-of-flight and tuples of arrival_time_pairs as a function of the event
    chain on the pulser. From these tuples, hits are computed in a process
    called hit_finding.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="raw_data",
            name_type="specified",
            optionality="optional",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRawDataProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRawDataSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_dld_wires = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-number-of-dld-wires-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The number of delay-line-detector (DLD) wires present."),
        a_nexus_field=NeXusField(
            name="number_of_dld_wires",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
    )
    dld_wire_names = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-dld-wire-names-field"
        ],
        shape=["*", 2],
        description=(
            "Alias tuple, typical for the begin and the end of each DLD wire of "
            "the detector. Order follows arrival_time_pairs. The order of the "
            "first dimension should match that of the second dimension of the "
            "arrival_time_pairs field."
        ),
        a_nexus_field=NeXusField(
            name="dld_wire_names",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    arrival_time_pairs = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-arrival-time-pairs-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*", "*", 2],
        description=(
            "Raw readings from the analog-to-digital-converter timing circuits "
            "of the detector wires."
        ),
        a_nexus_field=NeXusField(
            name="arrival_time_pairs",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRawDataProgramID(Program):
    """
    The control software that was used for running the measurement.

    At least the main software should be reported. If this is the only program
    to report name the group "program" and use its below fields program and
    version to detail the version used. E.g. program AP Suite, version 6.3

    It is recommended to report multiple programs though, i.e. also the
    libraries and dependencies of the software. In the case of AP Suite/IVAS
    this can be used to document the AP Suite GUI, LAS, CamecaRoot, and
    CernRoot versions. In this case always name the program groups program1,
    program2, ... with program one being AP Suite/IVAS.

    In the case of an open-source instrument, like P. Felfer's Oxcart or G.
    Schmitz's M-TAP instruments, also use program1, program2, ... with program1
    representing the control software e.g. `M. Monajem and P. Felfer PYCCAPT
    <https://pyccapt.readthedocs.io/en/latest/>`_. Further instances (program2,
    ...) can be used to list the dependencies, the python virtual environment.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRawDataSource(Note):
    """
    Possibility to point to files that contain raw data.

    Exemplar files that could be pointed to here when working with
    AMETEK/Cameca instruments are the proprietary STR, RRAW, or HITS files that
    AP Suite/IVAS generates.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-source-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-source-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-source-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-raw-data-source-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDHitFinding(Process):
    """
    The configuration of a hit finding algorithm and its output.

    Hit finding is the process of deciding which detector signals are
    significant and assigning specific ions colliding with the detector to each
    observed event.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="hit_finding",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDHitFindingProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDHitFindingConfig",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="config",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    hit_positions = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-hit-positions-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 2],
        description=(
            "Evaluated ion impact coordinates on the detector. Use the "
            "depends_on field to specify which reference frame the positions are "
            "defined in."
        ),
        a_nexus_field=NeXusField(
            name="hit_positions",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    hit_positions__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-hit-positions-depends-on-attribute"
        ],
        description=(
            "Contains the path to an instance of NX_coordinate_system in which "
            "the positions are defined."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="hit_positions",
        ),
    )
    total_event_golden = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-total-event-golden-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            'Number of events of type "golden" when APSuite/IVAS was used as '
            "the software with which the measurement was performed. The value "
            "can be extracted from the CRunHeader.fTotalEventGolden field of a "
            "CamecaRoot RHIT/HITS file."
        ),
        a_nexus_field=NeXusField(
            name="total_event_golden",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    total_event_incomplete = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-total-event-incomplete-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            'Number of events of type "incomplete" when APSuite/IVAS was used '
            "as the software with which the measurement was performed. The value "
            "can be extracted from the CRunHeader.fTotalEventIncomplete field of "
            "a CamecaRoot RHIT/HITS file."
        ),
        a_nexus_field=NeXusField(
            name="total_event_incomplete",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    total_event_multiple = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-total-event-multiple-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            'Number of events of type "multiple" when APSuite/IVAS was used as '
            "the software with which the measurement was performed. The value "
            "can be extracted from the CRunHeader.fTotalEventMultiple field of a "
            "CamecaRoot RHIT/HITS file."
        ),
        a_nexus_field=NeXusField(
            name="total_event_multiple",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    total_event_partials = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-total-event-partials-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            'Number of events of type "partials" when APSuite/IVAS was used as '
            "the software with which the measurement was performed. The value "
            "can be extracted from the CRunHeader.fTotalEventPartials field of a "
            "CamecaRoot RHIT/HITS file."
        ),
        a_nexus_field=NeXusField(
            name="total_event_partials",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    total_event_record = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-total-event-record-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Number of events when APSuite/IVAS was used as the software with "
            "which the measurement was performed. The value can be extracted "
            "from the CRunHeader.fTotalEventRecords field of a CamecaRoot "
            "RHIT/HITS file."
        ),
        a_nexus_field=NeXusField(
            name="total_event_record",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    hit_quality_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-hit-quality-type-field"
        ],
        shape=["*"],
        description=(
            "Hit quality is an integer that specifies which category/type a hit "
            "was assigned to. This field lists the human-readable, possibly "
            "though proprietary types distinguished. The indices of this array "
            "are used in hit_quality to encode hit_quality for each pulse in a "
            "more efficient way than by repeating the string that is used for "
            "each type as it is provided in this field. As an example, assume "
            'two types, "golden" and "partial", are distinguished. If '
            'hit_quality_type stores the array "golden", "partial", the '
            "index 0 in hit_quality identifies all those pulses of category "
            '"golden", while the index 1 in hit_quality identifies all of '
            'category "partial".'
        ),
        a_nexus_field=NeXusField(
            name="hit_quality_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    hit_quality = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-hit-quality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Hit quality identifier for each pulse. Identifier has to be within "
            "hit_quality_type."
        ),
        a_nexus_field=NeXusField(
            name="hit_quality",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    hit_multiplicity = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-hit-multiplicity-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The number of ions determined to have been collected on the same "
            "pulse. These ions may hit different pixels, or even the same "
            "detector pixel. The hit_multiplicity is not related to the makeup "
            "of the ions and should not be confused with the number of atoms or "
            "elements that constitute a molecular ion."
        ),
        a_nexus_field=NeXusField(
            name="hit_multiplicity",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDHitFindingProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDHitFindingConfig(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="config",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-config-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-config-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-config-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-finding-config-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDHitSpatialFiltering(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="hit_spatial_filtering",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDHitSpatialFilteringProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDHitSpatialFilteringSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="optional",
        ),
    )
    hit_filter = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDHitSpatialFilteringHitFilter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="hit_filter",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    evaporation_id_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-evaporation-id-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Integer which defines the first evaporation_id. Typically, this is "
            "either zero or one."
        ),
        a_nexus_field=NeXusField(
            name="evaporation_id_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    evaporation_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-evaporation-id-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "There are two possibilities to report evaporation_id values: If "
            "evaporation_id_offset is provided, the evaporation_id values are "
            "defined by the sequence :math:`[evaporation\\_id\\_offset, "
            "evaporation\\_id\\_offset + n]` with :math:`n` the number of ions "
            "in the reconstructed volume. Alternatively, evaporation_id_offset "
            "is not provided but instead a a sequence of :math:`n` values is "
            "defined, these integer values do not need to be sorted."
        ),
        a_nexus_field=NeXusField(
            name="evaporation_id",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDHitSpatialFilteringProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDHitSpatialFilteringSource(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-source-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-source-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-source-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-source-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDHitSpatialFilteringHitFilter(CsFilterBooleanMask):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-hit-filter-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_filter_boolean_mask",
            name="hit_filter",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_objects = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-hit-filter-number-of-objects-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_objects",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    bitdepth = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-hit-filter-bitdepth-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="bitdepth",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-hit-spatial-filtering-hit-filter-mask-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="mask",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDVoltageAndBowl(Process):
    """
    Configuration of and results obtained from a voltage-and-bowl
    time-of-flight correction algorithm.

    The voltage-and-bowl correction is a data post-processing step to correct
    ion impact positions for flight path differences, detector bias, and
    nonlinearities.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="voltage_and_bowl",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDVoltageAndBowlProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDVoltageAndBowlSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="optional",
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDVoltageAndBowlConfig",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    raw_tof = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-raw-tof-field"
        ],
        shape=["*"],
        description=("Raw time-of-flight data without corrections."),
        a_nexus_field=NeXusField(
            name="raw_tof",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    tof_zero_estimate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-tof-zero-estimate-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("The parameter :math:`t_0`, CAnalysis.CCalibMass.fT0Estimate"),
        a_nexus_field=NeXusField(
            name="tof_zero_estimate",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    calibrated_tof = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-calibrated-tof-field"
        ],
        shape=["*"],
        description=("Calibrated time-of-flight."),
        a_nexus_field=NeXusField(
            name="calibrated_tof",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDVoltageAndBowlProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDVoltageAndBowlSource(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-source-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-source-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-source-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-source-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDVoltageAndBowlConfig(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )

    correction_peak = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-voltage-and-bowl-config-correction-peak-field"
        ],
        description=(
            "Reference mass-to-charge state ratio value For example 16 Da as "
            "mentioned by `T. Blum et al. "
            "<https://doi.org/10.1002/9781119227250.ch18>`_ (page 371)."
        ),
        a_nexus_field=NeXusField(
            name="correction_peak",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDMassToChargeConversion(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="mass_to_charge_conversion",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDMassToChargeConversionProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDMassToChargeConversionSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDMassToChargeConversionConfig",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    mass_to_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-mass-to-charge-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="mass_to_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDMassToChargeConversionProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDMassToChargeConversionSource(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-source-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-source-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-source-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-source-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDMassToChargeConversionConfig(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="recommended",
        ),
    )

    mass_resolutionION = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDMassToChargeConversionConfigMass_resolutionION",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name="mass_resolutionION",
            name_type="partial",
            optionality="recommended",
        ),
    )

    mass_calibration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-config-mass-calibration-field"
        ],
        description=(
            "Mass calibration with unit peaks/interp. as mentioned by `T. Blum "
            "et al. <https://doi.org/10.1002/9781119227250.ch18>`_ (page 371)."
        ),
        a_nexus_field=NeXusField(
            name="mass_calibration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    mass_resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-config-mass-resolution-field"
        ],
        shape=["*"],
        description=(
            "Inverse of the mass resolution :math:`\\frac{M}{\\Delta M}` as "
            "mentioned by `T. Blum et al. "
            "<https://doi.org/10.1002/9781119227250.ch18>`_ (page 371). Multiple "
            "values can be reported but reporting each is only useful when "
            "stating also: * The full width at which :math:`{\\Delta M}_{fw}` "
            "fraction of maximum this value was defined. Examples are at tenth "
            ":math:`{\\Delta M}_{10}` or at half maximum (FWHM). Consequently, "
            "mass_resolution_fw should needs to be a vector of the same length "
            "and using the same order like used for mass_resolution, i.e. the "
            "first mass resolution was defined at the maximum as defined by the "
            "first value from mass_resolution_fw. * The reference molecular ion "
            "e.g. :math:`^{16}{O_{2}}^{+}` As many instances of "
            "mass_resolutionION should be used with instances numbered starting "
            "from 1 up to the length of the mass_resolution vector."
        ),
        a_nexus_field=NeXusField(
            name="mass_resolution",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    mass_resolution_fw = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-config-mass-resolution-fw-field"
        ],
        shape=["*"],
        description=(
            "The full width at which :math:`{\\Delta M}_{fw}` fraction of "
            "maximum this value was defined. Examples are at tenth "
            ":math:`{\\Delta M}_{10}` or at half maximum (FWHM). Consequently, "
            "mass_resolution_fw should needs to be a vector of the same length "
            "and using the same order like used for mass_resolution, i.e. the "
            "first mass resolution was defined at the maximum as defined by the "
            "first value from mass_resolution_fw."
        ),
        a_nexus_field=NeXusField(
            name="mass_resolution_fw",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDMassToChargeConversionConfigMass_resolutionION(Atom):
    """
    The reference molecular ion e.g. :math:`^{16}{O_{2}}^{+}` As many instances
    of mass_resolutionION should be used with instances numbered starting from
    1 up to the length of the mass_resolution vector.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-config-mass-resolutionion-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name="mass_resolutionION",
            name_type="partial",
            optionality="recommended",
        ),
    )

    nuclide_hash = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-config-mass-resolutionion-nuclide-hash-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="nuclide_hash",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-mass-to-charge-conversion-config-mass-resolutionion-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstruction(ApmReconstruction):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_reconstruction",
            name="reconstruction",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstructionProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstructionSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )
    results = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstructionResults",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="results",
            name_type="specified",
            optionality="recommended",
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstructionConfig",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="recommended",
        ),
    )
    naive_discretization = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstructionNaiveDiscretization",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="naive_discretization",
            name_type="specified",
            optionality="required",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    reconstructed_positions = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-reconstructed-positions-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", 3],
        a_nexus_field=NeXusField(
            name="reconstructed_positions",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLUME",
        ),
    )
    field_of_view = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-field-of-view-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="field_of_view",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstructionProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstructionSource(Note):
    """
    For LEAP and APSuite/IVAS-based analyses the root file which stores the
    settings whereby an RHIT/HITS file can be used to regenerate the
    reconstructed volume that is here referred to.

    The respective RHIT/HITS file should ideally be specified in the serialized
    group of the hit_finding section of this application definition.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-source-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-source-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-source-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-source-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstructionResults(Note):
    """
    For LEAP and APSuite/IVAS-based analyses the resulting typically file with
    the reconstructed positions and calibrated mass-to-charge- state ratio
    values.

    For other data collection/analysis software the data artifact which comes
    closest conceptually to AMETEK/Cameca's typical file formats.

    These are typically exported as a POS, ePOS, APT, ATO, ENV, or HDF5 file,
    which should be stored alongside this record in the research data
    management system.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-results-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="results",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-results-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-results-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-results-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-results-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstructionConfig(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="recommended",
        ),
    )

    voltage_filter_initial = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-voltage-filter-initial-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="voltage_filter_initial",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLTAGE",
        ),
    )
    voltage_filter_final = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-voltage-filter-final-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        a_nexus_field=NeXusField(
            name="voltage_filter_final",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLTAGE",
        ),
    )
    protocol_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-protocol-name-field"
        ],
        a_nexus_field=NeXusField(
            name="protocol_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["bas", "geiser", "gault", "cameca"],
            open_enum=True,
        ),
    )
    primary_element = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-primary-element-field"
        ],
        a_nexus_field=NeXusField(
            name="primary_element",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    efficiency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-efficiency-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="efficiency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )
    flight_path = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-flight-path-field"
        ],
        dimensionality="[length]",
        unit="m",
        a_nexus_field=NeXusField(
            name="flight_path",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )
    evaporation_field = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-evaporation-field-field"
        ],
        a_nexus_field=NeXusField(
            name="evaporation_field",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    image_compression = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-image-compression-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="image_compression",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    kfactor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-kfactor-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="kfactor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    shank_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-shank-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        a_nexus_field=NeXusField(
            name="shank_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANGLE",
        ),
    )
    ion_volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-ion-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        a_nexus_field=NeXusField(
            name="ion_volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLUME",
        ),
    )
    crystallographic_calibration = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-crystallographic-calibration-field"
        ],
        a_nexus_field=NeXusField(
            name="crystallographic_calibration",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-config-comment-field"
        ],
        a_nexus_field=NeXusField(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstructionNaiveDiscretization(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="naive_discretization",
            name_type="specified",
            optionality="required",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstructionNaiveDiscretizationProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDReconstructionNaiveDiscretizationData",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstructionNaiveDiscretizationProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDReconstructionNaiveDiscretizationData(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-intensity-field"
        ],
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-z-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_z",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_z__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-z-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_z",
        ),
    )
    axis_z__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-z-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_z",
        ),
    )
    axis_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-y-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_y__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-y-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_y",
        ),
    )
    axis_y__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-y-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_y",
        ),
    )
    axis_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-x-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_x__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-x-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_x",
        ),
    )
    axis_x__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-reconstruction-naive-discretization-data-axis-x-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_x",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRanging(ApmRanging):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_ranging",
            name="ranging",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )
    mass_to_charge_distribution = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingMassToChargeDistribution",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="mass_to_charge_distribution",
            name_type="specified",
            optionality="recommended",
        ),
    )
    background_quantification = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingBackgroundQuantification",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="background_quantification",
            name_type="specified",
            optionality="recommended",
        ),
    )
    peak_search = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakSearch",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="peak_search",
            name_type="specified",
            optionality="recommended",
        ),
    )
    peak_identification = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakIdentification",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="peak_identification",
            name_type="specified",
            optionality="recommended",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingSource(Note):
    """
    The respective ranging definitions file RNG/RRNG/ENV/HDF5.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-source-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-source-file-name-field"
        ],
        a_nexus_field=NeXusField(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    checksum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-source-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-source-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingMassToChargeDistribution(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="mass_to_charge_distribution",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingMassToChargeDistributionProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    mass_spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingMassToChargeDistributionMassSpectrum",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="mass_spectrum",
            name_type="specified",
            optionality="required",
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    min_mass_to_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-min-mass-to-charge-field"
        ],
        a_nexus_field=NeXusField(
            name="min_mass_to_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    max_mass_to_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-max-mass-to-charge-field"
        ],
        a_nexus_field=NeXusField(
            name="max_mass_to_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    n_mass_to_charge = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-n-mass-to-charge-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="n_mass_to_charge",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingMassToChargeDistributionProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingMassToChargeDistributionMassSpectrum(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="mass_spectrum",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-axisname-indices-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-intensity-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="intensity",
        ),
    )
    axis_mass_to_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-axis-mass-to-charge-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_mass_to_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_mass_to_charge__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-axis-mass-to-charge-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_mass_to_charge",
        ),
    )
    axis_mass_to_charge__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-mass-to-charge-distribution-mass-spectrum-axis-mass-to-charge-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="axis_mass_to_charge",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingBackgroundQuantification(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="background_quantification",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingBackgroundQuantificationProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    background = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-background-field"
        ],
        description=(
            "(Out-of-sync, time-independent) background levels in ppm/ns "
            "reported by e.g. APSuite/IVAS for LEAP systems."
        ),
        a_nexus_field=NeXusField(
            name="background",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    mrp_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-mrp-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "The mass-resolving power (MRP) value `D. Larson et al. "
            "<https://doi.org/10.1007/978-1-4614-8721-0>`_ report Eq. D.8 in "
            "page 282: :math:`MRP = \\frac{1}{2\\delta t} \\cdot "
            "\\sqrt{\\frac{m}{n}\\frac{1}{2eV}L}`, with :math:`\\delta t` "
            "representing the timing imprecision, :math:`\\frac{m}{n}` the "
            "mass-to-charge state ratio, :math:`e` the elementary charge, "
            ":math:`V` the potential difference, and :math:`L` the flight path "
            "length. Timing imprecision is caused by variations of flight path "
            "length and voltage, the fact that the precision of electronics is "
            "finite and a spread of the time-of-departure of individual ions is "
            "observed."
        ),
        a_nexus_field=NeXusField(
            name="mrp_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )
    mrp_mass_to_charge = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-mrp-mass-to-charge-field"
        ],
        description=(
            "Mass-to-charge state ratio :math:`\\frac{m}{n}` at which mrp_value "
            "was specified."
        ),
        a_nexus_field=NeXusField(
            name="mrp_mass_to_charge",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    mrp_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-mrp-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=(
            "Potential difference :math:`V` at which mrp_value was specified."
        ),
        a_nexus_field=NeXusField(
            name="mrp_voltage",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLTAGE",
        ),
    )
    mrp_flight_path_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-mrp-flight-path-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Flight path length :math:`L` at which mrp_value was specified."),
        a_nexus_field=NeXusField(
            name="mrp_flight_path_length",
            type="NX_FLOAT",
            name_type="specified",
            optionality="recommended",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingBackgroundQuantificationProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-background-quantification-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakSearch(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="peak_search",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakSearchProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    peakID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakSearchPeakID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="peakID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakSearchProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakSearchPeakID(Peak):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-peakid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="peakID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-peakid-label-field"
        ],
        a_nexus_field=NeXusField(
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-peakid-description-field"
        ],
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    category = Quantity(
        type=MEnum(["0", "1", "2", "3", "4", "5"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-peakid-category-field"
        ],
        description=(
            "Category for the peak offering a qualitative statement of the "
            "location of the peak in light of limited mass-resolving power that "
            "is relevant for composition quantification. See `D. Larson et al. "
            "(p172) <https://doi.org/10.1007/978-1-4614-8721-0>`_ for examples "
            "of each category: * 0, well-separated, :math:`^{10}B^{+}`, "
            ":math:`^{28}Si^{2+}` * 1, close, but can be sufficiently separated "
            "for quantification in a LEAP system, :math:`^{94}Mo^{3+}`, "
            ":math:`^{63}Cu^{2+}` * 2, closely overlapping, demands better than "
            "LEAP4000X MRP can provide :math:`^{14}N^{+}`, :math:`^{28}Si^{2+}` "
            "at different charge states * 3, overlapped exactly due to "
            "multi-charge molecular species, :math:`^{16}{O_{2}}^{2+}`, "
            ":math:`^{16}O^{+}` * 4, overlapped, same charge state, cannot as of "
            "2013 be discriminated with a LEAP4000X, :math:`^{14}{N_{2}}^{+}`, "
            ":math:`^{28}Si^{+}` * 5, overlapped, same charge state, any "
            "expectation of resolvability, :math:`^{54}Cr^{2+}`, "
            ":math:`^{54}Fe^{2+}`"
        ),
        a_nexus_field=NeXusField(
            name="category",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["0", "1", "2", "3", "4", "5"],
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-search-peakid-position-field"
        ],
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakIdentification(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="peak_identification",
            name_type="specified",
            optionality="recommended",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakIdentificationProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    ionID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakIdentificationIonID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name="ionID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=256,
        ),
    )

    sequence_index = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-sequence-index-field"
        ],
        a_nexus_field=NeXusField(
            name="sequence_index",
            type="NX_POSINT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_ion_types = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-number-of-ion-types-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_ion_types",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    maximum_number_of_atoms_per_molecular_ion = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-maximum-number-of-atoms-per-molecular-ion-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="maximum_number_of_atoms_per_molecular_ion",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    iontypes = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-iontypes-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The iontype identifier for each ion that was best matching; stored "
            "in the order of the evaporation_id. The value zero is reserved for "
            "documenting that an ion was unranged. Identifier for ranged ions "
            "need to start at 1 up to number_of_ion_types."
        ),
        a_nexus_field=NeXusField(
            name="iontypes",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakIdentificationProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-programid-program-field"
        ],
        a_nexus_field=NeXusField(
            name="program",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    program__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakIdentificationIonID(Atom):
    """
    Ions that were ranged.

    The value zero is reserved for documenting that an ion was unranged.
    Identifier for ranged ions need to start at 1 up to number_of_ion_types.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXatom",
            name="ionID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
            max_occurs=256,
        ),
    )

    charge_state_analysis = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakIdentificationIonIDChargeStateAnalysis",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_charge_state_analysis",
            name="charge_state_analysis",
            name_type="specified",
            optionality="optional",
        ),
    )

    nuclide_hash = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-nuclide-hash-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="nuclide_hash",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    charge_state = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="charge_state",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    mass_to_charge_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-mass-to-charge-range-field"
        ],
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="mass_to_charge_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    nuclide_list = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-nuclide-list-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 2],
        a_nexus_field=NeXusField(
            name="nuclide_list",
            type="NX_UINT",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakIdentificationIonIDChargeStateAnalysis(
    ApmChargeStateAnalysis
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_charge_state_analysis",
            name="charge_state_analysis",
            name_type="specified",
            optionality="optional",
        ),
    )

    config = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.apm.ApmAtom_probeIDRangingPeakIdentificationIonIDChargeStateAnalysisConfig",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )

    charge_state = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-charge-state-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="charge_state",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    nuclide_hash = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-nuclide-hash-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="nuclide_hash",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    mass = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-mass-field"
        ],
        dimensionality="[mass]",
        unit="kilogram",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="mass",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_MASS",
        ),
    )
    natural_abundance_product = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-natural-abundance-product-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="natural_abundance_product",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    shortest_half_life = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-shortest-half-life-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="shortest_half_life",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmAtom_probeIDRangingPeakIdentificationIonIDChargeStateAnalysisConfig(
    Parameters
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="required",
        ),
    )

    nuclides = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-config-nuclides-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="nuclides",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    mass_to_charge_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-config-mass-to-charge-range-field"
        ],
        shape=[2],
        a_nexus_field=NeXusField(
            name="mass_to_charge_range",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    min_half_life = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-config-min-half-life-field"
        ],
        dimensionality="[time]",
        unit="second",
        a_nexus_field=NeXusField(
            name="min_half_life",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )
    min_abundance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-config-min-abundance-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="min_abundance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    sacrifice_isotopic_uniqueness = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXapm.html#nxapm-entry-atom-probeid-ranging-peak-identification-ionid-charge-state-analysis-config-sacrifice-isotopic-uniqueness-field"
        ],
        a_nexus_field=NeXusField(
            name="sacrifice_isotopic_uniqueness",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
