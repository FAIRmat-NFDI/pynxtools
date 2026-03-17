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
"""Tests for MultiFormatReader pipeline contract."""

import json
import logging
import os
import tempfile
from typing import Any

import pytest
import yaml

from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.template import Template

# ---------------------------------------------------------------------------
# Minimal concrete subclasses used only in tests
# ---------------------------------------------------------------------------


class _OrderTracker:
    """Records the order in which pipeline hooks are called."""

    events: list[str]

    def __init__(self):
        self.events = []


class _TrackedReader(MultiFormatReader):
    """
    Minimal MultiFormatReader subclass that records pipeline hook calls
    so tests can verify execution order and data flow.
    """

    supported_nxdls = ["NXtest"]

    def __init__(self, tracker: _OrderTracker, **kwargs):
        super().__init__(**kwargs)
        self._tracker = tracker
        self.extensions = {
            ".txt": self._handle_txt,
        }

    def _handle_txt(self, file_path: str) -> dict[str, Any]:
        self._tracker.events.append(f"file:{os.path.basename(file_path)}")
        return {"/ENTRY[entry]/from_file": "yes"}

    def handle_objects(self, objects: tuple[Any]) -> dict[str, Any]:
        self._tracker.events.append("objects")
        return {"/ENTRY[entry]/from_objects": objects[0]}

    def setup_template(self) -> dict[str, Any]:
        self._tracker.events.append("setup_template")
        return {"/ENTRY[entry]/from_setup": "static"}

    def post_process(self) -> dict[str, Any] | None:
        self._tracker.events.append("post_process")
        self.config_dict["/ENTRY[entry]/from_post_in_config"] = "post_in_conf"
        return {"/ENTRY[entry]/from_post": "post"}

    def get_attr(self, key: str, path: str) -> Any:
        if path == "my_attr":
            return "attr_value"
        return None

    def get_data(self, key: str, path: str) -> Any:
        if path == "my_data":
            return 42
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_tmp_file(suffix: str, content: str = "") -> str:
    """Create a temporary file and return its path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w") as fh:
        fh.write(content)
    return path


# ---------------------------------------------------------------------------
# Pipeline order tests
# ---------------------------------------------------------------------------


def test_objects_processed_before_files():
    """handle_objects must be called before any file handler."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    tmp = _make_tmp_file(".txt", "hello")
    try:
        reader.read(template=Template(), file_paths=(tmp,), objects=("obj_data",))
    finally:
        os.unlink(tmp)

    obj_idx = tracker.events.index("objects")
    file_idx = next(i for i, e in enumerate(tracker.events) if e.startswith("file:"))
    assert obj_idx < file_idx, f"Expected objects before files, got: {tracker.events}"


def test_setup_template_after_files():
    """setup_template must be called after all file handlers."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    tmp = _make_tmp_file(".txt", "hello")
    try:
        reader.read(template=Template(), file_paths=(tmp,))
    finally:
        os.unlink(tmp)

    file_idx = next(i for i, e in enumerate(tracker.events) if e.startswith("file:"))
    setup_idx = tracker.events.index("setup_template")
    assert file_idx < setup_idx, (
        f"Expected file before setup_template, got: {tracker.events}"
    )


def test_post_process_after_setup_template():
    """post_process must be called after setup_template."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    reader.read(template=Template(), file_paths=())
    setup_idx = tracker.events.index("setup_template")
    post_idx = tracker.events.index("post_process")
    assert setup_idx < post_idx, (
        f"Expected setup_template before post_process, got: {tracker.events}"
    )


# ---------------------------------------------------------------------------
# Return value aggregation
# ---------------------------------------------------------------------------


def test_objects_result_in_output():
    """Entries returned from handle_objects appear in read() result."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    result = reader.read(template=Template(), file_paths=(), objects=("my_object",))
    assert result["/ENTRY[entry]/from_objects"] == "my_object"


def test_file_handler_result_in_output():
    """Entries returned from file handlers appear in read() result."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    tmp = _make_tmp_file(".txt", "x")
    try:
        result = reader.read(template=Template(), file_paths=(tmp,))
    finally:
        os.unlink(tmp)
    assert result["/ENTRY[entry]/from_file"] == "yes"


def test_setup_template_result_in_output():
    """Entries returned from setup_template appear in read() result."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    result = reader.read(template=Template(), file_paths=())
    assert result["/ENTRY[entry]/from_setup"] == "static"


def test_post_process_result_in_output():
    """Entries returned from post_process appear in read() result."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    result = reader.read(template=Template(), file_paths=())
    assert result["/ENTRY[entry]/from_post_in_config"] == "post_in_conf"
    assert result["/ENTRY[entry]/from_post"] == "post"


