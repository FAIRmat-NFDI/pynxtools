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
from pynxtools.nomad.metainfo.base_classes.cite import Cite
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.cs_profiling import CsProfiling
from pynxtools.nomad.metainfo.base_classes.em_simulation import EmSimulation
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.project import Project
from pynxtools.nomad.metainfo.base_classes.roi_process import RoiProcess
from pynxtools.nomad.metainfo.base_classes.sample import Sample
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
        section_def="pynxtools.nomad.metainfo.base_classes.em_measurement.EmMeasurement",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_measurement",
            name="measurement",
            name_type="specified",
            optionality="optional",
        ),
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
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
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

    environment = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
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
        section_def="pynxtools.nomad.metainfo.base_classes.em_img.EmImg",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_img",
            name="img",
            name_type="specified",
            optionality="optional",
        ),
    )
    ebsd = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_ebsd.EmEbsd",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_ebsd",
            name="ebsd",
            name_type="specified",
            optionality="optional",
        ),
    )
    eds = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_eds.EmEds",
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
