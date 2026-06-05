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
# Run `pynx nomad generate-metainfo --nx-class NXxpcs` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.sample import Sample

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Xpcs"]


class Xpcs(Entry):
    """
    X-ray Photon Correlation Spectroscopy (XPCS) data (results).

    The purpose of ``NXxpcs`` is to document and communicate an accepted
    vernacular for various XPCS results data in order to support development of
    community software tools. The definition presented here only represents a
    starting point and contains fields that a common software tool should
    support for community acceptance.

    Additional fields may be added to XPCS results file (either formally or
    informally). It is expected that this XPCS data will be part of multi-modal
    data set that could involve e.g., :ref:`NXcanSAS` or 1D and/or 2D data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXxpcs",
            category="application",
            symbols={"nP": "Number of points"},
        ),
    )

    data = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xpcs.XpcsData",
        repeats=False,
        description=(
            "The results data captured here are most commonly required for high "
            "throughput, equilibrium dynamics experiments. Data (results) "
            "describing on-equilibrium dynamics consume more memory resources so "
            "these data are separated."
        ),
    )
    twotime = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xpcs.XpcsTwotime",
        repeats=False,
        description=(
            "The data (results) in this section are based on the two-time "
            "intensity correlation function derived from a time series of "
            "scattering images."
        ),
    )
    instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.instrument.Instrument",
        repeats=False,
        description=(
            "XPCS instrument Metadata. Objects can be entered here directly or "
            "linked from other objects in the NeXus file (such as within "
            "``/entry/instrument``)."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXinstrument",
            name="instrument",
            name_type="specified",
            optionality="required",
        ),
    )
    sample = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.xpcs.XpcsSample",
        repeats=False,
    )
    NOTE = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "Any other notes. NAME: The NeXus convention, to use all upper case "
            "to indicate the name (here ``NOTE``), is left to the file writer. "
            "In our case, follow the suggested name pattern and sequence: "
            "note_1, note_2, note_3, ... Start with ``note_1`` if the first one, "
            "otherwise pick the next number in this sequence."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="NOTE",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )

    definition = Quantity(
        type=MEnum(["NXxpcs"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-definition-field"
        ],
        description=("Official NeXus NXDL schema to which this file conforms"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXxpcs"],
        ),
    )
    entry_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-entry-identifier-field"
        ],
        description=(
            "**Locally** unique identifier for the experiment (a.k.a. run or "
            'scan). * For bluesky users, this is the run\'s `"scan_id"`. * For '
            "SPEC users, this is the scan number (``SCAN_N``)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="entry_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    entry_identifier_uuid = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-entry-identifier-uuid-field"
        ],
        description=(
            "(optional) UUID identifier for this entry. See the `UUID standard "
            "<https://www.rfc-editor.org/rfc/rfc4122.html>`__ (or `wikipedia "
            "<https://en.wikipedia.org/wiki/Universally_unique_identifier>`__) "
            "for more information. * For `bluesky "
            '<https://blueskyproject.io/>`__ users, this is the run\'s `"uid"` '
            "and is expected for that application. * Typically, `SPEC "
            "<https://certif.com/content/spec/>`__ users will not use this field "
            "without further engineering."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="entry_identifier_uuid",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    scan_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-scan-number-field"
        ],
        description=(
            "Scan number (must be an integer). NOTE: Link to collection_identifier."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="scan_number",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            deprecated="Use the ``entry_identifier`` field.",
        ),
    )
    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-start-time-field"
        ],
        description=(
            'Starting time of experiment, such as "2021-02-11 11:22:33.445566Z".'
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-end-time-field"
        ],
        description=('Ending time of experiment, such as "2021-02-11 11:23:45Z".'),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="end_time",
            type="NX_DATE_TIME",
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


class XpcsData(Data):
    """
    The results data captured here are most commonly required for high
    throughput, equilibrium dynamics experiments. Data (results) describing
    on-equilibrium dynamics consume more memory resources so these data are
    separated.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="data",
            name_type="specified",
            optionality="required",
        ),
    )

    frame_sum = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-frame-sum-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Two-dimensional summation along the frames stack. sum of intensity "
            'v. time (in the units of "frames")'
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="frame_sum",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_COUNT",
        ),
    )
    frame_average = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-frame-average-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Two-dimensional average along the frames stack. average intensity "
            'v. time (in the units of "frames")'
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="frame_average",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_COUNT",
        ),
    )
    g2 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-g2-field"
        ],
        dimensionality="dimensionless",
        description=(
            "normalized intensity auto-correlation function, see Lumma, Rev. "
            "Sci. Instr. (2000), Eq 1 .. math:: g_2(\\boldsymbol Q,t) = \\frac{ "
            "\\langle I(\\boldsymbol Q,t\\prime) I(\\boldsymbol Q,t\\prime + t) "
            "\\rangle }{ \\langle I(\\boldsymbol Q,t\\prime)\\rangle^2 }; t > 0 "
            "Typically, :math:`g_2` is a quantity calculated for a group of "
            "pixels representing a specific region of reciprocal space. These "
            "groupings, or bins, are generically described as :math:`q`. Some "
            'open-source XPCS libraries refer to these bins as "rois", which '
            "are not to be confused with EPICS AreaDetector ROI. See usage "
            "guidelines for q_lists and roi_maps within a mask. [#]_ In short, "
            ":math:`g_2` should be ordered according to the roi_map value. In "
            "principle, any format is acceptable if the data and its axes are "
            "self-describing as per NeXus recommendations. However, the data is "
            "preferred in one of the following two formats: * iterable list of "
            "linked files (or keys) for each :math:`g_2` with 1 file (key) per "
            ":math:`q`, where `q` is called by the nth roi_map value * 2D array "
            "[#]_ with shape (:math:`g_2`, :math:`q`), where `q` is represented "
            "by the nth roi_map value, not the value `q` value Note it is "
            'expected that "g2" and all quantities following it will be of the '
            "same length. Other formats are acceptable with sufficient axes "
            "description. See references below for related implementation "
            "information: .. [#] mask: ``NXxpcs:/entry/instrument/masks-group`` "
            ".. [#] NeXus 2-D data and axes: "
            "https://manual.nexusformat.org/classes/base_classes/NXdata.html#nxdata"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="g2",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    g2__storage_mode = Quantity(
        type=MEnum(["one_array", "data_exchange_keys", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-g2-storage-mode-attribute"
        ],
        description=(
            "storage_mode describes the format of the data to be loaded We "
            "encourage the documentation of other formats not represented here. "
            '* one array representing entire data set ("one_array") * data '
            "exchange format with each key representing one ``q`` by its "
            'corresponding roi_map value ("data_exchange_keys")'
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["one_array", "data_exchange_keys", "other"],
            parent_field="g2",
        ),
    )
    g2_derr = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-g2-derr-field"
        ],
        dimensionality="dimensionless",
        description=(
            "error values for the :math:`g_2` values. The derivation of the "
            "error is left up to the implemented code. Symmetric error will be "
            "expected (:math:`\\pm` error). The data should be in the same "
            "format as ``g2``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="g2_derr",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    g2_derr__storage_mode = Quantity(
        type=MEnum(["one_array", "data_exchange_keys", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-g2-derr-storage-mode-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["one_array", "data_exchange_keys", "other"],
            parent_field="g2_derr",
        ),
    )
    G2_unnormalized = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-g2-unnormalized-field"
        ],
        description=(
            "unnormalized intensity auto-correlation function. Specifically, "
            "``g2`` without the denominator. The data should be in the same "
            "format as ``g2``."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="G2_unnormalized",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    G2_unnormalized__storage_mode = Quantity(
        type=MEnum(["one_array", "data_exchange_keys", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-g2-unnormalized-storage-mode-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["one_array", "data_exchange_keys", "other"],
            parent_field="G2_unnormalized",
        ),
    )
    delay_difference = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-delay-difference-field"
        ],
        dimensionality="dimensionless",
        description=(
            "delay_difference (also known as delay or lag step) This is "
            'quantized difference so that the "step" between two consecutive '
            "frames is one frame (or step ``= dt = 1 frame``) It is the "
            '"quantized" delay time corresponding to the ``g2`` values. The '
            "unit of delay_differences is ``NX_INT`` for units of frames (i.e., "
            "integers) preferred, refer to :ref:`NXdetector` for conversion to "
            "time units."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="delay_difference",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_COUNT",
        ),
    )
    delay_difference__storage_mode = Quantity(
        type=MEnum(["one_array", "data_exchange_keys", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-data-delay-difference-storage-mode-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["one_array", "data_exchange_keys", "other"],
            parent_field="delay_difference",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpcsTwotime(Data):
    """
    The data (results) in this section are based on the two-time intensity
    correlation function derived from a time series of scattering images.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="twotime",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )

    two_time_corr_func = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-two-time-corr-func-field"
        ],
        description=(
            "two-time correlation of speckle intensity for a given q-bin or roi "
            "(represented by the nth roi_map value) See Fluerasu, Phys Rev E "
            "(2007), Eq 1 and Sutton, Optics Express (2003) for an early "
            "description applied to X-ray scattering: .. math:: C(\\boldsymbol "
            "Q, t_1, t_2) = \\frac{ \\langle I(\\boldsymbol Q, "
            "t_1)I(\\boldsymbol Q, t_2)\\rangle }{ \\langle I(\\boldsymbol "
            "Q,t_1)\\rangle \\langle I(\\boldsymbol Q,t_2)\\rangle } in which "
            "time is quantized by frames. In principle, any data format is "
            "acceptable if the data and its axes are self-describing as per "
            "NeXus recommendations. However, the data is preferred in one of the "
            "following two formats: * iterable list of linked files (or keys) "
            "for each q-bin called by the nth roi_map value. data for each bin "
            "is a 2D array * 3D array with shape (frames, frames, q) or (q, "
            "frames, frames), where :math:`q` is represented by the nth roi_map "
            "value, not the value `q` value The computation of this result can "
            "be customized. These customizations can affect subsequently derived "
            "results (below). The following attributes will be used to manage "
            "the customization. * Other normalization methods may be applied, "
            "but the method will not be specified in this definition. Some of "
            "these normalization methods result in a baseline value of ``0``, "
            "not ``1``. * The various software libraries use different "
            "programming languages. Therefore, we need to specify the ``time = "
            "0`` origin location of the 2D array for each :math:`q`. * A method "
            "to reduce data storage needs is to only record half of the 2D array "
            "by populating array elements above or below the array diagonal."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="two_time_corr_func",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    two_time_corr_func__storage_mode = Quantity(
        type=MEnum(
            ["one_array_q_first", "one_array_q_last", "data_exchange_keys", "other"]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-two-time-corr-func-storage-mode-attribute"
        ],
        description=(
            "storage_mode describes the format of the data to be loaded We "
            "encourage the documentation of other formats represented here."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "one_array_q_first",
                "one_array_q_last",
                "data_exchange_keys",
                "other",
            ],
            parent_field="two_time_corr_func",
        ),
    )
    two_time_corr_func__baseline_reference = Quantity(
        type=MEnum(["0", "1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-two-time-corr-func-baseline-reference-attribute"
        ],
        description=(
            "baseline is the expected value of a full decorrelation The baseline "
            "is a constant value added to the functional form of the "
            "auto-correlation function. This value is required."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="baseline_reference",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            enumeration=["0", "1"],
            parent_field="two_time_corr_func",
        ),
    )
    two_time_corr_func__time_origin_location = Quantity(
        type=MEnum(["upper_left", "lower_left"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-two-time-corr-func-time-origin-location-attribute"
        ],
        description=("time_origin_location is the location of the origin"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="time_origin_location",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["upper_left", "lower_left"],
            parent_field="two_time_corr_func",
        ),
    )
    two_time_corr_func__populated_elements = Quantity(
        type=MEnum(["all", "upper_half", "lower_half"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-two-time-corr-func-populated-elements-attribute"
        ],
        description=(
            "populated_elements describe the elements of the 2D array that are "
            "populated with data"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="populated_elements",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["all", "upper_half", "lower_half"],
            parent_field="two_time_corr_func",
        ),
    )
    g2_from_two_time_corr_func = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-from-two-time-corr-func-field"
        ],
        dimensionality="dimensionless",
        description=(
            "frame weighted average along the diagonal direction in "
            "``two_time_corr_func`` The data format and description should be "
            'consistent with that found in "/NXxpcs/entry/data/g2" * iterable '
            "list of linked files for each :math:`g_2` with 1 file per :math:`q` "
            "* 2D array with shape (:math:`g_2`, :math:`q`) Note that "
            "delay_difference is not included here because it is derived from "
            "the shape of extracted :math:`g_2` because all frames are "
            "considered, which is not necessarily the case for :math:`g_2`. The "
            "computation of this result can be customized. The customization can "
            "affect the fitting required to extract quantitative results. The "
            "following attributes will be used to manage the customization."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="g2_from_two_time_corr_func",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    g2_from_two_time_corr_func__storage_mode = Quantity(
        type=MEnum(
            ["one_array_q_first", "one_array_q_last", "data_exchange_keys", "other"]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-from-two-time-corr-func-storage-mode-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "one_array_q_first",
                "one_array_q_last",
                "data_exchange_keys",
                "other",
            ],
            parent_field="g2_from_two_time_corr_func",
        ),
    )
    g2_from_two_time_corr_func__baseline_reference = Quantity(
        type=MEnum(["0", "1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-from-two-time-corr-func-baseline-reference-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="baseline_reference",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            enumeration=["0", "1"],
            parent_field="g2_from_two_time_corr_func",
        ),
    )
    g2_from_two_time_corr_func__first_point_for_fit = Quantity(
        type=MEnum(["0", "1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-from-two-time-corr-func-first-point-for-fit-attribute"
        ],
        description=(
            "first_point_for_fit describes if the first point should or should "
            "not be used in fitting the functional form of the dynamics to "
            "extract quantitative time-scale information. The "
            'first_point_for_fit is True ("1") or False ("0"). This value is '
            "required."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="first_point_for_fit",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            enumeration=["0", "1"],
            parent_field="g2_from_two_time_corr_func",
        ),
    )
    g2_err_from_two_time_corr_func = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-err-from-two-time-corr-func-field"
        ],
        dimensionality="dimensionless",
        description=(
            "error values for the :math:`g_2` values. The derivation of the "
            "error is left up to the implemented code. Symmetric error will be "
            "expected (:math:`\\pm` error)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="g2_err_from_two_time_corr_func",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    g2_err_from_two_time_corr_func__storage_mode = Quantity(
        type=MEnum(
            ["one_array_q_first", "one_array_q_last", "data_exchange_keys", "other"]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-err-from-two-time-corr-func-storage-mode-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=[
                "one_array_q_first",
                "one_array_q_last",
                "data_exchange_keys",
                "other",
            ],
            parent_field="g2_err_from_two_time_corr_func",
        ),
    )
    g2_from_two_time_corr_func_partials = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-from-two-time-corr-func-partials-field"
        ],
        dimensionality="dimensionless",
        description=(
            "subset of frame weighted average along the diagonal direction in "
            "``two_time_corr_func`` Time slicing along the diagonal can be very "
            "sophisticated. This entry currently assumes equal frame-binning. "
            "The data formats are highly dependent on the implantation of "
            "various analysis libraries. In principle, any data format is "
            "acceptable if the data and its axes are self describing as per "
            "NeXus recommendations. However, the data is preferred in one of the "
            "following two formats: * iterable list of linked files (or keys) "
            "for each partial :math:`g_2` of each q-bin represented by the "
            "roi_map value * 3D array with shape (:math:`g_2`, :math:`q`, "
            "nth_partial) Note that delay_difference is not included here "
            "because it is derived from the shape of extracted :math:`g_2`."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="g2_from_two_time_corr_func_partials",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    g2_from_two_time_corr_func_partials__storage_mode = Quantity(
        type=MEnum(["one_array", "data_exchange_keys", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-from-two-time-corr-func-partials-storage-mode-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="storage_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["one_array", "data_exchange_keys", "other"],
            parent_field="g2_from_two_time_corr_func_partials",
        ),
    )
    g2_from_two_time_corr_func_partials__baseline_reference = Quantity(
        type=MEnum(["0", "1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-from-two-time-corr-func-partials-baseline-reference-attribute"
        ],
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="baseline_reference",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            enumeration=["0", "1"],
            parent_field="g2_from_two_time_corr_func_partials",
        ),
    )
    g2_err_from_two_time_corr_func_partials = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-twotime-g2-err-from-two-time-corr-func-partials-field"
        ],
        dimensionality="dimensionless",
        description=(
            "error values for the :math:`g_2` values. The derivation of the "
            "error is left up to the implemented code. Symmetric error will be "
            "expected (:math:`\\pm` error)."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="g2_err_from_two_time_corr_func_partials",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class XpcsSample(Sample):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-sample-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsample",
            name="sample",
            name_type="specified",
            optionality="optional",
            min_occurs=0,
        ),
    )

    temperature_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-sample-temperature-set-field"
        ],
        dimensionality="[temperature]",
        description=("Sample temperature setpoint, (C or K)."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="temperature_set",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )
    temperature = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXxpcs.html#nxxpcs-entry-sample-temperature-field"
        ],
        dimensionality="[temperature]",
        description=("Sample temperature actual, (C or K)."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="temperature",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TEMPERATURE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
