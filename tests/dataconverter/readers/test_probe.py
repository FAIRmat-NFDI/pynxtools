# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for the FileProbe that parsers use to recognize their files."""

import struct
import subprocess
import sys
import zipfile

import h5py
import numpy as np
import pytest
from PIL import Image

from pynxtools.dataconverter.readers.parsers import probe as probe_module
from pynxtools.dataconverter.readers.parsers.probe import DEFAULT_HEAD_SIZE, FileProbe


def write_hdf5(path, userblock_size=0):
    """Write a small HDF5 file with a group, a dataset and a root attribute."""
    with h5py.File(path, "w", userblock_size=userblock_size) as hdf:
        hdf.create_group("entry")
        hdf.create_dataset("counts", data=np.arange(10))
        hdf.attrs["vendor"] = "Some Vendor"


def test_suffixes_are_lower_case_and_keep_the_whole_chain(tmp_path):
    """Suffixes are lower-cased and compound suffixes are kept as a chain."""
    path = tmp_path / "scan.MTEX.H5"
    path.write_bytes(b"")
    probe = FileProbe.from_path(path)
    assert probe.suffixes == (".mtex", ".h5")
    assert probe.size == 0
    assert probe.head == b""


@pytest.mark.parametrize(
    "name, suffix, expected",
    [
        ("scan.mtex.h5", ".mtex.h5", True),
        ("scan.mtex.h5", ".h5", True),
        ("SCAN.MTEX.H5", ".mtex.h5", True),
        ("001.range_.h5", "range_.h5", True),
        ("scan.h5", ".mtex.h5", False),
        ("scan.h5.txt", ".h5", False),
    ],
)
def test_has_suffix_handles_compound_endings(tmp_path, name, suffix, expected):
    """has_suffix matches compound and non-dotted endings, ignoring case."""
    path = tmp_path / name
    path.write_bytes(b"")
    assert FileProbe.from_path(path).has_suffix(suffix) is expected


def test_head_is_limited_to_the_head_size(tmp_path):
    """Only the first head_size bytes of a file are read into head."""
    path = tmp_path / "large.bin"
    path.write_bytes(b"a" * (DEFAULT_HEAD_SIZE + 100))
    assert len(FileProbe.from_path(path).head) == DEFAULT_HEAD_SIZE
    assert len(FileProbe.from_path(path, head_size=16).head) == 16


def test_a_directory_cannot_be_probed(tmp_path):
    """Probing a directory raises an OSError."""
    with pytest.raises(OSError):
        FileProbe.from_path(tmp_path)


def test_text_head_decodes_text(tmp_path):
    """text_head decodes a UTF-8 text file."""
    path = tmp_path / "spectrum.xy"
    path.write_text("# Created by: SpecsLab Prodigy\n1.0 2.0\n", encoding="utf-8")
    probe = FileProbe.from_path(path)
    assert probe.text_head is not None
    assert probe.text_head.startswith("# Created by: SpecsLab Prodigy")


def test_text_head_drops_a_byte_order_mark(tmp_path):
    """text_head drops a leading UTF-8 byte order mark."""
    path = tmp_path / "with_bom.txt"
    path.write_bytes(b"\xef\xbb\xbfVAMAS Surface Chemical Analysis")
    assert FileProbe.from_path(path).text_head == "VAMAS Surface Chemical Analysis"


def test_text_head_is_none_for_binary_files(tmp_path):
    """text_head is None for a file with NUL bytes."""
    path = tmp_path / "data.bin"
    path.write_bytes(b"\x00\x01\x02\x03")
    assert FileProbe.from_path(path).text_head is None


def test_checks_are_computed_once(tmp_path):
    """A check is computed once and then cached."""
    path = tmp_path / "spectrum.txt"
    path.write_text("some text")
    probe = FileProbe.from_path(path)
    assert probe.text_head is probe.text_head


