# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""A cheap, read-only view of one input file, shared by all parsers.

A reader creates one ``FileProbe`` per input file and passes it to every
parser that asks "is this my file?". The probe reads the first bytes of the
file once; everything else (HDF5 keys, TIFF tags, ...) is read lazily, only
when a parser asks for it, and then cached. No check ever loads the data
of a file, so probing stays cheap even for files of several GB.
"""

import os
import warnings
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from types import MappingProxyType
from typing import Any

import h5py
from PIL import TiffImagePlugin

#: Number of bytes read from the start of every file.
DEFAULT_HEAD_SIZE = 64 * 1024


def _read_bytes(path: Path, offset: int, size: int) -> bytes:
    """Read ``size`` bytes of ``path`` starting at ``offset``."""
    with path.open("rb") as file:
        file.seek(offset)
        return file.read(size)


@dataclass(frozen=True)
class FileProbe:
    """
    A read-only view of one input file.

    Create it with ``FileProbe.from_path``. The checks below never raise for
    unreadable or corrupt content: a file that looks like HDF5 but cannot be
    opened gives empty keys, and a broken TIFF gives no tags.

    Attributes:
        path: The file.
        suffixes: All suffixes of the file name, lower-case, e.g.
            ``(".mtex", ".h5")`` for ``scan.mtex.H5``.
        size: File size in bytes.
        head: The first ``DEFAULT_HEAD_SIZE`` bytes (fewer for a smaller file).
    """

    path: Path
    suffixes: tuple[str, ...]
    size: int
    head: bytes = field(repr=False)

    @classmethod
    def from_path(
        cls, path: str | os.PathLike, head_size: int = DEFAULT_HEAD_SIZE
    ) -> "FileProbe":
        """
        Probe the file at ``path``, reading only its first ``head_size`` bytes.

        Raises:
            OSError: If ``path`` is not a readable file, e.g. a directory.
        """
        path = Path(path)
        head = _read_bytes(path, 0, head_size)
        return cls(
            path=path,
            suffixes=tuple(suffix.lower() for suffix in path.suffixes),
            size=path.stat().st_size,
            head=head,
        )

    def has_suffix(self, suffix: str) -> bool:
        """
        Whether the file name ends with ``suffix``, ignoring case.

        Unlike ``pathlib`` suffixes, ``suffix`` can be any ending of the file
        name: ``".mtex.h5"`` matches ``"scan.mtex.h5"``, ``"range_.h5"``
        matches ``"001.range_.h5"``, and ``".h5"`` matches both.
        """
        return self.path.name.lower().endswith(suffix.lower())

    @cached_property
    def text_head(self) -> str | None:
        """
        The head decoded as text, or ``None`` if it looks binary.

        A head with a NUL byte counts as binary (so UTF-16 text is binary
        here). Bytes that are not valid UTF-8 are replaced, and a leading
        UTF-8 byte order mark is dropped.

        It covers only the first ``head_size`` bytes of the file (64 KiB by
        default). A parser that needs content further in reads ``path``
        itself.
        """
        if b"\x00" in self.head:
            return None
        return self.head.decode("utf-8-sig", errors="replace")

    @cached_property
    def is_hdf5(self) -> bool:
        """Whether the file carries the HDF5 signature, also after a user block."""
        return h5py.is_hdf5(self.path)

    @cached_property
    def _hdf5_root(self) -> tuple[frozenset[str], Mapping[str, Any]]:
        """Names and attributes of the HDF5 root group, read once together."""
        if not self.is_hdf5:
            return frozenset(), MappingProxyType({})
        try:
            # No file lock: the probe only reads, and locking fails on some
            # network drives and while another program writes the file.
            with h5py.File(self.path, "r", locking=False) as hdf:
                keys = frozenset(hdf.keys())
                attrs = dict(hdf.attrs.items())
        except (OSError, RuntimeError, KeyError, ValueError):
            # Corrupt or unsupported content: no keys, no raise. h5py raises
            # OSError if it cannot open the file, RuntimeError or KeyError
            # for a broken group index, and ValueError for unsupported options.
            return frozenset(), MappingProxyType({})
        return keys, MappingProxyType(attrs)

    @property
    def hdf5_root_keys(self) -> frozenset[str]:
        """Names of the groups and datasets in the HDF5 root (no data is read)."""
        return self._hdf5_root[0]

    @property
    def hdf5_root_attrs(self) -> Mapping[str, Any]:
        """Attributes of the HDF5 root group, e.g. a vendor name."""
        return self._hdf5_root[1]

    @cached_property
    def is_zip(self) -> bool:
        """Whether the file is a zip archive (checked by its index at the end)."""
        return zipfile.is_zipfile(self.path)

    @cached_property
    def is_tiff(self) -> bool:
        """Whether the file starts with a TIFF header that Pillow can read."""
        return self.head.startswith(tuple(TiffImagePlugin.PREFIXES))

    @cached_property
    def tiff_tags(self) -> Mapping[int, Any]:
        """
        The tags of the first TIFF page, keyed by tag number.

        Only the header and the tag directory are read, not the image, so
        this also works for images too large for Pillow to open. A broken
        TIFF gives no tags and no warning.
        """
        if not self.is_tiff:
            return MappingProxyType({})
        is_bigtiff = self.head[2:4] in (b"+\x00", b"\x00+")
        header = self.head[: 16 if is_bigtiff else 8]
        try:
            with warnings.catch_warnings():  # Pillow warns about broken tags
                warnings.simplefilter("ignore")
                directory = TiffImagePlugin.ImageFileDirectory_v2(header)
                with self.path.open("rb") as file:
                    file.seek(directory.next)
                    directory.load(file)
                tags = dict(directory)
        except Exception:  # broken TIFF: no tags, no raise
            return MappingProxyType({})
        return MappingProxyType(tags)
