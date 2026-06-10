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
Acceptance gate tests for NexusParserV2 (Phase 3).

Architecture: archive.data = Arpes/Entry() directly (no Root wrapper).
One NomadVisitorV2 per NXentry group; multi-NXentry files produce multiple archives.
"""

import json
from pathlib import Path

import pytest

try:
    from nomad.datamodel import EntryArchive
    from nomad.units import ureg
    from nomad.utils import get_logger
except ImportError:
    pytest.skip("nomad not installed", allow_module_level=True)

from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.parsers.parser_v2 import NexusParserV2

DATA_DIR = Path(__file__).parents[2] / "src" / "pynxtools" / "data"
TEST_DATA_DIR = Path(__file__).parents[1] / "data" / "nomad"
ARPES_FILE = str(DATA_DIR / "201805_WSe2_arpes.nxs")
ELLIPS_FILE = str(TEST_DATA_DIR / "SiO2onSi.ellips.nxs")
LAUETOF_FILE = str(TEST_DATA_DIR / "NXlauetof.hdf5")


@pytest.fixture(scope="module")
def arpes_archive():
    """Parse the ARPES example file and return the EntryArchive."""
    archive = EntryArchive()
    NexusParserV2().parse(ARPES_FILE, archive, get_logger(__name__))
    return archive


# ---------------------------------------------------------------------------
# ARPES golden output — archive.data is now the Entry directly
# ---------------------------------------------------------------------------
def test_arpes_example(arpes_archive):
    """Test contents of parsed arpes archive"""
    arpes_entry = arpes_archive.data

    assert arpes_entry is not None
    assert isinstance(arpes_entry, Entry)
    cls_name = type(arpes_entry).__name__
    assert cls_name in ("Arpes", "Entry"), f"Unexpected entry class: {cls_name}"
    assert arpes_entry.__dict__.get("nx_name") == "entry"
    assert getattr(arpes_entry, "definition", None) == "NXarpes"

    assert getattr(arpes_entry, "start_time", None) is not None

    # Instrument
    assert hasattr(arpes_entry, "instrument")
    assert len(arpes_entry.instrument) >= 1
    instrument = arpes_entry.instrument[0]
    assert instrument.nx_name == "instrument"

    # Source
    assert hasattr(instrument, "source")
    assert len(instrument.source) >= 1
    source = instrument.source[0]
    assert source.nx_name == "source"
    # good ENUM - x-ray
    assert source.probe == "x-ray"
    # wrong inherited ENUM - Burst (accepted for open enum)
    assert source.mode == "Burst"
    # wrong inherited ENUM for extended field - 'Free Electron Laser' (accepted for open enum)
    assert source.type == "Free Electron Laser"

    # Unit check
    assert instrument.analyser.entrance_slit_size == ureg.Quantity("750 micrometer")

    # Data
    assert hasattr(arpes_entry, "data")
    assert len(arpes_entry.data) >= 1
    data = arpes_entry.data[0]
    assert data.__dict__.get("nx_name") == "data"
    assert data.nx_name == "data"

    assert len(data.AXISNAME) == 3
    # there is still a bug in the variadic name resolution, so skip these
    assert data.delays is not None
    assert data.angles.check("1/Å")
    # ToDo: if AXISNAME and DATA can be resolved properly, extend this!
    # assert data.delays.check("fs")
    # but the following still works
    assert data.energies is not None
    assert data.energies.check("eV")
    # manual name resolution
    assert data.AXISNAME["angles"] is not None
    # TODO: reimplement with field statistics
    # assert data.AXISNAME__max["angles__max"].value == 2.168025463513032
    assert (1 * data.AXISNAME["angles"].unit).check("1/Å")
    assert (1 * data.AXISNAME["delays"].unit).check("fs")
    assert data.axes == ["angles", "energies", "delays"]


def test_arpes_m_nx_data_path(arpes_archive):
    """m_nx_data_path on archive.data must be a valid JSON dict."""
    arpes_entry = arpes_archive.data
    path_map_str = getattr(arpes_entry, "m_nx_data_path", None)
    assert path_map_str is not None, "m_nx_data_path not set on archive.data"
    path_map = json.loads(path_map_str)
    assert isinstance(path_map, dict)
    assert len(path_map) > 0


def test_arpes_serialization(arpes_archive):
    """Archive must serialize to dict without errors."""
    d = arpes_archive.m_to_dict(with_out_meta=True)
    assert isinstance(d, dict)


def test_arpes_metadata(arpes_archive):
    """Test metadata of the parsed ARPES archive."""
    # entry_type is the Python class name (Arpes if app loaded, Entry as fallback)."""
    metadata = arpes_archive.metadata
    entry_type = metadata.entry_type or ""
    assert entry_type in ("Arpes", "Entry"), f"Unexpected entry_type: {entry_type}"
    # entry_name is "{file stem} - {HDF5 NXentry group name}", not just "entry"."""
    assert metadata.entry_name == "201805_WSe2_arpes - entry"


