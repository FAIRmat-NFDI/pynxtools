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
# Run `pynx nomad generate-metainfo --nxdl NXcanSAS` to regenerate.
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
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.aperture import Aperture
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.collimator import Collimator
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.process import Process
from pynxtools.nomad.metainfo.base_classes.sample import Sample
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Cansas"]


class Cansas(Entry):
    """
    Implementation of the canSAS standard to store reduced small-angle
    scattering data of any dimension.

    .. index:: canSAS

    For more details, see:

    * http://www.cansas.org/ * http://www.cansas.org/formats/canSAS1d/1.1/doc/
    * http://cansas-org.github.io/canSAS2012/ *
    https://github.com/canSAS-org/NXcanSAS_examples

    The minimum requirements for *reduced* small-angle scattering data as
    described by canSAS are summarized in the following figure:

    .. _canSAS_2012_minimum:

    .. figure:: canSAS/2012-minimum.png :width: 60%

    The minimum requirements for *reduced* small-angle scattering data.
    (:download:`full image <canSAS/2012-minimum.png>`) See :ref:`below
    <NXcanSAS_minimum>` for the minimum required information for a NeXus data
    file written to the NXcanSAS specification.

    .. rubric:: Implementation of canSAS standard in NeXus

    This application definition is an implementation of the canSAS standard for
    storing both one-dimensional and multi-dimensional *reduced* small-angle
    scattering data.

    * NXcanSAS is for reduced SAS data and metadata to be stored together in
    one file. * *Reduced* SAS data consists of :math:`I(\vec{Q})` or
    :math:`I(|\vec{Q}|)` * External file links are not to be used for the
    reduced data. * A good practice is, at least, to include a reference to how
    the data was acquired and processed. Yet this is not a requirement. * There
    is no need for NXcanSAS to refer to any raw data.

    The canSAS data format has a structure similar to NeXus, not identical. To
    allow canSAS data to be expressed in NeXus, yet identifiable by the canSAS
    standard, an additional group attribute ``canSAS_class`` was introduced.
    Here is the mapping of some common groups.

    =============== ============ ========================== group (*) NX_class
    canSAS_class =============== ============ ==========================
    sasentry NXentry SASentry sasdata NXdata SASdata sasdetector NXdetector
    SASdetector sasinstrument NXinstrument SASinstrument sasnote NXnote SASnote
    sasprocess NXprocess SASprocess sasprocessnote NXcollection SASprocessnote
    sastransmission NXdata SAStransmission_spectrum sassample NXsample
    SASsample sassource NXsource SASsource =============== ============
    ==========================

    (*) The name of each group is a suggestion, not a fixed requirement and is
    chosen as fits each data file. See the section on defining :ref:`NXDL group
    and field names <RegExpName>`.

    Refer to the NeXus Coordinate System drawing
    (:ref:`Design-CoordinateSystem`) for choice and direction of :math:`x`,
    :math:`y`, and :math:`z` axes.

    .. _NXcanSAS_minimum:

    .. rubric:: The minimum required information for a NeXus data file written
    to the NXcanSAS specification.

    .. literalinclude:: canSAS/minimum-required.txt :tab-width: 4 :linenos:
    :language: text
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXcanSAS",
            category="application",
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasData",
        repeats=True,
        variable=True,
        description=(
            "A *SASData* group contains a single reduced small-angle scattering "
            "data set that can be represented as :math:`I(\\vec{Q})` or "
            ":math:`I(|\\vec{Q}|)`. *Q* can be either a vector "
            "(:math:`\\vec{Q}`) or a vector magnitude (:math:`|\\vec{Q}|`) The "
            "name of each *SASdata* group must be unique within a SASentry "
            "group. Suggest using names such as ``sasdata01``. NOTE: For the "
            "first *SASdata* group, be sure to write the chosen name into the "
            "`SASentry/@default` attribute, as in:: "
            'SASentry/@default="sasdata01" A *SASdata* group has several '
            "attributes: * I_axes * Q_indices * Mask_indices To indicate the "
            "dependency relationships of other varied parameters, use attributes "
            "similar to ``@Mask_indices`` (such as ``@Temperature_indices`` or "
            "``@Pressure_indices``)."
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasInstrument",
        repeats=True,
        variable=True,
        description=(
            "Description of the small-angle scattering instrument. Consider, "
            "carefully, the relevance to the SAS data analysis process when "
            "adding subgroups in this **NXinstrument** group. Additional "
            "information can be added but will likely be ignored by standardized "
            "data analysis processes. The NeXus :ref:`NXbeam` base class may be "
            "added as a subgroup of this **NXinstrument** group *or* as a "
            "subgroup of the **NXsample** group to describe properties of the "
            "beam at any point downstream from the source."
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasSample",
        repeats=True,
        variable=True,
        description=("Description of the sample."),
    )
    process = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasProcess",
        repeats=True,
        variable=True,
        description=(
            "Description of a processing or analysis step. Add additional fields "
            "as needed to describe value(s) of any variable, parameter, or term "
            "related to the *SASprocess* step. Be sure to include *units* "
            "attributes for all numerical fields."
        ),
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasCollection",
        repeats=True,
        variable=True,
        description=(
            "Free form description of anything not covered by other elements."
        ),
    )

    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-default-attribute"
        ],
        description=(
            ".. index:: plotting Declares which :ref:`NXdata` group contains the "
            "data to be shown by default. It is needed to resolve ambiguity when "
            "more than one :ref:`NXdata` group exists. The value is the name of "
            "the default :ref:`NXdata` group. Usually, this will be the name of "
            "the first *SASdata* group."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    canSAS_class = Quantity(
        type=MEnum(["SASentry"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-cansas-class-attribute"
        ],
        description=("Official canSAS group: **SASentry**"),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASentry"],
        ),
    )
    version = Quantity(
        type=MEnum(["1.1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-version-attribute"
        ],
        description=(
            "Describes the version of the canSAS standard used to write this "
            "data. This must be a text (not numerical) representation. Such as:: "
            '@version="1.1"'
        ),
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["1.1"],
        ),
    )
    definition = Quantity(
        type=MEnum(["NXcanSAS"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this subentry conforms."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXcanSAS"],
        ),
    )
    definition__name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-definition-name-attribute"
        ],
        description=(
            "Optional string attribute to identify this particular *run*. Could "
            "use this to associate (correlate) multiple *SASdata* elements with "
            "*run* elements."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="definition",
        ),
    )
    title = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-title-field"
        ],
        description=(
            "Title of this *SASentry*. Make it so that you can recognize the "
            "data by its title. Could be the name of the sample, the name for "
            "the measured data, or something else representative."
        ),
        a_nexus_field=NeXusField(
            name="title",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    title__name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-title-name-attribute"
        ],
        description=(
            "Optional string attribute to identify this particular *run*. Could "
            "use this to associate (correlate) multiple *SASdata* elements with "
            "*run* elements."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="title",
        ),
    )
    run = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-run-field"
        ],
        variable=True,
        description=(
            "Run identification for this *SASentry*. For many facilities, this "
            "is an integer, such as en experiment number. Use multiple instances "
            "of ``run`` as needed, keeping in mind that HDF5 requires unique "
            "names for all entities in a group."
        ),
        a_nexus_field=NeXusField(
            name="run",
            type="NX_CHAR",
            name_type="any",
            optionality="required",
        ),
    )
    run__name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-run-name-attribute"
        ],
        description=(
            "Optional string attribute to identify this particular *run*. Could "
            "use this to associate (correlate) multiple *SASdata* elements with "
            "*run* elements."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="run",
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


class CansasData(Data):
    """
    A *SASData* group contains a single reduced small-angle scattering data set
    that can be represented as :math:`I(\vec{Q})` or :math:`I(|\vec{Q}|)`.

    *Q* can be either a vector (:math:`\vec{Q}`) or a vector magnitude
    (:math:`|\vec{Q}|`)

    The name of each *SASdata* group must be unique within a SASentry group.
    Suggest using names such as ``sasdata01``.

    NOTE: For the first *SASdata* group, be sure to write the chosen name into
    the `SASentry/@default` attribute, as in::

    SASentry/@default="sasdata01"

    A *SASdata* group has several attributes:

    * I_axes * Q_indices * Mask_indices

    To indicate the dependency relationships of other varied parameters, use
    attributes similar to ``@Mask_indices`` (such as ``@Temperature_indices``
    or ``@Pressure_indices``).
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASdata"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASdata`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASdata"],
        ),
    )
    signal = Quantity(
        type=MEnum(["I"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-signal-attribute"
        ],
        description=("Name of the default data field."),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["I"],
        ),
    )
    I_axes = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-i-axes-attribute"
        ],
        description=(
            "String array that defines the independent data fields used in the "
            "default plot for all of the dimensions of the *signal* field (the "
            "*signal* field is the field in this group that is named by the "
            "``signal`` attribute of this group). One entry is provided for "
            "every dimension of the ``I`` data object. Such as:: "
            '@I_axes="Temperature", "Time", "Pressure", "Q", "Q" Since '
            "there are five items in the list, the intensity field of this "
            "example ``I`` must be a five-dimensional array (rank=5)."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="I_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    Q_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-q-indices-attribute"
        ],
        description=(
            "Integer or integer array that describes which indices (of the "
            ":math:`I` data object) are used to reference the ``Q`` data object. "
            "The items in this array use zero-based indexing. Such as:: "
            "@Q_indices=1,3,4 which indicates that ``Q`` requires three indices "
            "from the :math:`I` data object: one for time and two for Q "
            "position. Thus, in this example, the ``Q`` data is time-dependent: "
            ":math:`\\vec{Q}(t)`."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="Q_indices",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
    )
    mask = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-mask-attribute"
        ],
        description=(
            "Name of the data mask field. .. see: "
            "https://github.com/nexusformat/definitions/issues/533 The data "
            "*mask* must have the same shape as the *data* field. Positions in "
            "the mask correspond to positions in the *data* field. The value of "
            "the mask field may be either a boolean array where ``false`` means "
            "*no mask* and ``true`` means *mask* or a more descriptive array as "
            "as defined in :ref:`NXdetector`."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="mask",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    Mask_indices = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-mask-indices-attribute"
        ],
        description=(
            "Integer or integer array that describes which indices (of the "
            ":math:`I` data object) are used to reference the ``Mask`` data "
            "object. The items in this array use zero-based indexing. Such as:: "
            "@Mask_indices=3,4 which indicates that Q requires two indices from "
            "the :math:`I` data object for Q position."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="Mask_indices",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    timestamp = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-timestamp-attribute"
        ],
        description=("ISO-8601 time [#iso8601]_"),
        a_nexus_attribute=NeXusAttribute(
            name="timestamp",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    Q = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-q-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            ".. index:: NXcanSAS (applications); Q Array of :math:`Q` data to "
            "accompany :math:`I`. .. figure:: canSAS/Q-geometry.jpg :width: 60% "
            "The :math:`\\vec{Q}` geometry. (:download:`full image "
            "<canSAS/Q-geometry.jpg>`) :math:`Q` may be represented as either "
            "the three-dimensional scattering vector :math:`\\vec{Q}` or the "
            "magnitude of the scattering vector, :math:`|\\vec{Q}|`. .. math:: "
            "|\\vec{Q}| = (4\\pi/\\lambda) sin(\\theta) When we write :math:`Q`, "
            "we may refer to either or both of :math:`|\\vec{Q}|` or "
            ":math:`\\vec{Q}`, depending on the context."
        ),
        a_nexus_field=NeXusField(
            name="Q",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_PER_LENGTH",
        ),
    )
    Q__units = Quantity(
        type=MEnum(["1/m", "1/nm", "1/angstrom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-q-units-attribute"
        ],
        description=(
            "Engineering units to use when expressing :math:`Q` and related "
            "terms. Data expressed in other units will generate a warning from "
            "validation software and may not be processed by some analysis "
            "software packages."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="Q",
            enumeration=["1/m", "1/nm", "1/angstrom"],
        ),
    )
    Q__uncertainties = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-q-uncertainties-attribute"
        ],
        description=(
            "(optional: for numerical arrays) Names the dataset (in this SASdata "
            "group) that provides the uncertainty to be used for data analysis. "
            "The name of the dataset containing the :math:`Q` uncertainty is "
            "flexible. The name must be unique in the *SASdata* group. .. "
            "comment see: https://github.com/canSAS-org/canSAS2012/issues/7 Such "
            'as:: @uncertainties="Q_uncertainties" The *uncertainties* field '
            "will have the same *shape* (dimensions) as the Q field. These "
            "values are the estimates of uncertainty of each Q. By default, this "
            "will be interpreted to be the estimated standard deviation. In "
            "special cases, when a standard deviation cannot possibly be used, "
            "its value can specify another measure of distribution width. There "
            "may also be a subdirectory (optional) with constituent components. "
            ".. note:: To report distribution in reported :math:`Q` values, use "
            "the ``@resolutions`` attribute. It is possible for both "
            "``@resolutions`` and ``uncertainties`` to be reported."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="uncertainties",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="Q",
        ),
    )
    Q__resolutions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-q-resolutions-attribute"
        ],
        description=(
            ".. index:: NXcanSAS (applications); resolutions (optional: for "
            "numerical arrays) Names the dataset (in this SASdata group) "
            "containing the :math:`Q` resolution. The name of the dataset "
            "containing the :math:`Q` resolution is flexible. The name must be "
            "unique in the *SASdata* group. .. comment see: "
            "https://github.com/canSAS-org/canSAS2012/issues/7 The *resolutions* "
            "field will have the same *shape* (dimensions) as the Q field. "
            "Generally, this is the principal resolution of each :math:`Q`. "
            "Names the data object (in this SASdata group) that provides the "
            ":math:`Q` resolution to be used for data analysis. Such as:: "
            '@resolutions="Qdev" To specify two-dimensional resolution for '
            "slit-smearing geometry, such as (*dQw*, *dQl*), use a string array, "
            'such as:: @resolutions="dQw", "dQl" There may also be a '
            "subdirectory (optional) with constituent components. This pattern "
            "will demonstrate how to introduce further as-yet unanticipated "
            "terms related to the data. .. comment see: "
            "https://github.com/nexusformat/definitions/issues/492#issuecomment-262813907 "
            "By default, the values of the resolutions data object are assumed "
            "to be one standard deviation of any function used to approximate "
            "the resolution function. This equates to the width of the gaussian "
            "distribution if a Gaussian is chosen. See the "
            "``@resolutions_description`` attribute. .. note:: To report "
            "uncertainty in reported :math:`Q` values, use the "
            "``@uncertainties`` attribute. It is possible for both "
            "``@resolutions`` and ``uncertainties`` to be reported."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="resolutions",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="Q",
        ),
    )
    Q__resolutions_description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-q-resolutions-description-attribute"
        ],
        description=(
            "(optional) Generally, this describes the :math:`Q` ``@resolutions`` "
            'data object. By default, the value is assumed to be "Gaussian". '
            "These are suggestions: * Gaussian * Lorentzian * Square : note that "
            "the full width of the square would be ~2.9 times the standard "
            "deviation specified in the vector * Triangular * Sawtooth-outward : "
            "vertical edge pointing to larger Q * Sawtooth-inward vertical edge "
            "pointing to smaller Q * Bin : range of values contributing (for "
            "example, when 2-D detector data have been reduced to a 1-D "
            ":math:`I(|Q|)` dataset) For other meanings, it may be necessary to "
            "provide further details such as the function used to assess the "
            "resolution. In such cases, use additional datasets or a "
            ":ref:`NXnote` subgroup to include that detail."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="resolutions_description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="Q",
        ),
    )
    I = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-i-field"
        ],
        description=(
            ".. index:: NXcanSAS (applications); I Array of intensity "
            "(:math:`I`) data. The intensity may be represented in one of these "
            "forms: **absolute units**: :math:`d\\Sigma/d\\Omega(Q)` "
            "differential cross-section per unit volume per unit solid angle "
            "(such as: 1/cm/sr or 1/m/sr) **absolute units**: "
            ":math:`d\\sigma/d\\Omega(Q)` differential cross-section per unit "
            "atom per unit solid angle (such as: cm^2 or m^2) **arbitrary "
            "units**: :math:`I(Q)` usually a ratio of two detectors but units "
            "are meaningless (such as: a.u. or counts) This presents a few "
            "problems for analysis software to sort out when reading the data. "
            "Fortunately, it is possible to analyze the *units* to determine "
            "which type of intensity is being reported and make choices at the "
            "time the file is read. But this is an area for consideration and "
            "possible improvement. One problem arises with software that "
            "automatically converts data into some canonical units used by that "
            "software. The software should not convert units between these "
            "different types of intensity indiscriminately. A second problem is "
            "that when arbitrary units are used, then the set of possible "
            "analytical results is restricted. With such units, no meaningful "
            "volume fraction or number density can be determined directly from "
            ":math:`I(Q)`. In some cases, it is possible to apply a factor to "
            "convert the arbitrary units to an absolute scale. This should be "
            "considered as a possibility of the analysis process. Where this "
            "documentation says *typical units*, it is possible that small-angle "
            "data may be presented in other units and still be consistent with "
            "NeXus. See the :ref:`design-units` section."
        ),
        a_nexus_field=NeXusField(
            name="I",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
        ),
    )
    I__units = Quantity(
        type=MEnum(["1/m", "1/cm", "m2/g", "cm2/g", "arbitrary"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-i-units-attribute"
        ],
        description=(
            "Engineering units to use when expressing :math:`I` and "
            "intensity-related terms. Data expressed in other units (or missing "
            "a ``@units`` attribute) will be treated as ``arbitrary`` by some "
            "software packages. For software using the UDUNITS-2 library, "
            "``arbitrary`` will be changed to ``unknown`` for handling with that "
            "library."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="I",
            enumeration=["1/m", "1/cm", "m2/g", "cm2/g", "arbitrary"],
        ),
    )
    I__uncertainties = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-i-uncertainties-attribute"
        ],
        description=(
            "(optional: for numerical arrays) Names the dataset (in this SASdata "
            "group) that provides the uncertainty of :math:`I` to be used for "
            "data analysis. The name of the dataset containing the :math:`I` "
            "uncertainty is flexible. The name must be unique in the *SASdata* "
            "group. .. comment see: "
            "https://github.com/canSAS-org/canSAS2012/issues/7 Generally, this "
            "is the estimate of the uncertainty of each :math:`I`. Typically the "
            "estimated standard deviation. *Idev* is the canonical name from the "
            "1D standard. The NXcanSAS standard allows for the name to be "
            'described using this attribute. Such as:: @uncertainties="Idev"'
        ),
        a_nexus_attribute=NeXusAttribute(
            name="uncertainties",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="I",
        ),
    )
    I__scaling_factor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-i-scaling-factor-attribute"
        ],
        description=(
            "(optional) Names the field (a.k.a. dataset) that contains a factor "
            "to multiply ``I``. By default, this value is unity. Should an "
            "uncertainty be associated with the scaling factor field, the field "
            "containing that uncertainty would be designated via the "
            "``uncertainties`` attribute. Such as:: I : NX_NUMBER "
            '@uncertainties="Idev" : NX_CHAR @scaling_factor="I_scaling" : '
            "NX_CHAR Idev : NX_NUMBER I_scaling : NX_NUMBER "
            '@uncertainties="I_scaling_dev" : NX_CHAR I_scaling_dev : '
            "NX_NUMBER The exact names for ``I_scaling`` and ``I_scaling_dev`` "
            "are not defined by NXcanSAS. The user has the flexibility to use "
            "names different than those shown in this example."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="scaling_factor",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="I",
        ),
    )
    Idev = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-idev-field"
        ],
        description=(
            ".. index:: NXcanSAS (applications); Idev Estimated **uncertainty** "
            "(usually standard deviation) in :math:`I`. Must have the same units "
            "as :math:`I`. When present, the name of this field is also recorded "
            "in the *uncertainties* attribute of *I*, as in:: "
            'I/@uncertainties="Idev"'
        ),
        a_nexus_field=NeXusField(
            name="Idev",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    Idev__units = Quantity(
        type=MEnum(["1/m", "1/cm", "m2/g", "cm2/g", "arbitrary"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-idev-units-attribute"
        ],
        description=(
            "Engineering units to use when expressing :math:`I` and "
            "intensity-related terms. Data expressed in other units (or missing "
            "a ``@units`` attribute) will generate a warning from any validation "
            "process and will be treated as ``arbitrary`` by some analysis "
            "software packages. For software using the UDUNITS-2 library, "
            "``arbitrary`` will be changed to ``unknown`` for handling with that "
            "library."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="Idev",
            enumeration=["1/m", "1/cm", "m2/g", "cm2/g", "arbitrary"],
        ),
    )
    Qdev = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-qdev-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            ".. index:: NXcanSAS (applications); Qdev Estimated :math:`Q` "
            "**resolution** (usually standard deviation). Must have the same "
            "units as :math:`Q`. When present, the name of this field is also "
            "recorded in the *resolutions* attribute of *Q*, as in:: "
            'Q/@resolutions="Qdev" or:: Q/@resolutions="dQw", "dQl"'
        ),
        a_nexus_field=NeXusField(
            name="Qdev",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
    )
    Qdev__units = Quantity(
        type=MEnum(["1/m", "1/nm", "1/angstrom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-qdev-units-attribute"
        ],
        description=(
            "Engineering units to use when expressing :math:`Q` and related "
            "terms. Data expressed in other units may not be processed by some "
            "software packages."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="Qdev",
            enumeration=["1/m", "1/nm", "1/angstrom"],
        ),
    )
    dQw = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-dqw-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            ".. index:: NXcanSAS (applications); dQw :math:`Q` **resolution** "
            "along the axis of scanning (the high-resolution *slit width* "
            "direction). Useful for defining resolution data from slit-smearing "
            "instruments such as Bonse-Hart geometry. Must have the same units "
            "as :math:`Q`. When present, the name of this field is also recorded "
            "in the *resolutions* attribute of *Q*, as in:: "
            'Q/@resolutions="dQw", "dQl"'
        ),
        a_nexus_field=NeXusField(
            name="dQw",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
    )
    dQw__units = Quantity(
        type=MEnum(["1/m", "1/nm", "1/angstrom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-dqw-units-attribute"
        ],
        description=(
            "Engineering units to use when expressing :math:`Q` and related "
            "terms. Data expressed in other units may not be processed by some "
            "software packages."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="dQw",
            enumeration=["1/m", "1/nm", "1/angstrom"],
        ),
    )
    dQl = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-dql-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            ".. index:: NXcanSAS (applications); dQl :math:`Q` **resolution** "
            "perpendicular to the axis of scanning (the low-resolution *slit "
            "length* direction). Useful for defining resolution data from "
            "slit-smearing instruments such as Bonse-Hart geometry. Must have "
            "the same units as :math:`Q`. When present, the name of this field "
            "is also recorded in the *resolutions* attribute of *Q*, as in:: "
            'Q/@resolutions="dQw", "dQl"'
        ),
        a_nexus_field=NeXusField(
            name="dQl",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
    )
    dQl__units = Quantity(
        type=MEnum(["1/m", "1/nm", "1/angstrom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-dql-units-attribute"
        ],
        description=(
            "Engineering units to use when expressing :math:`Q` and related "
            "terms. Data expressed in other units may not be processed by some "
            "software packages."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="dQl",
            enumeration=["1/m", "1/nm", "1/angstrom"],
        ),
    )
    Qmean = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-qmean-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Mean value of :math:`Q` for this data point. Useful when describing "
            "data that has been binned from higher-resolution data. It is "
            "expected that ``Q`` is provided and that both ``Q`` and ``Qmean`` "
            "will have the same units."
        ),
        a_nexus_field=NeXusField(
            name="Qmean",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
    )
    Qmean__units = Quantity(
        type=MEnum(["1/m", "1/nm", "1/angstrom"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-qmean-units-attribute"
        ],
        description=(
            "Engineering units to use when expressing :math:`Q` and related "
            "terms. Data expressed in other units may not be processed by some "
            "software packages."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="units",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="Qmean",
            enumeration=["1/m", "1/nm", "1/angstrom"],
        ),
    )
    ShadowFactor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-data-shadowfactor-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "A numerical factor applied to pixels affected by the beam stop "
            "penumbra. Used in data files from NIST/NCNR instruments. See: J.G. "
            "Barker and J.S. Pedersen (1995) *J. Appl. Cryst.* **28**, 105-114."
        ),
        a_nexus_field=NeXusField(
            name="ShadowFactor",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasInstrument(Instrument):
    """
    Description of the small-angle scattering instrument.

    Consider, carefully, the relevance to the SAS data analysis process when
    adding subgroups in this **NXinstrument** group. Additional information can
    be added but will likely be ignored by standardized data analysis
    processes.

    The NeXus :ref:`NXbeam` base class may be added as a subgroup of this
    **NXinstrument** group *or* as a subgroup of the **NXsample** group to
    describe properties of the beam at any point downstream from the source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasInstrumentAperture",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    collimator = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasInstrumentCollimator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollimator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasInstrumentDetector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasInstrumentSource",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASinstrument"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASinstrument`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASinstrument"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasInstrumentAperture(Aperture):
    """
    :ref:`NXaperture` is generic and limits the variation in data files.

    Possible NeXus base class alternatives are: :ref:`NXpinhole` or
    :ref:`NXslit`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-aperture-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASaperture"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-aperture-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASaperture`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASaperture"],
        ),
    )
    shape = Quantity(
        type=MEnum(
            [
                "straight slit",
                "curved slit",
                "pinhole",
                "circle",
                "square",
                "hexagon",
                "octagon",
                "bladed",
                "open",
                "grid",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-aperture-shape-field"
        ],
        description=(
            "describe the type of aperture (pinhole, 4-blade slit, Soller slit, ...)"
        ),
        a_nexus_field=NeXusField(
            name="shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "straight slit",
                "curved slit",
                "pinhole",
                "circle",
                "square",
                "hexagon",
                "octagon",
                "bladed",
                "open",
                "grid",
            ],
        ),
    )
    x_gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-aperture-x-gap-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("opening along the :math:`x` axis"),
        a_nexus_field=NeXusField(
            name="x_gap",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y_gap = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-aperture-y-gap-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("opening along the :math:`y` axis"),
        a_nexus_field=NeXusField(
            name="y_gap",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasInstrumentCollimator(Collimator):
    """
    Description of a collimating element (defines the divergence of the beam)
    in the instrument.

    To document a slit, pinhole, or the beam, refer to the documentation of the
    ``NXinstrument`` group above.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-collimator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollimator",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SAScollimation"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-collimator-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SAScollimation`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SAScollimation"],
        ),
    )
    length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-collimator-length-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Amount/length of collimation inserted (as on a SANS instrument)"),
        a_nexus_field=NeXusField(
            name="length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-collimator-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Distance from this collimation element to the sample"),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasInstrumentDetector(Detector):
    """
    Description of a detector in the instrument.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASdetector"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASdetector`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASdetector"],
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-name-field"
        ],
        description=("Identifies the name of this detector"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    SDD = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-sdd-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Distance between sample and detector. Note: In NXdetector, the "
            "``distance`` field records the distance to the previous component "
            "... most often the sample. This use is the same as ``SDD`` for most "
            "SAS instruments but not all. For example, Bonse-Hart cameras have "
            "one or more crystals between the sample and detector. We define "
            "here the field ``SDD`` to document without ambiguity the distance "
            "between sample and detector."
        ),
        a_nexus_field=NeXusField(
            name="SDD",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    slit_length = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-slit-length-field"
        ],
        dimensionality="1 / [length]",
        unit="1 / m",
        description=(
            "Slit length of the instrument for this detector, expressed in the "
            "same units as :math:`Q`."
        ),
        a_nexus_field=NeXusField(
            name="slit_length",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_PER_LENGTH",
        ),
    )
    x_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-x-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Location of the detector in :math:`x`"),
        a_nexus_field=NeXusField(
            name="x_position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-y-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Location of the detector in :math:`y`"),
        a_nexus_field=NeXusField(
            name="y_position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    roll = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-roll-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation of the detector about the :math:`z` axis (roll)"),
        a_nexus_field=NeXusField(
            name="roll",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    pitch = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-pitch-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation of the detector about the :math:`x` axis (roll)"),
        a_nexus_field=NeXusField(
            name="pitch",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    yaw = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-detector-yaw-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation of the detector about the :math:`y` axis (yaw)"),
        a_nexus_field=NeXusField(
            name="yaw",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasInstrumentSource(Source):
    """
    Description of the radiation source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASsource"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASsource`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASsource"],
        ),
    )
    radiation = Quantity(
        type=MEnum(
            [
                "Spallation Neutron Source",
                "Pulsed Reactor Neutron Source",
                "Reactor Neutron Source",
                "Synchrotron X-ray Source",
                "Pulsed Muon Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "UV Laser",
                "Free-Electron Laser",
                "Optical Laser",
                "Ion Source",
                "UV Plasma Source",
                "neutron",
                "x-ray",
                "muon",
                "electron",
                "ultraviolet",
                "visible light",
                "positron",
                "proton",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-radiation-field"
        ],
        description=(
            "Name of the radiation used. Note that this is **not** the name of "
            "the facility! This field contains a value from either the ``probe`` "
            "or ``type`` fields in :ref:`NXsource`. Thus, it is redundant with "
            "existing NeXus structure."
        ),
        a_nexus_field=NeXusField(
            name="radiation",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "Spallation Neutron Source",
                "Pulsed Reactor Neutron Source",
                "Reactor Neutron Source",
                "Synchrotron X-ray Source",
                "Pulsed Muon Source",
                "Rotating Anode X-ray",
                "Fixed Tube X-ray",
                "UV Laser",
                "Free-Electron Laser",
                "Optical Laser",
                "Ion Source",
                "UV Plasma Source",
                "neutron",
                "x-ray",
                "muon",
                "electron",
                "ultraviolet",
                "visible light",
                "positron",
                "proton",
            ],
            deprecated="Use either (or both) ``probe`` or ``type`` fields from ``NXsource`` (issue #765)",
        ),
    )
    beam_shape = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-beam-shape-field"
        ],
        description=(
            "Text description of the shape of the beam (incident on the sample)."
        ),
        a_nexus_field=NeXusField(
            name="beam_shape",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    incident_wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-incident-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "wavelength (:math:`\\lambda`) of radiation incident on the sample"
        ),
        a_nexus_field=NeXusField(
            name="incident_wavelength",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    wavelength_min = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-wavelength-min-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Some facilities specify wavelength using a range. This is the "
            "lowest wavelength in such a range."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_min",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    wavelength_max = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-wavelength-max-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Some facilities specify wavelength using a range. This is the "
            "highest wavelength in such a range."
        ),
        a_nexus_field=NeXusField(
            name="wavelength_max",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    incident_wavelength_spread = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-incident-wavelength-spread-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Some facilities specify wavelength using a range. This is the width "
            "(FWHM) of such a range."
        ),
        a_nexus_field=NeXusField(
            name="incident_wavelength_spread",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )
    beam_size_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-beam-size-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Size of the incident beam along the x axis."),
        a_nexus_field=NeXusField(
            name="beam_size_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    beam_size_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-instrument-source-beam-size-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Size of the incident beam along the y axis."),
        a_nexus_field=NeXusField(
            name="beam_size_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasSample(Sample):
    """
    Description of the sample.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASsample"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASsample`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASsample"],
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-name-field"
        ],
        description=("**ID**: Text string that identifies this sample."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    transmission_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-transmission-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Transmission (:math:`I/I_0`) of this sample. There is no *units* "
            "attribute as this number is dimensionless. Note: the ability to "
            "store a transmission *spectrum*, instead of a single value, is "
            "provided elsewhere in the structure, in the "
            "*SAStransmission_spectrum* element."
        ),
        a_nexus_field=NeXusField(
            name="transmission",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-temperature-field"
        ],
        dimensionality="[temperature]",
        unit="kelvin",
        description=("Temperature of this sample."),
        a_nexus_field=NeXusField(
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    details = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-details-field"
        ],
        variable=True,
        description=("Any additional sample details."),
        a_nexus_field=NeXusField(
            name="details",
            type="NX_CHAR",
            name_type="any",
            optionality="optional",
        ),
    )
    x_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-x-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Location of the sample in :math:`x`"),
        a_nexus_field=NeXusField(
            name="x_position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y_position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-y-position-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("Location of the sample in :math:`y`"),
        a_nexus_field=NeXusField(
            name="y_position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    roll = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-roll-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation of the sample about the :math:`z` axis (roll)"),
        a_nexus_field=NeXusField(
            name="roll",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    pitch = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-pitch-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation of the sample about the :math:`x` axis (roll)"),
        a_nexus_field=NeXusField(
            name="pitch",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    yaw = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-sample-yaw-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        description=("Rotation of the sample about the :math:`y` axis (yaw)"),
        a_nexus_field=NeXusField(
            name="yaw",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasProcess(Process):
    """
    Description of a processing or analysis step.

    Add additional fields as needed to describe value(s) of any variable,
    parameter, or term related to the *SASprocess* step. Be sure to include
    *units* attributes for all numerical fields.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.cansas.CansasProcessCollection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASprocess"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-process-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASprocess`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASprocess"],
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-process-name-field"
        ],
        description=("Optional name for this data processing or analysis step"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-process-description-field"
        ],
        description=("Optional description for this data processing or analysis step"),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    term = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-process-term-field"
        ],
        variable=True,
        description=(
            "Specifies the value of a single variable, parameter, or term (while "
            "defined here as a string, it could be a number) related to the "
            "*SASprocess* step. Note: The name *term* is not required, it could "
            "take any name, as long as the name is unique within this group."
        ),
        a_nexus_field=NeXusField(
            name="term",
            type="NX_CHAR",
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasProcessCollection(Collection):
    """
    Describes anything about *SASprocess* that is not already described.

    Any content not defined in the canSAS standard can be placed at this point.

    Note: The name of this group is flexible, it could take any name, as long
    as it is unique within the **NXprocess** group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-process-collection-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASprocessnote"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-process-collection-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASprocessnote`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASprocessnote"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasCollection(Collection):
    """
    Free form description of anything not covered by other elements.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-collection-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SASnote"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-collection-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); SASnote`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SASnote"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class CansasTransmissionSpectrum(Data):
    """
    The *SAStransmission_spectrum* element

    This describes certain data obtained from a variable-wavelength source such
    as pulsed-neutron source.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )

    canSAS_class = Quantity(
        type=MEnum(["SAStransmission_spectrum"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-cansas-class-attribute"
        ],
        description=(
            "Official canSAS group: :index:`NXcanSAS (applications); "
            "SAStransmission_spectrum`"
        ),
        a_nexus_attribute=NeXusAttribute(
            name="canSAS_class",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["SAStransmission_spectrum"],
        ),
    )
    signal = Quantity(
        type=MEnum(["T"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-signal-attribute"
        ],
        description=("Name of the default data field."),
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["T"],
        ),
    )
    T_axes = Quantity(
        type=MEnum(["T"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-t-axes-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="T_axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["T"],
        ),
    )
    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-name-attribute"
        ],
        description=(
            "Identify what type of spectrum is being described. It is expected "
            "that this value will take either of these two values: ====== "
            "============================================== value meaning ====== "
            "============================================== sample measurement "
            "with the sample and container can measurement with just the "
            "container ====== =============================================="
        ),
        a_nexus_attribute=NeXusAttribute(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    timestamp = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-timestamp-attribute"
        ],
        description=("ISO-8601 time [#iso8601]_"),
        a_nexus_attribute=NeXusAttribute(
            name="timestamp",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    lambda_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-lambda-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "Wavelength of the radiation. This array is of the same shape as "
            "``T`` and ``Tdev``."
        ),
        a_nexus_field=NeXusField(
            name="lambda",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_WAVELENGTH",
        ),
    )
    T = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-t-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            "Transmission values (:math:`I/I_0`) as a function of wavelength. "
            "This array is of the same shape as ``lambda`` and ``Tdev``."
        ),
        a_nexus_field=NeXusField(
            name="T",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )
    T__uncertainties = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-t-uncertainties-attribute"
        ],
        description=(
            "Names the dataset (in this SASdata group) that provides the "
            "uncertainty of each transmission :math:`T` to be used for data "
            "analysis. The name of the dataset containing the :math:`T` "
            "uncertainty is expected to be ``Tdev``. .. comment see: "
            "https://github.com/canSAS-org/canSAS2012/issues/7 Typically: "
            '@uncertainties="Tdev"'
        ),
        a_nexus_attribute=NeXusAttribute(
            name="uncertainties",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="T",
        ),
    )
    Tdev = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/applications/NXcanSAS.html#nxcansas-entry-transmission-spectrum-tdev-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=(
            ".. index:: NXcanSAS (applications); Tdev Estimated uncertainty "
            "(usually standard deviation) in :math:`T`. Must have the same units "
            "as :math:`T`. This is the field is named in the *uncertainties* "
            'attribute of *T*, as in:: T/@uncertainties="Tdev" This array is '
            "of the same shape as ``lambda`` and ``T``."
        ),
        a_nexus_field=NeXusField(
            name="Tdev",
            type="NX_NUMBER",
            name_type="specified",
            optionality="required",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
