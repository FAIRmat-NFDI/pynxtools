# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Fallback for NeXus ``identifierNAME`` fields that don't correspond to an existing
typed basesections entity (sample, instrument, ...) — ``Object.normalize()`` uses
``resolve_or_create_entity`` for that leftover case, wrapping a plain
``basesections.EntityReference`` rather than a pynxtools-specific reference class.
Identifiers that do map onto a typed entity (e.g. a ``Fabrication``/``InstrumentEntry``
or ``Sample``/``System``) set that section's own ``lab_id`` directly instead, and
never go through here.
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from nomad.datamodel import EntryArchive, EntryMetadata
from nomad.datamodel.metainfo.basesections import v2 as basesections
from nomad.utils import hash as archive_hash

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger

__all__ = ["resolve_or_create_entity"]


def _slugify(value: str) -> str:
    """Turn an identifier value into a safe, readable raw-file name fragment."""
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return slug.strip("_") or "identifier"


def resolve_or_create_entity(
    archive: EntryArchive, logger: BoundLogger, lab_id: str, name: str | None
) -> basesections.EntityReference:
    """Resolve `lab_id` to an existing NOMAD entry (by the normal `EntityReference`
    search), or create a minimal standalone `Entity` archive for it if none is found.
    """
    reference = basesections.EntityReference(name=name, lab_id=lab_id)
    reference.normalize(archive, logger)
    if reference.reference is None:
        reference.reference = _create_entity(archive, logger, lab_id, name)
    return reference


def _create_entity(
    archive: EntryArchive, logger: BoundLogger, lab_id: str, name: str | None
) -> str:
    """Create a standalone `Entity` archive for `lab_id` and return a reference
    string to it. Mirrors the raw-file-writing pattern of pynxtools' old v1
    `AnchoredReference`, with a readable file name instead of a hash."""
    entity = basesections.Entity()
    entity.lab_id = lab_id
    entity.name = name or lab_id

    file_name = _unique_file_name(archive, logger, lab_id)
    if file_name is None:
        # A file for this exact lab_id already exists (the identifier was seen
        # more than once in this upload) — reuse it instead of writing again.
        upload_id = archive.metadata.upload_id
        existing_name = f"Entity_{_slugify(lab_id)}.archive.json"
        entry_id = archive_hash(upload_id, existing_name)
        return f"../uploads/{upload_id}/archive/{entry_id}#data"

    entry = EntryArchive(
        data=entity,
        m_context=archive.m_context,
        metadata=EntryMetadata(entry_type="identifier", domain="nexus", readonly=True),
    )
    with archive.m_context.raw_file(file_name, "w") as f_obj:
        json.dump(entry.m_to_dict(with_meta=True), f_obj)
    archive.m_context.process_updated_raw_file(file_name)

    upload_id = archive.metadata.upload_id
    entry_id = archive_hash(upload_id, file_name)
    return f"../uploads/{upload_id}/archive/{entry_id}#data"


def _unique_file_name(
    archive: EntryArchive, logger: BoundLogger, lab_id: str
) -> str | None:
    """Return a free, readable raw-file name for `lab_id`, disambiguating with a
    numeric suffix only if the readable name is already taken by a *different*
    lab_id (`_slugify` is lossy, so distinct identifiers could in principle
    collide). Returns None if a file for this exact lab_id already exists."""
    base = _slugify(lab_id)
    file_name = f"Entity_{base}.archive.json"
    suffix = 2
    # Bounded: a real collision chain this deep would mean this many distinct
    # lab_ids happen to slugify to the same base, which shouldn't happen in
    # practice — the cap only guards against looping forever on a
    # misbehaving raw_path_exists implementation.
    while suffix < 1000 and archive.m_context.raw_path_exists(file_name):
        try:
            with archive.m_context.raw_file(file_name, "r") as f_obj:
                existing_lab_id = json.load(f_obj).get("data", {}).get("lab_id")
        except Exception as e:
            logger.warn(
                f"Could not read existing raw file '{file_name}' while "
                f"anchoring identifier '{lab_id}'.",
                exc_info=e,
            )
            existing_lab_id = None
        if existing_lab_id == lab_id:
            return None
        file_name = f"Entity_{base}_{suffix}.archive.json"
        suffix += 1
    return file_name