@pytest.mark.parametrize("userblock_size", [0, 512, 128 * 1024])
def test_hdf5_is_recognized_with_and_without_a_user_block(tmp_path, userblock_size):
    """HDF5 files are recognized and their root read, also after a user block."""
    # 128 KiB puts the signature beyond the head.
    path = tmp_path / "data.h5"
    write_hdf5(path, userblock_size=userblock_size)
    probe = FileProbe.from_path(path)
    assert probe.is_hdf5
    assert probe.hdf5_root_keys == {"entry", "counts"}
    assert probe.hdf5_root_attrs["vendor"] == "Some Vendor"


def test_hdf5_keys_are_read_while_another_program_writes_the_file(tmp_path):
    """Root keys are read while another process holds the file open for writing."""
    path = tmp_path / "busy.h5"
    writer = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys, h5py\n"
            "hdf = h5py.File(sys.argv[1], 'w')\n"
            "hdf.create_group('entry')\n"
            "hdf.flush()\n"
            "print('open', flush=True)\n"
            "sys.stdin.read()\n",
            str(path),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert writer.stdout.readline().strip() == "open"
        probe = FileProbe.from_path(path)
        assert probe.hdf5_root_keys == {"entry"}
    finally:
        writer.communicate(input="")


def test_a_corrupt_hdf5_file_gives_no_keys(tmp_path):
    """A file with the HDF5 signature but corrupt content gives no keys."""
    path = tmp_path / "broken.h5"
    path.write_bytes(b"\x89HDF\r\n\x1a\n" + b"garbage" * 100)
    probe = FileProbe.from_path(path)
    assert probe.is_hdf5
    assert probe.hdf5_root_keys == frozenset()
    assert dict(probe.hdf5_root_attrs) == {}


def test_an_hdf5_file_with_a_broken_group_index_gives_no_keys(tmp_path):
    """A broken group index makes h5py raise a RuntimeError; the probe gives no keys."""
    path = tmp_path / "broken_index.h5"
    write_hdf5(path)
    content = path.read_bytes()
    path.write_bytes(content.replace(b"TREE", b"XXXX", 1))  # root group B-tree
    probe = FileProbe.from_path(path)
    assert probe.is_hdf5
    assert probe.hdf5_root_keys == frozenset()
    assert dict(probe.hdf5_root_attrs) == {}


def test_a_text_file_is_not_hdf5(tmp_path):
    """A text file with an .h5 extension is not HDF5."""
    path = tmp_path / "notes.h5"
    path.write_text("not an HDF5 file")
    probe = FileProbe.from_path(path)
    assert not probe.is_hdf5
    assert probe.hdf5_root_keys == frozenset()


def test_zip_is_recognized(tmp_path):
    """A zip archive is recognized and is neither HDF5 nor TIFF."""
    path = tmp_path / "archive.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("inside.txt", "hello")
    probe = FileProbe.from_path(path)
    assert probe.is_zip
    assert not probe.is_hdf5
    assert not probe.is_tiff


