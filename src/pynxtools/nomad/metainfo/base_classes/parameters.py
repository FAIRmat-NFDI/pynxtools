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
# Run `pynx nomad generate-metainfo --nxdl NXparameters` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Parameters"]


class Parameters(Object):
    """
    Container for parameters used in processing or analysing data.

    Typically, this group is stored in a :ref:`NXprocess` group in order to
    contain parameters that are either inputs to or resulting from the process
    defined by the parent group. However, this base class can also be added to
    other groups for use in other contexts.

    Although this base class can be used to store any kind of parameter, one
    possible use case is to store parameters that are refined by a fitting
    function or model. A number of attributes have been defined to store
    metadata associated with such a refinement.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXparameters",
            category="base",
        ),
    )

    model = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-model-attribute"
        ],
        description=(
            "The name of the model used in optimizing the parameter values. "
            "Fitting packages such as LMFIT (https://lmfit.github.io/lmfit-py/) "
            "provide models, which instantiate functions to be fitted to the "
            "data. If this attribute is provided, it is assumed that all the "
            "parameters in this group are associated with this model."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="model",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    PARAMETER = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-field"
        ],
        variable=True,
        description=("A parameter that is used in or results from processing."),
        a_nexus_field=NeXusField(
            name="PARAMETER",
            type="NX_CHAR_OR_NUMBER",
            name_type="any",
            optionality="optional",
        ),
    )
    PARAMETER__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-units-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )
    PARAMETER__error = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-error-attribute"
        ],
        description=(
            "The standard deviation of the parameter after optimizing its value."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="error",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )
    PARAMETER__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-description-attribute"
        ],
        description=("A description of what this parameter represents."),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )
    PARAMETER__expression = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-expression-attribute"
        ],
        description=(
            "A string representing an expression that can be used to relate the "
            "parameter to another parameter's value. The format of this string "
            "is dependent on the program used to optimize the parameters and is "
            "not specified by NeXus."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="expression",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )
    PARAMETER__initial = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-initial-attribute"
        ],
        description=("The initial value of the parameter used in optimization."),
        a_nexus_attribute=NeXusAttribute(
            name="initial",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )
    PARAMETER__max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-max-attribute"
        ],
        description=("The upper bound of the parameter used in optimization."),
        a_nexus_attribute=NeXusAttribute(
            name="max",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )
    PARAMETER__min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-min-attribute"
        ],
        description=("The lower bound of the parameter used in optimization."),
        a_nexus_attribute=NeXusAttribute(
            name="min",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )
    PARAMETER__vary = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXparameters.html#nxparameters-parameter-vary-attribute"
        ],
        description=("True if the parameter was varied during optimization."),
        a_nexus_attribute=NeXusAttribute(
            name="vary",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
