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
# Run `pynx nomad generate-metainfo --nxdl NXem` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.aberration import Aberration
from pynxtools.nomad.metainfo.base_classes.actuator import Actuator
from pynxtools.nomad.metainfo.base_classes.aperture import Aperture
from pynxtools.nomad.metainfo.base_classes.cite import Cite
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.corrector_cs import CorrectorCs
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.deflector import Deflector
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.ebeam_column import EbeamColumn
from pynxtools.nomad.metainfo.base_classes.electromagnetic_lens import (
    ElectromagneticLens,
)
from pynxtools.nomad.metainfo.base_classes.em_ebsd import EmEbsd
from pynxtools.nomad.metainfo.base_classes.em_eds import EmEds
from pynxtools.nomad.metainfo.base_classes.em_event_data import EmEventData
from pynxtools.nomad.metainfo.base_classes.em_img import EmImg
from pynxtools.nomad.metainfo.base_classes.em_instrument import EmInstrument
from pynxtools.nomad.metainfo.base_classes.em_measurement import EmMeasurement
from pynxtools.nomad.metainfo.base_classes.em_simulation import EmSimulation
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.fabrication import Fabrication
from pynxtools.nomad.metainfo.base_classes.ibeam_column import IbeamColumn
from pynxtools.nomad.metainfo.base_classes.image import Image
from pynxtools.nomad.metainfo.base_classes.manipulator import Manipulator
from pynxtools.nomad.metainfo.base_classes.microstructure import Microstructure
from pynxtools.nomad.metainfo.base_classes.microstructure_feature import (
    MicrostructureFeature,
)
from pynxtools.nomad.metainfo.base_classes.microstructure_ipf import MicrostructureIpf
from pynxtools.nomad.metainfo.base_classes.microstructure_odf import MicrostructureOdf
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.phase import Phase
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.program import Program
from pynxtools.nomad.metainfo.base_classes.project import Project
from pynxtools.nomad.metainfo.base_classes.pump import Pump
from pynxtools.nomad.metainfo.base_classes.roi_process import RoiProcess
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.scan_controller import ScanController
from pynxtools.nomad.metainfo.base_classes.source import Source
from pynxtools.nomad.metainfo.base_classes.spectrum import Spectrum
from pynxtools.nomad.metainfo.base_classes.unit_cell import UnitCell
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Em"]


