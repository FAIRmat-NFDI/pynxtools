# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""A common container for what a parser read for one NeXus entry.

A parser fills one ``ParsedData`` per entry: arrays in ``data``, flat
``/``-separated metadata in ``metadata``. A reader then looks values up for
the ``@data:`` and ``@attrs:`` tokens of its config file. The lookups record
which metadata keys were read, so the reader can report metadata that no
config entry used.

Plugins can subclass ``ParsedData`` to add their own fields or methods, for
example averaging over scans.
"""

import datetime
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _is_empty(value: Any) -> bool:
    """Whether a metadata value carries no information."""
    if value is None or str(value) in {"None", ""}:
        return True
    return isinstance(value, list) and all(item == "" for item in value)


@dataclass
class ParsedData:
    """
    What a parser read for one NeXus entry.

    Attributes:
        data: Arrays (numpy or xarray), addressed by ``@data:<path>``.
        metadata: Flat key-value metadata with ``/``-separated keys,
            addressed by ``@attrs:<path>``.
        dims: Dimension names per data path, used for ``*`` expansion in
            config files.
        source: The file this entry was read from, if any.
    """

    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    dims: dict[str, list[str]] = field(default_factory=dict)
    source: Path | None = None
    _used_metadata: set[str] = field(
        default_factory=set, init=False, repr=False, compare=False
    )

    def get_metadata(self, path: str) -> Any:
        """
        Look up a metadata value, as for an ``@attrs:<path>`` token.

        An exact key wins. Otherwise the first key that ends with
        ``"/" + path`` is used, so ``"energy/@units"`` also finds
        ``"instrument/analyser/energy/@units"``. Empty values (``None``,
        ``""``, ``"None"``, a list of empty strings) give ``None``, and a
        ``datetime`` is returned as an ISO 8601 string.

        The key that was found counts as used, see ``unused_metadata``.
        """
        key = self._find_metadata_key(path)
        if key is None:
            return None
        self._used_metadata.add(key)
        value = self.metadata[key]
        if _is_empty(value):
            return None
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        return value

    def _find_metadata_key(self, path: str) -> str | None:
        if path in self.metadata:
            return path
        return next((key for key in self.metadata if key.endswith(f"/{path}")), None)

    def get_data(self, path: str) -> Any:
        """Return the array stored under ``path`` (``@data:<path>``), or ``None``."""
        return self.data.get(path)

    def get_dims(self, path: str) -> list[str]:
        """Return the dimension names of the array under ``path``, or ``[]``."""
        return list(self.dims.get(path, []))

    @property
    def unused_metadata(self) -> set[str]:
        """Metadata keys that no ``get_metadata`` call has read so far."""
        return set(self.metadata) - self._used_metadata

    def mark_metadata_used(self, keys: Iterable[str]) -> None:
        """Count ``keys`` as used, e.g. metadata a parser maps by itself."""
        self._used_metadata.update(key for key in keys if key in self.metadata)
