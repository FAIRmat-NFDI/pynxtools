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
# Run `pynx nomad generate-metainfo --nx-class NXfit_function` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["FitFunction"]


class FitFunction(Object):
    """
    This describes a fit function that is used to fit data to any functional
    form.

    A fit function is used to describe a set of data :math:`y_k, k = 1 ... M`,
    which are collected as a function of one or more independent variables
    :math:`x` at the points :math:`x_k`. The fit function :math:`f` describes
    these data in an approximate way as :math:`y_k \approx f(a_0, . . . a_n,
    x_k)`, where :math:`a_i, i = 0 . . . n` are the *fit parameters* (which are
    stored the instances of ``NXfit_parameter``).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit_function.html#nxfit_function"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXfit_function",
            category="base",
        ),
    )

    fit_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fit_function.FitFunctionFitParameters",
        repeats=False,
    )

    function_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit_function.html#nxfit_function-function-type-field"
        ],
        description=(
            'Type of function used. Examples include "Gaussian" and '
            '"Lorentzian". In case a complicated functions, the the functional '
            "form of the function should be given by the ``formula_description`` "
            "field . The user is also encouraged to use the ``description`` "
            "field for describing the fit function in a human-readable way. "
            "Application definitions may limit the allowed fit functions by "
            "using an enumeration for the ``function_type`` field."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="function_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit_function.html#nxfit_function-description-field"
        ],
        description=(
            "Human-readable short description of this fit function. Software "
            "tools may use this field to write their local description of the "
            "fit function."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    formula_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit_function.html#nxfit_function-formula-description-field"
        ],
        description=(
            "Description of the mathematical formula of the function, taking "
            "into account the instances of ``TERM`` in ``fit_parameters``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="formula_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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


class FitFunctionFitParameters(Parameters):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit_function.html#nxfit_function-fit-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="fit_parameters",
            name_type="specified",
            optionality="optional",
        ),
    )

    PARAMETER = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit_function.html#nxfit_function-fit-parameters-parameter-field"
        ],
        description=(
            "A parameter for a fit function. This would typically be a variable "
            "that is optimized in a fit."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="PARAMETER",
            type="NX_CHAR_OR_NUMBER",
            name_type="any",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    PARAMETER__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit_function.html#nxfit_function-fit-parameters-parameter-description-attribute"
        ],
        description=("A description of what this parameter represents."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