class Em(Entry):
    """
    Application definition for normalized representation of electron microscopy
    research.

    This application definition is a comprehensive, general description for the
    standardization of data and metadata collected using electron microscopy.

    NXem is designed to be used for documenting experiments or computer
    simulations in which controlled electron beams are used to study
    electron-beam matter interactions, to simulate this, to explore physical
    mechanisms and phenomena, or to characterize materials.

    *The NeXus application definition NXem defines a hierarchical data model
    with ten building blocks:*

    The data model represents a tree of concepts. The tree is constructed from
    groups of concepts representing the branches surplus fields and attributes
    representing leafs.

    *NXem an introduction for typical use cases in material characterization
    and simulation:*

    Transmission electron microscopy (TEM) and Scanning Transmission Electron
    Microscopy (STEM) Scanning Electron Microscopy (SEM) Scanning Electron
    Microscopy combined a Focused-Ion Beam (SEM/FIB)

    *A deeper dive into the branches of NXem:*

    NXem is constructed from composing and specializing base classes into the
    following ten categories:

    - The field ``definition`` specifies that the data schema is NXem. In
    combination with administrative metadata such as the ``NeXus_version``
    provided by :ref:`NXroot` this specifies which version of NXem the instance
    data in a NeXus/HDF5 file are compliant with. - The fields
    ``identifier_experiment``, ``experiment_alias``, ``experiment_description``
    and the group ``userID`` provide concepts for storing organizational
    metadata that contextualize the work within the research workflow and
    humans involved in this. - The fields ``start_time``, ``end_time`` provide
    concepts for framing a temporal context for the research. - The groups
    ``citeID``, ``noteID`` provide concepts for adding contextual details such
    as citations that are associated with or notes, i.e. other artifacts that
    are deemed relevant when reporting about a measurement or simulation. These
    groups are useful when NXem is used as a serialization format for
    technology-partner-agnostic archival of data and metadata that have been
    collected during a session with an electron microscope or when a simulation
    was performed. - The group ``sampleID`` provides concepts for storing
    metadata about the sample that was characterized or simulated during the
    session. - The group ``measurement`` provides concepts that are useful for
    describing a measurement during a session with an electron microscope. This
    includes the chain of events of data and metadata that were collected
    during such a session. - The group``simulation`` provides concepts that are
    useful for describing a simulation of an electron beam that interacts with
    matter. Combined with ``measurement`` this provides a data schema for
    defining a digital twin of the microscope and its optical setup. - The
    groups ``consistent_rotations``, ``NAMED_reference_frame`` provide concepts
    for reporting coordinate systems (frames of reference) and rotation
    conventions that clarify how data should be interpreted specifying the
    rotation of orientable objects in the microscope, its components, or of
    crystals and crystal defects in the material analyzed. These metadata
    support interpretation for downstream or on-the-fly data analyses which
    electron microscopes typically nowadays perform during a session. Examples
    are the indexing of diffraction patterns, image analysis in general, or
    analyses of the chemical composition. - The group ``roiID`` provides
    concepts for reporting several domain- and technique-specific configuration
    parameter and results of data processing steps that were applied. - The
    group ``profiling`` provides concepts for reporting computational details
    such as programs and libraries used, for documenting the libraries of
    virtual environments such as those used by conda or python virtual
    environment, including details about the computing hardware used, and
    documenting capabilities for performance analyses and benchmarking of the
    software or its parts.

    *Design choices:*

    Specific details about how an electron microscope was used and eventually
    its configuration modified differ between user groups. This holds also true
    for computer simulations of electron-beam matter interaction. Different
    peer groups in different sub-domains in electron microscopy consider
    different data and metadata relevant. NXem defines constraints on the
    existence and cardinality of concepts and its concept branches but seeks to
    offer a compromise. The key design pattern followed is that most branches
    are made optional or at most recommended but their child concepts
    conditional required. Thereby, NXem can cover a variety of simple but also
    complex use cases. An example of this
    parent-optional-but-children-stronger-restricted design is the combination
    of the optional group ``measurement`` with its required child
    ``measurement/instrument``: Users which report simulations are not forced
    to document the instrument but users which have characterized a sample are
    motivated to report about the instrument. They are though not necessarily
    required to report all the details of the instruments' components because
    the design pattern is-used applied recursively.

    *Inclusive design, one schema for scanning, focused-ion beam, and
    transmission electron microscopes:*

    Contrary to many other proposals of a data schema for electron microscopy,
    NXem seeks to highlight the similarity of the three fundamental types of
    electron microscopes that are nowadays used most routinely in academia and
    industry: An electron microscope is a beamline that provides a controlled
    beam of electrons combined with eventually beams of other particles (ions)
    to investigate electron/ion(-beam) matter interaction. This design of
    per-particle-type concept branches is realized in the base classes
    ``NXebeam_column`` and ``NXibeam_column``. These provide concepts for
    reporting the technical components that are typically used for generating a
    controllable (and typically scanning) beam of particles such as electrons
    or ions.

    Focused-ion beam capabilities are modelled by adding an optional group
    ``measurement/instrument/ibeam_column``. We foresee that this design is
    beneficial also in the future when research should be documented where
    photon-electron interactions via an electron microscope are combined. The
    current proposal though does not include such a ``NXpbeam_column`` base
    class that could be used for photon-/light-beam, i.e. laser plus optical
    beam path descriptions and components.

    We acknowledge that scanning and transmission electron microscopes are
    different types of instruments that have distinct differences in the
    electron-optical setup and the components used. What remains the same from
    the perspective of an observer who monitors the experiment inside the
    electron-matter interaction volume, i.e. in, on, or close to the surface of
    the specimen is the imaginary split into an upper and a lower half-space.
    In the upper half-space a specific but eventually differently shaped
    electron beam illuminates the specimen when comparing a scanning with a
    transmission electron microscope. In the lower half-space the beam or
    particles exit the specimen or end up thermalized in thick specimens.

    *NXem distinguishes and stores instance data based on how long they remain
    unchanged:*

    ``measurement`` provides two groups ``measurement/instrument`` and
    ``measurement/eventID``. The first group is designed for storing metadata
    about the instrument which do not change over the course of the session.
    Examples are the name of the technology partner who built the microscope,
    the microscope's serial number, or the type of lenses mounted, etc. The
    second group is designed for metadata and data that are collected during
    the microscope session. For these, specializations of ``NXdata``
    specifically ``NXimage`` and ``NXspectrum`` are provided. Each
    ``measurement/eventID`` event can be time-stamped individually. Each
    instance of a group ``measurement/eventID`` contains
    ``measurement/instrument`` whose purpose is to store those specific state
    and settings of the microscope that was present during the collection of
    the event. This includes lens settings, apertures used, aberrations, and
    other components, etc. By virtue of design this reduces unnecessary
    repetition of metadata stored in the first group like is often observed in
    image-based archival formats like TIFF, PNG, etc.

    *NXem offers domain-specific classes for standardized reporting of
    method-specific configurations, data processing, and results:*

    These include ``NXem_img`` for generic and specific imaging including
    diffraction, ``NXem_eds`` for energy-dispersive X-ray spectroscopy,
    ``NXem_ebsd`` for electron backscatter diffraction, as well as
    ``NXem_eels`` for electron energy loss spectroscopy. These branches provide
    examples that proof how NeXus can be used for combining session-centric
    data storage with data processing. These examples are naturally incomplete
    but show at different levels of technical depth and breath how
    standardization can be useful even to report specifically formatted data
    representations like multi-dimensional plotting. Thereby, downstream
    processing using software for data analyses or research data management can
    take advantage of a standardized reporting rather than demanding for a zoo
    of parsers that interconvert between many representations.

    *NXem within the ecosystem of data schemata for electron microscopy:**

    We support the statement that substantially fewer standardized rather than
    many ad hoc schemata are required to facilitate the documentation and
    exchange of knowledge within electron microscopy. We tailored NXem to serve
    the materials science and materials engineering usage of electron
    microscopy to provide a complementary coverage to what OMERO has
    established for the bio- and life science usage of electron microscopy.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem",
            category="application",
        ),
    )

    profiling = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmProfiling",
        repeats=False,
        description=(
            "The configuration of the software that was used to generate this "
            "NeXus file."
        ),
    )
    citeID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmCiteID",
        repeats=True,
        variable=True,
    )
    noteID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmNoteID",
        repeats=True,
        variable=True,
        description=(
            "Collection of serialized resources associated with the experiment. "
            "Examples of such resources are files which are formatted using "
            "proprietary data models of technology partners as those generated "
            "by the control software of the microscope during the instrument "
            "session."
        ),
    )
    project = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmProject",
        repeats=False,
    )
    userID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmUserID",
        repeats=True,
        variable=True,
        description=(
            "Information about persons who performed or were involved in the "
            "microscope session or simulation run."
        ),
    )
    sampleID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmSampleID",
        repeats=True,
        variable=True,
        description=(
            "A physical entity which contains material intended to be "
            "investigated. Sample and specimen are treated as de facto synonyms. "
            "Samples can be real or virtual ones as annotated via is_simulation. "
            "The suggested best practice is to call this group sample. In those "
            "cases when multiple samples need to be grouped inside one entry, "
            "these SAMPLE groups should be named using the prefix sample "
            "followed an index starting from 1, i.e. (sample1, sample2). There "
            "are at least two strategies how to store (meta)data when one "
            "analyzes multiple samples - not different ROIs on a single sample "
            "though - in one session. One strategy is to store each sample and "
            "its results under an own NXem/ENTRY. This is one of the most "
            "frequent use cases as during most sessions typically only a single "
            "sample is investigated. In this case the name of this group should "
            "be sample. If multiple samples are investigated storing each of "
            "them in their own ENTRY group eventually will demand unnecessary "
            "duplication of instrument details. This can be avoided by using "
            "another strategy for storing samples and their results. Namely, by "
            "using only one instance of NXem/ENTRY. That NXem/ENTRY should then "
            "be named, like in the previous case, NXem/entry1 and the samples "
            "should be named sample1, sample2, etc., i.e. instances should use "
            "sample as a name prefix. In this case the collection of events "
            "should use identifier_sample to state clearly for which of the "
            "samples loaded the (characterization) event was detected. This "
            "concept is related to term `Specimen`_ of the EMglossary standard. "
            ".. _Specimen: https://purls.helmholtz-metadaten.de/emg/EMG_00000046"
        ),
    )
    consistent_rotations = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmConsistentRotations",
        repeats=False,
        description=(
            "The conventions used when reporting crystal orientations. We follow "
            "the best practices of the Material Science community that are "
            "defined in reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_."
        ),
    )
    NAMED_reference_frameID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmNAMED_reference_frameID",
        repeats=True,
        variable=True,
    )
    processing_reference_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmProcessingReferenceFrame",
        repeats=False,
    )
    sample_reference_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmSampleReferenceFrame",
        repeats=False,
    )
    detector_reference_frameID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmDetector_reference_frameID",
        repeats=True,
        variable=True,
        description=("The reference frame that is defined by a specific detector."),
    )
    measurement = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurement",
        repeats=False,
    )
    simulation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmSimulation",
        repeats=False,
        description=(
            "Documentation for a simulation of electron beam-matter interaction."
        ),
    )
    roiID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiID",
        repeats=True,
        variable=True,
        description=(
            "This concept is related to term `Region Of Interest`_ of the "
            "EMglossary standard. .. _Region Of Interest: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000042"
        ),
    )

    definition = Quantity(
        type=MEnum(["NXem"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-definition-field"
        ],
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXem"],
        ),
    )
    identifier_experiment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-identifier-experiment-field"
        ],
        description=(
            "A (globally) unique persistent identifier for referring to this "
            "experiment."
        ),
        a_nexus_field=NeXusField(
            name="identifier_experiment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    experiment_alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-experiment-alias-field"
        ],
        description=(
            "Alias (short name) which scientists can use to refer to this experiment."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-experiment-description-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the microscope session started. If the application "
            "demands that time codes in this section of the application "
            "definition should only be used for specifying when the experiment "
            "was performed - and the exact duration is not relevant - use this "
            "start_time field. Often though it is useful to specify a time "
            "interval via setting both a start_time and an end_time because this "
            "enables software tools and users to collect a more detailed "
            "bookkeeping of the experiment. Users should be aware though that "
            "even using only start_time and end_time may not be sufficient to "
            "infer how long the experiment took or for how long data were "
            "acquired. To bookkeep more fine-grained timestamps over the course "
            "of the experiment is possible with start_time and end_time fields "
            "of respective :ref:`NXem_event_data` instances."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-end-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC included when "
            "the microscope session ended. See docstring of the start_time field "
            "to see how to use the start_time and end_time together."
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


class EmProfiling(CsProfiling):
    """
    The configuration of the software that was used to generate this NeXus
    file.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-profiling-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcs_profiling",
            name="profiling",
            name_type="specified",
            optionality="optional",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmProfilingProgramID",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmProfilingProgramID(Program):
    """
    A collection of all programs and libraries used to generate this NeXus
    file. Ideally, this would enable a binary recreation from the input data.

    Examples include the name and version of the libraries used to write the
    instance. Ideally, the software which writes these NXprogram instances also
    includes the version of the set of NeXus classes i.e. the specific set of
    base classes, application definitions, and contributed definitions with
    which the here described concepts can be resolved.

    For the `pynxtools library <https://github.com/FAIRmat-NFDI/pynxtools>`_
    which is used by the `NOMAD <https://nomad-lab.eu/nomad-lab>`_ research
    data management system, it makes sense to store e.g. the GitHub repository
    commit and respective submodule references used.

    Instances can also be used to document the modules and libraries that are
    offered by the computational environment such as those parsed from conda or
    python virtualenv environments.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-profiling-programid-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-profiling-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-profiling-programid-program-version-attribute"
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


class EmCiteID(Cite):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-citeid-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-citeid-author-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-citeid-doi-field"
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


class EmNoteID(Note):
    """
    Collection of serialized resources associated with the experiment. Examples
    of such resources are files which are formatted using proprietary data
    models of technology partners as those generated by the control software of
    the microscope during the instrument session.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-noteid-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-noteid-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-noteid-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-noteid-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-noteid-algorithm-field"
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


class EmProject(Project):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-project-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-project-name-field"
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


