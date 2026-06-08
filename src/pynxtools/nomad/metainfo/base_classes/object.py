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
# Run `pynx nomad generate-metainfo --nxdl NXobject` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import Quantity, Section, SubSection

from pynxtools.nomad.annotations import (
    NeXusAttribute,
    NeXusDefinition,
    NeXusField,
    NeXusGroup,
)

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Object"]


class Object(BaseSection):
    """
    This is the base object of NeXus. The groups and fields contained within
    this file are allowed to be present in any derived base class.

    If nameType="partial", the placeholders (e.g., FIELDNAME or GROUPNAME) can
    be replaced by the name of any object (field or group, respectively) that
    exists within the same group.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXobject",
            category="base",
        ),
    )

    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
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
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    parameters = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.parameters.Parameters",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name=None,
            name_type="any",
            optionality="optional",
            min_occurs=0,
        ),
    )
    GROUPNAME_log = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.log.Log",
        repeats=True,
        variable=True,
        description=("NXlog group containing logged values of GROUPNAME."),
        a_nexus_group=NeXusGroup(
            nx_class="NXlog",
            name="GROUPNAME_log",
            name_type="partial",
            optionality="optional",
            min_occurs=0,
        ),
    )

    FIELDNAME_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject-fieldname-set-field"
        ],
        variable=True,
        description=("Target values of FIELDNAME."),
        a_nexus_field=NeXusField(
            name="FIELDNAME_set",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    FIELDNAME_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject-fieldname-errors-field"
        ],
        variable=True,
        description=("Uncertainties of FIELDNAME values."),
        a_nexus_field=NeXusField(
            name="FIELDNAME_errors",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    FIELDNAME_weights = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject-fieldname-weights-field"
        ],
        variable=True,
        description=("Weights of FIELDNAME values."),
        a_nexus_field=NeXusField(
            name="FIELDNAME_weights",
            type="NX_NUMBER",
            name_type="partial",
            optionality="optional",
        ),
    )
    FIELDNAME_mask = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject-fieldname-mask-field"
        ],
        variable=True,
        description=(
            "Boolean mask of FIELDNAME values. The value is masked if set to 1."
        ),
        a_nexus_field=NeXusField(
            name="FIELDNAME_mask",
            type="NX_BOOLEAN",
            name_type="partial",
            optionality="optional",
        ),
    )
    identifierNAME = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject-identifiername-field"
        ],
        variable=True,
        description=(
            "An identifier for a (persistent) resource. An identifier, provided "
            "by some authority, that has been assigned to an object described by "
            "this ``NXobject``. To be useful, the identifier must not be "
            "reassigned to a different real-world object. It is typical for "
            "there to be some mechanism to resolve an identifier, obtaining "
            "metadata about the object. Identifiers for which some guarantees "
            "exist regarding this resolution process are called persistent "
            "identifiers. Persistent identifiers are also known as PIDs."
        ),
        a_nexus_field=NeXusField(
            name="identifierNAME",
            type="NX_CHAR",
            name_type="partial",
            optionality="optional",
        ),
    )
    identifierNAME__type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject-identifiername-type-attribute"
        ],
        description=(
            "The type of identifier used. It is recommended to use the most "
            "specific type when describing the identifier. For example, all "
            "IGSNs (see below) are DOIs and all DOIs are Handles; however, an "
            "IGSN should have type IGSN (and not DOI or Hdl). Similarly, an ARK, "
            "Purl, ORCID and ROR identifiers should have their corresponding "
            "types and should not use the more generic URL identifier."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="identifierNAME",
            enumeration=[
                "ARK",
                "DOI",
                "Hdl",
                "IGSN",
                "ISNI",
                "ISSN",
                "ISSN-L",
                "ORCID",
                "PURL",
                "ROR",
                "URL",
                "URN",
            ],
            open_enum=True,
        ),
    )
    default = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXobject.html#nxobject-default-attribute"
        ],
        description=(
            ".. index:: plotting Declares which child group contains a path "
            "leading to a :ref:`NXdata` group or a group using a base class "
            "extending :ref:`NXdata`. It is recommended (as of NIAC2014) to use "
            "this attribute to help define the path to the default dataset to be "
            "plotted. See "
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
