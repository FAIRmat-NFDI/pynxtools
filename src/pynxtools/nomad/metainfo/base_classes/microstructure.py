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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.microstructure_feature import (
    MicrostructureFeature,
)
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Microstructure"]


class Microstructure(Object):
    r"""
    Base class to describe a microstructure, its structural aspects, associated
    descriptors, properties.

    Whether one uses a continuum or atomic scale description of materials,
    these are always a model only of the true internal structure of a material.
    Such models are useful as they enable a coarse-graining and categorizing of
    properties and representational aspects from which measured or simulated
    descriptions can be correlated with properties, i.e. descriptor values. The
    base class here can be used to describe the structural aspect of a
    region-of-interest for a specimen that was investigated or a computer
    simulation that was performed for a virtual specimen.

    Specimens experience thermo-chemo-mechanical processing (steps) before
    characterization. Therefore, the characterized microstructure may not turn
    out to be the same structure as of the untreated sample from which the
    region-of-interests on the specimen were sampled.

    Fields such as time and increment enable a quantification of the
    spatiotemporal evolution of a materials' structure by using multiple
    instances of NXmicrostructure. Both measurements and simulation virtually
    always sample this evolution. Most microscopy techniques characterize only
    a two-dimensional representation (projection) of the characterized material
    volume. Often materials are characterized only for specific states or via
    sampling coarsely in time relative to the timescale at which the physical
    phenomena take place. This is typically a compromise between the research
    questions and technical surplus practical limitations.

    The term microstructural feature covers here crystals and all sorts of
    crystal defects within the material (interfaces, triple junctions,
    dislocations, pores, etc.). A key challenge with the description of
    representations and properties of such microstructural features is that
    they can be represented and view as features with different dimensionality.
    Furthermore, combinations of features of different dimensionality are
    frequently expected to be documented with intuitive naming conventions when
    flat property lists are used. For these key-value dictionaries often
    folksonomies are used. These can be based on ad hoc documentation of such
    dictionaries in the literature and the metadata section of public data
    repositories.

    NXmicrostructure is an attempt to standardize these descriptions stronger.

    For crystals the number of typically used technical terms are smaller than
    for interfaces or line like defects and junctions of different types of
    crystal defects. The term grain describes a contiguous region of material
    that is delineated by interfaces (phase or grain boundaries). With its
    origin motivated by light optical microscopy though a grain is not
    necessarily a single crystal but can have an internal structure of defect
    such as dislocations. In this base class we use the term and respective
    group crystals though for single crystals and grains. The reason why this
    is possible is that when e.g. materials engineers talk about grains they
    inherently assume that the internal structure of these grains can be
    described with homogenized effective properties. If alternatively the
    individual structural crystalline or features of this grain should be
    distinguished it is useful to instantiate these as individual instances of
    crystals.

    Grain boundaries and phase boundaries are two main categories of
    interfaces. A grain boundary delineates two regions with similar crystal
    structure and phase but different orientation. A grain boundary is thus a
    homophase interface. By contrast, a heterophase boundary delineates two
    regions with typically but not necessarily dissimilar crystal structure but
    a different atomic occupation that justifies to distinguish two phases.
    There is a substantial variety of interfaces whose distinction was
    classically based on geometrical arguments but considers that atomic
    segregation is an equally important structural aspect to consider when
    classifying grain boundaries. A concise overview on theoretical aspect of
    and the semantics for characterizing interfaces and their properties is
    provided in e.g. `W. Bollmann <https://doi.org/10.1007/978-3-642-49173-3>`_
    and A. Sutton and R. W. Baluffi, Interfaces in Crystalline Materials,
    Clarendon Press, ISBN 9780198500612.

    Also for junctions between crystal defects there is a considerable variety
    of terms. Junctions are features in three-dimensional Euclidean space even
    if they are formed maybe only through a monolayer or a pearl chain of
    atoms. Either way their local atomic and electronic environment is
    different compared to the situation of an ideal crystal, or the adjoining
    defects, which gives typically rise to a plethora of configurations of
    which some yield useful material properties or affect material properties.

    Like crystals and interfaces, junctions are assumed to represent groups of
    atoms that have specific descriptor values which are different to other
    features. Taking an example, a triple junction is practically a
    three-dimensional defect as its atoms are arranged in three-dimensional
    space but the characteristics of that defect can often be reduced to a
    lower-dimensional description such as a triple line or a triple point as
    the projection of a line. Therefore, different representations can be used
    to describe the location, shape, and structure of such defect.

    This base class provides definitions for crystals, grains, interfaces,
    triple junctions, and quadruple junctions thus covering, volumetric, patch,
    line, and point like features that can serve as examples for future
    extension.

    As different types of crystal defects can interact, there is a substantial
    number of in principle characterizable and representable objects. Take
    again a triple line as an example. It is a tubular feature built from three
    adjoining interfaces. However, dislocations as line defects can interact
    with triple lines. Therefore, one can also argue that along a triple line
    there exist dislocation-line- triple-line junctions, likewise dislocations
    form own junctions.

    The description took inspiration from `E. E. Underwood
    <https://doi.org/10.1111/j.1365-2818.1972.tb03709.x>`_ and E. E.
    Underwood's book on Quantitative Stereology published in 1970 to categorize
    features based on their dimensionality.

    Indices can be defined either implicitly or explicitly. Indices for
    implicit indexing are defined on the interval :math:`[index\_offset,
    index\_offset + cardinality - 1]`. Indices can be used as identifiers for
    distinguishing instances, i.e. indices are equivalent to instance names of
    individual crystals.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure",
            category="base",
            symbols={
                "n_c": "The number of crystals or their projections",
                "n_i": "The number of interfaces or their projections",
                "n_tj": "The number of triple junctions or their projections",
                "n_qj": "The number of quadruple junctions or their projections",
                "n_c_one": "The number of one-dimensional crystal projections",
                "n_i_one": "The number of one-dimensional interface projections",
                "n_c_two": "The number of two-dimensional crystal projections",
                "n_i_two": "The number of two-dimensional interface projections",
                "n_tj_two": "The number of two-dimensional triple line projections",
                "n_ld_two": "The number of two-dimensional line defect projections",
                "n_c_three": "The number of crystals (grain and sub-grain are exact synonyms for crystal).",
                "n_i_three": "The number of interfaces (grain boundary and phase boundary are subclasses of\n                interfaces).",
                "n_tj_three": "The number of triple junctions (triple line is a exact synonym for triple\n                junction, triple point is projection of a triple junction).",
                "n_qj_three": "The number of quadruple junctions.",
                "d": "The dimensionality of the representation that needs to match the value for\n                configuration/dimensionality",
            },
        ),
    )

    configuration = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.MicrostructureConfiguration",
        repeats=False,
        description=(
            "Group where to store details about the configuration and "
            "parameterization of algorithms used whereby microstructural "
            "features were identified."
        ),
    )
    cg_grid = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_grid.CgGrid",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_grid",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_point = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_point.CgPoint",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_point",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_polyline = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyline.CgPolyline",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyline",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_triangle = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_triangle.CgTriangle",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_polygon = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polygon.CgPolygon",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polygon",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_polyhedron = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_polyhedron.CgPolyhedron",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_polyhedron",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    chemical_composition = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.chemical_composition.ChemicalComposition",
        repeats=False,
        description=("The chemical composition of this microstructure (region)."),
        a_nexus_group=NeXusGroup(
            nx_class="NXchemical_composition",
            name="chemical_composition",
            name_type="specified",
            optionality="optional",
        ),
    )
    phases = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.MicrostructurePhases",
        repeats=False,
        description=(
            "Different (thermodynamic) phases can be distinguished for the "
            "region-of- interest."
        ),
    )
    crystals = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.MicrostructureCrystals",
        repeats=False,
        description=(
            "One- or two-dimensional projections, or three-dimensional "
            "representations of crystals. An example for a volume bounded by "
            "other crystal defects. Crystals can be grains of different phases, "
            "precipitates, dispersoids; there are many terms used specifically "
            "in the materials engineering community. Typically, crystals are "
            "measured on the surface of a sample via optical or electron "
            "microscopy. Using X-ray diffraction methods crystals can be "
            "observed in bulk specimens. Crystals are represented by a set of "
            "pixel, voxel, or polygons and their polyline boundaries. In rare "
            "cases the volume bounded gets represented using constructive solid "
            "geometry approaches."
        ),
    )
    interfaces = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.MicrostructureInterfaces",
        repeats=False,
        description=(
            "One- or two-dimensional projections or three-dimensional "
            "representation of interfaces between crystals as topological "
            "entities equivalent to dual_junctions. An example for a surface "
            "defect. Most important are interfaces such as grain and phase "
            "boundaries but factually interfaces also exist between the "
            "environment and crystals exposed at the surface of the specimen or "
            "internal surfaces like between crystals, cracks, or pores. "
            "Interfaces are typically reported as discretized features. For "
            "interface projections on the 2D plane these are most frequently "
            "polyline segments. For interface patches in 3D these are most "
            "frequently triangulations. Descriptions with continuous functions "
            "are seldom used unless simplified configurations are studied in "
            "modeling and theoretical studies. When using discretizations the "
            "individual interface segments need to be distinguished from the "
            "interfaces themselves. Consequently, there are two sets of indices."
        ),
    )
    triple_junctions = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.MicrostructureTripleJunctions",
        repeats=False,
        description=(
            "Projections or representations of junctions at which three "
            "interfaces meet. An example for a line defect. Triple junctions are "
            "characterized as triple lines or triple points as their "
            "projections, or junctions observed between crystals (at the "
            "specimen surface exposed to an environment) (including wetting "
            "phenomena) or inside the specimen (crack, pores)."
        ),
    )
    quadruple_junctions = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure.MicrostructureQuadrupleJunctions",
        repeats=False,
        description=(
            "Quadruple junctions as a region where four crystals meet. An "
            "example for a point (like) defect. Thermodynamically such junctions "
            "can be unstable. Specifically when discretizations are used in "
            "simulations that do not address the thermodynamics of and splitting "
            "characteristics of junctions in cases when more than four crystals "
            "meet, it is possible that so-called higher-order junctions are "
            "observed."
        ),
    )

    comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-comment-field"
        ],
        description=("Discouraged free-text field for leaving comments"),
        a_nexus_field=NeXusField(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-date-field"
        ],
        description=(
            "ISO8601 with offset to local time zone included when a timestamp is "
            "required."
        ),
        a_nexus_field=NeXusField(
            name="date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Measured or simulated physical time stamp for this microstructure "
            "snapshot. Not to be confused with wall-clock timing or profiling "
            "data."
        ),
        a_nexus_field=NeXusField(
            name="time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    iteration = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-iteration-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Iteration or increment counter."),
        a_nexus_field=NeXusField(
            name="iteration",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
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


class MicrostructureConfiguration(Process):
    """
    Group where to store details about the configuration and parameterization
    of algorithms used whereby microstructural features were identified.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-configuration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="configuration",
            name_type="specified",
            optionality="optional",
        ),
    )

    dimensionality = Quantity(
        type=MEnum(["1", "2", "3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-configuration-dimensionality-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Dimensionality of Euclidean space in which the analysis is "
            "performed. This field can be used e.g. by a research data "
            "management system to identify if the description specifies one-, "
            "two-, or three-dimensional microstructural representations."
        ),
        a_nexus_field=NeXusField(
            name="dimensionality",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-configuration-algorithm-field"
        ],
        description=(
            "Algorithm whereby interfaces between crystals were reconstructed. * "
            "Disorientation clustering groups nearby material points based on "
            "their crystallographic disorientation * Fast multiscale clustering "
            "based on `D. Kushnir et al. "
            "<https://doi.org/10.1016/j.patcog.2006.04.007>`_ * Markov chain "
            "clustering `F. Niessen et al. "
            "<https://doi.org/10.1107/S1600576721011560>`_"
        ),
        a_nexus_field=NeXusField(
            name="algorithm",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-configuration-disorientation-threshold-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=(
            "Threshold to define at which disorientation angle to assume two "
            "crystalline regions have a significant orientation difference that "
            "warrants to assume that there exists an interface between the two "
            "regions."
        ),
        a_nexus_field=NeXusField(
            name="disorientation_threshold",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructurePhases(MicrostructureFeature):
    """
    Different (thermodynamic) phases can be distinguished for the region-of-
    interest.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-phases-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="phases",
            name_type="specified",
            optionality="optional",
        ),
    )

    phase = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.phase.Phase",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXphase",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-phases-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("First identifier whereby to identify phases implicitly."),
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureCrystals(MicrostructureFeature):
    """
    One- or two-dimensional projections, or three-dimensional representations
    of crystals.

    An example for a volume bounded by other crystal defects. Crystals can be
    grains of different phases, precipitates, dispersoids; there are many terms
    used specifically in the materials engineering community.

    Typically, crystals are measured on the surface of a sample via optical or
    electron microscopy. Using X-ray diffraction methods crystals can be
    observed in bulk specimens.

    Crystals are represented by a set of pixel, voxel, or polygons and their
    polyline boundaries. In rare cases the volume bounded gets represented
    using constructive solid geometry approaches.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXmicrostructure_feature",
            name="crystals",
            name_type="specified",
            optionality="optional",
        ),
    )

    orientation = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.rotations.Rotations",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXrotations",
            name="orientation",
            name_type="specified",
            optionality="optional",
        ),
    )

    representation = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-representation-field"
        ],
        description=(
            "Reference to an instance of: * :ref:`NXcg_polyline` for a one- or "
            "two-dimensional representation as only a projection is available "
            "(like in linear intercept analysis) * :ref:`NXcg_polygon`, "
            ":ref:`NXcg_triangle`, or :ref:`NXcg_polyhedron` for a two- or "
            "three-dimensional representation as only a projection is available "
            "(like in most experiments) * :ref:`NXcg_grid` for regularly "
            "pixelated (in 1D, 2D) or voxelated representations (in 3D) which "
            "represent the geometrical entities of the discretization."
        ),
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    number_of_crystals = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-number-of-crystals-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "How many crystals are distinguished. Crystals are listed "
            "irrespective of the phase to which these are assigned."
        ),
        a_nexus_field=NeXusField(
            name="number_of_crystals",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    number_of_phases = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-number-of-phases-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "How many phases are distinguished. Phases are typically "
            "distinguished based on statistical thermodynamics argument and "
            "crystal structure."
        ),
        a_nexus_field=NeXusField(
            name="number_of_phases",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("First identifier whereby to identify crystals implicitly."),
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_crystal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-indices-crystal-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Identifier whereby to identify each crystal explicitly."),
        a_nexus_field=NeXusField(
            name="indices_crystal",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_phase = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-indices-phase-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Identifier whereby to identify phase for each crystal explicitly."
        ),
        a_nexus_field=NeXusField(
            name="indices_phase",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    boundary_contact = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-boundary-contact-field"
        ],
        shape=["*"],
        description=(
            "True, if the feature makes contact with the edge of the ROI. False, "
            "if the feature does not make contact with the edge of the ROI."
        ),
        a_nexus_field=NeXusField(
            name="boundary_contact",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    orientation_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-orientation-spread-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Average disorientation angle for each crystal between individual "
            "orientations of that crystal evaluated as a summary statistic for "
            "all probed positions vs the average disorientation of that crystal."
        ),
        a_nexus_field=NeXusField(
            name="orientation_spread",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=("Length of each crystal"),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=("Area of each crystal."),
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-crystals-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        shape=["*"],
        description=("Volume of each crystal"),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureInterfaces(MicrostructureFeature):
    """
    One- or two-dimensional projections or three-dimensional representation of
    interfaces between crystals as topological entities equivalent to
    dual_junctions.

    An example for a surface defect. Most important are interfaces such as
    grain and phase boundaries but factually interfaces also exist between the
    environment and crystals exposed at the surface of the specimen or internal
    surfaces like between crystals, cracks, or pores.

    Interfaces are typically reported as discretized features. For interface
    projections on the 2D plane these are most frequently polyline segments.
    For interface patches in 3D these are most frequently triangulations.
    Descriptions with continuous functions are seldom used unless simplified
    configurations are studied in modeling and theoretical studies.

    When using discretizations the individual interface segments need to be
    distinguished from the interfaces themselves. Consequently, there are two
    sets of indices.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-representation-field"
        ],
        description=(
            "Reference to an instance of: * :ref:`NXcg_point` for a "
            "one-dimensional representation as only a projection is available "
            "(as in linear intercept analyses) * :ref:`NXcg_polyline` or "
            ":ref:`NXcg_polygon` for a two-dimensional representation as only a "
            "projection is available (like in most experiments) * "
            ":ref:`NXcg_grid` for regularly pixelated (in 1D, 2D) or voxelated "
            "representations (in 3D) using (boolean) masks (like in computer "
            "simulations or 3D experiments) which represent the geometrical "
            "entities of the discretization."
        ),
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    number_of_interfaces = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-number-of-interfaces-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("How many interfaces are distinguished."),
        a_nexus_field=NeXusField(
            name="number_of_interfaces",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("First identifier whereby to identify interfaces implicitly."),
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_interface = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-indices-interface-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Identifier whereby to identify each interface explicitly. An array "
            "with as many entries as interfaces or their projections."
        ),
        a_nexus_field=NeXusField(
            name="indices_interface",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_crystal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-indices-crystal-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 2],
        description=(
            "Set of pairs of indices_crystal values, for each interface one "
            "value pair. An array with as many pairs as interfaces or their "
            "projections."
        ),
        a_nexus_field=NeXusField(
            name="indices_crystal",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_crystal__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-indices-crystal-use-these-attribute"
        ],
        description=("The specific identifiers whereby to resolve ambiguities."),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_crystal",
        ),
    )
    indices_phase = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-indices-phase-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 2],
        description=(
            "Set of pairs of indices_phase values, for each interface one value "
            "pair. An array with as many pairs as interfaces or their "
            "projections."
        ),
        a_nexus_field=NeXusField(
            name="indices_phase",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_phase__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-indices-phase-use-these-attribute"
        ],
        description=("The specific identifiers whereby to resolve ambiguities."),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_phase",
        ),
    )
    number_of_triple_junctions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-number-of-triple-junctions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Interfaces can be the physical three-dimensional surfaces or two- "
            "or one-dimensional projections. The latter situation applies "
            "typically for characterization with electron microscopy. In the "
            "case of a two-dimensional projection interfaces are interface "
            "traces. These have two terminating junctions. In three dimensions "
            "though the interface is a surface patch that is bounded by multiple "
            "triple lines. Number of triple_junctions adjoining each interface. "
            "This array resolves the number of values along the second dimension "
            "for the field indices_triple_junctions."
        ),
        a_nexus_field=NeXusField(
            name="number_of_triple_junctions",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_triple_junction = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-indices-triple-junction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Set of pairs of indices_triple_junction for each interface. An "
            "array with as many tuples of pairs to describe all junctions about "
            "all interfaces."
        ),
        a_nexus_field=NeXusField(
            name="indices_triple_junction",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_triple_junction__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-indices-triple-junction-use-these-attribute"
        ],
        description=("The specific identifiers whereby to resolve ambiguities."),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_triple_junction",
        ),
    )
    boundary_contact = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-boundary-contact-field"
        ],
        shape=["*"],
        description=(
            "True, if the interface makes contact with the edge of the ROI. "
            "False, if the interface does not make contact with the edge of the "
            "ROI."
        ),
        a_nexus_field=NeXusField(
            name="boundary_contact",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    surface_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-surface-energy-field"
        ],
        shape=["*"],
        description=("Gibbs free surface energy for each interface."),
        a_nexus_field=NeXusField(
            name="surface_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    mobility = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-mobility-field"
        ],
        shape=["*"],
        description=("Non-intrinsic mobility of each interface."),
        a_nexus_field=NeXusField(
            name="mobility",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The length of each interface if only projections are available. "
            "This is not necessarily the same as the length of the individual "
            "polyline segments whereby the interface is discretized."
        ),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-interfaces-area-field"
        ],
        dimensionality="[length] ** 2",
        unit="m ** 2",
        shape=["*"],
        description=("The surface area of all interfaces."),
        a_nexus_field=NeXusField(
            name="area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_AREA",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureTripleJunctions(MicrostructureFeature):
    """
    Projections or representations of junctions at which three interfaces meet.

    An example for a line defect. Triple junctions are characterized as triple
    lines or triple points as their projections, or junctions observed between
    crystals (at the specimen surface exposed to an environment) (including
    wetting phenomena) or inside the specimen (crack, pores).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-representation-field"
        ],
        description=(
            "Reference to an instance of: * :ref:`NXcg_point` for a "
            "one-dimensional representation as only a projection is available "
            "(like in most experiments) * :ref:`NXcg_polyline` for a "
            "two-dimensional representation as only a projection is available * "
            ":ref:`NXcg_polygon` for a two-dimensional representation in the "
            "(seldom) case of sufficient spatial resolution and the line in the "
            "projection plane or cases where triple junction locations are "
            "approximated e.g. using a set of triangles * :ref:`NXcg_polyhedron` "
            "for a three-dimensional representation via e.g. a representation of "
            "Voronoi cells about atoms * :ref:`NXcg_grid` for regularly "
            "pixelated or voxelated representation in one, two, or three "
            "dimensions using (boolean) masks which represent the geometrical "
            "entities of the discretization."
        ),
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    number_of_junctions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-number-of-junctions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Number of triple junctions."),
        a_nexus_field=NeXusField(
            name="number_of_junctions",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("First identifier to identify triple junctions implicitly."),
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_triple_junction = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-indices-triple-junction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Identifier to identify each triple junction explicitly."),
        a_nexus_field=NeXusField(
            name="indices_triple_junction",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    location = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-location-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Set of identifier for positions whereby to identify the location of "
            "each junction."
        ),
        a_nexus_field=NeXusField(
            name="location",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    location__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-location-use-these-attribute"
        ],
        description=("The specific identifiers whereby to resolve ambiguities."),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="location",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Explicit positions."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    indices_crystal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-indices-crystal-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=(
            "Set of tuples of identifier of crystals connected to the junction "
            "for each triple junction."
        ),
        a_nexus_field=NeXusField(
            name="indices_crystal",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_interface = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-indices-interface-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=(
            "Set of tuples of identifier of interfaces connected to the junction "
            "for each triple junction."
        ),
        a_nexus_field=NeXusField(
            name="indices_interface",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_interface__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-indices-interface-use-these-attribute"
        ],
        description=(
            "The specific interface identifiers whereby to resolve ambiguities."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_interface",
        ),
    )
    indices_polyline = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-indices-polyline-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=(
            "Set of tuples of identifier for polyline segments connected to the "
            "junction for each triple junction."
        ),
        a_nexus_field=NeXusField(
            name="indices_polyline",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_polyline__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-indices-polyline-use-these-attribute"
        ],
        description=("The specific indices_polyline whereby to resolve ambiguities."),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_polyline",
        ),
    )
    boundary_contact = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-boundary-contact-field"
        ],
        shape=["*"],
        description=(
            "True, if the triple line makes contact with the edge of the ROI. "
            "False, if the triple line does not make contact with the edge of "
            "the ROI."
        ),
        a_nexus_field=NeXusField(
            name="boundary_contact",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    line_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-line-energy-field"
        ],
        shape=["*"],
        description=("Specific line energy of each triple junction"),
        a_nexus_field=NeXusField(
            name="line_energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    mobility = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-mobility-field"
        ],
        shape=["*"],
        description=("Non-intrinsic mobility of each triple junction."),
        a_nexus_field=NeXusField(
            name="mobility",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The length of each triple junction. This is not necessarily the "
            "same as the length of the individual polyline segments whereby the "
            "junction is discretized."
        ),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-triple-junctions-volume-field"
        ],
        dimensionality="[length] ** 3",
        unit="m ** 3",
        shape=["*"],
        description=(
            "The volume about each triple junction. Respective cut-off criteria "
            "need to be specified."
        ),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureQuadrupleJunctions(MicrostructureFeature):
    """
    Quadruple junctions as a region where four crystals meet.

    An example for a point (like) defect.

    Thermodynamically such junctions can be unstable. Specifically when
    discretizations are used in simulations that do not address the
    thermodynamics of and splitting characteristics of junctions in cases when
    more than four crystals meet, it is possible that so-called higher-order
    junctions are observed.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-group"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-representation-field"
        ],
        description=(
            "Reference to an instance of: * :ref:`NXcg_point` * :ref:`NXcg_grid` "
            "for regularly pixelated (in 1D, 2D) or voxelated representations "
            "(in 3D) using (boolean) masks which represent the geometrical "
            "entities of the discretization."
        ),
        a_nexus_field=NeXusField(
            name="representation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    number_of_junctions = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-number-of-junctions-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Number of quadruple junctions."),
        a_nexus_field=NeXusField(
            name="number_of_junctions",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    index_offset = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-index-offset-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("First identifier to identify quadruple junctions implicitly."),
        a_nexus_field=NeXusField(
            name="index_offset",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_quadruple_junction = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-quadruple-junction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("Identifier to identify each quadruple junction explicitly."),
        a_nexus_field=NeXusField(
            name="indices_quadruple_junction",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    location = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-location-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "Set of identifier for positions whereby to identify the location of "
            "each junction."
        ),
        a_nexus_field=NeXusField(
            name="location",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    location__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-location-use-these-attribute"
        ],
        description=("The specific point identifier whereby to resolve ambiguities."),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="location",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=("Explicit positions."),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    indices_crystal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-crystal-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 4],
        description=(
            "Set of tuples of identifier of crystals connected to the junction "
            "for each junction."
        ),
        a_nexus_field=NeXusField(
            name="indices_crystal",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_crystal__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-crystal-use-these-attribute"
        ],
        description=(
            "The specific identifier to instances of crystal identifiers whereby "
            "to resolve ambiguities."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_crystal",
        ),
    )
    indices_interface = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-interface-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 4],
        description=(
            "Set of tuples of identifier of interfaces connected to the junction "
            "for each junction."
        ),
        a_nexus_field=NeXusField(
            name="indices_interface",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_interface__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-interface-use-these-attribute"
        ],
        description=(
            "The specific identifier to instances of interface identifiers "
            "whereby to resolve ambiguities."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_interface",
        ),
    )
    indices_triple_junction = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-triple-junction-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=(
            "Set of tuples of identifier for triple junctions connected to the "
            "junction for each quadruple junction."
        ),
        a_nexus_field=NeXusField(
            name="indices_triple_junction",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_triple_junction__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-triple-junction-use-these-attribute"
        ],
        description=(
            "The specific identifier to instances of triple junction identifiers "
            "whereby to resolve ambiguities."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_triple_junction",
        ),
    )
    indices_phase = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-phase-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 4],
        description=(
            "Set of tuples of identifier for phases of crystals connected to the "
            "junction for each quadruple junction."
        ),
        a_nexus_field=NeXusField(
            name="indices_phase",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_phase__use_these = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-indices-phase-use-these-attribute"
        ],
        description=(
            "The specific identifier to instances of phase identifier whereby to "
            "resolve ambiguities."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="use_these",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_phase",
        ),
    )
    boundary_contact = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-boundary-contact-field"
        ],
        shape=["*"],
        description=(
            "True, if the junction makes contact with the edge of the ROI. True, "
            "if the junction does not make contact with the edge of the ROI."
        ),
        a_nexus_field=NeXusField(
            name="boundary_contact",
            type="NX_UINT",
            name_type="specified",
            optionality="optional",
        ),
    )
    energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-energy-field"
        ],
        shape=["*"],
        description=("Energy of the quadruple_junction as a defect."),
        a_nexus_field=NeXusField(
            name="energy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    mobility = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure.html#nxmicrostructure-quadruple-junctions-mobility-field"
        ],
        shape=["*"],
        description=("Non-intrinsic mobility of each quadruple_junction."),
        a_nexus_field=NeXusField(
            name="mobility",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
