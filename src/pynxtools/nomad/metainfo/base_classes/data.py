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
# Run `pynx nomad generate-metainfo --nxdl NXdata` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    SchemaAnnotation,
)
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

__all__ = ["Data"]


class Data(Object, basesections.ActivityResult):
    """
    The :ref:`NXdata` class is designed to encapsulate all the information
    required for a set of data to be plotted. NXdata groups contain plottable
    data (also referred to as *signals* or *dependent variables*) and their
    associated axis coordinates (also referred to as *axes* or *independent
    variables*).

    The actual names of the :ref:`DATA </NXdata/DATA-field>` and :ref:`AXISNAME
    </NXdata/AXISNAME-field>` fields can be chosen :ref:`freely
    <validItemName>`, as indicated by the upper case (this is a common
    convention in all NeXus classes).

    .. note:: ``NXdata`` provides data and coordinates to be plotted but does
    not describe how the data is to be plotted or even the dimensionality of
    the plot.
    https://www.nexusformat.org/NIAC2018Minutes.html#nxdata-plottype--attribute

    .. include:: data/index.rst :start-line: 1

    .. admonition:: Example of a simple curve plot

    .. code-block::

    data:NXdata @signal = "data" @axes = ["x"] data: float[100] x: float[100]

    More complex cases are supported

    * histogram data: ``x`` has one more value than ``data``. * alternative
    axes: instead of a single ``x`` axis you can have several axes, one of
    which being the default. * signals with more than one dimension: ``data``
    could be 2D with axes ``x`` and ``y`` along each dimension. * axes with
    more than one dimension: ``data`` could be 2D with axes ``x`` and ``y``
    also being 2D, providing a unique ``(x, y)`` coordinate for each ``data``
    point.

    **Signals:**

    .. index:: plotting

    .. admonition:: Defined by

    * :ref:`DATA </NXdata/DATA-field>` fields * the :ref:`signal
    </NXdata@signal-attribute>` attribute * the
    :ref:`auxiliary_signals</NXdata@auxiliary_signals-attribute>` attribute

    The :ref:`DATA </NXdata/DATA-field>` fields contain the signal values to be
    plotted. The name of the field to be used as the *default plot signal* is
    provided by the :ref:`signal </NXdata@signal-attribute>` attribute. The
    names of the fields to be used as *secondary plot signals* are provided by
    the :ref:`auxiliary_signals</NXdata@auxiliary_signals-attribute>`
    attribute.

    .. admonition:: An example with three signals, one of which being the
    default

    .. code-block::

    data:NXdata @signal = "data1" @auxiliary_signals = ["data2", "data3"]
    data1: float[10,20,30] # the default signal data2: float[10,20,30] data3:
    float[10,20,30]

    **Axes:**

    .. index:: axes (attribute) .. index:: coordinates

    .. admonition:: Defined by

    * :ref:`AXISNAME </NXdata/AXISNAME-field>` fields * the :ref:`axes
    </NXdata@axes-attribute>` attribute * :ref:`AXISNAME_indices
    </NXdata@AXISNAME_indices-attribute>` attributes

    The fields and attributes are defined as follows

    1. The :ref:`AXISNAME </NXdata/AXISNAME-field>` fields contain the axis
    coordinates associated with the signal values.

    2. The :ref:`axes </NXdata@axes-attribute>` attribute provides the names of
    the :ref:`AXISNAME </NXdata/AXISNAME-field>` fields to be used as the
    `default axis` for each dimension of the :ref:`DATA </NXdata/DATA-field>`
    fields.

    3. The :ref:`AXISNAME_indices </NXdata@AXISNAME_indices-attribute>`
    attributes describe the :ref:`DATA </NXdata/DATA-field>` dimensions spanned
    by the corresponding :ref:`AXISNAME </NXdata/AXISNAME-field>` fields.

    The fields and attributes have the following constraints

    1. The length of the :ref:`axes </NXdata@axes-attribute>` attribute must be
    equal to the rank of the :ref:`DATA </NXdata/DATA-field>` fields. When a
    particular dimension has no default axis, the string “.” is used in that
    position.

    2. The number of values in :ref:`AXISNAME_indices
    </NXdata@AXISNAME_indices-attribute>` must be equal to the rank of the
    corresponding :ref:`AXISNAME </NXdata/AXISNAME-field>` field.

    3. When :ref:`AXISNAME_indices </NXdata@AXISNAME_indices-attribute>` is
    missing for a given :ref:`AXISNAME </NXdata/AXISNAME-field>` field, the
    positions of the :ref:`AXISNAME </NXdata/AXISNAME-field>` field name in the
    :ref:`axes </NXdata@axes-attribute>` attribute are used.

    4. When :ref:`AXISNAME_indices </NXdata@AXISNAME_indices-attribute>` is the
    same as the indices of "AXISNAME" in the :ref:`axes
    </NXdata@axes-attribute>` attribute, there is no need to provide
    :ref:`AXISNAME_indices </NXdata@AXISNAME_indices-attribute>`.

    5. The indices of "AXISNAME" in the :ref:`axes </NXdata@axes-attribute>`
    attribute must be a subset of :ref:`AXISNAME_indices
    </NXdata@AXISNAME_indices-attribute>`.

    6. The shape of an :ref:`AXISNAME </NXdata/AXISNAME-field>` field must
    correspond to the shape of the :ref:`DATA </NXdata/DATA-field>` dimensions
    it spans. This means that for each dimension ``i`` in ``[0,
    AXISNAME.ndim)`` spanned by axis field :ref:`AXISNAME
    </NXdata/AXISNAME-field>`, the number of axis values ``AXISNAME.shape[i]``
    along dimension ``i`` must be equal to the number of data points
    ``DATA.shape[AXISNAME_indices[i]]`` along dimension ``i`` or one more than
    the number of data points ``DATA.shape[AXISNAME_indices[i]]+1`` in case the
    :ref:`AXISNAME </NXdata/AXISNAME-field>` field contains histogram bin edges
    along dimension ``i``.

    Highlight consequences of these constraints

    1. An :ref:`AXISNAME </NXdata/AXISNAME-field>` field can have more than one
    dimension and can therefore span more than one :ref:`DATA
    </NXdata/DATA-field>` dimension. Conversely, one :ref:`DATA
    </NXdata/DATA-field>` dimension can be spanned by more than one
    :ref:`AXISNAME </NXdata/AXISNAME-field>` field. The default axis name (if
    any) of each dimension can be found in the :ref:`axes
    </NXdata@axes-attribute>` attribute.

    2. A list of all available axes is not provided directly. All strings in
    the :ref:`axes </NXdata@axes-attribute>` attribute (excluding the “.”
    string) are axis field names. In addition the prefix of an attribute ending
    with the string "_indices" is also an axis field name.

    .. admonition:: The following example covers all axes features supported
    (see :ref:`sphx_glr_classes_base_classes_data_plot_fscan2d.py`)

    .. code-block::

    data:NXdata @signal = "data" @axes = ["x_set", "y_set", "."] # default axes
    for all three dimensions @x_encoder_indices = [0, 1] @y_encoder_indices = 1
    # or [1] data: float[10,7,1024] x_encoder: float[11,7] # coordinates along
    the first and second dimensions y_encoder: float[7] # coordinates along the
    second dimension x_set: float[10] # default coordinates along the first
    dimension y_set: float[7] # default coordinates along the second dimension

    **Uncertainties:**

    .. admonition:: Defined by

    * :ref:`FIELDNAME_errors </NXdata/FIELDNAME_errors-field>` fields

    Standard deviations on data values as well as coordinates can be provided
    by :ref:`FIELDNAME_errors </NXdata/FIELDNAME_errors-field>` fields where
    ``FIELDNAME`` is the name of a :ref:`DATA </NXdata/DATA-field>` field or an
    :ref:`AXISNAME </NXdata/AXISNAME-field>` field.

    .. admonition:: An example of uncertainties on the signal, auxiliary
    signals and axis coordinates

    .. code-block::

    data:NXdata @signal = "data1" @auxiliary_signals = ["data2", "data3"] @axes
    = ["x", ".", "z"] data1: float[10,20,30] data2: float[10,20,30] data3:
    float[10,20,30] x: float[10] z: float[30] data1_errors: float[10,20,30]
    data2_errors: float[10,20,30] data3_errors: float[10,20,30] x_errors:
    float[10] z_errors: float[30]
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdata",
            category="base",
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
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-signal-attribute"
        ],
        description=(
            ".. index:: find the default plottable data .. index:: plotting .. "
            "index:: signal attribute value The value is the :ref:`name "
            "<validItemName>` of the signal that contains the default plottable "
            "data. This field or link *must* exist and be a direct child of this "
            "NXdata group. It is recommended (as of NIAC2014) to use this "
            "attribute rather than adding a signal attribute to the field. See "
            "https://www.nexusformat.org/2014_How_to_find_default_data.html for "
            "a summary of the discussion."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    auxiliary_signals = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-auxiliary-signals-attribute"
        ],
        description=(
            ".. index:: plotting Array of strings holding the :ref:`names "
            "<validItemName>` of additional signals to be plotted with the "
            ":ref:`default signal </NXdata@signal-attribute>`. These fields or "
            "links *must* exist and be direct children of this NXdata group. "
            "Each auxiliary signal needs to be of the same shape as the default "
            "signal. .. NIAC2018: "
            "https://www.nexusformat.org/NIAC2018Minutes.html"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="auxiliary_signals",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    default_slice = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-default-slice-attribute"
        ],
        description=(
            "Which slice of data to show in a plot by default. This is useful "
            "especially for datasets with more than 2 dimensions. Should be an "
            "array of length equal to the number of dimensions in the data, with "
            'the following possible values: * ".": All the data in this '
            "dimension should be included * Integer: Only this slice should be "
            "used. * String: Only this slice should be used. Use if ``AXISNAME`` "
            'is a string array. Example:: data:NXdata @signal = "data" @axes = '
            '["image_id", "channel", ".", "."] @image_id_indices = 0 '
            '@channel_indices = 1 @default_slice = [".", "difference", '
            '".", "."] image_id = [1, ..., nP] channel = ["threshold_1", '
            '"threshold_2", "difference"] data = uint[nP, nC, i, j] Here, a '
            "data array with four dimensions, including the number of images "
            "(nP) and number of channels (nC), specifies more dimensions than "
            "can be visualized with a 2D image viewer for a given image. "
            "Therefore the default_slice attribute specifies that the "
            '"difference" channel should be shown by default. Alternate '
            "version using an integer would look like this (note 2 is a "
            'string):: data:NXdata @signal = "data" @axes = ["image_id", '
            '"channel", ".", "."] @image_id_indices = 0 @channel_indices = '
            '1 @default_slice = [".", "2", ".", "."] image_id = [1, ..., '
            'nP] channel = ["threshold_1", "threshold_2", "difference"] '
            "data = uint[nP, nC, i, j]"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="default_slice",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    reference = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-reference-attribute"
        ],
        description=(
            "Points to the path of a field defining the data to which the `DATA` "
            "group refers. This concept allows to link the data to a respective "
            "field in the NeXus hierarchy, thereby defining the physical "
            "quantity it represents. Example: If the data corresponds to a "
            "readout of a detector, ``@reference`` links to that detectors data: "
            "@reference: '/entry/instrument/detector/data' for a 2D detector"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-indices-attribute"
        ],
        variable=True,
        description=(
            "The ``AXISNAME_indices`` attribute is a single integer or an array "
            "of integers that defines which :ref:`DATA </NXdata/DATA-field>` "
            "dimensions are spanned by the corresponding axis. The first "
            "dimension index is ``0`` (zero). The number of indices must be "
            "equal to the rank of the :ref:`AXISNAME </NXdata/AXISNAME-field>` "
            "field. When the ``AXISNAME_indices`` attribute is missing for a "
            "given :ref:`AXISNAME </NXdata/AXISNAME-field>` field, its value "
            "becomes the index (or indices) of the :ref:`AXISNAME "
            "</NXdata/AXISNAME-field>` name in the :ref:`axes "
            "</NXdata@axes-attribute>` attribute. .. note:: When "
            "``AXISNAME_indices`` contains multiple integers, it must be saved "
            "as an actual array of integers and not a comma separated string."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_INT",
            name_type="partial",
            optionality="optional",
        ),
    )
    axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axes-attribute"
        ],
        shape=["*"],
        description=(
            ".. index:: plotting The ``axes`` attribute is a list of strings "
            "which are the names of the :ref:`AXISNAME </NXdata/AXISNAME-field>` "
            "fields to be used as the default axis along every :ref:`DATA "
            "</NXdata/DATA-field>` dimension. As a result the length must be "
            "equal to the rank of the :ref:`DATA </NXdata/DATA-field>` fields. "
            'The string "." can be used for dimensions without a default axis. '
            ".. note:: When ``axes`` contains multiple strings, it must be saved "
            "as an actual array of strings and not a single comma separated "
            "string."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    AXISNAME = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-field"
        ],
        variable=True,
        description=(
            "Coordinate values along one or more :ref:`DATA "
            "</NXdata/DATA-field>` dimensions. The shape of an ``AXISNAME`` "
            "field must correspond to the shape of the :ref:`DATA "
            "</NXdata/DATA-field>` dimensions it spans. This means that for each "
            "``i`` in ``[0, AXISNAME.ndim)`` the number of data points "
            "``DATA.shape[AXISNAME_indices[i]]`` must be equal to the number of "
            "coordinates ``AXISNAME.shape[i]`` or the number of bin edges "
            "``AXISNAME.shape[i]+1`` in case of histogram data. As the upper "
            "case ``AXISNAME`` indicates, the names of the ``AXISNAME`` fields "
            "can be chosen :ref:`freely <validItemName>`. Most ``AXISNAME`` "
            "fields will be sequences of numbers but if an axis is better "
            "represented using names, such as channel names, an array of NX_CHAR "
            "can be provided."
        ),
        a_nexus_field=NeXusField(
            name="AXISNAME",
            type="NX_CHAR_OR_NUMBER",
            name_type="any",
            optionality="optional",
        ),
    )
    AXISNAME__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-long-name-attribute"
        ],
        description=("Axis label"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    AXISNAME__units = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-units-attribute"
        ],
        description=(
            "Unit in which the coordinate values are expressed. See the section "
            ":ref:`Design-Units` for more information."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    AXISNAME__distribution = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-distribution-attribute"
        ],
        description=("``0|false``: single value, ``1|true``: multiple values"),
        a_nexus_attribute=NeXusAttribute(
            name="distribution",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    AXISNAME__first_good = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-first-good-attribute"
        ],
        description=("Index of first good value"),
        a_nexus_attribute=NeXusAttribute(
            name="first_good",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    AXISNAME__last_good = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-last-good-attribute"
        ],
        description=("Index of last good value"),
        a_nexus_attribute=NeXusAttribute(
            name="last_good",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    AXISNAME__axis = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-axis-attribute"
        ],
        description=(
            "Index (positive integer) identifying this specific set of numbers. "
            "N.B. The ``axis`` attribute is the old way of designating a link. "
            "Do not use the :ref:`axes </NXdata@axes-attribute>` attribute with "
            "the ``axis`` attribute. The :ref:`axes </NXdata@axes-attribute>` "
            "attribute is now preferred."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axis",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
            deprecated="Use the group ``axes`` attribute   (NIAC2014)",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    AXISNAME__reference = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-axisname-reference-attribute"
        ],
        description=(
            "Points to the path of a field defining the axis to which the "
            "``AXISNAME`` axis refers. This concept allows to link an axis to a "
            "respective field in the NeXus hierarchy, thereby defining the "
            "physical quantity it represents. Examples: If a calibration has "
            "been performed, ``@reference`` links to the result of that "
            "calibration: @reference: "
            "'/entry/process/calibration/calibrated_axis' If the axis "
            "corresponds to a coordinate of a detector, ``@reference`` links to "
            "that detector axis: @reference: "
            "'/entry/instrument/detector/axis/some_axis' for a 2D detector If "
            "the axis is a scanned motor, ``@reference`` links to the "
            "transformation describing the respective motion, e.g.: @reference: "
            "'/entry/instrument/detector/transformations/some_transformation' "
            "for a motion of the detector"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="AXISNAME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    DATA = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-data-field"
        ],
        variable=True,
        description=(
            ".. index:: plotting Data values to be used as the NeXus *plottable "
            "data*. As the upper case ``DATA`` indicates, the names of the "
            "``DATA`` fields can be chosen :ref:`freely <validItemName>`. The "
            ":ref:`signal attribute </NXdata@signal-attribute>` and "
            ":ref:`auxiliary_signals "
            "attribute</NXdata@auxiliary_signals-attribute>` can be used to find "
            "all datasets in the ``NXdata`` that contain data values. The "
            "maximum rank is ``32`` for compatibility with backend file formats."
        ),
        a_nexus_field=NeXusField(
            name="DATA",
            type="NX_NUMBER",
            name_type="any",
            optionality="optional",
        ),
    )
    DATA__signal = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-data-signal-attribute"
        ],
        description=(
            ".. index:: plotting Plottable (independent) axis, indicate index "
            "number. Only one field in a :ref:`NXdata` group may have the "
            "``signal=1`` attribute. Do not use the ``signal`` attribute with "
            "the ``axis`` attribute."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
            deprecated="Use the group ``signal`` attribute   (NIAC2014)",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    DATA__axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-data-axes-attribute"
        ],
        description=(
            "Defines the names of the coordinates (independent axes) for this "
            "data set as a colon-delimited array. NOTE: The :ref:`axes "
            "</NXdata@axes-attribute>` attribute is the preferred method of "
            "designating a link. Do not use the :ref:`axes "
            "</NXdata@axes-attribute>` attribute with the ``axis`` attribute."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
            deprecated="Use the group ``axes`` attribute   (NIAC2014)",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    DATA__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-data-long-name-attribute"
        ],
        description=("data label"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    DATA__reference = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-data-reference-attribute"
        ],
        description=(
            "Points to the path of a field defining the data to which the `DATA` "
            "field refers. This concept allows to link the data to a respective "
            "field in the NeXus hierarchy, thereby defining the physical "
            "quantity it represents. Here, *DATA* is to be replaced by the name "
            "of each data field. Example: If the data corresponds to a readout "
            "of a detector, ``@reference`` links to that detectors data: "
            "@reference: '/entry/instrument/detector/data' for a 2D detector"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="reference",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="DATA",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    FIELDNAME_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-fieldname-errors-field"
        ],
        variable=True,
        description=(
            '"Errors" (meaning *uncertainties* or *standard deviations*) '
            "associated with any field named ``FIELDNAME`` in this ``NXdata`` "
            "group. This can be a :ref:`DATA </NXdata/DATA-field>` field (signal "
            "or auxiliary signal) or a :ref:`AXISNAME </NXdata/AXISNAME-field>` "
            "field (axis). The dimensions of the ``FIELDNAME_errors`` field must "
            "match the dimensions of the corresponding ``FIELDNAME`` field."
        ),
        a_nexus_field=NeXusField(
            name="FIELDNAME_errors",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-errors-field"
        ],
        description=(
            "Standard deviations of data values - the data array is identified "
            "by the group attribute ``signal``. The ``errors`` array must have "
            "the same dimensions as ``DATA``. Client is responsible for defining "
            "the dimensions of the data."
        ),
        a_nexus_field=NeXusField(
            name="errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            deprecated="Use ``DATA_errors`` instead (NIAC2018)",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    FIELDNAME_scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-fieldname-scaling-factor-field"
        ],
        variable=True,
        description=(
            "An optional scaling factor to apply to the values in any field "
            "named ``FIELDNAME`` in this ``NXdata`` group. This can be a "
            ":ref:`DATA </NXdata/DATA-field>` field (signal or auxiliary signal) "
            "or a :ref:`AXISNAME </NXdata/AXISNAME-field>` field (axis). The "
            "elements stored in NXdata datasets are often stored as integers for "
            "efficiency reasons and need further correction or conversion, "
            "generating floats. For example, raw values could be stored from a "
            "device that need to be converted to values that represent the "
            "physical values. The two fields FIELDNAME_scaling_factor and "
            "FIELDNAME_offset allow linear corrections using the following "
            "convention: .. code-block:: corrected values = (FIELDNAME + offset) "
            "* scaling_factor This formula will derive the values to use in "
            "downstream applications, when necessary. When omitted, the scaling "
            "factor is assumed to be 1."
        ),
        a_nexus_field=NeXusField(
            name="FIELDNAME_scaling_factor",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    FIELDNAME_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-fieldname-offset-field"
        ],
        variable=True,
        description=(
            "An optional offset to apply to the values in FIELDNAME (usually the "
            "signal). When omitted, the offset is assumed to be 0. See "
            ":ref:`FIELDNAME_scaling_factor "
            "</NXdata/FIELDNAME_scaling_factor-field>` for more information."
        ),
        a_nexus_field=NeXusField(
            name="FIELDNAME_offset",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    scaling_factor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-scaling-factor-field"
        ],
        description=(
            "The scaling_factor and FIELDNAME_scaling_factor fields have similar "
            "semantics. However, scaling_factor is ambiguous in the case of "
            "multiple signals. Therefore scaling_factor is deprecated. Use "
            "FIELDNAME_scaling_factor instead, even when only a single signal is "
            "present."
        ),
        a_nexus_field=NeXusField(
            name="scaling_factor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            deprecated="Use FIELDNAME_scaling_factor instead",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-offset-field"
        ],
        description=(
            "The offset and FIELDNAME_offset fields have similar semantics. "
            "However, offset is ambiguous in the case of multiple signals. "
            "Therefore offset is deprecated. Use FIELDNAME_offset instead, even "
            "when only a single signal is present."
        ),
        a_nexus_field=NeXusField(
            name="offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            deprecated="Use FIELDNAME_offset instead",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    title = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-title-field"
        ],
        description=("Title for the plot."),
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-x-field"
        ],
        shape=["*"],
        description=(
            "This is an array holding the values to use for the x-axis of data. "
            "The units must be appropriate for the measurement. This is a "
            "special case of a :ref:`AXISNAME field </NXdata/AXISNAME-field>` "
            "kept for backward compatibility."
        ),
        a_nexus_field=NeXusField(
            name="x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-y-field"
        ],
        shape=["*"],
        description=(
            "This is an array holding the values to use for the y-axis of data. "
            "The units must be appropriate for the measurement. This is a "
            "special case of a :ref:`AXISNAME field </NXdata/AXISNAME-field>` "
            "kept for backward compatibility."
        ),
        a_nexus_field=NeXusField(
            name="y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    z = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdata.html#nxdata-z-field"
        ],
        shape=["*"],
        description=(
            "This is an array holding the values to use for the z-axis of data. "
            "The units must be appropriate for the measurement. This is a "
            "special case of a :ref:`AXISNAME field </NXdata/AXISNAME-field>` "
            "kept for backward compatibility."
        ),
        a_nexus_field=NeXusField(
            name="z",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
