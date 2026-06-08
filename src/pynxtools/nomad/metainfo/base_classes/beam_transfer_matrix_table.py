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
# Run `pynx nomad generate-metainfo --nxdl NXbeam_transfer_matrix_table` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.metainfo import MEnum, Quantity, Section

from pynxtools.nomad.annotations import NeXusAttribute, NeXusDefinition, NeXusField
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["BeamTransferMatrixTable"]


class BeamTransferMatrixTable(Object):
    """
    Contains data structures of an experimental optical setup (i.e., multiple
    transfer matrix tables). These data structures are used to relate physical
    properties of two beams (NXbeam) which have one common optical component
    (NXcomponent) (one specific transfer matrix). One of these beams is an
    input beam and the other one is an output beam.

    The data describes the change of beam properties, e.g. the intensity of a
    beam is reduced because the transmission coefficient of the beam device is
    lower than 1.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_transfer_matrix_table.html#nxbeam_transfer_matrix_table"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXbeam_transfer_matrix_table",
            category="base",
            symbols={"N_variables": "Length of the array associated to the data type."},
        ),
    )

    datatype_N = Quantity(
        type=MEnum(["aperture", "focal length", "orientation", "jones matrix"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_transfer_matrix_table.html#nxbeam_transfer_matrix_table-datatype-n-field"
        ],
        variable=True,
        description=(
            "Select which type of data was recorded, for example aperture and "
            "focal length. It is possible to have multiple selections. This "
            "selection defines how many columns (N_variables) are stored in the "
            "data array. N in the name, is the index number in which order the "
            "given property is listed."
        ),
        a_nexus_field=NeXusField(
            name="datatype_N",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
            enumeration=["aperture", "focal length", "orientation", "jones matrix"],
        ),
    )
    matrix_elements = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_transfer_matrix_table.html#nxbeam_transfer_matrix_table-matrix-elements-field"
        ],
        shape=["*"],
        description=(
            "Please list in this array the column and row names used in your "
            "actual data. That is in the case of aperture ['diameter'] or focal "
            "length ['focal_length_value'] and for orientation matrix ['OM1', "
            "'OM2', 'OM3'] or for jones matrix ['JM1','JM2']"
        ),
        a_nexus_field=NeXusField(
            name="matrix_elements",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    TRANSFER_MATRIX = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_transfer_matrix_table.html#nxbeam_transfer_matrix_table-transfer-matrix-field"
        ],
        variable=True,
        shape=["*", "*"],
        description=(
            "Contains the datastructure which relates beam properties of an "
            "input and output beam as result of the input beam interaction with "
            "the beam device. Transfer matrix relationship between N input beams "
            "and M output beams. It contains a table with the relevant matrices "
            "to be used for different transmitted properties (such as "
            "polarization, intensity, phase). Data structure for all "
            "transfermatrices of a beam device in a setup. For each combination "
            "of N input and M output beams and for L physical concept (i.e. beam "
            "intensity), one matrix can be defined. In this way, the transfer "
            "matrix table has the dimension NxM. For each entry, in this "
            "transfer matrix, there are L formalisms. Each formalism has the "
            "dimension math:`dim(L_i)xdim(L_i)`, whereby math:`L_i` is the "
            "specific physical concept (Intensity, polarization, direction). A "
            "beamsplitter with two input laser beams can have a total of four "
            "transfermatrices (2 Input x 2 Output). The dimension of the "
            "transfer matrix depends on the parameters. Examples are: 1x1 for "
            "intensity/power 2x2 for jones formalism 3x3 for direction"
        ),
        a_nexus_field=NeXusField(
            name="TRANSFER_MATRIX",
            type="NX_NUMBER",
            name_type="any",
            optionality="optional",
        ),
    )
    TRANSFER_MATRIX__input = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_transfer_matrix_table.html#nxbeam_transfer_matrix_table-transfer-matrix-input-attribute"
        ],
        description=(
            "Specific name of input beam which the transfer matrix table is related to."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="input",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="TRANSFER_MATRIX",
        ),
    )
    TRANSFER_MATRIX__output = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam_transfer_matrix_table.html#nxbeam_transfer_matrix_table-transfer-matrix-output-attribute"
        ],
        description=(
            "Specific name of output beam which the transfer matrix table is "
            "related to."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="output",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="TRANSFER_MATRIX",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
