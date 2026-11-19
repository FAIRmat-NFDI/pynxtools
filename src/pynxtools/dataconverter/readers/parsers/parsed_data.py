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
import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeAlias

import numpy as np
import xarray as xr

logger = logging.getLogger("pynxtools")


@dataclass(frozen=True)
class HDF5Reference:
    """
    A dataset that stays in a source HDF5 file instead of being loaded.

    Input files are not kept open between reading, validation and writing, so
    a live ``h5py.Dataset`` can't be passed on. A reference names the file and
    the dataset path instead; whoever needs the data opens the file briefly.

    Attributes:
        file: The HDF5 file.
        path: The path of the dataset inside the file, e.g. ``"/entry/data"``.
    """

    file: Path
    path: str


#: What ``ParsedData.data`` may hold. ``np.memmap`` is an ``np.ndarray``
#: subclass, so raw binary files can be mapped instead of loaded.
DataValue: TypeAlias = np.ndarray | xr.DataArray | HDF5Reference


@dataclass
class ParsedData:
    """
    What a parser read for one NeXus entry.

    Attributes:
        data: Arrays addressed by ``@data:<path>``: a numpy array (also
            ``np.memmap``), an ``xarray.DataArray``, or an ``HDF5Reference``
            to a dataset that stays in its source file.
        metadata: Flat key-value metadata with ``/``-separated keys,
            addressed by ``@attrs:<path>``.
        dims: Dimension names per data path, used for ``*`` expansion in
            config files.
        source: The file this entry was read from, if any.
    """

    data: dict[str, DataValue] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    dims: dict[str, list[str]] = field(default_factory=dict)
    source: Path | None = None
    _used_metadata: set[str] = field(
        default_factory=set, init=False, repr=False, compare=False
    )

    def get_metadata(self, path: str) -> Any:
        """
        Look up a metadata value, as for an ``@attrs:<path>`` token.

        Empty values give ``None``, and a ``datetime`` is returned as an
        ISO 8601 string. The key that was found counts as used, see
        ``unused_metadata``.
        """

        def find_key() -> str | None:
            """
            The key for ``path``: an exact key wins. Otherwise the first key
            that ends with ``"/" + path`` is used, so ``"energy/@units"`` also
            finds ``"instrument/analyser/energy/@units"``. If several keys end
            with it, a warning names them all.
            """
            if path in self.metadata:
                return path
            matches = [key for key in self.metadata if key.endswith(f"/{path}")]
            if len(matches) > 1:
                logger.warning(
                    f"Several metadata keys end with '{path}': "
                    f"{', '.join(matches)}. Using '{matches[0]}'; write the full "
                    "key in the config file to choose another one."
                )
            return matches[0] if matches else None

        def is_empty(value: Any) -> bool:
            """``None``, ``""``, ``"None"`` and a list of empty strings."""
            if value is None or str(value) in {"None", ""}:
                return True
            return isinstance(value, list) and all(item == "" for item in value)

        key = find_key()
        if key is None:
            return None
        self._used_metadata.add(key)
        value = self.metadata[key]
        if is_empty(value):
            return None
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        return value

    def get_data(self, path: str) -> DataValue | None:
        """Return the data stored under ``path`` (``@data:<path>``), or ``None``."""
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
