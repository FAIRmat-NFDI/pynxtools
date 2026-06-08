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

DATA_DIR = Path(__file__).parents[2] / "src" / "pynxtools" / "data"
ARPES_FILE = str(DATA_DIR / "201805_WSe2_arpes.nxs")
ELLIPS_FILE = str(Path(__file__).parent / "data" / "SiO2onSi.ellips.nxs")
LAUETOF_FILE = str(Path(__file__).parent / "data" / "NXlauetof.hdf5")


@pytest.fixture(scope="module")
def arpes_archive():
    """Parse the ARPES example file and return the EntryArchive."""
    from nomad.datamodel import EntryArchive
    from nomad.utils import get_logger

    from pynxtools.nomad.parsers.parser_v2 import NexusParserV2

    archive = EntryArchive()
    NexusParserV2().parse(ARPES_FILE, archive, get_logger(__name__))
    return archive


# ---------------------------------------------------------------------------
# Test 1: ARPES golden output — archive.data is now the Entry directly
# ---------------------------------------------------------------------------


def test_nexus_v2_arpes_archive_data_is_entry(arpes_archive):
    """archive.data must be an Entry/Arpes instance (not a Root wrapper)."""
    from pynxtools.nomad.metainfo.base_classes.entry import Entry

    assert arpes_archive.data is not None
    assert isinstance(arpes_archive.data, Entry)


def test_nexus_v2_arpes_application_class(arpes_archive):
    """NXarpes application class must be resolved as archive.data."""
    cls_name = type(arpes_archive.data).__name__
    assert cls_name in ("Arpes", "Entry"), f"Unexpected entry class: {cls_name}"


def test_nexus_v2_arpes_entry_name(arpes_archive):
    """HDF5 entry group name must be preserved as nx_name on archive.data."""
    assert arpes_archive.data.__dict__.get("nx_name") == "entry"


def test_nexus_v2_arpes_definition(arpes_archive):
    """Definition field must be set on archive.data."""
    assert getattr(arpes_archive.data, "definition", None) == "NXarpes"


def test_nexus_v2_arpes_start_time(arpes_archive):
    """start_time must be populated on archive.data."""
    assert getattr(arpes_archive.data, "start_time", None) is not None


def test_nexus_v2_arpes_instrument(arpes_archive):
    """Instrument subsection must exist directly on archive.data."""
    entry = arpes_archive.data
    assert hasattr(entry, "instrument")
    assert len(entry.instrument) >= 1
    assert entry.instrument[0].__dict__.get("nx_name") == "instrument"


def test_nexus_v2_arpes_m_nx_data_path(arpes_archive):
    """m_nx_data_path on archive.data must be a valid JSON dict."""
    path_map_str = getattr(arpes_archive.data, "m_nx_data_path", None)
    assert path_map_str is not None, "m_nx_data_path not set on archive.data"
    path_map = json.loads(path_map_str)
    assert isinstance(path_map, dict)
    assert len(path_map) > 0


def test_nexus_v2_arpes_serialization(arpes_archive):
    """Archive must serialize to dict without errors."""
    d = arpes_archive.m_to_dict(with_out_meta=True)
    assert isinstance(d, dict)


def test_nexus_v2_arpes_entry_type(arpes_archive):
    """entry_type metadata must mention NXarpes."""
    assert "NXarpes" in (arpes_archive.metadata.entry_type or "")


# ---------------------------------------------------------------------------
# Test 2: Entry is a valid EntryData subclass
# ---------------------------------------------------------------------------


def test_nexus_v2_entry_bases():
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
# Test 3: Parity with v1 parser (structural)
# ---------------------------------------------------------------------------


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
# Test 4: Ellipsometry file (no serialization errors)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not Path(ELLIPS_FILE).exists(), reason="ellips file not found")
def test_nexus_v2_ellips_no_error():
    """Ellipsometry file must parse and serialize without errors."""
    from nomad.datamodel import EntryArchive
    from nomad.utils import get_logger

    from pynxtools.nomad.parsers.parser_v2 import NexusParserV2

    archive = EntryArchive()
    NexusParserV2().parse(ELLIPS_FILE, archive, get_logger(__name__))
    assert archive.data is not None
    archive.m_to_dict(with_out_meta=True)


# ---------------------------------------------------------------------------
# Test 5: NXlauetof (renamed groups)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not Path(LAUETOF_FILE).exists(), reason="lauetof file not found")
def test_nexus_v2_lauetof_renamed_groups():
    """NXlauetof must parse with archive.data set."""
    from nomad.datamodel import EntryArchive
    from nomad.utils import get_logger

    from pynxtools.nomad.parsers.parser_v2 import NexusParserV2

    archive = EntryArchive()
    NexusParserV2().parse(LAUETOF_FILE, archive, get_logger(__name__))
    assert archive.data is not None


# ---------------------------------------------------------------------------
# Test 6: App v2 configuration
# ---------------------------------------------------------------------------


def test_nexus_app_v2_schema():
    """App v2 must reference the correct Entry class."""
    from pynxtools.nomad.apps.app_v2 import nexus_app_v2, schema

    assert schema == "pynxtools.nomad.metainfo.base_classes.entry.Entry"
    filters = nexus_app_v2.app.filters_locked
    assert "section_defs.definition_qualified_name" in filters
    assert filters["section_defs.definition_qualified_name"] == [schema]


def test_nexus_app_v2_basic_properties():
    """App v2 must have correct label, path, and category."""
    from pynxtools.nomad.apps.app_v2 import nexus_app_v2

    app = nexus_app_v2.app
    assert app.label == "NeXus v2"
    assert app.path == "nexusappv2"
    assert app.category == "Experiment"


# ---------------------------------------------------------------------------
# Test 7: Pre-scan detection
# ---------------------------------------------------------------------------


def test_nexus_v2_prescan_detects_definition():
    """Pre-scan must detect the NXarpes definition in the ARPES file."""
    from nomad.utils import get_logger

    from pynxtools.nexus.handler import NexusFileHandler
    from pynxtools.nomad.parsers.parser_v2 import _PrescanVisitor

    prescan = _PrescanVisitor()
    NexusFileHandler(ARPES_FILE).prescan(prescan)
    assert prescan.entry_definitions == {"entry": "NXarpes"}
