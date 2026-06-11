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
# Run `pynx nomad generate-metainfo --nxdl NXreflections` to regenerate.
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

__all__ = ["Reflections"]


class Reflections(Object):
    """
    Reflection data from diffraction experiments
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXreflections",
            category="base",
            symbols={"n": "number of reflections", "m": "number of experiments"},
        ),
    )

    experiments = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-experiments-field"
        ],
        shape=["*"],
        description=("The experiments from which the reflection data derives"),
        a_nexus_field=NeXusField(
            name="experiments",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    h = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-h-field"
        ],
        shape=["*"],
        description=("The h component of the miller index"),
        a_nexus_field=NeXusField(
            name="h",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    h__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-h-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="h",
        ),
    )
    k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-k-field"
        ],
        shape=["*"],
        description=("The k component of the miller index"),
        a_nexus_field=NeXusField(
            name="k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    k__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-k-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="k",
        ),
    )
    l = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-l-field"
        ],
        shape=["*"],
        description=("The l component of the miller index"),
        a_nexus_field=NeXusField(
            name="l",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    l__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-l-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="l",
        ),
    )
    id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-id-field"
        ],
        shape=["*"],
        description=(
            "The id of the experiment which resulted in the reflection. If the "
            "value is greater than 0, the experiments must link to a "
            "multi-experiment NXmx group"
        ),
        a_nexus_field=NeXusField(
            name="id",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    id__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-id-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="id",
        ),
    )
    reflection_id = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-reflection-id-field"
        ],
        shape=["*"],
        description=(
            "The id of the reflection. Multiple partials from the same "
            "reflection should all have the same id"
        ),
        a_nexus_field=NeXusField(
            name="reflection_id",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    reflection_id__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-reflection-id-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="reflection_id",
        ),
    )
    entering = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-entering-field"
        ],
        shape=["*"],
        description=("Is the reflection entering or exiting the Ewald sphere"),
        a_nexus_field=NeXusField(
            name="entering",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    entering__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-entering-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="entering",
        ),
    )
    det_module = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-det-module-field"
        ],
        shape=["*"],
        description=("The detector module on which the reflection was recorded"),
        a_nexus_field=NeXusField(
            name="det_module",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    det_module__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-det-module-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="det_module",
        ),
    )
    flags = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-flags-field"
        ],
        shape=["*"],
        description=(
            "Status flags describing the reflection. This is a bit mask. The "
            "bits in the mask follow the convention used by DIALS, and have the "
            "following names: === ========================================== bit "
            "name === ========================================== 0 ``predicted`` "
            "1 ``observed`` 2 ``indexed`` 3 ``used_in_refinement`` 4 ``strong`` "
            "5 ``reference_spot`` 6 ``dont_integrate`` 7 ``integrated_sum`` 8 "
            "``integrated_prf`` 9 ``integrated`` 10 ``overloaded`` 11 "
            "``overlapped`` 12 ``overlapped_fg`` 13 ``in_powder_ring`` 14 "
            "``foreground_includes_bad_pixels`` 15 "
            "``background_includes_bad_pixels`` 16 ``includes_bad_pixels`` 17 "
            "``bad_shoebox`` 18 ``bad_spot`` 19 ``used_in_modelling`` 20 "
            "``centroid_outlier`` 21 ``failed_during_background_modelling`` 22 "
            "``failed_during_summation`` 23 ``failed_during_profile_fitting`` 24 "
            "``bad_reference`` === =========================================="
        ),
        a_nexus_field=NeXusField(
            name="flags",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    flags__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-flags-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="flags",
        ),
    )
    d = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-d-field"
        ],
        shape=["*"],
        description=("The resolution of the reflection"),
        a_nexus_field=NeXusField(
            name="d",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    d__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-d-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="d",
        ),
    )
    partiality = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-partiality-field"
        ],
        shape=["*"],
        description=(
            "The partiality of the reflection. Dividing by this number will "
            "inflate the measured intensity to the full reflection equivalent."
        ),
        a_nexus_field=NeXusField(
            name="partiality",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    partiality__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-partiality-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="partiality",
        ),
    )
    predicted_frame = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-frame-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The frame on which the bragg peak of the reflection is predicted"
        ),
        a_nexus_field=NeXusField(
            name="predicted_frame",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    predicted_frame__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-frame-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="predicted_frame",
        ),
    )
    predicted_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The x position at which the bragg peak of the reflection is predicted"
        ),
        a_nexus_field=NeXusField(
            name="predicted_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    predicted_x__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-x-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="predicted_x",
        ),
    )
    predicted_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The y position at which the bragg peak of the reflection is predicted"
        ),
        a_nexus_field=NeXusField(
            name="predicted_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    predicted_y__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-y-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="predicted_y",
        ),
    )
    predicted_phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-phi-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "The phi angle at which the bragg peak of the reflection is predicted"
        ),
        a_nexus_field=NeXusField(
            name="predicted_phi",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    predicted_phi__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-phi-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="predicted_phi",
        ),
    )
    predicted_px_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-px-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The x pixel position at which the bragg peak of the reflection is "
            "predicted"
        ),
        a_nexus_field=NeXusField(
            name="predicted_px_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    predicted_px_x__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-px-x-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="predicted_px_x",
        ),
    )
    predicted_px_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-px-y-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The y pixel position at which the bragg peak of the reflection is "
            "predicted"
        ),
        a_nexus_field=NeXusField(
            name="predicted_px_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    predicted_px_y__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-predicted-px-y-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="predicted_px_y",
        ),
    )
    observed_frame = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-frame-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The estimate of the frame at which the central impact of the "
            "reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_frame",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_frame__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-frame-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_frame",
        ),
    )
    observed_frame_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-frame-var-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The variance on the estimate of the frame at which the central "
            "impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_frame_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_frame_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-frame-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_frame_var",
        ),
    )
    observed_frame_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-frame-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the frame at which the "
            "central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_frame_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_frame_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-frame-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_frame_errors",
        ),
    )
    observed_px_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-x-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The estimate of the pixel x position at which the central impact of "
            "the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_px_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_px_x__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-x-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_px_x",
        ),
    )
    observed_px_x_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-x-var-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The variance on the estimate of the pixel x position at which the "
            "central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_px_x_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_px_x_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-x-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_px_x_var",
        ),
    )
    observed_px_x_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-x-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the pixel x position at "
            "which the central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_px_x_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_px_x_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-x-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_px_x_errors",
        ),
    )
    observed_px_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-y-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The estimate of the pixel y position at which the central impact of "
            "the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_px_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_px_y__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-y-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_px_y",
        ),
    )
    observed_px_y_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-y-var-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The variance on the estimate of the pixel y position at which the "
            "central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_px_y_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_px_y_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-y-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_px_y_var",
        ),
    )
    observed_px_y_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-y-errors-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the pixel y position at "
            "which the central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_px_y_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    observed_px_y_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-px-y-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_px_y_errors",
        ),
    )
    observed_phi = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-phi-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "The estimate of the phi angle at which the central impact of the "
            "reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_phi",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    observed_phi__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-phi-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_phi",
        ),
    )
    observed_phi_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-phi-var-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "The variance on the estimate of the phi angle at which the central "
            "impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_phi_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    observed_phi_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-phi-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_phi_var",
        ),
    )
    observed_phi_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-phi-errors-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the phi angle at which "
            "the central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_phi_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    observed_phi_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-phi-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_phi_errors",
        ),
    )
    observed_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The estimate of the x position at which the central impact of the "
            "reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    observed_x__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-x-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_x",
        ),
    )
    observed_x_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-x-var-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The variance on the estimate of the x position at which the central "
            "impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_x_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    observed_x_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-x-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_x_var",
        ),
    )
    observed_x_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-x-errors-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the x position at which "
            "the central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_x_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    observed_x_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-x-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_x_errors",
        ),
    )
    observed_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The estimate of the y position at which the central impact of the "
            "reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    observed_y__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-y-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_y",
        ),
    )
    observed_y_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-y-var-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The variance on the estimate of the y position at which the central "
            "impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_y_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    observed_y_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-y-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_y_var",
        ),
    )
    observed_y_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-y-errors-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the y position at which "
            "the central impact of the reflection was recorded"
        ),
        a_nexus_field=NeXusField(
            name="observed_y_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    observed_y_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-observed-y-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="observed_y_errors",
        ),
    )
    bounding_box = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-bounding-box-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 6],
        description=(
            "The bounding box around the recorded recorded reflection. Should be "
            "an integer array of length 6, where the 6 values are pixel "
            "positions or frame numbers, as follows: ===== "
            "=========================== index meaning ===== "
            "=========================== 0 The lower pixel x position 1 The "
            "upper pixel x position 2 The lower pixel y position 3 The upper "
            "pixel y position 4 The lower frame number 5 The upper frame number "
            "===== ==========================="
        ),
        a_nexus_field=NeXusField(
            name="bounding_box",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    bounding_box__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-bounding-box-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="bounding_box",
        ),
    )
    background_mean = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-background-mean-field"
        ],
        shape=["*"],
        description=("The mean background under the reflection peak"),
        a_nexus_field=NeXusField(
            name="background_mean",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    background_mean__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-background-mean-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="background_mean",
        ),
    )
    int_prf = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-prf-field"
        ],
        shape=["*"],
        description=("The estimate of the reflection intensity by profile fitting"),
        a_nexus_field=NeXusField(
            name="int_prf",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    int_prf__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-prf-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="int_prf",
        ),
    )
    int_prf_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-prf-var-field"
        ],
        shape=["*"],
        description=(
            "The variance on the estimate of the reflection intensity by profile "
            "fitting"
        ),
        a_nexus_field=NeXusField(
            name="int_prf_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    int_prf_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-prf-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="int_prf_var",
        ),
    )
    int_prf_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-prf-errors-field"
        ],
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the reflection intensity "
            "by profile fitting"
        ),
        a_nexus_field=NeXusField(
            name="int_prf_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    int_prf_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-prf-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="int_prf_errors",
        ),
    )
    int_sum = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-sum-field"
        ],
        shape=["*"],
        description=("The estimate of the reflection intensity by summation"),
        a_nexus_field=NeXusField(
            name="int_sum",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    int_sum__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-sum-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="int_sum",
        ),
    )
    int_sum_var = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-sum-var-field"
        ],
        shape=["*"],
        description=(
            "The variance on the estimate of the reflection intensity by summation"
        ),
        a_nexus_field=NeXusField(
            name="int_sum_var",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    int_sum_var__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-sum-var-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="int_sum_var",
        ),
    )
    int_sum_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-sum-errors-field"
        ],
        shape=["*"],
        description=(
            "The standard deviation of the estimate of the reflection intensity "
            "by summation"
        ),
        a_nexus_field=NeXusField(
            name="int_sum_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    int_sum_errors__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-int-sum-errors-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="int_sum_errors",
        ),
    )
    lp = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-lp-field"
        ],
        shape=["*"],
        description=(
            "The LP correction factor to be applied to the reflection intensities"
        ),
        a_nexus_field=NeXusField(
            name="lp",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    lp__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-lp-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="lp",
        ),
    )
    prf_cc = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-prf-cc-field"
        ],
        shape=["*"],
        description=(
            "The correlation of the reflection profile with the reference "
            "profile used in profile fitting"
        ),
        a_nexus_field=NeXusField(
            name="prf_cc",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    prf_cc__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-prf-cc-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="prf_cc",
        ),
    )
    overlaps = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-overlaps-field"
        ],
        description=(
            "An adjacency list specifying the spatial overlaps of reflections. "
            "The adjacency list is specified using an array data type where the "
            "elements of the array are the indices of the adjacent overlapped "
            "reflection"
        ),
        a_nexus_field=NeXusField(
            name="overlaps",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    overlaps__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-overlaps-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="overlaps",
        ),
    )
    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Polar angle of reflection centroid, following the NeXus simple "
            "(spherical polar) coordinate system"
        ),
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    polar_angle__description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-polar-angle-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="polar_angle",
        ),
    )
    azimuthal_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*"],
        description=(
            "Azimuthal angle of reflection centroid, following the NeXus simple "
            "(spherical polar) coordinate system"
        ),
        a_nexus_field=NeXusField(
            name="azimuthal_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXreflections.html#nxreflections-description-attribute"
        ],
        description=("Describes the dataset"),
        a_nexus_attribute=NeXusAttribute(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
