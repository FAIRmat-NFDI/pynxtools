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
# Run `pynx nomad generate-metainfo --nx-class NXregion` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Region"]


class Region(Object):
    r"""
    Geometry and logical description of a region of data in a parent group.
    When used, it could be a child group to, say, :ref:`NXdetector`.

    This can be used to describe a subset of data used to create downsampled
    data or to derive some data from that subset.

    Note, the fields for the rectangular region specifiers follow HDF5’s
    dataspace hyperslab parameters (see
    https://portal.hdfgroup.org/display/HDF5/H5S_SELECT_HYPERSLAB). Note when
    **block** :math:`= 1`, then **stride** :math:`\equiv` **step** in Python
    slicing.

    For example, a ROI sum of an area starting at index of [20,50] and shape
    [220,120] in image data::

    detector:NXdetector/ data[60,256,512] region:NXregion/ @region_type =
    "rectangular" parent = "data" start = [20,50] count = [220,120]
    statistics:NXdata/ @signal = "sum" sum[60]

    the ``sum`` dataset contains the summed areas in each frame. Another
    example, a hyperspectral image downsampled 16-fold in energy::

    detector:NXdetector/ data[128,128,4096] region:NXregion/ @region_type =
    "rectangular" parent = "data" start = [2] count = [20] stride = [32] block
    = [16] downsampled:NXdata/ @signal = "maximum" @auxiliary_signals = "copy"
    maximum[128,128,20] copy[128,128,320]

    the ``copy`` dataset selects 20 16-channel blocks that start 32 channels
    apart, the ``maximum`` dataset will show maximum values in each 16-channel
    block in every spectra.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXregion",
            category="base",
            symbols={"O": "Outer rank", "R": "Region rank"},
        ),
    )

    downsampled = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=(
            "An optional group containing data copied/downsampled from parent "
            "group’s data. Its dataset name must reflect how the downsampling is "
            "done over each block. So it could be a reduction operation such as "
            "sum, minimum, maximum, mean, mode, median, etc. If downsampling is "
            'merely copying each block then use "copy" as the name. Where more '
            "than one downsample dataset is written (specified with ``@signal``) "
            "then add ``@auxiliary_signals`` listing the others. In the copy "
            "case, the field should have a shape of :math:`(D_0, ..., "
            "D_{\\mathbf{O}-1}, \\mathbf{block}[0] * \\mathbf{count}[0], ..., "
            "\\mathbf{block}[\\mathbf{R}-1] * \\mathbf{count}[\\mathbf{R}-1])`, "
            "otherwise the expected shape is :math:`(D_0, ..., "
            "D_{\\mathbf{O}-1}, \\mathbf{count}[0], ..., "
            "\\mathbf{count}[\\mathbf{R}-1])`. The following figure shows how "
            "blocks are used in downsampling: .. figure:: "
            "region/NXregion-example.png :width: 60% A selection with "
            ":math:`\\mathbf{start}=2, \\mathbf{count}=4, \\mathbf{stride}=3, "
            "\\mathbf{block}=2` from a dataset with shape [13] will result in "
            "the ``reduce`` dataset of shape [4] and a ``copy`` dataset of shape "
            "[8]."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="downsampled",
            name_type="specified",
            optionality="optional",
        ),
    )
    statistics = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=(
            "An optional group containing any statistics derived from the region "
            "in parent group’s data such as sum, minimum, maximum, mean, mode, "
            "median, rms, variance, etc. Where more than one statistical dataset "
            "is written (specified with ``@signal``) then add "
            "``@auxiliary_signals`` listing the others. All data fields should "
            "have shapes of :math:`\\boldsymbol{D}`."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="statistics",
            name_type="specified",
            optionality="optional",
        ),
    )

    region_type = Quantity(
        type=MEnum(["rectangular"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-region-type-attribute"
        ],
        description=(
            "This is ``rectangular`` to describe the region as a hyper-rectangle "
            "in the index space of its parent group's data field."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="region_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["rectangular"],
        ),
    )
    parent = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-parent-field"
        ],
        description=(
            "The name of data field in the parent group or the path of a data "
            "field relative to the parent group (so it could be a field in a "
            "subgroup of the parent group)"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="parent",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    parent_mask = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-parent-mask-field"
        ],
        description=(
            "The name of an optional mask field in the parent group with rank "
            ":math:`\\boldsymbol{R}` and dimensions :math:`\\boldsymbol{d}`. For "
            "example, this could be ``pixel_mask`` of an :ref:`NXdetector`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="parent_mask",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    start = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-start-field"
        ],
        shape=["*"],
        description=(
            "The starting position for region in detector data field array. This "
            "is recommended as it also defines the region rank. If omitted then "
            "defined as an array of zeros."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start",
            type="NX_NUMBER",
            name_type="specified",
            optionality="recommended",
        ),
    )
    count = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-count-field"
        ],
        shape=["*"],
        description=(
            "The number of blocks or items in the hyperslab selection. If "
            "omitted then defined as an array of dimensions that take into "
            "account the other hyperslab selection fields to span the parent "
            "data field's shape."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="count",
            type="NX_INT",
            name_type="specified",
            optionality="recommended",
        ),
    )
    stride = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-stride-field"
        ],
        shape=["*"],
        description=(
            "An optional field to define striding used to downsample data. If "
            "omitted then defined as an array of ones."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="stride",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    block = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-block-field"
        ],
        shape=["*"],
        description=(
            "An optional field to define the block size used to copy or "
            "downsample data. In the :math:`i`-th dimension, if "
            ":math:`\\mathbf{block}[i] < \\mathbf{stride}[i]` then the "
            "downsampling blocks have gaps between them; when ``block`` matches "
            "``stride`` then the blocks are contiguous; otherwise the blocks "
            "overlap. If omitted then defined as an array of ones."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="block",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    scale = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXregion.html#nxregion-scale-field"
        ],
        shape=["*"],
        description=(
            "An optional field to define a divisor for scaling of reduced data. "
            "For example, in a downsampled sum, it can reduce the maximum values "
            "to fit in the domain of the result data type. In an image that is "
            "downsampled by summing 2x2 blocks, using :math:`\\mathrm{scale}=4` "
            "allows the result to fit in the same integer type dataset as the "
            "parent dataset. If omitted then no scaling occurs."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="scale",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
