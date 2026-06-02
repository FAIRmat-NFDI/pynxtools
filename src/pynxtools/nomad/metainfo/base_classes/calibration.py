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
# Run `pynx nomad generate-metainfo --nx-class NXcalibration` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Calibration"]


class Calibration(Process):
    """
    Subclass of NXprocess to describe post-processing calibrations.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcalibration",
            category="base",
            symbols={
                "ncal": "Number of points of the calibrated and uncalibrated axes"
            },
        ),
    )

    calibration_object = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "A file serialization of a calibration which may not be publicly "
            "available (externally from the NeXus file). This metadata can be a "
            "documentation of the source (file) or database (entry) from which "
            "pieces of information have been extracted for consumption (e.g. in "
            "a research data management system (RDMS)). It is also possible to "
            "include the actual file by using the `file` field. The axis values "
            "may be copied or linked in the appropriate NXcalibration fields for "
            "reference."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="calibration_object",
            name_type="specified",
            optionality="optional",
        ),
    )
    fit_formula_inputs = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.CalibrationFitFormulaInputs",
        repeats=False,
        description=("Additional input axis to be used in the formula."),
    )
    calibration_parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.calibration.CalibrationCalibrationParameters",
        repeats=False,
        description=(
            "Fit coefficients to be used in ``fit_formula_description``. As an "
            "example, for nonlinear energy calibrations, e.g. in a "
            "time-of-flight (TOF) detector, a polynomial function is fitted to a "
            "set of features (peaks) at well defined energy positions to "
            "determine E(TOF). Here we can store the fit coefficients for that "
            "procedure."
        ),
    )
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        description=(
            "Any data acquired/used during the calibration that does not fit the "
            "`NX_FLOAT` fields above. NXdata groups can be used for "
            "multidimensional data which are relevant to the calibration"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-description-field"
        ],
        description=("A description of the procedures employed."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    physical_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-physical-quantity-field"
        ],
        description=(
            "The physical quantity of the calibration, e.g., energy, momentum, "
            "time, etc."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="physical_quantity",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_calibration_method = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-identifier-calibration-method-field"
        ],
        description=(
            "A digital persistent identifier (e.g., DOI, ISO standard) referring "
            "to a detailed description of a calibration method but no actual "
            "calibration data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier_calibration_method",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_calibration_reference = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-identifier-calibration-reference-field"
        ],
        description=(
            "A digital persistent identifier (e.g., a DOI) referring to a "
            "publicly available calibration measurement used for this "
            "instrument, e.g., a measurement of a known standard containing "
            "calibration information. The axis values may be copied or linked in "
            "the appropriate NXcalibration fields for reference."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="identifier_calibration_reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    last_process = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-last-process-field"
        ],
        description=(
            "Indicates the name of the last operation applied in the NXprocess "
            "sequence."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="last_process",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-applied-field"
        ],
        description=("Has the calibration been applied?"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    original_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-original-axis-field"
        ],
        shape=["*"],
        description=(
            "Array containing the data coordinates in the original uncalibrated axis"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="original_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    original_axis__symbol = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-original-axis-symbol-attribute"
        ],
        description=(
            "The symbol of the axis to be used in the fit_function, e.g., "
            "`energy`, `E`. This should comply to the following naming rules "
            "(similar to python's naming rules): * A variable name must start "
            "with a letter or the underscore character * A variable name cannot "
            "start with a number * A variable name can only contain "
            "alpha-numeric characters and underscores (A-z, 0-9, and _ ) * "
            "Variable names are case-sensitive (age, Age and AGE are three "
            "different variables)"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="symbol",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="original_axis",
        ),
    )
    original_axis__input_path = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-original-axis-input-path-attribute"
        ],
        description=(
            "The path from which this data is derived, e.g., raw detector axis. "
            "Should be a valid NeXus path name, e.g., "
            "/entry/instrument/detector/raw."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="input_path",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="original_axis",
        ),
    )
    fit_formula_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-fit-formula-description-field"
        ],
        description=(
            "Here we can store a description of the formula used for the fit "
            "function. For polynomial fits, use a0, a1, ..., an for the "
            "coefficients, corresponding to the values in the coefficients "
            "group. Use x0, x1, ..., xm for the mth position in the "
            "`original_axis` field. If there is the symbol attribute specified "
            "for the `original_axis` this may be used instead of x. If you want "
            "to use the whole axis use `x`. Alternate axis can also be available "
            "as specified by the `fit_formula_inputs` group. The data should "
            "then be referred here by the `SYMBOL` name, e.g., for a field name "
            "``my_field`` in ``fit_formula_inputs``, it should be referred here "
            "by ``my_field`` or ``my_field0`` if you want to read the zeroth "
            "element of the array."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="fit_formula_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    mapping_MAPPING = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-mapping-mapping-field"
        ],
        description=(
            "Mapping data for calibration. This can be used to map data points "
            "from uncalibrated to calibrated values, i.e., by multiplying each "
            "point in the input axis by the corresponding point in the mapping "
            "data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="mapping_MAPPING",
            type="NX_FLOAT",
            name_type="partial",
            optionality="optional",
        ),
    )
    calibrated_axis = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-calibrated-axis-field"
        ],
        shape=["*"],
        description=(
            "An array representing the axis after calibration, matching the data length"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="calibrated_axis",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-default-attribute"
        ],
        description=(
            ".. index:: plotting Declares which child group contains a path "
            "leading to a :ref:`NXdata` group. It is recommended (as of "
            "NIAC2014) to use this attribute to help define the path to the "
            "default dataset to be plotted. See "
            "https://www.nexusformat.org/2014_How_to_find_default_data.html for "
            "a summary of the discussion."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="default",
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


class CalibrationFitFormulaInputs(Parameters):
    """
    Additional input axis to be used in the formula.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-fit-formula-inputs-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="fit_formula_inputs",
            name_type="specified",
            optionality="optional",
        ),
    )

    PARAMETER__input_path = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-fit-formula-inputs-parameter-input-path-attribute"
        ],
        description=(
            "The path from which this data is derived, e.g., raw detector axis. "
            "Should be a valid NeXus path name, e.g., "
            "/entry/instrument/detector/raw."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="input_path",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="PARAMETER",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CalibrationCalibrationParameters(Parameters):
    """
    Fit coefficients to be used in ``fit_formula_description``.

    As an example, for nonlinear energy calibrations, e.g. in a time-of-flight
    (TOF) detector, a polynomial function is fitted to a set of features
    (peaks) at well defined energy positions to determine E(TOF). Here we can
    store the fit coefficients for that procedure.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-calibration-parameters-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="calibration_parameters",
            name_type="specified",
            optionality="optional",
        ),
    )

    aN = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-calibration-parameters-an-field"
        ],
        description=(
            "Use a0, a1, ..., an for the coefficients of a polynomial fit, "
            "corresponding to the values in the ``fit_formula_description``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="aN",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-calibration-parameters-scaling-factor-field"
        ],
        description=(
            "For linear calibration. Scaling parameter. This should yield the "
            "relation `calibrated_axis` = (`original_axis` + `offset`) * "
            "`scaling_factor`. For a more detailed description of scaling "
            "factors, see :ref:`/NXdata/FIELDNAME_scaling_factor "
            "</NXdata/FIELDNAME_scaling_factor-field>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="scaling_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXcalibration.html#nxcalibration-calibration-parameters-offset-field"
        ],
        description=(
            "For linear calibration. Offset parameter. This should yield the "
            "relation `calibrated_axis` = (`original_axis` + `offset`) * "
            "`scaling_factor`. For a more detailed description of offset, see "
            ":ref:`/NXdata/FIELDNAME_offset </NXdata/FIELDNAME_offset-field>`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
