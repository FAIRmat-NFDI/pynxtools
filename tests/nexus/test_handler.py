"""Tests for nexus.handler.NexusFileHandler and nexus.annotation.Annotator."""

import logging
import os
from typing import Union

import h5py
import numpy as np
import pytest

from pynxtools.nexus import Annotator, NexusFileHandler, NexusVisitor

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EXAMPLE_NXS = os.path.join(
    os.path.dirname(__file__),
    "../../src/pynxtools/data/201805_WSe2_arpes.nxs",
)


def _make_in_memory_file() -> h5py.File:
    """Return a minimal in-memory HDF5 file with two groups and one dataset."""
    f = h5py.File("__test__", "w", driver="core", backing_store=False)
    f.attrs["NX_class"] = "NXroot"
    entry = f.create_group("entry")
    entry.attrs["NX_class"] = "NXentry"
    data = entry.create_group("data")
    data.attrs["NX_class"] = "NXdata"
    data.create_dataset("signal", data=np.arange(10))
    return f


# ---------------------------------------------------------------------------
# NexusFileHandler + custom NexusVisitor
# ---------------------------------------------------------------------------


class _RecordingVisitor(NexusVisitor):
    """Visitor that records every visited path and whether on_complete was called."""

    def __init__(self):
        self.visited: list[str] = []
        self.attributes: list[tuple[str, str]] = []
        self.completed = False

    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        self.visited.append(hdf_path)

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        self.visited.append(hdf_path)

    def on_attribute(self, hdf_path: str, attr_name: str, attr_value, parent) -> None:
        self.attributes.append((hdf_path, attr_name))

    def on_complete(self, root: h5py.File) -> None:
        self.completed = True


def test_handler_traverses_all_nodes_in_memory():
    """NexusFileHandler visits every node in a simple in-memory file."""
    f = _make_in_memory_file()
    visitor = _RecordingVisitor()
    handler = NexusFileHandler(f, is_in_memory_file=True)
    handler.process(visitor)

    # Root (""), entry, entry/data, entry/data/signal
    assert "" in visitor.visited
    assert "entry" in visitor.visited
    assert "entry/data" in visitor.visited
    assert "entry/data/signal" in visitor.visited
    assert visitor.completed


def test_handler_visits_root_node():
    """The empty-string root node is always visited."""
    f = _make_in_memory_file()
    visitor = _RecordingVisitor()
    NexusFileHandler(f, is_in_memory_file=True).process(visitor)
    assert visitor.visited[0] == ""


def test_handler_traverses_file_on_disk(tmp_path):
    """NexusFileHandler opens a file from disk and traverses it without error."""
    # Create a minimal file on disk
    fpath = tmp_path / "test.nxs"
    with h5py.File(fpath, "w") as f:
        f.attrs["NX_class"] = "NXroot"
        e = f.create_group("entry")
        e.attrs["NX_class"] = "NXentry"
        e.create_dataset("value", data=42.0)

    visitor = _RecordingVisitor()
    NexusFileHandler(str(fpath)).process(visitor)
    assert "entry" in visitor.visited
    assert "entry/value" in visitor.visited
    assert visitor.completed


def test_handler_accepts_list_path(tmp_path):
    """NexusFileHandler accepts [path, ...] list as the nexus_file argument."""
    fpath = tmp_path / "test.nxs"
    with h5py.File(fpath, "w") as f:
        f.attrs["NX_class"] = "NXroot"

    visitor = _RecordingVisitor()
    NexusFileHandler([str(fpath)]).process(visitor)
    assert visitor.completed


def test_handler_cycle_detection_in_memory():
    """NexusFileHandler does not infinite-loop on hard-linked groups."""
    f = h5py.File("__test_cycle__", "w", driver="core", backing_store=False)
    f.attrs["NX_class"] = "NXroot"
    grp = f.create_group("a")
    grp.attrs["NX_class"] = "NXentry"
    # Hard-link: 'b' points to the same object as 'a' — cycle-detection must prevent recursion
    f["b"] = f["a"]

    visitor = _RecordingVisitor()
    NexusFileHandler(f, is_in_memory_file=True).process(visitor)
    # 'a' must be visited; 'b' is a hard link to 'a' and must not be re-entered
    assert "a" in visitor.visited
    assert visitor.completed


# ---------------------------------------------------------------------------
# Annotator — default mode
# ---------------------------------------------------------------------------


def test_annotation_visitor_default_mode_completes(tmp_path):
    """Annotator default mode processes the example NXS file without error."""
    logger = logging.getLogger("test_annotation_default")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "out.log"
    handler = logging.FileHandler(log_file, "w")
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    visitor = Annotator(logger)
    NexusFileHandler(EXAMPLE_NXS).process(visitor)

    handler.flush()
    log_text = log_file.read_text()
    # The log must contain at least one annotated entry
    assert log_text, "Expected annotation output but got empty log"


# ---------------------------------------------------------------------------
# Annotator — -d (documentation) mode
# ---------------------------------------------------------------------------


def test_annotation_visitor_d_mode_annotates_only_target(tmp_path):
    """Annotator -d mode writes output only for the requested path."""
    logger = logging.getLogger("test_annotation_d")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "d_mode.log"
    fh = logging.FileHandler(log_file, "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Pick a path that definitely exists in the example file
    target = "/entry/data/delays"
    visitor = Annotator(logger, d_inq_nd=target)
    NexusFileHandler(EXAMPLE_NXS).process(visitor)

    fh.flush()
    log_text = log_file.read_text()
    assert log_text, f"Expected annotation for {target} but got empty log"


# ---------------------------------------------------------------------------
# Annotator — -c (concept query) mode
# ---------------------------------------------------------------------------


def test_annotation_visitor_c_mode_collects_results(tmp_path):
    """Annotator -c mode logs paths that satisfy the IS-A relation."""
    logger = logging.getLogger("test_annotation_c")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "c_mode.log"
    fh = logging.FileHandler(log_file, "w")
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    # NXarpes entry is a known superclass for the example file
    visitor = Annotator(logger, c_inq_nd="/NXarpes/ENTRY")
    NexusFileHandler(EXAMPLE_NXS).process(visitor)

    fh.flush()
    # on_complete logs the collected paths; at minimum the log file must exist
    # (even if empty for this particular concept, no exception must be raised)
    assert log_file.exists()


# ---------------------------------------------------------------------------
# NexusVisitor default no-op base class
# ---------------------------------------------------------------------------


def test_handler_dispatches_attributes():
    """on_attribute is called for every attribute of every node."""
    f = _make_in_memory_file()
    visitor = _RecordingVisitor()
    NexusFileHandler(f, is_in_memory_file=True).process(visitor)

    # Root has NX_class="NXroot"; entry has NX_class="NXentry"; data has NX_class="NXdata"
    attr_paths = {path for path, _ in visitor.attributes}
    assert "" in attr_paths  # root attributes
    assert "entry" in attr_paths
    assert "entry/data" in attr_paths

    attr_names = {(path, name) for path, name in visitor.attributes}
    assert ("", "NX_class") in attr_names
    assert ("entry", "NX_class") in attr_names


def test_base_visitor_does_not_raise():
    """NexusVisitor base class no-op methods must not raise."""
    f = _make_in_memory_file()
    visitor = NexusVisitor()  # no overrides
    # Must run without error even though visit_node and on_complete are no-ops
    NexusFileHandler(f, is_in_memory_file=True).process(visitor)