def test_post_process_can_inject_config_entries():
    """post_process can add entries to self.config_dict for fill_from_config."""

    class _InjectingReader(MultiFormatReader):
        supported_nxdls = ["NXtest"]

        def __init__(self):
            super().__init__()
            self.extensions = {}

        def post_process(self) -> dict[str, Any] | None:
            self.config_dict["/ENTRY[entry]/injected"] = "from_config"
            return None

        def get_attr(self, key: str, path: str) -> Any:
            return None

    reader = _InjectingReader()
    result = reader.read(template=Template(), file_paths=())
    assert result["/ENTRY[entry]/injected"] == "from_config"


# ---------------------------------------------------------------------------
# Extension dispatch
# ---------------------------------------------------------------------------


def test_unknown_extension_logs_warning(caplog):
    """Files with unregistered extensions produce a logger warning."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    tmp = _make_tmp_file(".xyz", "data")
    try:
        with caplog.at_level(logging.WARNING, logger="pynxtools"):
            reader.read(template=Template(), file_paths=(tmp,))
    finally:
        os.unlink(tmp)
    assert any("unsupported extension" in msg.lower() for msg in caplog.messages)


def test_only_registered_extension_dispatched():
    """Only files whose extension is in self.extensions are handled."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    tmp_txt = _make_tmp_file(".txt", "data")
    tmp_xyz = _make_tmp_file(".xyz", "ignored")
    try:
        reader.read(template=Template(), file_paths=(tmp_txt, tmp_xyz))
    finally:
        os.unlink(tmp_txt)
        os.unlink(tmp_xyz)

    file_events = [e for e in tracker.events if e.startswith("file:")]
    assert len(file_events) == 1
    assert os.path.basename(tmp_txt) in file_events[0]


def test_nonexistent_file_logs_warning(caplog):
    """Files that do not exist on disk produce a logger warning."""
    tracker = _OrderTracker()
    reader = _TrackedReader(tracker)
    with caplog.at_level(logging.WARNING, logger="pynxtools"):
        reader.read(template=Template(), file_paths=("/nonexistent/path/file.txt",))
    assert any("does not exist" in msg.lower() for msg in caplog.messages)


# ---------------------------------------------------------------------------
# setup_template contract: static dict, no template or reader-data access
# ---------------------------------------------------------------------------


def test_setup_template_returns_empty_dict_by_default():
    """The base setup_template must return an empty dict with no side effects."""
    reader = MultiFormatReader()
    result = reader.setup_template()
    assert result == {}
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# ELN data handling
# ---------------------------------------------------------------------------


def test_get_eln_data_returns_none_when_no_eln_data():
    """get_eln_data returns None when self.eln_data is empty."""
    reader = _TrackedReader(_OrderTracker())
    assert reader.get_eln_data("/ENTRY[entry]/title", "title") is None


def test_handle_eln_file_populates_eln_data(tmp_path):
    """handle_eln_file stores parsed ELN data in self.eln_data."""
    eln_file = tmp_path / "eln.yaml"
    eln_file.write_text(yaml.dump({"title": "My Sample"}))

    reader = _TrackedReader(_OrderTracker())
    reader.handle_eln_file(str(eln_file))
    assert reader.eln_data  # must be non-empty after parsing


def test_handle_eln_file_via_extension(tmp_path):
    """When handle_eln_file is registered for .yaml, ELN data is auto-loaded."""

    class _ElnReader(MultiFormatReader):
        supported_nxdls = ["*"]

        def __init__(self):
            super().__init__()
            self.extensions = {".yaml": self.handle_eln_file}

    eln_file = tmp_path / "eln.yaml"
    eln_file.write_text(yaml.dump({"title": "My Title"}))

    reader = _ElnReader()
    reader.read(template=Template(), file_paths=(str(eln_file),))
    assert reader.eln_data


# ---------------------------------------------------------------------------
# set_config_file built-in
# ---------------------------------------------------------------------------


def test_set_config_file_stores_path(tmp_path):
    """set_config_file stores the given path in self.config_file."""
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({}))

    reader = _TrackedReader(_OrderTracker())
    reader.set_config_file(str(cfg))
    assert reader.config_file == str(cfg)


def test_set_config_file_warns_on_replacement(tmp_path, caplog):
    """set_config_file logs a warning when a config file is already set."""
    cfg1 = tmp_path / "c1.json"
    cfg2 = tmp_path / "c2.json"
    cfg1.write_text("{}")
    cfg2.write_text("{}")

    reader = _TrackedReader(_OrderTracker())
    reader.set_config_file(str(cfg1))

    with caplog.at_level(logging.WARNING, logger="pynxtools"):
        reader.set_config_file(str(cfg2))

    assert any("already set" in msg.lower() for msg in caplog.messages)
    assert reader.config_file == str(cfg2)


# ---------------------------------------------------------------------------
# Extension dict isolation
# ---------------------------------------------------------------------------


def test_extensions_are_instance_isolated():
    """Two reader instances must have independent extension dicts."""
    reader_a = _TrackedReader(_OrderTracker())
    reader_b = _TrackedReader(_OrderTracker())

    reader_a.extensions[".extra"] = lambda p: {}

    assert ".extra" not in reader_b.extensions
