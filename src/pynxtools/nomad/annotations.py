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
"""
NOMAD annotation models for NeXus sections and quantities.

NeXusDefinition — attached to Section.m_def; mirrors NXDL <definition> semantics.
NeXusGroup      — attached to SubSection definitions; mirrors NXDL <group> semantics.
NeXusField      — attached to Quantity definitions; mirrors NXDL <field> semantics.
NeXusAttribute  — attached to Quantity definitions; mirrors NXDL <attribute> semantics.
NeXusLink       — attached to Quantity definitions; mirrors NXDL <link> semantics.
NeXusChoice     — attached to SubSection definitions; one per alternative in a <choice>.

The split between NeXusDefinition and NeXusGroup mirrors the NXDL schema:
- <definition> carries category, ignore-extra flags, symbols, and restricts.
- <group> carries the instance name, name_type, optionality, and occurrence limits.

Usage:

    m_def = Section(a_nexus_definition=NeXusDefinition(nx_class="NXentry", ...))
    data  = SubSection(..., a_nexus_group=NeXusGroup(nx_class="NXdata", ...))
    fld   = Quantity(..., a_nexus_field=NeXusField(name="energy", ...))
    attr  = Quantity(..., a_nexus_attribute=NeXusAttribute(name="signal", ...))
    link   = Quantity(..., a_nexus_link=NeXusLink(name="data", target="/NXentry/..."))
    geom  = SubSection(..., a_nexus_choice=NeXusChoice(nx_class="NXoff_geometry",
                                                       group_name="pixel_shape"))

Naming convention
-----------------
Fields mirror plain NXDL XML attribute names where possible (no prefix needed
since the class name already provides the NeXus namespace).

The only exception is ``nx_class``: ``class`` is a Python reserved keyword and
cannot be used as a Pydantic field name, so the ``nx_`` prefix is kept there.
"""

from __future__ import annotations

from typing import Literal

try:
    from nomad.metainfo.annotation import AnnotationModel
    from nomad.metainfo.metainfo import (
        Definition,  # noqa: F401 — needed for model_rebuild
    )
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install 'nomad-lab'."
    ) from exc


class NeXusDefinition(AnnotationModel):
    """Annotation on Section.m_def for NeXus definition-level semantics.

    Corresponds to the NXDL <definition> element. Carries the class identity
    and definition-level validation controls. One per generated Python class.
    """

    # ``class`` is a Python reserved keyword → must keep nx_ prefix here.
    nx_class: str
    category: Literal["base", "application", "contributed"] = "base"
    # From NXDL definition/@restricts.
    restricts: bool = False
    # From NXDL definition/@ignoreExtra*: suppress unknown-child warnings.
    ignore_extra_groups: bool = False
    ignore_extra_fields: bool = False
    ignore_extra_attributes: bool = False
    # Symbolic dimension names from the NXDL <symbols> table: {symbol: doc}.
    symbols: dict[str, str] | None = None
    deprecated: str | None = None


class NeXusGroup(AnnotationModel):
    """Annotation on SubSection for NeXus group-reference semantics.

    Corresponds to a NXDL <group> child element. Carries the instance name,
    naming convention, optionality, and occurrence limits that describe how a
    group of a given nx_class appears inside its parent definition.
    """

    # ``class`` is a Python reserved keyword → must keep nx_ prefix here.
    nx_class: str
    name: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    min_occurs: int | None = None
    max_occurs: int | None = None
    deprecated: str | None = None


class NeXusField(AnnotationModel):
    """Annotation on a Quantity for NXDL <field> semantics.

    Corresponds to a NXDL <field> child element. Fields hold typed data arrays
    and may carry unit categories, interpretation hints, and long names.
    """

    name: str
    # ``type`` is a Python builtin but valid as a Pydantic field name.
    type: str = "NX_CHAR"
    # NX unit category (e.g. "NX_ENERGY").
    units: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    enumeration: list[str] | None = None
    open_enum: bool = False
    interpretation: str | None = None
    long_name: str | None = None
    deprecated: str | None = None


class NeXusAttribute(AnnotationModel):
    """Annotation on a Quantity for NXDL <attribute> semantics.

    Corresponds to a NXDL <attribute> element — either a group-level attribute
    or a field-level attribute. Field-level attributes set ``parent_field`` to
    the name of the parent field (e.g. ``parent_field="energy"`` for
    ``energy__units``).
    """

    name: str
    # Set when this is an attribute of a field rather than of the group.
    parent_field: str | None = None
    # ``type`` is a Python builtin but valid as a Pydantic field name.
    type: str = "NX_CHAR"
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    enumeration: list[str] | None = None
    open_enum: bool = False
    deprecated: str | None = None


class NeXusLink(AnnotationModel):
    """Annotation on a Quantity for NXDL <link> semantics.

    A <link> element names a reference to another field or group elsewhere in
    the HDF5 file.  The ``target`` is the schema-level default target path as
    written in the NXDL; the actual HDF5 target is resolved by the parser at
    read time.
    """

    name: str
    target: str
    optionality: Literal["required", "recommended", "optional"] = "optional"
    deprecated: str | None = None


class NeXusChoice(AnnotationModel):
    """Annotation on a SubSection for one alternative in an NXDL <choice>.

    A <choice name="pixel_shape"> block allows exactly one of several NX
    classes to occupy a named slot.  One SubSection is generated per
    alternative; all share the same ``group_name`` so consumers can identify
    the alternatives that belong together.

    Naming convention: ``{group_name}_{nxdl_class_suffix}`` where the suffix
    is the NX class name with the ``NX`` prefix removed and lowercased
    (e.g. ``pixel_shape_off_geometry``, ``pixel_shape_cylindrical_geometry``).
    """

    # ``class`` is a Python reserved keyword → must keep nx_ prefix here.
    nx_class: str
    group_name: str
    optionality: Literal["required", "recommended", "optional"] = "optional"
    deprecated: str | None = None


# Resolve the `Definition` ForwardRef used inside AnnotationModel.m_definition.
NeXusDefinition.model_rebuild()
NeXusGroup.model_rebuild()
NeXusField.model_rebuild()
NeXusAttribute.model_rebuild()
NeXusLink.model_rebuild()
NeXusChoice.model_rebuild()

# Explicit registration so that a_nexus_definition=... / a_nexus_group=... /
# a_nexus_field=... / a_nexus_attribute=... / a_nexus_link=... / a_nexus_choice=...
# work on Section / SubSection / Quantity definitions.
# Must be imported before any schema package loads.
AnnotationModel.m_registry["nexus_definition"] = NeXusDefinition
AnnotationModel.m_registry["nexus_group"] = NeXusGroup
AnnotationModel.m_registry["nexus_field"] = NeXusField
AnnotationModel.m_registry["nexus_attribute"] = NeXusAttribute
AnnotationModel.m_registry["nexus_link"] = NeXusLink
AnnotationModel.m_registry["nexus_choice"] = NeXusChoice