class EmUserID(User):
    """
    Information about persons who performed or were involved in the microscope
    session or simulation run.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-userid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name="userID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    identifierNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-userid-identifiername-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-userid-identifiername-type-attribute"
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


class EmSampleID(Sample):
    """
    A physical entity which contains material intended to be investigated.
    Sample and specimen are treated as de facto synonyms. Samples can be real
    or virtual ones as annotated via is_simulation.

    The suggested best practice is to call this group sample. In those cases
    when multiple samples need to be grouped inside one entry, these SAMPLE
    groups should be named using the prefix sample followed an index starting
    from 1, i.e. (sample1, sample2).

    There are at least two strategies how to store (meta)data when one analyzes
    multiple samples - not different ROIs on a single sample though - in one
    session.

    One strategy is to store each sample and its results under an own
    NXem/ENTRY. This is one of the most frequent use cases as during most
    sessions typically only a single sample is investigated. In this case the
    name of this group should be sample.

    If multiple samples are investigated storing each of them in their own
    ENTRY group eventually will demand unnecessary duplication of instrument
    details.

    This can be avoided by using another strategy for storing samples and their
    results. Namely, by using only one instance of NXem/ENTRY. That NXem/ENTRY
    should then be named, like in the previous case, NXem/entry1 and the
    samples should be named sample1, sample2, etc., i.e. instances should use
    sample as a name prefix.

    In this case the collection of events should use identifier_sample to state
    clearly for which of the samples loaded the (characterization) event was
    detected.

    This concept is related to term `Specimen`_ of the EMglossary standard.

    .. _Specimen: https://purls.helmholtz-metadaten.de/emg/EMG_00000046
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sampleID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    is_simulation = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-is-simulation-field"
        ],
        description=(
            "Qualifier whether the sample is a real (in which case is_simulation "
            "should be set to false) or a virtual one (in which case "
            "is_simulation should be set to true)."
        ),
        a_nexus_field=NeXusField(
            name="is_simulation",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    physical_form = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-physical-form-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_form",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["bulk", "foil", "thin_film", "powder"],
            open_enum=True,
        ),
    )
    identifier_sample = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-identifier-sample-field"
        ],
        description=(
            "Ideally, (globally) unique persistent identifier which "
            "distinguishes this sample from all others and especially the "
            "predecessor/origin from where that sample was cut off. An example "
            "of cutting off is a steel sheet that is the parent sample from "
            "which a small portion was wire-eroded that represents the sample "
            "that was then prepared for characterization with an electron "
            "microscope. The terms sample and specimen are here considered as "
            "exact synonyms. This field must not be used for an alias for the "
            "sample name. Instead, use name. In cases where multiple specimens "
            "were loaded into the microscope, the identifier has to resolve the "
            "specific sample, whose results are stored by this :ref:`NXentry` "
            "instance, because a single NXentry should be used for the "
            "characterization of a single specimen. Details about the specimen "
            "preparation should be stored in resources referring to "
            "identifier_parent."
        ),
        a_nexus_field=NeXusField(
            name="identifier_sample",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier_sample__type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-identifier-sample-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="identifier_sample",
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
    identifier_parent = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-identifier-parent-field"
        ],
        description=(
            "Identifier of the sample from which the sample was cut off or the "
            "string *None*. I.e. the parent to this sample. The purpose of this "
            "field is to support functionalities for tracking sample provenance "
            "in a research data management system."
        ),
        a_nexus_field=NeXusField(
            name="identifier_parent",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier_parent__type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-identifier-parent-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="identifier_parent",
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
    preparation_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-preparation-date-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "when the specimen was prepared. Ideally, report the end of the "
            "preparation, i.e. the last known timestamp when the measured "
            "specimen surface was actively prepared. Ideally, this matches the "
            "last timestamp that is mentioned in the digital resource pointed to "
            "by identifier_parent. Knowing when the specimen was exposed to e.g. "
            "specific atmosphere is especially required for material that is "
            "sensitive to the environment such as specimens that were charged "
            "with fast diffusing elements or short-lived radioactive tracers. "
            "Additional time stamps prior to preparation_date are better placed "
            "in resources which describe but do not pollute the description here "
            "with prose. Resolving these connected metadata is considered the "
            "responsibility of the research data management system and not the a "
            "NeXus file."
        ),
        a_nexus_field=NeXusField(
            name="preparation_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-name-field"
        ],
        description=("Specimen name"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-atom-types-field"
        ],
        description=(
            "List of comma-separated elements from the periodic table that are "
            "contained in the sample. If the sample substance has multiple "
            "components, all elements from each component must be included in "
            "atom_types. The purpose of the field is to offer research data "
            "management systems an opportunity to parse the relevant elements "
            "without having to interpret these from the resources pointed to by "
            "identifier_parent or walk through eventually deeply nested groups "
            "in individual data instances."
        ),
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-thickness-field"
        ],
        dimensionality="[length]",
        description=(
            "(Measured) sample thickness. The information is recorded to qualify "
            "if the beam used was likely able to shine through the specimen. For "
            "scanning electron microscopy, in many cases the specimen is "
            "typically thicker than what is illuminable by the electron beam. In "
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
    density = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sampleid-density-field"
        ],
        description=(
            "(Measured) density of the specimen. For multi-layered specimens "
            "this field should only be used to describe the density of the "
            "excited volume. For scanning electron microscopy the usage of this "
            "field is discouraged and instead an instance of a "
            "region-of-interest connected to individual :ref:`NXem_event_data` "
            "instances can provide a cleaner description of the relevant "
            "details."
        ),
        a_nexus_field=NeXusField(
            name="density",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmConsistentRotations(Parameters):
    """
    The conventions used when reporting crystal orientations. We follow the
    best practices of the Material Science community that are defined in
    reference `<https://doi.org/10.1088/0965-0393/23/8/083501>`_.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-consistent-rotations-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-consistent-rotations-rotation-handedness-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-consistent-rotations-rotation-convention-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-consistent-rotations-euler-angle-convention-field"
        ],
        description=(
            "How are Euler angles interpreted given that there are several "
            "choices (e.g. zxz, xyz) according to convention 4 of reference "
            "`<https://doi.org/10.1088/0965-0393/23/8/083501>`_. The most "
            "frequently used convention in Materials Science is zxz, which is "
            "based on the work of H.-J. Bunge but using other conventions is "
            "possible. Proper Euler angles are distinguished from (improper) "
            "Tait-Bryan angles."
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-consistent-rotations-axis-angle-convention-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-consistent-rotations-sign-convention-field"
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


class EmNAMED_reference_frameID(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="NAMED_reference_frameID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-alias-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-origin-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-x-field"
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
    x_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-x-direction-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-y-field"
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
    y_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-y-direction-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-z-field"
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
    z_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-named-reference-frameid-z-direction-field"
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


class EmProcessingReferenceFrame(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="processing_reference_frame",
            name_type="specified",
            optionality="recommended",
        ),
    )

    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-alias-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-origin-field"
        ],
        description=(
            "Location of the origin of the processing_reference_frame. It is "
            "assumed that regions-of-interest in this reference frame form a "
            "rectangle or cuboid. Edges are interpreted by inspecting the "
            "direction of their outer unit normals (which point either parallel "
            "or antiparallel) along respective base vector direction of the "
            "reference frame. If any of these assumptions is not met, the user "
            "is required to explicitly state this."
        ),
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "front_top_left",
                "front_top_right",
                "front_bottom_right",
                "front_bottom_left",
                "back_top_left",
                "back_top_right",
                "back_bottom_right",
                "back_bottom_left",
            ],
            open_enum=True,
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-x-field"
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
    x_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-x-direction-field"
        ],
        description=(
            "Direction of the positively pointing x-axis base vector of the "
            "processing_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-y-field"
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
    y_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-y-direction-field"
        ],
        description=(
            "Direction of the positively pointing y-axis base vector of the "
            "processing_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-z-field"
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
    z_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-processing-reference-frame-z-direction-field"
        ],
        description=(
            "Direction of the positively pointing z-axis base vector of the "
            "processing_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmSampleReferenceFrame(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="sample_reference_frame",
            name_type="specified",
            optionality="recommended",
        ),
    )

    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-alias-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-origin-field"
        ],
        description=(
            "Location of the origin of the sample_reference_frame. It is assumed "
            "that regions-of-interest in this reference frame form a rectangle "
            "or cuboid. Edges are interpreted by inspecting the direction of "
            "their outer unit normals (which point either parallel or "
            "antiparallel) along respective base vector direction of the "
            "reference frame. If any of these assumptions is not met, the user "
            "is required to explicitly state this."
        ),
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "front_top_left",
                "front_top_right",
                "front_bottom_right",
                "front_bottom_left",
                "back_top_left",
                "back_top_right",
                "back_bottom_right",
                "back_bottom_left",
            ],
            open_enum=True,
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-x-field"
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
    x_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-x-direction-field"
        ],
        description=(
            "Direction of the positively pointing x-axis base vector of the "
            "sample_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-y-field"
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
    y_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-y-direction-field"
        ],
        description=(
            "Direction of the positively pointing y-axis base vector of the "
            "sample_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-z-field"
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
    z_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-sample-reference-frame-z-direction-field"
        ],
        description=(
            "Direction of the positively pointing z-axis base vector of the "
            "sample_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmDetector_reference_frameID(CoordinateSystem):
    """
    The reference frame that is defined by a specific detector.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="detector_reference_frameID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-alias-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-origin-field"
        ],
        description=(
            "Location of the origin of the detector_reference_frame. If the "
            "regions-of-interest forms a rectangle or cuboid, it is assumed that "
            "edges are interpreted by inspecting the direction of their outer "
            "unit normals (which point either parallel or antiparallel) along "
            "respective base vector direction of the reference frame. If any of "
            "these assumptions is not met, the user is required to explicitly "
            "state this."
        ),
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=[
                "front_top_left",
                "front_top_right",
                "front_bottom_right",
                "front_bottom_left",
                "back_top_left",
                "back_top_right",
                "back_bottom_right",
                "back_bottom_left",
            ],
            open_enum=True,
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-x-field"
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
    x_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-x-direction-field"
        ],
        description=(
            "Direction of the positively pointing x-axis base vector of the "
            "detector_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-y-field"
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
    y_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-y-direction-field"
        ],
        description=(
            "Direction of the positively pointing y-axis base vector of the "
            "detector_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-z-field"
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
    z_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-detector-reference-frameid-z-direction-field"
        ],
        description=(
            "Direction of the positively pointing z-axis base vector of the "
            "detector_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurement(EmMeasurement):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXem_measurement",
            name="measurement",
            name_type="specified",
            optionality="optional",
        ),
    )

    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrument",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_instrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )
    eventID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_event_data",
            name="eventID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrument(EmInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXem_instrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="required",
        ),
    )
    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )
    ebeam_column = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumn",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXebeam_column",
            name="ebeam_column",
            name_type="specified",
            optionality="required",
        ),
    )
    ibeam_column = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumn",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXibeam_column",
            name="ibeam_column",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    detectorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentDetectorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    gas_injector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentGasInjector",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="gas_injector",
            name_type="specified",
            optionality="optional",
        ),
    )
    stageID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentStageID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stageID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    nanoprobeID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentNanoprobeID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="nanoprobeID",
            name_type="partial",
            optionality="optional",
        ),
    )
    pumpID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentPumpID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="pumpID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    sensorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sensorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    actuatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    location = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-location-field"
        ],
        a_nexus_field=NeXusField(
            name="location",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-fabrication-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="required",
        ),
    )

    vendor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentProgramID(Program):
    """
    Details about the control program used for operating the microscope.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-programid-program-version-attribute"
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


class EmEmMeasurementInstrumentEbeamColumn(EbeamColumn):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXebeam_column",
            name="ebeam_column",
            name_type="specified",
            optionality="required",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )
    electron_source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnElectronSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="electron_source",
            name_type="specified",
            optionality="recommended",
        ),
    )
    lensID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnLensID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    apertureID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnApertureID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    deflectorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnDeflectorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="deflectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    blankerID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnBlankerID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="blankerID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    monochromatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnMonochromatorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    corrector_csID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnCorrector_csID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcorrector_cs",
            name="corrector_csID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    corrector_ax = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnCorrectorAx",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="corrector_ax",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )
    biprismID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnBiprismID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="biprismID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    phaseplateID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnPhaseplateID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="phaseplateID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    sensorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sensorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    actuatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    beamID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beamID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    scan_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnScanController",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentEbeamColumnFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnElectronSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-electron-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="electron_source",
            name_type="specified",
            optionality="recommended",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnElectronSourceFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    emitter_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-electron-source-emitter-type-field"
        ],
        a_nexus_field=NeXusField(
            name="emitter_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    probe = Quantity(
        type=MEnum(["electron"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-electron-source-probe-field"
        ],
        a_nexus_field=NeXusField(
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["electron"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentEbeamColumnElectronSourceFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-electron-source-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-electron-source-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-electron-source-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-electron-source-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnLensID(ElectromagneticLens):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-lensid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnLensIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-lensid-name-field"
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


class EmEmMeasurementInstrumentEbeamColumnLensIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-lensid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-lensid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-lensid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-lensid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnApertureID(Aperture):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-apertureid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnApertureIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-apertureid-name-field"
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


class EmEmMeasurementInstrumentEbeamColumnApertureIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-apertureid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-apertureid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-apertureid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-apertureid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnDeflectorID(Deflector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-deflectorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="deflectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnDeflectorIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-deflectorid-name-field"
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


class EmEmMeasurementInstrumentEbeamColumnDeflectorIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-deflectorid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-deflectorid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-deflectorid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-deflectorid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnBlankerID(Deflector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-blankerid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="blankerID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnBlankerIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-blankerid-name-field"
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


class EmEmMeasurementInstrumentEbeamColumnBlankerIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-blankerid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-blankerid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-blankerid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-blankerid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnMonochromatorID(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-monochromatorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnMonochromatorIDFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(
            [
                "wien",
                "alfa",
                "omega",
                "castaing_henry",
                "gatan_imaging",
                "sector_analyzer",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-monochromatorid-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "wien",
                "alfa",
                "omega",
                "castaing_henry",
                "gatan_imaging",
                "sector_analyzer",
            ],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentEbeamColumnMonochromatorIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-monochromatorid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-monochromatorid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-monochromatorid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-monochromatorid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnCorrector_csID(CorrectorCs):
    """
    A spherical aberration corrector is a typical component in a transmission
    electron microscope. Many instruments have only one, in this case the
    variadic suffix should be dropped. If there are multiple instances these
    should be numbered starting from 1, i.e. corrector_cs1, corrector_cs2.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-csid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcorrector_cs",
            name="corrector_csID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnCorrector_csIDFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-csid-name-field"
        ],
        description=("Use specifically when there are multiple instances."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentEbeamColumnCorrector_csIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-csid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-csid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-csid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-csid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnCorrectorAx(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-ax-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="corrector_ax",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnCorrectorAxFabrication",
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


class EmEmMeasurementInstrumentEbeamColumnCorrectorAxFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-ax-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-ax-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-ax-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-corrector-ax-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnBiprismID(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-biprismid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="biprismID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnBiprismIDFabrication",
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


class EmEmMeasurementInstrumentEbeamColumnBiprismIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-biprismid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-biprismid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-biprismid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-biprismid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnPhaseplateID(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-phaseplateid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="phaseplateID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnPhaseplateIDFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-phaseplateid-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["thin_film", "electrostatic"],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentEbeamColumnPhaseplateIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-phaseplateid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-phaseplateid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-phaseplateid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-phaseplateid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentEbeamColumnScanController(ScanController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-scan-controller-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentEbeamColumnScanControllerFabrication",
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


class EmEmMeasurementInstrumentEbeamColumnScanControllerFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-scan-controller-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-scan-controller-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-scan-controller-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ebeam-column-scan-controller-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumn(IbeamColumn):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXibeam_column",
            name="ibeam_column",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
            max_occurs=1,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )
    ion_source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnIonSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="ion_source",
            name_type="specified",
            optionality="required",
        ),
    )
    lensID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnLensID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    apertureID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnApertureID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    deflectorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnDeflectorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="deflectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    blankerID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnBlankerID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="blankerID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    monochromatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnMonochromatorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    sensorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sensorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    actuatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    beamID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beamID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    scan_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnScanController",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentIbeamColumnFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumnIonSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-ion-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="ion_source",
            name_type="specified",
            optionality="required",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnIonSourceFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    emitter_type = Quantity(
        type=MEnum(["liquid_metal", "plasma", "gas_field", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-ion-source-emitter-type-field"
        ],
        a_nexus_field=NeXusField(
            name="emitter_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["liquid_metal", "plasma", "gas_field", "other"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentIbeamColumnIonSourceFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-ion-source-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-ion-source-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-ion-source-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-ion-source-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumnLensID(ElectromagneticLens):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-lensid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnLensIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-lensid-name-field"
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


class EmEmMeasurementInstrumentIbeamColumnLensIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-lensid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-lensid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-lensid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-lensid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumnApertureID(Aperture):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-apertureid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnApertureIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-apertureid-name-field"
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


class EmEmMeasurementInstrumentIbeamColumnApertureIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-apertureid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-apertureid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-apertureid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-apertureid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumnDeflectorID(Deflector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-deflectorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="deflectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnDeflectorIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-deflectorid-name-field"
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


class EmEmMeasurementInstrumentIbeamColumnDeflectorIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-deflectorid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-deflectorid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-deflectorid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-deflectorid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumnBlankerID(Deflector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-blankerid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="blankerID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnBlankerIDFabrication",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-blankerid-name-field"
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


class EmEmMeasurementInstrumentIbeamColumnBlankerIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-blankerid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-blankerid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-blankerid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-blankerid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumnMonochromatorID(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-monochromatorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnMonochromatorIDFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-monochromatorid-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-monochromatorid-name-field"
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


class EmEmMeasurementInstrumentIbeamColumnMonochromatorIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-monochromatorid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-monochromatorid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-monochromatorid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-monochromatorid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentIbeamColumnScanController(ScanController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-scan-controller-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentIbeamColumnScanControllerFabrication",
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


class EmEmMeasurementInstrumentIbeamColumnScanControllerFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-scan-controller-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-scan-controller-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-scan-controller-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-ibeam-column-scan-controller-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentDetectorID(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-detectorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentDetectorIDFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-detectorid-name-field"
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


class EmEmMeasurementInstrumentDetectorIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-detectorid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-detectorid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-detectorid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-detectorid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentGasInjector(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-gas-injector-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="gas_injector",
            name_type="specified",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentGasInjectorFabrication",
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


class EmEmMeasurementInstrumentGasInjectorFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-gas-injector-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-gas-injector-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-gas-injector-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-gas-injector-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentStageID(Manipulator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-stageid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stageID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentStageIDFabrication",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name="fabrication",
            name_type="specified",
            optionality="recommended",
        ),
    )

    design = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-stageid-design-field"
        ],
        a_nexus_field=NeXusField(
            name="design",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementInstrumentStageIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-stageid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-stageid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-stageid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-stageid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentNanoprobeID(Manipulator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-nanoprobeid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="nanoprobeID",
            name_type="partial",
            optionality="optional",
        ),
    )

    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementInstrumentNanoprobeIDFabrication",
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


class EmEmMeasurementInstrumentNanoprobeIDFabrication(Fabrication):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-nanoprobeid-fabrication-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-nanoprobeid-fabrication-vendor-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-nanoprobeid-fabrication-model-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-nanoprobeid-fabrication-serial-number-field"
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


class EmEmMeasurementInstrumentPumpID(Pump):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-pumpid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="pumpID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    design = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-instrument-pumpid-design-field"
        ],
        a_nexus_field=NeXusField(
            name="design",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "membrane",
                "rotary_vane",
                "roots",
                "turbo_molecular",
                "ion",
                "cryo",
                "diffusion",
                "scroll",
            ],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventID(EmEventData):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_event_data",
            name="eventID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    imageID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="imageID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    spectrumID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspectrum",
            name="spectrumID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrument",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_instrument",
            name="instrument",
            name_type="specified",
            optionality="recommended",
        ),
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-start-time-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-end-time-field"
        ],
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
    identifier_sample = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-identifier-sample-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="identifier_sample",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageID(Image):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="imageID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDProcess",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    image_1d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDImage1d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_1d",
            name_type="specified",
            optionality="optional",
        ),
    )
    image_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDImage2d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="optional",
        ),
    )
    image_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDImage3d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_3d",
            name_type="specified",
            optionality="optional",
        ),
    )
    image_4d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDImage4d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_4d",
            name_type="specified",
            optionality="optional",
        ),
    )
    stack_1d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDStack1d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_1d",
            name_type="specified",
            optionality="optional",
        ),
    )
    stack_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDStack2d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_2d",
            name_type="specified",
            optionality="optional",
        ),
    )
    stack_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDStack3d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDProcess(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    input = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDImageIDProcessInput",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="recommended",
        ),
    )

    detector_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-detector-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="detector_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDProcessInput(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-input-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-input-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-input-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-input-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-input-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    context = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-process-input-context-field"
        ],
        a_nexus_field=NeXusField(
            name="context",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDImage1d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_1d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    real__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-real-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="real",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-imag-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="imag",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-complex-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="complex",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-1d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDImage2d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    real__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-real-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="real",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-imag-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="imag",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    magnitude = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
        ),
    )
    magnitude__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-magnitude-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="magnitude",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-axis-j-field"
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
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-2d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDImage3d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    real__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-real-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="real",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-imag-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="imag",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-complex-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="complex",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axis-k-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axis-k-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axis-j-field"
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
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-3d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDImage4d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_4d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    real__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-real-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="real",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-imag-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="imag",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-complex-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="complex",
        ),
    )
    axis_m = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-m-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_m",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_m__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-m-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_m",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-k-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-k-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-j-field"
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
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-image-4d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDStack1d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_1d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    real__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-real-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="real",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-imag-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="imag",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-complex-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="complex",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-indices-group-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_group",
        ),
    )
    indices_image = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-indices-image-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_image",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_image__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-indices-image-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_image",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-1d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDStack2d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    real__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-real-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="real",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-imag-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="imag",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-complex-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="complex",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-indices-group-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_group",
        ),
    )
    indices_image = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-indices-image-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_image",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_image__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-indices-image-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_image",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-axis-j-field"
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
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-2d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDImageIDStack3d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    real__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-real-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="real",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-imag-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="imag",
        ),
    )
    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-complex-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="complex",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-indices-group-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_group",
        ),
    )
    indices_image = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-indices-image-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_image",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_image__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-indices-image-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_image",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axis-k-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axis-k-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axis-j-field"
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
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-imageid-stack-3d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumID(Spectrum):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspectrum",
            name="spectrumID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDProcess",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )
    spectrum_0d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDSpectrum0d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_0d",
            name_type="specified",
            optionality="optional",
        ),
    )
    spectrum_1d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDSpectrum1d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_1d",
            name_type="specified",
            optionality="optional",
        ),
    )
    spectrum_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDSpectrum2d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_2d",
            name_type="specified",
            optionality="optional",
        ),
    )
    spectrum_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDSpectrum3d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_3d",
            name_type="specified",
            optionality="optional",
        ),
    )
    stack_0d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDStack0d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_0d",
            name_type="specified",
            optionality="optional",
        ),
    )
    stack_1d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDStack1d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_1d",
            name_type="specified",
            optionality="optional",
        ),
    )
    stack_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDStack2d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_2d",
            name_type="specified",
            optionality="optional",
        ),
    )
    stack_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDStack3d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDProcess(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="recommended",
        ),
    )

    input = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDSpectrumIDProcessInput",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="recommended",
        ),
    )

    detector_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-detector-identifier-field"
        ],
        a_nexus_field=NeXusField(
            name="detector_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDProcessInput(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-input-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="input",
            name_type="specified",
            optionality="recommended",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-input-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-input-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-input-checksum-field"
        ],
        a_nexus_field=NeXusField(
            name="checksum",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    algorithm = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-input-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    context = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-process-input-context-field"
        ],
        a_nexus_field=NeXusField(
            name="context",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDSpectrum0d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_0d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-0d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDSpectrum1d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_1d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-1d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDSpectrum2d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-2d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDSpectrum3d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="spectrum_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-k-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-k-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-spectrum-3d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDStack0d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_0d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    indices_spectrum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-indices-spectrum-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_spectrum",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_spectrum__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-indices-spectrum-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_spectrum",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-0d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDStack1d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_1d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-intensity-field"
        ],
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    indices_spectrum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-indices-spectrum-field"
        ],
        a_nexus_field=NeXusField(
            name="indices_spectrum",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    indices_spectrum__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-indices-spectrum-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_spectrum",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-axis-i-field"
        ],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-axis-energy-field"
        ],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-1d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDStack2d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    indices_spectrum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-indices-spectrum-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_spectrum",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_spectrum__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-indices-spectrum-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_spectrum",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-2d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDSpectrumIDStack3d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    indices_spectrum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-indices-spectrum-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="indices_spectrum",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indices_spectrum__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-indices-spectrum-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="indices_spectrum",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-k-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-k-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-j-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-i-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-spectrumid-stack-3d-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrument(EmInstrument):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXem_instrument",
            name="instrument",
            name_type="specified",
            optionality="recommended",
        ),
    )

    ebeam_column = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumn",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXebeam_column",
            name="ebeam_column",
            name_type="specified",
            optionality="required",
        ),
    )
    ibeam_column = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentIbeamColumn",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXibeam_column",
            name="ibeam_column",
            name_type="specified",
            optionality="optional",
        ),
    )
    optics = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_optical_system.EmOpticalSystem",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_optical_system",
            name="optics",
            name_type="specified",
            optionality="recommended",
        ),
    )
    detectorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentDetectorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    stageID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentStageID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stageID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    pumpID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pump.Pump",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
            name="pumpID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    sensorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sensorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    actuatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumn(EbeamColumn):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXebeam_column",
            name="ebeam_column",
            name_type="specified",
            optionality="required",
        ),
    )

    electron_source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnElectronSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="electron_source",
            name_type="specified",
            optionality="optional",
        ),
    )
    lensID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnLensID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    apertureID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnApertureID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    deflectorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="deflectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    monochromatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnMonochromatorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    corrector_csID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcorrector_cs",
            name="corrector_csID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    corrector_ax = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrectorAx",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="corrector_ax",
            name_type="specified",
            optionality="optional",
        ),
    )
    sensorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sensorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    actuatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    beamID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beamID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    scan_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnScanController",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="recommended",
        ),
    )

    operation_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-operation-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="operation_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnElectronSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-electron-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="electron_source",
            name_type="specified",
            optionality="optional",
        ),
    )

    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-electron-source-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
    )
    extraction_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-electron-source-extraction-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        a_nexus_field=NeXusField(
            name="extraction_voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    emission_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-electron-source-emission-current-field"
        ],
        dimensionality="[current]",
        a_nexus_field=NeXusField(
            name="emission_current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    filament_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-electron-source-filament-current-field"
        ],
        dimensionality="[current]",
        a_nexus_field=NeXusField(
            name="filament_current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnLensID(ElectromagneticLens):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-lensid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    power_setting = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-lensid-power-setting-field"
        ],
        a_nexus_field=NeXusField(
            name="power_setting",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnApertureID(Aperture):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-apertureid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    setting = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-apertureid-setting-field"
        ],
        description=(
            "Descriptor for the aperture setting when the exact technical "
            "details are unknown or not directly controllable as the control "
            "software of the microscope does not enable or was not configured to "
            "display these values for users."
        ),
        a_nexus_field=NeXusField(
            name="setting",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnMonochromatorID(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-monochromatorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-monochromatorid-applied-field"
        ],
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    dispersion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-monochromatorid-dispersion-field"
        ],
        a_nexus_field=NeXusField(
            name="dispersion",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_ANY",
        ),
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-monochromatorid-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csID(CorrectorCs):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcorrector_cs",
            name="corrector_csID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    tableauID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="tableauID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-applied-field"
        ],
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauID(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="tableauID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    c_1 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC1",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_1 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA1",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_1",
            name_type="specified",
            optionality="optional",
        ),
    )
    b_2 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDB2",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="b_2",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_2 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA2",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_2",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC3",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3",
            name_type="specified",
            optionality="optional",
        ),
    )
    s_3 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDS3",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="s_3",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_3 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA3",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_3",
            name_type="specified",
            optionality="optional",
        ),
    )
    b_4 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDB4",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="b_4",
            name_type="specified",
            optionality="optional",
        ),
    )
    d_4 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDD4",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="d_4",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_4 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA4",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_4",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC5",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5",
            name_type="specified",
            optionality="optional",
        ),
    )
    s_5 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDS5",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="s_5",
            name_type="specified",
            optionality="optional",
        ),
    )
    r_5 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDR5",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="r_5",
            name_type="specified",
            optionality="optional",
        ),
    )
    a_6 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA6",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_6",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_1_0 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC10",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_0",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_1_2_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC12A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_1_2_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC12B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_1_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC21A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_1_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_1_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC21B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_1_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_3_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC23A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_3_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_2_3_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC23B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_3_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_0 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC30",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_0",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_2_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC32A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_2_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC32B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_4_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC34A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_4_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_3_4_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC34B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_4_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_1_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC41A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_1_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_1_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC41B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_1_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_3_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC43A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_3_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_3_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC43B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_3_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_5_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC45A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_5_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_4_5_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC45B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_5_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_0 = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC50",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_0",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_2_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC52A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_2_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC52B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_4_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC54A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_4_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_4_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC54B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_4_b",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_6_a = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC56A",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_6_a",
            name_type="specified",
            optionality="optional",
        ),
    )
    c_5_6_b = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC56B",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_6_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC1(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA1(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-1-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_1",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-1-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDB2(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-b-2-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="b_2",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-b-2-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA2(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-2-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_2",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-2-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC3(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDS3(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-s-3-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="s_3",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-s-3-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA3(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-3-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_3",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-3-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDB4(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-b-4-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="b_4",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-b-4-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDD4(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-d-4-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="d_4",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-d-4-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA4(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-4-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_4",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-4-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC5(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDS5(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-s-5-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="s_5",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-s-5-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDR5(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-r-5-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="r_5",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-r-5-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDA6(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-6-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="a_6",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-a-6-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC10(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-0-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_0",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-0-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC12A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-2-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-2-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC12B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-2-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_1_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-1-2-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC21A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-1-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_1_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-1-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC21B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-1-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_1_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-1-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC23A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-3-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_3_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-3-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC23B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-3-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_2_3_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-2-3-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC30(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-0-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_0",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-0-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC32A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-2-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-2-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC32B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-2-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-2-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC34A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-4-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_4_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-4-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC34B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-4-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_3_4_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-3-4-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC41A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-1-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_1_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-1-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC41B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-1-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_1_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-1-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC43A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-3-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_3_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-3-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC43B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-3-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_3_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-3-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC45A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-5-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_5_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-5-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC45B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-5-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_4_5_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-4-5-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC50(Aberration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-0-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_0",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-0-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC52A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-2-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_2_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-2-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC52B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-2-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_2_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-2-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC54A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-4-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_4_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-4-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC54B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-4-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_4_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-4-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC56A(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-6-a-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_6_a",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-6-a-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrector_csIDTableauIDC56B(
    Aberration
):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-6-b-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXaberration",
            name="c_5_6_b",
            name_type="specified",
            optionality="optional",
        ),
    )

    magnitude = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-csid-tableauid-c-5-6-b-magnitude-field"
        ],
        a_nexus_field=NeXusField(
            name="magnitude",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnCorrectorAx(Component):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-ax-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="corrector_ax",
            name_type="specified",
            optionality="optional",
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-ax-applied-field"
        ],
        a_nexus_field=NeXusField(
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
        ),
    )
    value_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-ax-value-x-field"
        ],
        a_nexus_field=NeXusField(
            name="value_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    value_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-corrector-ax-value-y-field"
        ],
        a_nexus_field=NeXusField(
            name="value_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentEbeamColumnScanController(ScanController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-scan-controller-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="recommended",
        ),
    )

    scan_schema = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-scan-controller-scan-schema-field"
        ],
        a_nexus_field=NeXusField(
            name="scan_schema",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    dwell_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ebeam-column-scan-controller-dwell-time-field"
        ],
        dimensionality="[time]",
        a_nexus_field=NeXusField(
            name="dwell_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentIbeamColumn(IbeamColumn):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXibeam_column",
            name="ibeam_column",
            name_type="specified",
            optionality="optional",
        ),
    )

    ion_source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentIbeamColumnIonSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="ion_source",
            name_type="specified",
            optionality="required",
        ),
    )
    lensID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentIbeamColumnLensID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    apertureID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentIbeamColumnApertureID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    deflectorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="deflectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    monochromatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentIbeamColumnMonochromatorID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    sensorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name="sensorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    actuatorID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="actuatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    beamID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name="beamID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    scan_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentIbeamColumnScanController",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="recommended",
        ),
    )

    operation_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-operation-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="operation_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentIbeamColumnIonSource(Source):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-ion-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="ion_source",
            name_type="specified",
            optionality="required",
        ),
    )

    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-ion-source-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_VOLTAGE",
        ),
    )
    flux = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-ion-source-flux-field"
        ],
        a_nexus_field=NeXusField(
            name="flux",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentIbeamColumnLensID(ElectromagneticLens):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-lensid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
            name="lensID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    power_setting = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-lensid-power-setting-field"
        ],
        a_nexus_field=NeXusField(
            name="power_setting",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentIbeamColumnApertureID(Aperture):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-apertureid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name="apertureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    setting = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-apertureid-setting-field"
        ],
        description=(
            "Descriptor for the aperture setting when the exact technical "
            "details are unknown or not directly controllable as the control "
            "software of the microscope does not enable or was not configured to "
            "display these values for users."
        ),
        a_nexus_field=NeXusField(
            name="setting",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentIbeamColumnMonochromatorID(Monochromator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-monochromatorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name="monochromatorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-monochromatorid-applied-field"
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


class EmEmMeasurementEventIDInstrumentIbeamColumnScanController(ScanController):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-scan-controller-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="recommended",
        ),
    )

    scan_schema = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-scan-controller-scan-schema-field"
        ],
        a_nexus_field=NeXusField(
            name="scan_schema",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    dwell_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-ibeam-column-scan-controller-dwell-time-field"
        ],
        dimensionality="[time]",
        a_nexus_field=NeXusField(
            name="dwell_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentDetectorID(Detector):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-detectorid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name="detectorID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    operation_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-detectorid-operation-mode-field"
        ],
        description=(
            "Operation mode of the detector as displayed by the control software."
        ),
        a_nexus_field=NeXusField(
            name="operation_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentStageID(Manipulator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stageID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    sample_heater = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmMeasurementEventIDInstrumentStageIDSampleHeater",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_heater",
            name_type="specified",
            optionality="optional",
        ),
    )

    design = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-design-field"
        ],
        a_nexus_field=NeXusField(
            name="design",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    tilt1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-tilt1-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="tilt1",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    tilt2 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-tilt2-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="tilt2",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    rotation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-rotation-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="rotation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-position-field"
        ],
        dimensionality="[length]",
        shape=[3],
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmMeasurementEventIDInstrumentStageIDSampleHeater(Actuator):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-sample-heater-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name="sample_heater",
            name_type="specified",
            optionality="optional",
        ),
    )

    physical_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-sample-heater-physical-quantity-field"
        ],
        a_nexus_field=NeXusField(
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    heater_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-sample-heater-heater-current-field"
        ],
        dimensionality="[current]",
        description=("Nominal current of the heater."),
        a_nexus_field=NeXusField(
            name="heater_current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    heater_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-sample-heater-heater-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("Nominal voltage of the heater."),
        a_nexus_field=NeXusField(
            name="heater_voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    heater_power = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-measurement-eventid-instrument-stageid-sample-heater-heater-power-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3",
        a_nexus_field=NeXusField(
            name="heater_power",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_POWER",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmSimulation(EmSimulation):
    """
    Documentation for a simulation of electron beam-matter interaction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXem_simulation",
            name="simulation",
            name_type="specified",
            optionality="optional",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmSimulationProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )
    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmSimulationEnvironment",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="optional",
        ),
    )
    results = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmSimulationResults",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="results",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEmSimulationProgramID(Program):
    """
    The program with which the simulation was performed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-programid-program-version-attribute"
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


class EmEmSimulationEnvironment(Collection):
    """
    Programs and libraries representing the computational environment
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-environment-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="environment",
            name_type="specified",
            optionality="recommended",
        ),
    )

    program = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmEmSimulationEnvironmentProgram",
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


class EmEmSimulationEnvironmentProgram(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-environment-program-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-environment-program-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-environment-program-program-version-attribute"
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


class EmEmSimulationResults(Process):
    """
    Results of the simulation
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-simulation-results-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="results",
            name_type="specified",
            optionality="optional",
        ),
    )

    image = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.Image",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.Spectrum",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspectrum",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    interaction_volumeID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_interaction_volume.EmInteractionVolume",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_interaction_volume",
            name="interaction_volumeID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiID(RoiProcess):
    """
    This concept is related to term `Region Of Interest`_ of the EMglossary
    standard.

    .. _Region Of Interest:
    https://purls.helmholtz-metadaten.de/emg/EMG_00000042
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXroi_process",
            name="roiID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    img = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDImg",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_img",
            name="img",
            name_type="specified",
            optionality="optional",
        ),
    )
    ebsd = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsd",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_ebsd",
            name="ebsd",
            name_type="specified",
            optionality="optional",
        ),
    )
    eds = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEds",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_eds",
            name="eds",
            name_type="specified",
            optionality="optional",
        ),
    )
    eels = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eels.EmEels",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_eels",
            name="eels",
            name_type="specified",
            optionality="optional",
        ),
    )
    tomo = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDTomo",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="tomo",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDImg(EmImg):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-img-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXem_img",
            name="img",
            name_type="specified",
            optionality="optional",
        ),
    )

    imageID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDImgImageID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="imageID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDImgImageID(Image):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-img-imageid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name="imageID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    microstructureID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.Microstructure",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="microstructureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    imaging_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-img-imageid-imaging-mode-field"
        ],
        a_nexus_field=NeXusField(
            name="imaging_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "secondary_electron",
                "backscattered_electron",
                "annular_dark_field",
                "cathodoluminescence",
            ],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsd(EmEbsd):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXem_ebsd",
            name="ebsd",
            name_type="specified",
            optionality="optional",
        ),
    )

    gnomonic_reference_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdGnomonicReferenceFrame",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="gnomonic_reference_frame",
            name_type="specified",
            optionality="recommended",
        ),
    )
    pattern_center = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdPatternCenter",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="pattern_center",
            name_type="specified",
            optionality="recommended",
        ),
    )
    measurement = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdMeasurement",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="measurement",
            name_type="specified",
            optionality="optional",
        ),
    )
    simulation = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdSimulation",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="simulation",
            name_type="specified",
            optionality="optional",
        ),
    )
    indexing = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexing",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdGnomonicReferenceFrame(CoordinateSystem):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="gnomonic_reference_frame",
            name_type="specified",
            optionality="recommended",
        ),
    )

    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-alias-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-type-field"
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
        type=MEnum(["in_the_pattern_center"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-origin-field"
        ],
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["in_the_pattern_center"],
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-x-field"
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
    x_direction = Quantity(
        type=MEnum(["north", "east", "south", "west", "in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-x-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-y-field"
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
    y_direction = Quantity(
        type=MEnum(["north", "east", "south", "west", "in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-y-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-z-field"
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
    z_direction = Quantity(
        type=MEnum(["north", "east", "south", "west", "in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-gnomonic-reference-frame-z-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["north", "east", "south", "west", "in", "out"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdPatternCenter(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-pattern-center-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="pattern_center",
            name_type="specified",
            optionality="recommended",
        ),
    )

    x_boundary_convention = Quantity(
        type=MEnum(["top", "right", "bottom", "left"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-pattern-center-x-boundary-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="x_boundary_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["top", "right", "bottom", "left"],
        ),
    )
    x_normalization_direction = Quantity(
        type=MEnum(["north", "east", "south", "west"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-pattern-center-x-normalization-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="x_normalization_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["north", "east", "south", "west"],
        ),
    )
    y_boundary_convention = Quantity(
        type=MEnum(["top", "right", "bottom", "left"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-pattern-center-y-boundary-convention-field"
        ],
        a_nexus_field=NeXusField(
            name="y_boundary_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["top", "right", "bottom", "left"],
        ),
    )
    y_normalization_direction = Quantity(
        type=MEnum(["north", "east", "south", "west"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-pattern-center-y-normalization-direction-field"
        ],
        a_nexus_field=NeXusField(
            name="y_normalization_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["north", "east", "south", "west"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdMeasurement(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-measurement-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="measurement",
            name_type="specified",
            optionality="optional",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdMeasurementSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-measurement-depends-on-field"
        ],
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdMeasurementSource(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-measurement-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-measurement-source-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-measurement-source-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-measurement-source-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-measurement-source-algorithm-field"
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


class EmRoiIDEbsdSimulation(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-simulation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="simulation",
            name_type="specified",
            optionality="optional",
        ),
    )

    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdSimulationSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-simulation-depends-on-field"
        ],
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdSimulationSource(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-simulation-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="required",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-simulation-source-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-simulation-source-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-simulation-source-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-simulation-source-algorithm-field"
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


class EmRoiIDEbsdIndexing(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="optional",
        ),
    )

    microstructureID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingMicrostructureID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="microstructureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingSource",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="source",
            name_type="specified",
            optionality="optional",
        ),
    )
    phaseID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXphase",
            name="phaseID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    roi = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingRoi",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="roi",
            name_type="specified",
            optionality="recommended",
        ),
    )

    number_of_scan_points = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-number-of-scan-points-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_scan_points",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    indexing_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-indexing-rate-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="indexing_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingMicrostructureID(Microstructure):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure",
            name="microstructureID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    configuration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingMicrostructureIDConfiguration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="configuration",
            name_type="specified",
            optionality="required",
        ),
    )
    grid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_grid.CgGrid",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name="grid",
            name_type="specified",
            optionality="optional",
        ),
    )
    points = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_point.CgPoint",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_point",
            name="points",
            name_type="specified",
            optionality="optional",
        ),
    )
    polylines = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyline.CgPolyline",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyline",
            name="polylines",
            name_type="specified",
            optionality="optional",
        ),
    )
    triangles = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_triangle.CgTriangle",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name="triangles",
            name_type="specified",
            optionality="optional",
        ),
    )
    polygons = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polygon.CgPolygon",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polygon",
            name="polygons",
            name_type="specified",
            optionality="optional",
        ),
    )
    polyhedra = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyhedron.CgPolyhedron",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name="polyhedra",
            name_type="specified",
            optionality="optional",
        ),
    )
    crystals = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingMicrostructureIDCrystals",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="crystals",
            name_type="specified",
            optionality="optional",
        ),
    )
    interfaces = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingMicrostructureIDInterfaces",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="interfaces",
            name_type="specified",
            optionality="optional",
        ),
    )
    triple_junctions = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingMicrostructureIDTripleJunctions",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="triple_junctions",
            name_type="specified",
            optionality="optional",
        ),
    )
    quadruple_junctions = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingMicrostructureIDQuadrupleJunctions",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="quadruple_junctions",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingMicrostructureIDConfiguration(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-configuration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="configuration",
            name_type="specified",
            optionality="required",
        ),
    )

    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingMicrostructureIDConfigurationProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-configuration-dimensionality-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
            enumeration=["1", "2", "3"],
        ),
    )
    algorithm = Quantity(
        type=MEnum(
            [
                "unknown",
                "disorientation_clustering",
                "fast_multiscale_clustering",
                "markov_chain_clustering",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-configuration-algorithm-field"
        ],
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "unknown",
                "disorientation_clustering",
                "fast_multiscale_clustering",
                "markov_chain_clustering",
            ],
        ),
    )
    disorientation_threshold = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-configuration-disorientation-threshold-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="disorientation_threshold",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingMicrostructureIDConfigurationProgramID(Program):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-configuration-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )

    mtex = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_mtex_config.MicrostructureMtexConfig",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_mtex_config",
            name="mtex",
            name_type="specified",
            optionality="optional",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-configuration-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-configuration-programid-program-version-attribute"
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


class EmRoiIDEbsdIndexingMicrostructureIDCrystals(MicrostructureFeature):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-crystals-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="crystals",
            name_type="specified",
            optionality="optional",
        ),
    )

    representation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-crystals-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_crystals = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-crystals-number-of-crystals-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_crystals",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-crystals-index-offset-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingMicrostructureIDInterfaces(MicrostructureFeature):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-interfaces-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="interfaces",
            name_type="specified",
            optionality="optional",
        ),
    )

    representation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-interfaces-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_interfaces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-interfaces-number-of-interfaces-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_interfaces",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-interfaces-index-offset-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingMicrostructureIDTripleJunctions(MicrostructureFeature):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-triple-junctions-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="triple_junctions",
            name_type="specified",
            optionality="optional",
        ),
    )

    representation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-triple-junctions-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_junctions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-triple-junctions-number-of-junctions-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_junctions",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-triple-junctions-index-offset-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingMicrostructureIDQuadrupleJunctions(MicrostructureFeature):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-quadruple-junctions-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="quadruple_junctions",
            name_type="specified",
            optionality="optional",
        ),
    )

    representation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-quadruple-junctions-representation-field"
        ],
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_junctions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-quadruple-junctions-number-of-junctions-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_junctions",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-microstructureid-quadruple-junctions-index-offset-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingSource(Note):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-source-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-source-type-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-source-file-name-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-source-checksum-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-source-algorithm-field"
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


class EmRoiIDEbsdIndexingPhaseID(Phase):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXphase",
            name="phaseID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    unit_cell = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDUnitCell",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXunit_cell",
            name="unit_cell",
            name_type="specified",
            optionality="required",
        ),
    )
    ipfID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDIpfID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_ipf",
            name="ipfID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )
    odfID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDOdfID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_odf",
            name="odfID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )
    pfID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_pf.MicrostructurePf",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_pf",
            name="pfID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-name-field"
        ],
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    number_of_scan_points = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-number-of-scan-points-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="number_of_scan_points",
            type="NX_UINT",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDUnitCell(UnitCell):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXunit_cell",
            name="unit_cell",
            name_type="specified",
            optionality="required",
        ),
    )

    a = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-a-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="a",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    b = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-b-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="b",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    c = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-c-field"
        ],
        dimensionality="[length]",
        a_nexus_field=NeXusField(
            name="c",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-alpha-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="alpha",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    beta = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-beta-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="beta",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    gamma = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-gamma-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="gamma",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    space_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-unit-cell-space-group-field"
        ],
        a_nexus_field=NeXusField(
            name="space_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDIpfID(MicrostructureIpf):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_ipf",
            name="ipfID",
            name_type="partial",
            optionality="required",
            min_occurs=1,
        ),
    )

    map = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDIpfIDMap",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="map",
            name_type="specified",
            optionality="required",
        ),
    )
    legend = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDIpfIDLegend",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="legend",
            name_type="specified",
            optionality="required",
        ),
    )

    color_model = Quantity(
        type=MEnum(["tsl", "mtex"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-color-model-field"
        ],
        a_nexus_field=NeXusField(
            name="color_model",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["tsl", "mtex"],
        ),
    )
    projection_direction = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-projection-direction-field"
        ],
        dimensionality="dimensionless",
        shape=[3],
        a_nexus_field=NeXusField(
            name="projection_direction",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDIpfIDMap(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="map",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-data-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    data_quantity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-data-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="data",
        ),
    )
    axis_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axis-x-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_x__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axis-x-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_x",
        ),
    )
    axis_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axis-y-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_y__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axis-y-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_y",
        ),
    )
    axis_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axis-z-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    axis_z__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-map-axis-z-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_z",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDIpfIDLegend(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="legend",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-data-field"
        ],
        shape=["*", "*", 3],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
    )
    data_quantity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-data-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="data",
        ),
    )
    axis_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-axis-x-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    axis_x__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-axis-x-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_x",
        ),
    )
    axis_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-axis-y-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    axis_y__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-ipfid-legend-axis-y-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_y",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDOdfID(MicrostructureOdf):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_odf",
            name="odfID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    configuration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDOdfIDConfiguration",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="configuration",
            name_type="specified",
            optionality="recommended",
        ),
    )
    characteristics = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDOdfIDCharacteristics",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="characteristics",
            name_type="specified",
            optionality="optional",
        ),
    )
    phi_two_plot = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEbsdIndexingPhaseIDOdfIDPhiTwoPlot",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="phi_two_plot",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDOdfIDConfiguration(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-configuration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="configuration",
            name_type="specified",
            optionality="recommended",
        ),
    )

    crystal_symmetry_point_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-configuration-crystal-symmetry-point-group-field"
        ],
        a_nexus_field=NeXusField(
            name="crystal_symmetry_point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    specimen_symmetry_point_group = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-configuration-specimen-symmetry-point-group-field"
        ],
        a_nexus_field=NeXusField(
            name="specimen_symmetry_point_group",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    kernel_halfwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-configuration-kernel-halfwidth-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="kernel_halfwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    kernel_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-configuration-kernel-name-field"
        ],
        a_nexus_field=NeXusField(
            name="kernel_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    resolution = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-configuration-resolution-field"
        ],
        dimensionality="[angle]",
        a_nexus_field=NeXusField(
            name="resolution",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDOdfIDCharacteristics(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-characteristics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="characteristics",
            name_type="specified",
            optionality="optional",
        ),
    )

    texture_index = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-characteristics-texture-index-field"
        ],
        dimensionality="dimensionless",
        a_nexus_field=NeXusField(
            name="texture_index",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingPhaseIDOdfIDPhiTwoPlot(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="phi_two_plot",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    varphi_one = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-varphi-one-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="varphi_one",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    varphi_one__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-varphi-one-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="varphi_one",
        ),
    )
    capital_phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-capital-phi-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="capital_phi",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    capital_phi__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-capital-phi-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="capital_phi",
        ),
    )
    varphi_two = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-varphi-two-field"
        ],
        dimensionality="[angle]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="varphi_two",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ANGLE",
        ),
    )
    varphi_two__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-phaseid-odfid-phi-two-plot-varphi-two-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="varphi_two",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEbsdIndexingRoi(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="roi",
            name_type="specified",
            optionality="recommended",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-title-field"
        ],
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    descriptor = Quantity(
        type=MEnum(["band_contrast", "confidence_index", "mean_angular_deviation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-descriptor-field"
        ],
        a_nexus_field=NeXusField(
            name="descriptor",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["band_contrast", "confidence_index", "mean_angular_deviation"],
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-data-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    axis_z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axis-z-field"
        ],
        a_nexus_field=NeXusField(
            name="axis_z",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    axis_z__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axis-z-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_z",
        ),
    )
    axis_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axis-y-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_y__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axis-y-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_y",
        ),
    )
    axis_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axis-x-field"
        ],
        dimensionality="[length]",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
    )
    axis_x__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-ebsd-indexing-roi-axis-x-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_x",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEds(EmEds):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXem_eds",
            name="eds",
            name_type="specified",
            optionality="optional",
        ),
    )

    indexing = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEdsIndexing",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEdsIndexing(Process):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="required",
        ),
    )

    summary = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEdsIndexingSummary",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="summary",
            name_type="specified",
            optionality="optional",
        ),
    )
    image = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEdsIndexingImage",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=118,
        ),
    )

    atom_types = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-atom-types-field"
        ],
        a_nexus_field=NeXusField(
            name="atom_types",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEdsIndexingSummary(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="summary",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    axis_energy = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-axis-energy-field"
        ],
        a_nexus_field=NeXusField(
            name="axis_energy",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_energy__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-summary-axis-energy-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_energy",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEdsIndexingImage(Image):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
            max_occurs=118,
        ),
    )

    image_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDEdsIndexingImageImage2d",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="required",
        ),
    )

    iupac_line_candidates = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-iupac-line-candidates-field"
        ],
        a_nexus_field=NeXusField(
            name="iupac_line_candidates",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
        ),
    )
    energy_range = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-energy-range-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        shape=[2],
        a_nexus_field=NeXusField(
            name="energy_range",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_ENERGY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDEdsIndexingImageImage2d(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    intensity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-intensity-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="intensity",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-axis-i-field"
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
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-axis-j-field"
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
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-eds-indexing-element-specific-map-image-2d-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDTomo(Process):
    """
    Electron tomography
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="tomo",
            name_type="specified",
            optionality="optional",
        ),
    )

    reconstructionID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDTomoReconstructionID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="reconstructionID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDTomoReconstructionID(Process):
    """
    Processing a single tilt series into an electron tomogram
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="reconstructionID",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    configuration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="configuration",
            name_type="specified",
            optionality="recommended",
        ),
    )
    programID = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDTomoReconstructionIDProgramID",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )
    tomogram = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.em.EmRoiIDTomoReconstructionIDTomogram",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="tomogram",
            name_type="specified",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDTomoReconstructionIDProgramID(Program):
    """
    The program with which the reconstruction was performed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-programid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name="programID",
            name_type="partial",
            optionality="recommended",
        ),
    )

    program = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-programid-program-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-programid-program-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            parent_field="program",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmRoiIDTomoReconstructionIDTomogram(Data):
    """
    The resulting tomogram
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="tomogram",
            name_type="specified",
            optionality="required",
        ),
    )

    signal = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-signal-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axes-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axisname-indices-attribute"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-title-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-intensity-field"
        ],
        shape=["*", "*", "*"],
        a_nexus_field=NeXusField(
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axis-k-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_k",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axis-k-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axis-j-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_j",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axis-j-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axis-i-field"
        ],
        shape=["*"],
        a_nexus_field=NeXusField(
            name="axis_i",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXem.html#nxem-entry-roiid-tomo-reconstructionid-tomogram-axis-i-long-name-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
