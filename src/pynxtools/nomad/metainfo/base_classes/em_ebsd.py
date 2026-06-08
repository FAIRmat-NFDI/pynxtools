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
# Run `pynx nomad generate-metainfo --nxdl NXem_ebsd` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.coordinate_system import CoordinateSystem
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmEbsd"]


class EmEbsd(Process):
    """
    Base class method-specific for Electron Backscatter Diffraction (EBSD).

    The general procedure of an EBSD experiment is as follows: Users load the
    specimen, collect first a coarse image of the surface. Next, they set an
    approximate value for the calibrated working distance and tilt the stage
    into diffraction conditions.

    Users then typically configure the microscope for collecting quality data.
    The EBSD detector is pushed in (if retractable). Subsequently, they fine
    tune the illumination and aberration corrector settings and select one or
    multiple ROIs for the microscope to machine off automatically. They
    configure on-the-fly indexing parameter and then typically start the
    measurement queue. From this point onwards typically the microscope runs
    automatically.

    Diffraction pattern get collected until the queue finishes or gets
    interrupted by either errors or arrival at the end of the users' allocated
    time slot at the instrument.

    Kikuchi pattern (EBSP) are usually indexed on-the-fly. These patterns are
    the raw data. Once indexed, these patterns are often not stored.

    Results are stored in files, which afterwards are typically copied
    automatically or manually for archival purposes to certain storage
    locations for further consumption. The result of such an EBSD
    measurement/experiment is a set of usually proprietary or open files from
    technology partners.

    This :ref:`NXem_ebsd` base class is a proposal how to represent
    method-specific data, metadata, and connections between these for the
    research field of electron microscopy exemplified here for electron
    backscatter diffraction (EBSD). The base class solves two key documentation
    issues within the EBSD community:

    Firstly, an instance of NXem_ebsd (such as a NeXus/HDF5 file that is
    formatted according to NXem_ebsd) stores the connection between the
    microscope session and the key datasets which are considered typically
    results of the afore-mentioned steps involved in an EBSD experiment.

    Different groups in NXem_ebsd make connections to data artifacts which were
    collected when working with electron microscopes via the NXem application
    definition. Using a file which stores information according to the NXem
    application definition has the benefit that it connects the sample,
    references to the sample processing, the user operating the microscope,
    details about the microscope session, and details about the acquisition and
    eventual indexing of Kikuchi patterns, associated overview images, like
    secondary electron or backscattered electron images of the
    region-of-interest probed, and many more (meta)data.

    Secondly, NXem_ebsd connects and stores the conventions and reference
    frames which were used and which are the key to a correct mathematical
    interpretation of every experiment or simulation using EBSD.

    Otherwise, results would be ripped out of their context like it is the
    current situation with many traditional studies where EBSD data were
    indexed on-the-fly and shared with the community only via sharing the
    strongly processed files with results in some formatting but without
    communicating all conventions used or just relying on the assumptions that
    colleagues likely know these conventions even though multiple definitions
    are possible.

    NXem_ebsd covers experiments with one-, two-dimensional, and so-called
    three- dimensional EBSD datasets. The third dimension is either time (in
    the case of quasi in-situ experiments) or space (in the case of
    serial-sectioning) experiments where a combination of repetitive removal of
    material from the surface layer to measure otherwise the same
    region-of-interest at different depth increments. Material removal can be
    achieved with mechanical, electron, or ion polishing, using manual steps or
    automated equipment like a robot system `S. Tsai et al.
    <https://doi.org/10.1063/5.0087945>`_.

    Three-dimensional experiments require to follow a sequence of specimen,
    surface preparation, and data collection steps. By virtue of design, these
    methods are destructive either because of the necessary material removal or
    surface degradation due to e.g. contamination or other electron-matter
    interaction.

    For three-dimensional EBSD, multiple two-dimensional EBSD orientation
    mappings are combined into one reconstructed stack via a computational
    workflow. Users collect data for each serial sectioning step via an
    experiment. This assures that data for associated microscope sessions and
    steps of data processing stay contextualized and connected.

    Eventual tomography methods also use such a workflow because first
    diffraction images are collected (e.g. with X-ray) and then these images
    are indexed to process a 3D orientation mapping. Therefore, the here
    proposed base class can be a blueprint also for future classes to embrace
    our colleagues from X-ray-based techniques be it 3DXRD or HEDM.

    This concept is related to term `Electron Backscatter Diffraction`_ of the
    EMglossary standard.

    .. _Electron Backscatter Diffraction:
    https://purls.helmholtz-metadaten.de/emg/EMG_00000019
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_ebsd",
            category="base",
            symbols={
                "n_op": "Number of arguments per orientation for given parameterization.",
                "n_sc": "Number of scan points.",
                "n_z": "Number of pixel along the slowest changing dimension for a rediscretized,\n                i.e. standardized default plot orientation mapping.",
                "n_y": "Number of pixel along slow changing dimension for a rediscretized i.e.\n                standardized default plot orientation mapping.",
                "n_x": "Number of pixel along fast changing dimension for a rediscretized i.e.\n                standardized default plot orientation mapping.",
                "n_solutions": "Number of phase solutions",
                "n_hkl": "Number of reflectors (Miller crystallographic plane triplets).",
            },
        ),
    )

    gnomonic_reference_frame = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_ebsd.EmEbsdGnomonicReferenceFrame",
        repeats=False,
        description=(
            "Details about the gnomonic (projection) reference frame. It is "
            "assumed that the configuration is inspected by looking towards the "
            "sample surface. If a detector is involved, it is assumed that the "
            "configuration is inspected from a position that is located behind "
            "this detector. If any of these assumptions are not met, the user is "
            "required to explicitly state this. Reference "
            "`<https://doi.org/10.1016/j.matchar.2016.04.008>`_ suggests to "
            "label the base vectors of this coordinate system as :math:`X_g, "
            "Y_g, Z_g`."
        ),
    )
    pattern_center = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_ebsd.EmEbsdPatternCenter",
        repeats=False,
        description=(
            "Details about the definition of the pattern center as a special "
            "point in the gnomonic_reference_frame. Typically the gnomonic space "
            "is embedded in the detector space. Specifically, the XgYg plane is "
            "defined such that it is laying inside the XdYd plane (of the "
            "detector reference frame). When the normalization direction is the "
            "same as e.g. the detector x-axis direction one effectively "
            "normalizes in fractions of the width of the detector. The issue "
            "with terms like width and height, though, is that these become "
            "degenerated if the detector region-of-interest is square-shaped. "
            "This is why instead of referring to width and height it is better "
            "to state explicitly which direction is considered positive when "
            "measuring distances. For the concepts used to specify the "
            "boundary_convention it is assumed that the region-of-interest is "
            "defined by a rectangle, referring to the direction of outer-unit "
            "normals to the respective edges of this rectangle."
        ),
    )
    measurement = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_ebsd.EmEbsdMeasurement",
        repeats=False,
        description=(
            "This group documents relevant details about the conditions and the "
            "tools for measuring diffraction patterns with an electron "
            "microscope. The most frequently collected EBSD data are captured "
            "for rectangular regions-of-interest using a discretization into "
            "square or hexagon tiles."
        ),
    )
    simulation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_ebsd.EmEbsdSimulation",
        repeats=False,
        description=(
            "This group documents relevant details about the conditions and the "
            "tools used for simulating diffraction patterns with some physical "
            "model. This group should be used if (e.g. instead of a measurement) "
            "the patterns were simulated (possibly awaiting indexing). In many "
            "practical cases where patterns are analyzed on-the-fly and "
            "dictionary indexing strategies used, so-called master pattern(s) "
            "are used to compare measured or simulated patterns with the master "
            "patterns."
        ),
    )
    calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_ebsd.EmEbsdCalibration",
        repeats=False,
        description=(
            "The EBSD system, including components like the electron gun, "
            "pole-piece, stage tilt, EBSD detector, and the gnomonic projection "
            "have to be calibrated to achieve reliable, precise, and accurate "
            "scientific results. Specifically, the gnomonic projection has to be "
            "calibrated. Typically, standard specimens made from silicon or "
            "quartz crystals in specific orientations are used for this purpose. "
            "Considering that a system used is already calibrated well-enough is "
            "much more frequently the case in practice than that users perform "
            "the calibration themselves (with above-mentioned standard "
            "specimens). In the first case, the user assumes that the principle "
            "geometry of the hardware components and the settings in the control "
            "and EBSD pattern acquisition software has been calibrated already. "
            "Consequently, users pick from an existent library of phase "
            "candidates, i.e. :ref:`NXunit_cell` instances. Examples are "
            "reflector models as stored in CRY files (HKL/Channel 5/Flamenco). "
            "In the second case, users calibrate the system during the session "
            "using standards (silicon, quartz, or other common specimens). There "
            "is usually one person in each lab responsible for doing such "
            "calibrations. Often this person or technician is also in charge of "
            "configuring the graphical user interface and software with which "
            "most users control and perform their analyses. For EBSD this has "
            "key implications: Taking TSL OIM/EDAX as an example, the "
            "conventions how orientations are stored is affected by how the "
            "reference frames are configured and how this setup in the GUI. "
            "Unfortunately, these pieces of information are not necessarily "
            "stored in the results files. In effect, key conventions become "
            "disconnected from the data so it remains the users' obligation to "
            "remember these settings or write these down in a lab notebook. "
            "Otherwise, these metadata get lost. All these issues are a "
            "motivation and problem which :ref:`NXem_ebsd` solves in that all "
            "conventions can be specified explicitly."
        ),
    )
    indexing = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_ebsd.EmEbsdIndexing",
        repeats=False,
        description=(
            "Indexing is a data processing step performed either after or while "
            "(aka on-the-fly) the beam scans the specimen. The resulting method "
            "is also known as orientation imaging microscopy (OIM). Different "
            "algorithms can be used to index EBSP. Common to them is the "
            "computational step where simulated or theoretically assumed "
            "patterns are compared with the measured ones. These latter patterns "
            "are referred to via the measurement or simulation groups of this "
            "base class respectively. Quality descriptors are defined based on "
            "which an indexing algorithm yields a quantitative measure of how "
            "similar measured and reference patterns are, and thus if no, one, "
            "or multiple so-called solutions were found. Assumed or simulated "
            "patterns are simulated using kinematical or dynamical theory of "
            "electron diffraction delivering master patterns. The Hough "
            "transform, one of the most frequently used traditional method for "
            "indexing EBSP is essentially a discretized Radon transform (for "
            "details see `M. van Ginkel et al. "
            "<https://www.semanticscholar.org/paper/A-short-introduction-to-the-Radon-and-Hough-and-how-Ginkel/fb6226f606cad489a15e38ed961c419037ccc858>`_). "
            "Recently, dictionary-based and artificial intelligence-based "
            "methods find more widespread usage for indexing."
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


class EmEbsdGnomonicReferenceFrame(CoordinateSystem):
    """
    Details about the gnomonic (projection) reference frame.

    It is assumed that the configuration is inspected by looking towards the
    sample surface. If a detector is involved, it is assumed that the
    configuration is inspected from a position that is located behind this
    detector.

    If any of these assumptions are not met, the user is required to explicitly
    state this.

    Reference `<https://doi.org/10.1016/j.matchar.2016.04.008>`_ suggests to
    label the base vectors of this coordinate system as :math:`X_g, Y_g, Z_g`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-gnomonic-reference-frame-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcoordinate_system",
            name="gnomonic_reference_frame",
            name_type="specified",
            optionality="optional",
        ),
    )

    origin = Quantity(
        type=MEnum(["in_the_pattern_center"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-gnomonic-reference-frame-origin-field"
        ],
        description=(
            "Origin of the gnomonic_reference_frame. Reference "
            "`<https://doi.org/10.1016/j.matchar.2016.04.008>`_ suggests to "
            "assume that this is coordinate :math:`Xg = 0, Yg = 0, Zg = 0`."
        ),
        a_nexus_field=NeXusField(
            name="origin",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["in_the_pattern_center"],
        ),
    )
    x_direction = Quantity(
        type=MEnum(["north", "east", "south", "west", "in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-gnomonic-reference-frame-x-direction-field"
        ],
        description=(
            "Direction of the positively pointing x-axis base vector of the "
            "gnomonic_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="x_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["north", "east", "south", "west", "in", "out"],
        ),
    )
    y_direction = Quantity(
        type=MEnum(["north", "east", "south", "west", "in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-gnomonic-reference-frame-y-direction-field"
        ],
        description=(
            "Direction of the positively pointing y-axis base vector of the "
            "gnomonic_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="y_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["north", "east", "south", "west", "in", "out"],
        ),
    )
    z_direction = Quantity(
        type=MEnum(["north", "east", "south", "west", "in", "out"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-gnomonic-reference-frame-z-direction-field"
        ],
        description=(
            "Direction of the positively pointing z-axis base vector of the "
            "gnomonic_reference_frame."
        ),
        a_nexus_field=NeXusField(
            name="z_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["north", "east", "south", "west", "in", "out"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEbsdPatternCenter(Process):
    """
    Details about the definition of the pattern center as a special point in
    the gnomonic_reference_frame.

    Typically the gnomonic space is embedded in the detector space.
    Specifically, the XgYg plane is defined such that it is laying inside the
    XdYd plane (of the detector reference frame).

    When the normalization direction is the same as e.g. the detector x-axis
    direction one effectively normalizes in fractions of the width of the
    detector.

    The issue with terms like width and height, though, is that these become
    degenerated if the detector region-of-interest is square-shaped. This is
    why instead of referring to width and height it is better to state
    explicitly which direction is considered positive when measuring distances.

    For the concepts used to specify the boundary_convention it is assumed that
    the region-of-interest is defined by a rectangle, referring to the
    direction of outer-unit normals to the respective edges of this rectangle.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-pattern-center-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="pattern_center",
            name_type="specified",
            optionality="optional",
        ),
    )

    x_boundary_convention = Quantity(
        type=MEnum(["top", "right", "bottom", "left"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-pattern-center-x-boundary-convention-field"
        ],
        description=(
            "From which border of the EBSP (in the detector reference frame) is "
            "the pattern center's x-position (PCx) measured."
        ),
        a_nexus_field=NeXusField(
            name="x_boundary_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["top", "right", "bottom", "left"],
        ),
    )
    x_normalization_direction = Quantity(
        type=MEnum(["north", "east", "south", "west"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-pattern-center-x-normalization-direction-field"
        ],
        description=(
            "In which direction are positive values for the x-axis coordinate "
            "value measured from the specified boundary."
        ),
        a_nexus_field=NeXusField(
            name="x_normalization_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["north", "east", "south", "west"],
        ),
    )
    y_boundary_convention = Quantity(
        type=MEnum(["top", "right", "bottom", "left"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-pattern-center-y-boundary-convention-field"
        ],
        description=(
            "From which border of the EBSP (in the detector reference frame) is "
            "the pattern center's y-position (PCy) measured."
        ),
        a_nexus_field=NeXusField(
            name="y_boundary_convention",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["top", "right", "bottom", "left"],
        ),
    )
    y_normalization_direction = Quantity(
        type=MEnum(["north", "east", "south", "west"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-pattern-center-y-normalization-direction-field"
        ],
        description=(
            "In which direction are positive values for the y-axis coordinate "
            "value measured from the specified boundary."
        ),
        a_nexus_field=NeXusField(
            name="y_normalization_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["north", "east", "south", "west"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEbsdMeasurement(Process):
    """
    This group documents relevant details about the conditions and the tools
    for measuring diffraction patterns with an electron microscope.

    The most frequently collected EBSD data are captured for rectangular
    regions-of-interest using a discretization into square or hexagon tiles.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-measurement-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="measurement",
            name_type="specified",
            optionality="optional",
        ),
    )

    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-measurement-time-field"
        ],
        dimensionality="[time]",
        description=(
            "Physical time since the beginning of a timestamp that is required "
            "to be the same for all experiments in the set. The purpose of this "
            "marker is to identify how all experiments in the set need to be "
            "arranged sequentially based on the time elapsed. The time is "
            "relevant to sort e.g. experiments of consecutive quasi in-situ "
            "experiments where a measurement was e.g. taken after 0 minutes, 30 "
            "minutes, 6 hours, or 24 hours of annealing."
        ),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    time__epoch_start = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-measurement-time-epoch-start-attribute"
        ],
        description=(
            "Timestamp relative to which time was counted to aid converting "
            "between time and timestamp."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="epoch_start",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="time",
        ),
    )
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-measurement-depends-on-field"
        ],
        description=(
            "Path to an instance of :ref:`NXdata` where the measured patterns "
            "are stored."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEbsdSimulation(Process):
    """
    This group documents relevant details about the conditions and the tools
    used for simulating diffraction patterns with some physical model.

    This group should be used if (e.g. instead of a measurement) the patterns
    were simulated (possibly awaiting indexing).

    In many practical cases where patterns are analyzed on-the-fly and
    dictionary indexing strategies used, so-called master pattern(s) are used
    to compare measured or simulated patterns with the master patterns.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-simulation-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="simulation",
            name_type="specified",
            optionality="optional",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-simulation-depends-on-field"
        ],
        description=(
            "Path to an instance of :ref:`NXimage` where the simulated patterns "
            "are stored."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEbsdCalibration(Process):
    """
    The EBSD system, including components like the electron gun, pole-piece,
    stage tilt, EBSD detector, and the gnomonic projection have to be
    calibrated to achieve reliable, precise, and accurate scientific results.

    Specifically, the gnomonic projection has to be calibrated. Typically,
    standard specimens made from silicon or quartz crystals in specific
    orientations are used for this purpose.

    Considering that a system used is already calibrated well-enough is much
    more frequently the case in practice than that users perform the
    calibration themselves (with above-mentioned standard specimens).

    In the first case, the user assumes that the principle geometry of the
    hardware components and the settings in the control and EBSD pattern
    acquisition software has been calibrated already. Consequently, users pick
    from an existent library of phase candidates, i.e. :ref:`NXunit_cell`
    instances. Examples are reflector models as stored in CRY files
    (HKL/Channel 5/Flamenco).

    In the second case, users calibrate the system during the session using
    standards (silicon, quartz, or other common specimens). There is usually
    one person in each lab responsible for doing such calibrations. Often this
    person or technician is also in charge of configuring the graphical user
    interface and software with which most users control and perform their
    analyses.

    For EBSD this has key implications: Taking TSL OIM/EDAX as an example, the
    conventions how orientations are stored is affected by how the reference
    frames are configured and how this setup in the GUI.

    Unfortunately, these pieces of information are not necessarily stored in
    the results files. In effect, key conventions become disconnected from the
    data so it remains the users' obligation to remember these settings or
    write these down in a lab notebook. Otherwise, these metadata get lost. All
    these issues are a motivation and problem which :ref:`NXem_ebsd` solves in
    that all conventions can be specified explicitly.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-calibration-depends-on-field"
        ],
        description=(
            "Path to an instance of :ref:`NXem` where calibration data are stored."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EmEbsdIndexing(Process):
    """
    Indexing is a data processing step performed either after or while (aka
    on-the-fly) the beam scans the specimen. The resulting method is also known
    as orientation imaging microscopy (OIM).

    Different algorithms can be used to index EBSP. Common to them is the
    computational step where simulated or theoretically assumed patterns are
    compared with the measured ones. These latter patterns are referred to via
    the measurement or simulation groups of this base class respectively.

    Quality descriptors are defined based on which an indexing algorithm yields
    a quantitative measure of how similar measured and reference patterns are,
    and thus if no, one, or multiple so-called solutions were found.

    Assumed or simulated patterns are simulated using kinematical or dynamical
    theory of electron diffraction delivering master patterns.

    The Hough transform, one of the most frequently used traditional method for
    indexing EBSP is essentially a discretized Radon transform (for details see
    `M. van Ginkel et al.
    <https://www.semanticscholar.org/paper/A-short-introduction-to-the-Radon-and-Hough-and-how-Ginkel/fb6226f606cad489a15e38ed961c419037ccc858>`_).
    Recently, dictionary-based and artificial intelligence-based methods find
    more widespread usage for indexing.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="indexing",
            name_type="specified",
            optionality="optional",
        ),
    )

    method = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-method-field"
        ],
        description=("Principal algorithm used for indexing."),
        a_nexus_field=NeXusField(
            name="method",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["hough_transform", "dictionary", "radon_transform"],
            open_enum=True,
        ),
    )
    status = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-status-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Which return value did the indexing algorithm yield for each scan "
            "point. * 0 - Not analyzed * 1 - Too high angular deviation * 2 - No "
            "solution * 100 - Success * 255 - Unexpected errors"
        ),
        a_nexus_field=NeXusField(
            name="status",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    phases_per_scan_point = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-phases-per-scan-point-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "How many phases i.e. crystal structure models were used to index "
            "each scan point if any? Let's assume an example to explain how this "
            "field should be used: In the simplest case users collected one "
            "pattern for each scan point and have indexed using one phase, i.e. "
            "one instance of an :ref:`NXunit_cell`. In another example users may "
            "have skipped some scan points (not indexed them at all) or used "
            "differing numbers of phases for indexing different scan points. The "
            "cumulated of this array decodes how phase_id and matching_phase "
            "arrays have to be interpreted. In the simplest case (one pattern "
            "per scan point, and all scan points indexed using that same single "
            "phase model), phase_id has as many entries as scan points and "
            "matching_phase has also as many entries as scan points."
        ),
        a_nexus_field=NeXusField(
            name="phases_per_scan_point",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    phase_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-phase-id-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "The array phases_per_scan_point details how the phase_id and the "
            "matching_phase arrays have to be interpreted. For the example of a "
            "single-phase material phase_id has trivial values either 0 (no "
            "solution) or 1 (solution matching sufficiently significant with the "
            "model for phase1, an instance of :ref:`NXphase`). For the example "
            "of multi-phase material, it is possible (although not frequently "
            "required) that a pattern agrees significantly with multiple "
            "patterns. Examples are cases of pseudosymmetry, insufficiently "
            "precise and accurate calibrated systems, or usage of inaccurate "
            "phase models. Having such field is especially relevant for recent "
            "dictionary- or artificial intelligence-based indexing methods to "
            "communicate the results in a model-agnostic way in combination with "
            "matching_phase. Depending on the phases_per_scan_point value, "
            "phase_id and matching_phase arrays represent a collection of "
            "concatenated tuples. These are organized in sequence: The solutions "
            "for the 0-th scan point, the 1-th scan point, the n_sc - 1 th scan "
            "point and omitting tuples for those scan points with no phases "
            "according to phases_per_scan_point."
        ),
        a_nexus_field=NeXusField(
            name="phase_id",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    matching_phase = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-matching-phase-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "One-dimensional array, pattern-by-pattern labelling the solutions "
            "found. The array phases_per_scan_point has to be specified because "
            "it details how the phase_id and the matching_phase arrays are "
            "interpreted. See documentation of phase_id for further details."
        ),
        a_nexus_field=NeXusField(
            name="matching_phase",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    matching_phase_descriptor = Quantity(
        type=MEnum(["confidence_index", "mean_angular_deviation", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-matching-phase-descriptor-field"
        ],
        description=(
            "Phase_matching is a descriptor for how well the solution matches or "
            "not. Examples can be confidence_index, mean_angular_deviation, or "
            "other."
        ),
        a_nexus_field=NeXusField(
            name="matching_phase_descriptor",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["confidence_index", "mean_angular_deviation", "other"],
        ),
    )
    scan_point_positions = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-scan-point-positions-field"
        ],
        dimensionality="[length]",
        shape=["*", 2],
        description=(
            "Calibrated center positions of each scan point in the sample "
            "surface reference system."
        ),
        a_nexus_field=NeXusField(
            name="scan_point_positions",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    indexing_rate = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-indexing-rate-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Fraction of successfully indexed patterns with a phase not the "
            "null-phase vs the number_of_scan_points."
        ),
        a_nexus_field=NeXusField(
            name="indexing_rate",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    number_of_scan_points = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-number-of-scan-points-field"
        ],
        dimensionality="dimensionless",
        description=("Number of scan points in the original mapping."),
        a_nexus_field=NeXusField(
            name="number_of_scan_points",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    pixel_shape = Quantity(
        type=MEnum(["square", "hexagon", "cube", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_ebsd.html#nxem_ebsd-indexing-pixel-shape-field"
        ],
        description=(
            "The shape of the polygon or polyhedron that was used for the tiling "
            "respectively tessellation of the region-of-interest into scan "
            "points."
        ),
        a_nexus_field=NeXusField(
            name="pixel_shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["square", "hexagon", "cube", "other"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
