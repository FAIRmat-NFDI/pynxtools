"""
NOMAD annotation models for NeXus sections and quantities.

NeXusDefinition — attached to Section.m_def; mirrors NXDL <definition> semantics.
NeXusGroup      — attached to SubSection definitions; mirrors NXDL <group> semantics.
NeXusQuantity   — attached to Quantity definitions; mirrors NXDL <field>/<attribute>.

The split between NeXusDefinition and NeXusGroup mirrors the NXDL schema:
- <definition> carries category, ignore-extra flags, symbols, and restricts.
- <group> carries the instance name, name_type, optionality, and occurrence limits.

Usage:

    m_def = Section(a_nexus_definition=NeXusDefinition(nx_class="NXentry", ...))
    data  = SubSection(..., a_nexus_group=NeXusGroup(nx_class="NXdata", ...))
    qty   = Quantity(..., a_nexus_quantity=NeXusQuantity(kind="field", ...))

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

    Corresponds to the NXDL <definition> element.  Carries the class identity
    and definition-level validation controls.  One per generated Python class.
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

    Corresponds to a NXDL <group> child element.  Carries the instance name,
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


class NeXusQuantity(AnnotationModel):
    """Annotation on Quantity for NeXus field and attribute semantics.

    Field names mirror NXDL XML attributes directly.  ``kind`` distinguishes
    fields (have units, interpretation, long_name) from attributes (do not).
    """

    kind: Literal["field", "attribute"]
    name: str
    parent_field: str | None = None
    # ``type`` is a Python builtin but valid as a Pydantic field name.
    type: str = "NX_CHAR"
    # NX unit category (e.g. "NX_ENERGY").  Only meaningful for kind="field".
    units: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    enumeration: list[str] | None = None
    open_enum: bool = False
    # From NXDL fieldType/@interpretation.  Only meaningful for kind="field".
    interpretation: str | None = None
    # From NXDL fieldType/@long_name.  Only meaningful for kind="field".
    long_name: str | None = None
    deprecated: str | None = None


# Resolve the `Definition` ForwardRef used inside AnnotationModel.m_definition.
NeXusDefinition.model_rebuild()
NeXusGroup.model_rebuild()
NeXusQuantity.model_rebuild()

# Explicit registration so that a_nexus_definition=... / a_nexus_group=... /
# a_nexus_quantity=... work on Section / SubSection / Quantity definitions.
# Must be imported before any schema package loads.
AnnotationModel.m_registry["nexus_definition"] = NeXusDefinition
AnnotationModel.m_registry["nexus_group"] = NeXusGroup
AnnotationModel.m_registry["nexus_quantity"] = NeXusQuantity
