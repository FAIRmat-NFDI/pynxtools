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
# Run `pynx nomad generate-metainfo --nx-class NXtest` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Test"]


class Test(Object):
    """
    This is a dummy NXDL to test out the dataconverter.
    """

    m_def = Section(
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtest",
            category="application",
            symbols={"n": "number of data points shared across symbol_group fields"},
        ),
    )

    entry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.test.TestEntry",
        repeats=True,
        variable=True,
    )

    file_time = Quantity(
        type=Datetime,
        description=("Date and time file was originally created"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="file_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    file_name = Quantity(
        type=str,
        description=("File name of original NeXus file"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    file_update_time = Quantity(
        type=Datetime,
        description=("Date and time of last file change at close"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="file_update_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    NeXus_version = Quantity(
        type=str,
        description=(
            "Version of NeXus API used in writing the file. Note that this is "
            "different from the version of the base class or application "
            "definition version number."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="NeXus_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            deprecated="NAPI is frozen.",
        ),
    )
    NeXus_repository = Quantity(
        type=str,
        description=(
            "A repository containing the application definitions used for "
            "creating this file. If the ``NeXus_release`` attribute contains a "
            "commit distance and hash, this should refer to this repository."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="NeXus_repository",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    NeXus_release = Quantity(
        type=str,
        description=(
            "The version of NeXus definitions used in writing the file. This can "
            "either be a date-based NeXus release (e.g., YYYY.MM), see "
            "https://github.com/nexusformat/definitions/releases or a version "
            "tag that includes additional development information, such as a "
            "commit distance and a Git hash. This is typically formatted as "
            "`vYYYY.MM.post1.dev<commit-distance>-g<git-hash>`, where `YYYY.MM` "
            "refers to the base version of the NeXus definitions. "
            "`post1.dev<commit-distance>` indicates that the definitions are "
            "based on a commit after the base version (post1), with "
            "`<commit-distance>` being the number of commits since that version. "
            "`g<git-hash>` is the abbreviated Git hash that identifies the "
            "specific commit of the definitions being used. If the version "
            "includes both a commit distance and a Git hash, the "
            "``NeXus_repository`` attribute must be included, specifying the URL "
            "of the repository containing that version."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="NeXus_release",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    HDF_version = Quantity(
        type=str,
        description=("Version of HDF (version 4) library used in writing the file"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="HDF_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    HDF5_Version = Quantity(
        type=str,
        description=(
            "Version of HDF5 library used in writing the file. Note this "
            'attribute is spelled with uppercase "V", different than other '
            "version attributes."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="HDF5_Version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    XML_version = Quantity(
        type=str,
        description=("Version of XML support library used in writing the XML file"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="XML_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    h5py_version = Quantity(
        type=str,
        description=("Version of h5py Python package used in writing the file"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="h5py_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    partial = Quantity(
        type=str,
        description=(
            "A list of concepts in an application definition this file "
            "describes. This is for partially filling an application definition. "
            "If this attribute is not present the application definition is "
            "assumed to be valid, if not only the specified concepts/paths are "
            "assumed to be valid."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="partial",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    creator = Quantity(
        type=str,
        description=("facility or program where file originated"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="creator",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    creator_version = Quantity(
        type=str,
        description=("Version of facility or program used in writing the file"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="creator_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    default = Quantity(
        type=str,
        description=(
            ".. index:: find the default plottable data .. index:: plotting .. "
            "index:: default attribute value Declares which :ref:`NXentry` group "
            "contains the data to be shown by default. It is used to resolve "
            "ambiguity when more than one :ref:`NXentry` group exists. The value "
            ":ref:`names <validItemName>` the default :ref:`NXentry` group. The "
            "value must be the name of a child of the current group. The child "
            "must be a NeXus group or a link to a NeXus group. It is recommended "
            "(as of NIAC2014) to use this attribute to help define the path to "
            "the default dataset to be plotted. See "
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


class TestEntry(Entry):
    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXentry",
            name=None,
            name_type="any",
            optionality="required",
        ),
    )

    program_name = Quantity(
        type=str,
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="program_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
    )
    definition = Quantity(
        type=MEnum(["NXTEST", "NXtest"]),
        description=("This is a dummy NXDL to test out the dataconverter."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXTEST", "NXtest"],
        ),
    )
    definition__version = Quantity(
        type=str,
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
