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
# Run `pynx nomad generate-metainfo --nx-class NXcg_alpha_complex` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.cg_primitive import CgPrimitive

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["CgAlphaComplex"]


class CgAlphaComplex(CgPrimitive):
    """
    Computational geometry of alpha complexes (alpha shapes or alpha wrappings)
    about primitives.

    For details see:

    * https://dx.doi.org/10.1109/TIT.1983.1056714 for 2D, *
    https://dx.doi.org/10.1145/174462.156635 for 3D, *
    https://dl.acm.org/doi/10.5555/871114 for weighted, and *
    https://doc.cgal.org/latest/Alpha_shapes_3 for 3D implementation of alpha
    shapes, and *
    https://doc.cgal.org/latest/Manual/packages.html#PkgAlphaWrap3 for 3D alpha
    wrappings

    in CGAL, the Computational Geometry Algorithms Library respectively. As a
    starting point, we follow the conventions of the CGAL library.

    In general, an alpha complex is a not necessarily connected or not
    necessarily pure complex, i.e. singular faces may exist. The number of
    cells, faces, and edges depends on how a specific alpha complex is filtered
    for lower-dimensional simplices. The fields is_regularized and
    regularization can be used to provide details about regularization
    procedures.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_alpha_complex.html#nxcg_alpha_complex"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcg_alpha_complex",
            category="base",
        ),
    )

    cg_point = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_point.CgPoint",
        repeats=True,
        variable=True,
        description=(
            "Point cloud serving as input for the computation of the alpha complex."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_point",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_triangle = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_triangle.CgTriangle",
        repeats=True,
        variable=True,
        description=(
            "Triangle soup serving as input for the computation of the alpha complex."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_triangle",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    cg_tetrahedron = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cg_tetrahedron.CgTetrahedron",
        repeats=True,
        variable=True,
        description=(
            "Tetrahedra representing an interior volume of the alpha complex (if "
            "such exists)."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcg_tetrahedron",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["convex_hull", "alpha_shape", "alpha_wrapping"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_alpha_complex.html#nxcg_alpha_complex-type-field"
        ],
        description=(
            "Type of alpha complex following the terminology used by CGAL for "
            "now. Alpha_shape means meshes created using one of the alpha_shape "
            "algorithm. Alpha_wrapping means meshes created using the "
            "alpha_wrapping algorithm."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["convex_hull", "alpha_shape", "alpha_wrapping"],
        ),
    )
    regularization = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_alpha_complex.html#nxcg_alpha_complex-regularization-field"
        ],
        description=("Human-readable description about regularization procedures."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="regularization",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    is_regularized = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_alpha_complex.html#nxcg_alpha_complex-is-regularized-field"
        ],
        description=(
            "Was the alpha complex regularized, i.e. have singular faces been "
            "removed, or not."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="is_regularized",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    alpha = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_alpha_complex.html#nxcg_alpha_complex-alpha-field"
        ],
        description=(
            "The alpha parameter, i.e. the squared radius of the alpha-sphere "
            "that is used when computing the alpha complex."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="alpha",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcg_alpha_complex.html#nxcg_alpha_complex-offset-field"
        ],
        dimensionality="[length]",
        description=(
            "The offset distance parameter used when computing alpha_wrappings."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="offset",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
