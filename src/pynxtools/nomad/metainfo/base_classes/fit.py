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
# Run `pynx nomad generate-metainfo --nx-class NXfit` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.peak import Peak
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Fit"]


class Fit(Process):
    """
    Description of a fit procedure using a scalar valued global function
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXfit",
            category="base",
            symbols={
                "dimRank": "Rank of the dependent and independent data arrays (for\n                multivariate scalar-valued fit.)"
            },
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fit.FitData",
        repeats=False,
        description=("Data and results of the fit."),
    )
    peakPEAK = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fit.FitPeakPEAK",
        repeats=True,
        variable=True,
        description=(
            "An instance of the peak model. If there is no characteristic name "
            "for each peak component, the peaks could be labeled as peak_0, "
            "peak_1, and so on."
        ),
    )
    backgroundBACKGROUND = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.peak.Peak",
        repeats=True,
        variable=True,
        description=(
            "One fitted background (functional form, position (see "
            ":ref:`data/input_independent "
            "</NXfit/data/input_independent-field>`), and intensities) of the "
            "peak fit. If there is no characteristic name for each background "
            "component, it is envisioned that backgrounds are labeled as "
            "background_0, background_1, and so on."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="backgroundBACKGROUND",
            name_type="partial",
            optionality="optional",
        ),
    )
    global_fit_function = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fit_function.FitFunction",
        repeats=False,
        description=(
            "Function used to describe the overall fit to the data, taking into "
            "account the parameters of the individual :ref:`NXpeak` components."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="global_fit_function",
            name_type="specified",
            optionality="optional",
        ),
    )
    error_function = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fit_function.FitFunction",
        repeats=False,
        description=("Function used to optimize the parameters during peak fitting."),
        a_nexus_group=NeXusGroup(
            nx_class="NXfit_function",
            name="error_function",
            name_type="specified",
            optionality="optional",
        ),
    )

    label = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-label-field"
        ],
        description=("Human-readable label for this fit procedure."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="label",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    figure_of_meritMETRIC = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-figure-of-meritmetric-field"
        ],
        variable=True,
        dimensionality="dimensionless",
        description=(
            "Figure-of-merit to determine the goodness of fit, i.e., how well "
            "the fit model (i.e., the set of peaks and backgrounds) fits the "
            "measured observations. This value (which is a single number) is "
            "often used to guide adjustments to the fitting parameters in the "
            "peak fitting process."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="figure_of_meritMETRIC",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    figure_of_meritMETRIC__metric = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-figure-of-meritmetric-metric-attribute"
        ],
        description=(
            "Metric used to determine the goodness of fit. Examples include: - "
            ":math:`\\chi^2`, the squared sum of the sigma-weighted residuals - "
            "reduced :math:`\\chi^2`:, :math:`\\chi^2`: per degree of freedom - "
            ":math:`R^2`, the coefficient of determination"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="metric",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="figure_of_meritMETRIC",
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


class FitData(Data):
    """
    Data and results of the fit.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="optional",
        ),
    )

    input_independent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-data-input-independent-field"
        ],
        description=(
            "Independent variable(s) for this fit procedure, representing the "
            "values to be fitted by the ``global_fit_function``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="input_independent",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    input_dependent = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-data-input-dependent-field"
        ],
        description=(
            "Dependent variable(s) for this fit procedure (i.e., the observed data)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="input_dependent",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    fit_sum = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-data-fit-sum-field"
        ],
        description=(
            "Resulting fit obtained by evaluating the ``global_fit_function`` at "
            "the points specified in ``input_independent`` using the optimized "
            "fit parameters. This represents the best-fit curve or surface "
            "approximating the input_dependent data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="fit_sum",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    residual = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-data-residual-field"
        ],
        description=(
            "The difference between the observed data (``input_dependent``) and "
            "the predicted fit values (``fit_sum``). A lower magnitude of "
            "residuals indicates a better fit."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="residual",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class FitPeakPEAK(Peak):
    """
    An instance of the peak model. If there is no characteristic name for each
    peak component, the peaks could be labeled as peak_0, peak_1, and so on.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-peakpeak-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpeak",
            name="peakPEAK",
            name_type="partial",
            optionality="optional",
        ),
    )

    relative_sensitivity_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-peakpeak-relative-sensitivity-factor-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Relative sensitivity for this peak, to be used for quantification "
            "in an NXprocess. As an example, in X-ray spectroscopy could depend "
            "on the energy scale (see position), the ionization cross section, "
            "and the element probed."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="relative_sensitivity_factor",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    relative_area = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXfit.html#nxfit-peakpeak-relative-area-field"
        ],
        description=(
            "Relative area of this peak compared to other peaks. The relative "
            "area can simply be derived by dividing the total_area by the total "
            "area of all peaks or by a more complicated method (e.g., by "
            "additionally dividing by the relative sensitivity factors). Details "
            "shall be given in `global_fit_function`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="relative_area",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
