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
# Run `pynx nomad generate-metainfo --nxdl NXroot` to regenerate.
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

__all__ = ["Root"]


class Root(Object):
    """
    The root of a NeXus file.

    In the NeXus standard, only NXentry groups are allowed at the root level of
    a file, although it is permitted to include additional groups and fields
    that are not part of the NeXus standard and will not be validated by NeXus
    tools. NeXus defines a number of root-level attributes that can be used to
    annotate the NeXus tree.

    Note that NXroot is the only base class that does not inherit from the
    NXobject class, since the latter permits the inclusion of NeXus objects
    that are not allowed at the root level.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXroot",
            category="base",
        ),
    )

    entry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.Entry",
        repeats=True,
        variable=True,
        description=("entries"),
        a_nexus_group=NeXusGroup(
            nx_class="NXentry",
            name=None,
            name_type="any",
            optionality="required",
            min_occurs=1,
        ),
    )

    file_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-file-time-attribute"
        ],
        description=("Date and time file was originally created"),
        a_nexus_attribute=NeXusAttribute(
            name="file_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    file_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-file-name-attribute"
        ],
        description=("File name of original NeXus file"),
        a_nexus_attribute=NeXusAttribute(
            name="file_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    file_update_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-file-update-time-attribute"
        ],
        description=("Date and time of last file change at close"),
        a_nexus_attribute=NeXusAttribute(
            name="file_update_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    NeXus_version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-nexus-version-attribute"
        ],
        description=(
            "Version of NeXus API used in writing the file. Note that this is "
            "different from the version of the base class or application "
            "definition version number."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="NeXus_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            deprecated="NAPI is frozen.",
        ),
    )
    NeXus_repository = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-nexus-repository-attribute"
        ],
        description=(
            "A repository containing the application definitions used for "
            "creating this file. If the ``NeXus_release`` attribute contains a "
            "commit distance and hash, this should refer to this repository."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="NeXus_repository",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    NeXus_release = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-nexus-release-attribute"
        ],
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
        a_nexus_attribute=NeXusAttribute(
            name="NeXus_release",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    HDF_version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-hdf-version-attribute"
        ],
        description=("Version of HDF (version 4) library used in writing the file"),
        a_nexus_attribute=NeXusAttribute(
            name="HDF_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    HDF5_Version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-hdf5-version-attribute"
        ],
        description=(
            "Version of HDF5 library used in writing the file. Note this "
            'attribute is spelled with uppercase "V", different than other '
            "version attributes."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="HDF5_Version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    XML_version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-xml-version-attribute"
        ],
        description=("Version of XML support library used in writing the XML file"),
        a_nexus_attribute=NeXusAttribute(
            name="XML_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    h5py_version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-h5py-version-attribute"
        ],
        description=("Version of h5py Python package used in writing the file"),
        a_nexus_attribute=NeXusAttribute(
            name="h5py_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    partial = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-partial-attribute"
        ],
        description=(
            "A list of concepts in an application definition this file "
            "describes. This is for partially filling an application definition. "
            "If this attribute is not present the application definition is "
            "assumed to be valid, if not only the specified concepts/paths are "
            "assumed to be valid."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="partial",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    creator = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-creator-attribute"
        ],
        description=("facility or program where file originated"),
        a_nexus_attribute=NeXusAttribute(
            name="creator",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    creator_version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-creator-version-attribute"
        ],
        description=("Version of facility or program used in writing the file"),
        a_nexus_attribute=NeXusAttribute(
            name="creator_version",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXroot.html#nxroot-default-attribute"
        ],
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
        a_nexus_attribute=NeXusAttribute(
            name="default",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
