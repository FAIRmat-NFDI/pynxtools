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
# Run `pynx nomad generate-metainfo --nx-class NXdata` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.basesections import ActivityResult
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusGroup, NeXusQuantity

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Data"]


class Data(ActivityResult):
    """The :ref:`NXdata` class is designed to encapsulate all the information required for a set of data to be plotted.
    NXdata groups contain plottable data (also referred to as *signals* or *dependent variables*) and their
    associated axis coordinates (also referred to as *axes* or *independent variables*).

    The actual names of the :ref:`DATA </NXdata/DATA-field>` and :ref:`AXISNAME </NXdata/AXISNAME-field>` fields
    can be chosen :ref:`freely <validItemName>`, as indicated by the upper case (..."""

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            category="base",
            optionality="optional",
            ignore_extra_fields=True,
            ignore_extra_attributes=True,
            symbols={
                "dataRank": "rank of the ``DATA`` field(s)",
                "nx": "length of the ``x`` field",
                "ny": "length of the ``y`` field",
                "nz": "length of the ``z`` field",
            },
        ),
    )

    signal = Quantity(
        type=str,
        description=".. index:: find the default plottable data .. index:: plotting .. index:: signal attribute value The value is the :ref:`name <validItemName>` of the signal that contains the default plottable data. This field or link *must* exist and be a direct child of this NXdata group. It is recommended (as of NIAC2014) to use this attribute rather than adding a signal attribute to the field. See https://www.nexusformat.org/2014_How_to_find_default_data.html for a summary of the discussion.",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    auxiliary_signals = Quantity(
        type=str,
        description=".. index:: plotting Array of strings holding the :ref:`names <validItemName>` of additional signals to be plotted with the :ref:`default signal </NXdata@signal-attribute>`. These fields or links *must* exist and be direct children of this NXdata group. Each auxiliary signal needs to be of the same shape as the default signal. .. NIAC2018: https://www.nexusformat.org/NIAC2018Minutes.html",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="auxiliary_signals",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    default_slice = Quantity(
        type=np.float64,
        description='Which slice of data to show in a plot by default. This is useful especially for datasets with more than 2 dimensions. Should be an array of length equal to the number of dimensions in the data, with the following possible values: * ".": All the data in this dimension should be included * Integer: Only this slice should be used. * String: Only this slice should be used. Use if ``AXISNAME`` is a string array. Example:: data:NXdata @signal = "data" @axes = ["image_id", "channel", ".", "."] @image_id_indices = 0 @channel_indices = 1 @default_slice = [".", "difference", ".", "."] image_id = [1, ..., nP] channel = ["threshold_1", "threshold_2", "difference"] data = uint[nP, nC, i, j] Here, a data array with four dimensions, including the number of images (nP) and number of channels (nC), specifies more dimensions than can be visualized with a 2D image viewer for a given image. Therefore the default_slice attribute specifies that the "difference" channel should be shown by default. Alternate version using an integer would look like this (note 2 is a string):: data:NXdata @signal = "data" @axes = ["image_id", "channel", ".", "."] @image_id_indices = 0 @channel_indices = 1 @default_slice = [".", "2", ".", "."] image_id = [1, ..., nP] channel = ["threshold_1", "threshold_2", "difference"] data = uint[nP, nC, i, j]',
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="default_slice",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    reference = Quantity(
        type=str,
        description="Points to the path of a field defining the data to which the `DATA` group refers. This concept allows to link the data to a respective field in the NeXus hierarchy, thereby defining the physical quantity it represents. Example: If the data corresponds to a readout of a detector, ``@reference`` links to that detectors data: @reference: '/entry/instrument/detector/data' for a 2D detector",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        description="The ``AXISNAME_indices`` attribute is a single integer or an array of integers that defines which :ref:`DATA </NXdata/DATA-field>` dimensions are spanned by the corresponding axis. The first dimension index is ``0`` (zero). The number of indices must be equal to the rank of the :ref:`AXISNAME </NXdata/AXISNAME-field>` field. When the ``AXISNAME_indices`` attribute is missing for a given :ref:`AXISNAME </NXdata/AXISNAME-field>` field, its value becomes the index (or indices) of the :ref:`AXISNAME </NXdata/AXISNAME-field>` name in the :ref:`axes </NXdata@axes-attribute>` attribute. .. note:: When ``AXISNAME_indices`` contains multiple integers, it must be saved as an actual array of integers and not a comma separated string.",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="AXISNAME_indices",
            type="NX_INT",
            name_type="partial",
            optionality="optional",
        ),
    )
    axes = Quantity(
        type=str,
        shape=["*"],
        description='.. index:: plotting The ``axes`` attribute is a list of strings which are the names of the :ref:`AXISNAME </NXdata/AXISNAME-field>` fields to be used as the default axis along every :ref:`DATA </NXdata/DATA-field>` dimension. As a result the length must be equal to the rank of the :ref:`DATA </NXdata/DATA-field>` fields. The string "." can be used for dimensions without a default axis. .. note:: When ``axes`` contains multiple strings, it must be saved as an actual array of strings and not a single comma separated string.',
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    AXISNAME = Quantity(
        type=np.float64,
        description="Coordinate values along one or more :ref:`DATA </NXdata/DATA-field>` dimensions. The shape of an ``AXISNAME`` field must correspond to the shape of the :ref:`DATA </NXdata/DATA-field>` dimensions it spans. This means that for each ``i`` in ``[0, AXISNAME.ndim)`` the number of data points ``DATA.shape[AXISNAME_indices[i]]`` must be equal to the number of coordinates ``AXISNAME.shape[i]`` or the number of bin edges ``AXISNAME.shape[i]+1`` in case of histogram data. As the upper case ``AXISNAME`` indicates, the names of the ``AXISNAME`` fields can be chosen :ref:`freely <validItemName>`. Most ``AXISNAME`` fields will be sequences of numbers but if an axis is better represented using names, such as channel names, an array of NX_CHAR can be provided.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="AXISNAME",
            type="NX_CHAR_OR_NUMBER",
            name_type="any",
            optionality="optional",
        ),
    )
    AXISNAME__long_name = Quantity(
        type=str,
        description="Axis label",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__units = Quantity(
        type=str,
        description="Unit in which the coordinate values are expressed. See the section :ref:`Design-Units` for more information.",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__distribution = Quantity(
        type=bool,
        description="``0|false``: single value, ``1|true``: multiple values",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="distribution",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__first_good = Quantity(
        type=np.int64,
        description="Index of first good value",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="first_good",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__last_good = Quantity(
        type=np.int64,
        description="Index of last good value",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="last_good",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    AXISNAME__axis = Quantity(
        type=np.int64,
        description="Index (positive integer) identifying this specific set of numbers. N.B. The ``axis`` attribute is the old way of designating a link. Do not use the :ref:`axes </NXdata@axes-attribute>` attribute with the ``axis`` attribute. The :ref:`axes </NXdata@axes-attribute>` attribute is now preferred.",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="axis",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
            deprecated="Use the group ``axes`` attribute   (NIAC2014)",
        ),
    )
    AXISNAME__reference = Quantity(
        type=str,
        description="Points to the path of a field defining the axis to which the ``AXISNAME`` axis refers. This concept allows to link an axis to a respective field in the NeXus hierarchy, thereby defining the physical quantity it represents. Examples: If a calibration has been performed, ``@reference`` links to the result of that calibration: @reference: '/entry/process/calibration/calibrated_axis' If the axis corresponds to a coordinate of a detector, ``@reference`` links to that detector axis: @reference: '/entry/instrument/detector/axis/some_axis' for a 2D detector If the axis is a scanned motor, ``@reference`` links to the transformation describing the respective motion, e.g.: @reference: '/entry/instrument/detector/transformations/some_transformation' for a motion of the detector",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
    )
    DATA = Quantity(
        type=np.float64,
        description=".. index:: plotting Data values to be used as the NeXus *plottable data*. As the upper case ``DATA`` indicates, the names of the ``DATA`` fields can be chosen :ref:`freely <validItemName>`. The :ref:`signal attribute </NXdata@signal-attribute>` and :ref:`auxiliary_signals attribute</NXdata@auxiliary_signals-attribute>` can be used to find all datasets in the ``NXdata`` that contain data values. The maximum rank is ``32`` for compatibility with backend file formats.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="DATA",
            type="NX_NUMBER",
            name_type="any",
            optionality="optional",
        ),
    )
    DATA__signal = Quantity(
        type=np.int64,
        description=".. index:: plotting Plottable (independent) axis, indicate index number. Only one field in a :ref:`NXdata` group may have the ``signal=1`` attribute. Do not use the ``signal`` attribute with the ``axis`` attribute.",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="signal",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
            deprecated="Use the group ``signal`` attribute   (NIAC2014)",
        ),
    )
    DATA__axes = Quantity(
        type=str,
        description="Defines the names of the coordinates (independent axes) for this data set as a colon-delimited array. NOTE: The :ref:`axes </NXdata@axes-attribute>` attribute is the preferred method of designating a link. Do not use the :ref:`axes </NXdata@axes-attribute>` attribute with the ``axis`` attribute.",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
            deprecated="Use the group ``axes`` attribute   (NIAC2014)",
        ),
    )
    DATA__long_name = Quantity(
        type=str,
        description="data label",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
        ),
    )
    DATA__reference = Quantity(
        type=str,
        description="Points to the path of a field defining the data to which the `DATA` field refers. This concept allows to link the data to a respective field in the NeXus hierarchy, thereby defining the physical quantity it represents. Here, *DATA* is to be replaced by the name of each data field. Example: If the data corresponds to a readout of a detector, ``@reference`` links to that detectors data: @reference: '/entry/instrument/detector/data' for a 2D detector",
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
        ),
    )
    FIELDNAME_errors = Quantity(
        type=np.float64,
        description='"Errors" (meaning *uncertainties* or *standard deviations*) associated with any field named ``FIELDNAME`` in this ``NXdata`` group. This can be a :ref:`DATA </NXdata/DATA-field>` field (signal or auxiliary signal) or a :ref:`AXISNAME </NXdata/AXISNAME-field>` field (axis). The dimensions of the ``FIELDNAME_errors`` field must match the dimensions of the corresponding ``FIELDNAME`` field.',
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="FIELDNAME_errors",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    errors = Quantity(
        type=np.float64,
        description="Standard deviations of data values - the data array is identified by the group attribute ``signal``. The ``errors`` array must have the same dimensions as ``DATA``. Client is responsible for defining the dimensions of the data.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            deprecated="Use ``DATA_errors`` instead (NIAC2018)",
        ),
    )
    FIELDNAME_scaling_factor = Quantity(
        type=np.float64,
        description="An optional scaling factor to apply to the values in any field named ``FIELDNAME`` in this ``NXdata`` group. This can be a :ref:`DATA </NXdata/DATA-field>` field (signal or auxiliary signal) or a :ref:`AXISNAME </NXdata/AXISNAME-field>` field (axis). The elements stored in NXdata datasets are often stored as integers for efficiency reasons and need further correction or conversion, generating floats. For example, raw values could be stored from a device that need to be converted to values that represent the physical values. The two fields FIELDNAME_scaling_factor and FIELDNAME_offset allow linear corrections using the following convention: .. code-block:: corrected values = (FIELDNAME + offset) * scaling_factor This formula will derive the values to use in downstream applications, when necessary. When omitted, the scaling factor is assumed to be 1.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="FIELDNAME_scaling_factor",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    FIELDNAME_offset = Quantity(
        type=np.float64,
        description="An optional offset to apply to the values in FIELDNAME (usually the signal). When omitted, the offset is assumed to be 0. See :ref:`FIELDNAME_scaling_factor </NXdata/FIELDNAME_scaling_factor-field>` for more information.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="FIELDNAME_offset",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    scaling_factor = Quantity(
        type=np.float64,
        description="The scaling_factor and FIELDNAME_scaling_factor fields have similar semantics. However, scaling_factor is ambiguous in the case of multiple signals. Therefore scaling_factor is deprecated. Use FIELDNAME_scaling_factor instead, even when only a single signal is present.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="scaling_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            deprecated="Use FIELDNAME_scaling_factor instead",
        ),
    )
    offset = Quantity(
        type=np.float64,
        description="The offset and FIELDNAME_offset fields have similar semantics. However, offset is ambiguous in the case of multiple signals. Therefore offset is deprecated. Use FIELDNAME_offset instead, even when only a single signal is present.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            deprecated="Use FIELDNAME_offset instead",
        ),
    )
    title = Quantity(
        type=np.float64,
        description="Title for the plot.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="title",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    x = Quantity(
        type=np.float64,
        shape=["*"],
        description="This is an array holding the values to use for the x-axis of data. The units must be appropriate for the measurement. This is a special case of a :ref:`AXISNAME field </NXdata/AXISNAME-field>` kept for backward compatibility.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    y = Quantity(
        type=np.float64,
        shape=["*"],
        description="This is an array holding the values to use for the y-axis of data. The units must be appropriate for the measurement. This is a special case of a :ref:`AXISNAME field </NXdata/AXISNAME-field>` kept for backward compatibility.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    z = Quantity(
        type=np.float64,
        shape=["*"],
        description="This is an array holding the values to use for the z-axis of data. The units must be appropriate for the measurement. This is a special case of a :ref:`AXISNAME field </NXdata/AXISNAME-field>` kept for backward compatibility.",
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="z",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