# ---------------------------------------------------------------------------
# Ellipsometry file (no serialization errors)
# NXlauetof (renamed groups)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("file_path", "reason"),
    [
        (ELLIPS_FILE, "ellips file not found"),
        (LAUETOF_FILE, "lauetof file not found"),
    ],
)
def test_parse_valid_files(file_path, reason):
    print(file_path)
    pytest.skip(reason) if not Path(file_path).exists() else None

    archive = EntryArchive()
    NexusParserV2().parse(file_path, archive, get_logger(__name__))

    assert archive.data is not None

    if file_path == ELLIPS_FILE:
        archive.m_to_dict(with_out_meta=True)


# ---------------------------------------------------------------------------
# Entry is a valid EntryData subclass
# ---------------------------------------------------------------------------


# TODO: move this to the schema test
def test_entry_bases():
    """Entry inherits from Object and Measurement (not EntryData — would break frontend).

    archive.data = Entry() produces a SyntaxWarning but works correctly.
    EntryData.m_def has no m_package, so including it in base_sections breaks
    NOMAD's frontend schema resolution (_allBaseSections JS error).
    """
    from nomad.datamodel.metainfo.basesections import Measurement

    from pynxtools.nomad.metainfo.base_classes.entry import Entry
    from pynxtools.nomad.metainfo.base_classes.object import Object

    assert issubclass(Entry, Object)
    assert issubclass(Entry, Measurement)


# ---------------------------------------------------------------------------
# Parity with v1 parser (structural)
# ---------------------------------------------------------------------------


# This is good to have now, but will be useless when the v2 parser is the default
# TODO: remove this one the original NexusParser goes away
def test_nexus_v2_parity_structural():
    """V2 produces same definition field value as v1."""
    from nomad.datamodel import EntryArchive
    from nomad.utils import get_logger

    from pynxtools.nomad.parsers.parser import NexusParser
    from pynxtools.nomad.parsers.parser_v2 import NexusParserV2

    v1 = EntryArchive()
    v2 = EntryArchive()
    NexusParser().parse(ARPES_FILE, v1, get_logger(__name__))
    NexusParserV2().parse(ARPES_FILE, v2, get_logger(__name__))

    # v1: archive.data.ENTRY[0].definition__field
    # v2: archive.data.definition (Entry is directly archive.data)
    v1_entries = getattr(v1.data, "ENTRY", [])
    v1_def = getattr(v1_entries[0], "definition__field", None) if v1_entries else None
    v2_def = getattr(v2.data, "definition", None)

    assert v1_def == v2_def, f"Definition mismatch: v1={v1_def!r}, v2={v2_def!r}"


# ---------------------------------------------------------------------------
# Pre-scan detection
# ---------------------------------------------------------------------------


def test_nexus_v2_prescan_detects_definition():
    """Pre-scan must detect the NXarpes definition in the ARPES file."""
    from pynxtools.nexus.handler import NexusFileHandler
    from pynxtools.nomad.parsers.parser_v2 import _PrescanVisitor

    prescan = _PrescanVisitor()
    NexusFileHandler(ARPES_FILE).prescan(prescan)
    assert prescan.entry_definitions == {"entry": "NXarpes"}


# ---------------------------------------------------------------------------
# Root (Experiment) entry
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def arpes_root_archive():
    """Parse the ARPES file with a "root" child archive and return it."""
    archive = EntryArchive()
    root_archive = EntryArchive()
    NexusParserV2().parse(
        ARPES_FILE,
        archive,
        get_logger(__name__),
        child_archives={"root": root_archive},
    )
    return root_archive


def test_nexus_v2_root_archive_data_is_root(arpes_root_archive):
    """The "root" child archive must hold a Root instance grouping all NXentries."""
    from pynxtools.nomad.metainfo.base_classes.root import Root

    assert isinstance(arpes_root_archive.data, Root)
    assert arpes_root_archive.data.m_entry_paths == ["entry"]


def test_nexus_v2_root_archive_metadata(arpes_root_archive):
    """Root archive metadata must use the file-grouping naming convention."""
    assert arpes_root_archive.metadata.entry_name == "201805_WSe2_arpes (NeXus file)"
    assert arpes_root_archive.results.eln.methods == ["Arpes"]


def test_nexus_v2_root_nxroot_attributes(arpes_root_archive):
    """NXroot HDF5 group attributes (file_name, HDF5_Version, ...) must be parsed."""
    root = arpes_root_archive.data
    assert root.file_name == "/home/tommaso/Desktop/NeXus/Test/201805_WSe2_arpes.nxs"
    assert root.HDF5_Version == "1.10.5"
    assert root.file_time is not None
