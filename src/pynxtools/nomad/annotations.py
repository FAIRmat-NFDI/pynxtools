"""
NOMAD annotation models for NeXus sections and quantities.

NeXusGroup  — attached to Section.m_def and SubSection definitions.
NeXusQuantity — attached to Quantity definitions (fields and attributes).

Both are registered into NOMAD's AnnotationModel.m_registry so they can be
used as keyword arguments on Section / Quantity / SubSection definitions:

    m_def = Section(a_nexus_group=NeXusGroup(nx_class="NXentry", ...))
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


class NeXusGroup(AnnotationModel):
    """Annotation on Section.m_def (or SubSection) for NeXus group semantics.

    Applied to the Section.m_def of a generated base/application class, and to
    every SubSection definition within it, to carry the full NXDL provenance.

    Field names mirror NXDL XML attributes directly.  ``nx_class`` keeps its
    prefix because ``class`` is a Python reserved keyword.
    """

    # ``class`` is a Python reserved keyword → must keep nx_ prefix here.
    nx_class: str
    name: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    category: Literal["base", "application", "contributed"] = "base"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    min_occurs: int | None = None
    max_occurs: int | None = None
    # From NXDL definition/@restricts: non-standard items are errors, not warnings.
    restricts: bool = False
    # From NXDL definition/@ignoreExtra*: suppress unknown-child warnings during validation.
    ignore_extra_groups: bool = False
    ignore_extra_fields: bool = False
    ignore_extra_attributes: bool = False
    # Symbolic dimension names from the NXDL symbols table: {symbol: doc}.
    symbols: dict[str, str] | None = None
    doc_url: str | None = None
    deprecated: str | None = None


class NeXusQuantity(AnnotationModel):
    """Annotation on Quantity for NeXus field and attribute semantics.

    Field names mirror NXDL XML attributes directly.
    """

    kind: Literal["field", "attribute"]
    name: str
    parent_field: str | None = None
    # ``type`` is a Python builtin but valid as a Pydantic field name.
    type: str = "NX_CHAR"
    units: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    enumeration: list[str] | None = None
    open_enum: bool = False
    shape: list[str] | None = None
    # From NXDL fieldType/@interpretation: how to interpret data dimensions for
    # plotting. Values: scalar, spectrum, image, rgb-image, rgba-image,
    # hsl-image, hsla-image, cmyk-image, vertex.
    interpretation: str | None = None
    # From NXDL fieldType/@long_name: human-readable label for plot axes.
    long_name: str | None = None
    doc_url: str | None = None
    deprecated: str | None = None


# Resolve the `Definition` ForwardRef used inside AnnotationModel.m_definition.
NeXusGroup.model_rebuild()
NeXusQuantity.model_rebuild()

# Explicit registration so that a_nexus_group=... / a_nexus_quantity=... work
# on Section / SubSection / Quantity definitions.  Must be imported before any
# schema package loads.
AnnotationModel.m_registry["nexus_group"] = NeXusGroup
AnnotationModel.m_registry["nexus_quantity"] = NeXusQuantity