def test_a_truncated_zip_is_not_a_zip(tmp_path):
    """A file that starts like a zip but has no archive index is not a zip."""
    path = tmp_path / "truncated.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("inside.txt", "hello")
    content = path.read_bytes()
    path.write_bytes(content[: len(content) // 2])
    assert not FileProbe.from_path(path).is_zip


def test_a_zip_with_data_in_front_is_a_zip(tmp_path):
    """A zip with other data before it, e.g. a self-extracting archive, is a zip."""
    archive_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("inside.txt", "hello")
    path = tmp_path / "self_extracting.exe"
    path.write_bytes(b"MZ" + b"\x00" * 100 + archive_path.read_bytes())
    assert FileProbe.from_path(path).is_zip


def test_tiff_tags_are_read(tmp_path):
    """The tags of a TIFF image are read."""
    path = tmp_path / "image.tif"
    image_description = 270
    Image.new("L", (4, 4)).save(path, tiffinfo={image_description: "my microscope"})
    probe = FileProbe.from_path(path)
    assert probe.is_tiff
    assert probe.tiff_tags[image_description] == "my microscope"
    assert not probe.is_zip


def test_a_tiff_with_a_nonstandard_header_is_recognized(tmp_path):
    """A TIFF with a nonstandard header that Pillow still reads is recognized."""
    path = tmp_path / "image.tif"
    image_description = 270
    Image.new("L", (4, 4)).save(path, tiffinfo={image_description: "my microscope"})
    content = path.read_bytes()
    assert content.startswith(b"II*\x00")
    path.write_bytes(b"II\x00*" + content[4:])
    probe = FileProbe.from_path(path)
    assert probe.is_tiff
    assert probe.tiff_tags[image_description] == "my microscope"


def write_tiff_header(path, width, height):
    """Write a classic TIFF with tags for a ``width`` x ``height`` image but no pixels."""
    tags = [  # (tag, type, value); type 3: SHORT, 4: LONG
        (256, 4, width),
        (257, 4, height),
        (258, 3, 8),
        (259, 3, 1),
        (262, 3, 1),
        (273, 4, 0),
        (277, 3, 1),
        (278, 4, height),
        (279, 4, width * height),
    ]
    directory = struct.pack("<H", len(tags))
    for tag, kind, value in tags:
        packed = struct.pack("<HH", value, 0) if kind == 3 else struct.pack("<I", value)
        directory += struct.pack("<HHI", tag, kind, 1) + packed
    path.write_bytes(b"II*\x00" + struct.pack("<I", 8) + directory + b"\x00" * 4)


def test_tiff_tags_are_read_for_images_too_large_for_pillow(tmp_path):
    """Tags are read for a TIFF that Pillow refuses to open as a decompression bomb."""
    path = tmp_path / "large_map.tif"
    write_tiff_header(path, 20000, 20000)  # 400 million pixels
    probe = FileProbe.from_path(path)
    assert probe.tiff_tags[256] == 20000
    assert probe.tiff_tags[257] == 20000


def test_bigtiff_tags_are_read(tmp_path):
    """The tags of a BigTIFF image are read."""
    path = tmp_path / "image.tif"
    try:
        Image.new("L", (4, 3)).save(path, big_tiff=True)
    except (TypeError, ValueError):
        pytest.skip("this Pillow version cannot write BigTIFF")
    probe = FileProbe.from_path(path)
    assert probe.is_tiff
    assert probe.tiff_tags[256] == 4


def test_a_non_tiff_file_has_no_tiff_tags(tmp_path):
    """A file with a .tif extension but no TIFF signature has no tags."""
    path = tmp_path / "image.tif"
    path.write_text("not a TIFF")
    probe = FileProbe.from_path(path)
    assert not probe.is_tiff
    assert dict(probe.tiff_tags) == {}


def test_a_broken_tiff_gives_no_tags(tmp_path):
    """A TIFF with a broken tag directory gives no tags and does not raise."""
    path = tmp_path / "broken.tif"
    path.write_bytes(b"II*\x00" + b"\xff" * 20)
    probe = FileProbe.from_path(path)
    assert probe.is_tiff
    assert dict(probe.tiff_tags) == {}


def test_probing_a_5_gb_file_reads_only_a_little(tmp_path, monkeypatch):
    """The probe itself reads less than 1 MiB of a 5 GB file."""
    path = tmp_path / "huge.raw"
    with path.open("wb") as file:
        file.truncate(5 * 1024**3)  # sparse: takes no real disk space

    bytes_read = []
    original_read_bytes = probe_module._read_bytes

    def counting_read_bytes(path, offset, size):
        data = original_read_bytes(path, offset, size)
        bytes_read.append(len(data))
        return data

    monkeypatch.setattr(probe_module, "_read_bytes", counting_read_bytes)
    probe = FileProbe.from_path(path)
    assert probe.text_head is None
    assert not probe.is_hdf5
    assert not probe.is_zip
    assert not probe.is_tiff
    assert sum(bytes_read) < 1024**2
