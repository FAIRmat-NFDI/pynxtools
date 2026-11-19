# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for ParsedData, the common container of parser results."""

import dataclasses
import datetime
import logging
from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from pynxtools import logger as pynx_logger
from pynxtools.dataconverter.readers.parsers.parsed_data import (
    HDF5Reference,
    ParsedData,
)


@pytest.fixture
def parsed():
    return ParsedData(
        data={"energy": np.arange(3.0), "intensity": np.ones(3)},
        metadata={
            "instrument/analyser/energy/@units": "eV",
            "instrument/source/name": "Al Ka",
            "sample/name": "Au foil",
            "comment": "",
            "operator": None,
            "notes": ["", ""],
            "start_time": datetime.datetime(2026, 11, 18, 14, 0),
        },
        dims={"intensity": ["energy"]},
        source=Path("scan.xy"),
    )


def test_defaults_are_empty_and_not_shared():
    first, second = ParsedData(), ParsedData()
    first.metadata["key"] = "value"
    assert second.metadata == {}
    assert first.data == {} and first.dims == {} and first.source is None


def test_get_metadata_finds_exact_keys(parsed):
    assert parsed.get_metadata("sample/name") == "Au foil"


def test_get_metadata_falls_back_to_the_key_suffix(parsed):
    assert parsed.get_metadata("energy/@units") == "eV"
    assert parsed.get_metadata("name") == "Al Ka"  # first key ending in /name


def test_get_metadata_prefers_the_exact_key():
    parsed = ParsedData(metadata={"source/name": "suffix", "name": "exact"})
    assert parsed.get_metadata("name") == "exact"


@pytest.mark.parametrize("path", ["comment", "operator", "notes", "missing"])
def test_empty_or_missing_metadata_gives_none(parsed, path):
    assert parsed.get_metadata(path) is None


def test_datetimes_are_returned_as_iso_strings(parsed):
    assert parsed.get_metadata("start_time") == "2026-11-18T14:00:00"


def test_get_data_and_get_dims(parsed):
    np.testing.assert_array_equal(parsed.get_data("energy"), [0.0, 1.0, 2.0])
    assert parsed.get_data("missing") is None
    assert parsed.get_dims("intensity") == ["energy"]
    assert parsed.get_dims("energy") == []


def test_get_dims_returns_a_copy(parsed):
    parsed.get_dims("intensity").append("other")
    assert parsed.get_dims("intensity") == ["energy"]


def test_unused_metadata_lists_keys_that_were_never_read(parsed):
    parsed.get_metadata("energy/@units")  # found by suffix
    parsed.get_metadata("comment")  # empty, but read
    parsed.get_metadata("missing")  # not there, changes nothing
    assert parsed.unused_metadata == {
        "instrument/source/name",
        "sample/name",
        "operator",
        "notes",
        "start_time",
    }


def test_mark_metadata_used(parsed):
    parsed.mark_metadata_used(["sample/name", "not/a/key"])
    assert "sample/name" not in parsed.unused_metadata
    assert "not/a/key" not in parsed.unused_metadata


def test_tracking_is_not_part_of_equality(parsed):
    other = ParsedData(
        data=parsed.data,
        metadata=parsed.metadata,
        dims=parsed.dims,
        source=parsed.source,
    )
    parsed.get_metadata("sample/name")
    assert parsed == other


def test_plugins_can_subclass_it():
    class ParsedSpectrum(ParsedData):
        def average(self):
            return self.get_data("intensity").mean()

    spectrum = ParsedSpectrum(data={"intensity": np.array([1.0, 3.0])})
    assert spectrum.average() == 2.0


def test_data_can_hold_xarray_memmap_and_hdf5_references(tmp_path):
    raw = tmp_path / "detector.raw"
    np.arange(6, dtype=np.uint16).tofile(raw)
    reference = HDF5Reference(file=tmp_path / "source.h5", path="/entry/image")
    parsed = ParsedData(
        data={
            "spectrum": xr.DataArray(np.ones(3), dims=["energy"]),
            "image": np.memmap(raw, dtype=np.uint16, mode="r", shape=(2, 3)),
            "external": reference,
        }
    )
    assert isinstance(parsed.get_data("spectrum"), xr.DataArray)
    image = parsed.get_data("image")
    assert isinstance(image, np.memmap) and image.dtype == np.uint16
    assert parsed.get_data("external") is reference


def test_get_data_returns_the_stored_object_without_copying(parsed):
    assert parsed.get_data("intensity") is parsed.data["intensity"]


def test_hdf5_references_are_immutable(tmp_path):
    reference = HDF5Reference(file=tmp_path / "source.h5", path="/entry/image")
    with pytest.raises(dataclasses.FrozenInstanceError):
        reference.path = "/other"  # type: ignore[misc]


@pytest.fixture
def pynx_caplog(caplog):
    """caplog that also sees the pynxtools logger, which does not propagate."""
    pynx_logger.addHandler(caplog.handler)
    caplog.set_level(logging.INFO, logger="pynxtools")
    try:
        yield caplog
    finally:
        pynx_logger.removeHandler(caplog.handler)


def test_several_keys_with_the_same_ending_give_the_first_and_a_warning(pynx_caplog):
    parsed = ParsedData(
        metadata={"analyser/energy/@units": "eV", "source/energy/@units": "keV"}
    )
    assert parsed.get_metadata("energy/@units") == "eV"
    [record] = pynx_caplog.records
    assert record.levelno == logging.WARNING
    assert "analyser/energy/@units, source/energy/@units" in record.getMessage()


def test_a_unique_key_ending_logs_nothing(pynx_caplog):
    parsed = ParsedData(
        metadata={"analyser/energy/@units": "eV", "source/power/@units": "W"}
    )
    assert parsed.get_metadata("energy/@units") == "eV"
    assert parsed.get_metadata("source/energy/@units") is None
    assert pynx_caplog.records == []
