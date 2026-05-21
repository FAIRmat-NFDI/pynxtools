"""Tests for nexus.handler.NexusFileHandler and nexus.annotation.Annotator."""

import logging
import os
from typing import Union

import h5py
import numpy as np
import pytest

from pynxtools.nexus.handler import NexusFileHandler, NexusVisitor

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
    handler = NexusFileHandler(f, is_open=True)
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
    NexusFileHandler(f, is_open=True).process(visitor)
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
    NexusFileHandler(f, is_open=True).process(visitor)
    # 'a' must be visited; 'b' is a hard link to 'a' and must not be re-entered
    assert "a" in visitor.visited
    assert visitor.completed


# ---------------------------------------------------------------------------
# NexusVisitor default no-op base class
# ---------------------------------------------------------------------------


def test_handler_dispatches_attributes():
    """on_attribute is called for every attribute of every node."""
    f = _make_in_memory_file()
    visitor = _RecordingVisitor()
    NexusFileHandler(f, is_open=True).process(visitor)

    # Root has NX_class="NXroot"; entry has NX_class="NXentry"; data has NX_class="NXdata"
    attr_paths = {path for path, _ in visitor.attributes}
    assert "" in attr_paths  # root attributes
    assert "entry" in attr_paths
    assert "entry/data" in attr_paths

    attr_names = {(path, name) for path, name in visitor.attributes}
    assert ("", "NX_class") in attr_names
    assert ("entry", "NX_class") in attr_names


def test_base_visitor_does_not_raise():
    """A visitor that implements all hooks as pass must not raise."""

    class _NullVisitor(NexusVisitor):
        def on_group(self, hdf_path, hdf_node) -> None:
            pass

        def on_field(self, hdf_path, hdf_node) -> None:
            pass

        def on_attribute(self, hdf_path, attr_name, attr_value, parent) -> None:
            pass

        def on_complete(self, root) -> None:
            pass

    f = _make_in_memory_file()
    NexusFileHandler(f, is_open=True).process(_NullVisitor())


# ---------------------------------------------------------------------------
# Link traversal tests
# ---------------------------------------------------------------------------


class _LinkVisitor(_RecordingVisitor):
    """Extends _RecordingVisitor to track broken and external links."""

    def __init__(self):
        super().__init__()
        self.broken_links: list[tuple[str, object]] = []
        self.external_links: list[tuple[str, h5py.ExternalLink]] = []

    def on_broken_link(self, hdf_path: str, link) -> None:
        self.broken_links.append((hdf_path, link))

    def on_external_link(self, hdf_path: str, link: h5py.ExternalLink) -> None:
        self.external_links.append((hdf_path, link))


def test_handler_broken_soft_link(tmp_path):
    """on_broken_link is called for a soft link whose target does not exist."""
    fpath = tmp_path / "broken_soft.nxs"
    with h5py.File(fpath, "w") as f:
        f.create_group("entry")
        f["entry/missing"] = h5py.SoftLink("/nonexistent")

    visitor = _LinkVisitor()
    NexusFileHandler(str(fpath)).process(visitor)

    assert len(visitor.broken_links) == 1
    path, link = visitor.broken_links[0]
    assert path == "entry/missing"
    assert isinstance(link, h5py.SoftLink)
    assert "entry/missing" not in visitor.visited


def test_handler_valid_soft_link(tmp_path):
    """A resolvable soft link is visited; on_broken_link is not called."""
    fpath = tmp_path / "valid_soft.nxs"
    with h5py.File(fpath, "w") as f:
        f.create_dataset("entry/real_data", data=42.0)
        f["entry/alias"] = h5py.SoftLink("/entry/real_data")

    visitor = _LinkVisitor()
    NexusFileHandler(str(fpath)).process(visitor)

    assert visitor.broken_links == []
    assert "entry/real_data" in visitor.visited


def test_handler_broken_external_link_missing_file(tmp_path):
    """on_broken_link fires when the external file does not exist."""
    fpath = tmp_path / "main.nxs"
    with h5py.File(fpath, "w") as f:
        f["entry/ext"] = h5py.ExternalLink("nonexistent.h5", "/data")

    visitor = _LinkVisitor()
    NexusFileHandler(str(fpath)).process(visitor)

    assert len(visitor.broken_links) == 1
    path, link = visitor.broken_links[0]
    assert path == "entry/ext"
    assert isinstance(link, h5py.ExternalLink)
    assert len(visitor.external_links) == 1


def test_handler_broken_external_link_missing_path(tmp_path):
    """on_broken_link fires when the external file exists but the path is absent."""
    ext_file = tmp_path / "ext.h5"
    with h5py.File(ext_file, "w") as f:
        f.create_dataset("existing", data=1.0)

    main_file = tmp_path / "main.nxs"
    with h5py.File(main_file, "w") as f:
        f["entry/ext"] = h5py.ExternalLink(str(ext_file), "/nonexistent")

    visitor = _LinkVisitor()
    NexusFileHandler(str(main_file)).process(visitor)

    assert len(visitor.broken_links) == 1
    path, link = visitor.broken_links[0]
    assert path == "entry/ext"
    assert isinstance(link, h5py.ExternalLink)


def test_handler_valid_external_link(tmp_path):
    """A resolvable external link is traversed; on_external_link fires before traversal."""
    ext_file = tmp_path / "ext.h5"
    with h5py.File(ext_file, "w") as f:
        grp = f.create_group("sensor")
        grp.create_dataset("value", data=3.14)

    main_file = tmp_path / "main.nxs"
    with h5py.File(main_file, "w") as f:
        f["entry/ext"] = h5py.ExternalLink(str(ext_file), "/sensor")

    visitor = _LinkVisitor()
    NexusFileHandler(str(main_file)).process(visitor)

    assert visitor.broken_links == []
    assert len(visitor.external_links) == 1
    ext_path, ext_link = visitor.external_links[0]
    assert ext_path == "entry/ext"
    assert isinstance(ext_link, h5py.ExternalLink)
    # The external subtree is visited under the main-file path
    assert "entry/ext" in visitor.visited
    assert "entry/ext/value" in visitor.visited
