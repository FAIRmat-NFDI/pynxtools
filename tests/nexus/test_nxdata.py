"""Unit tests for pynxtools.nexus.nxdata — pure NXdata detection and validation."""

import contextlib

import h5py
import numpy as np
import pytest

from pynxtools.nexus.nxdata import (
    NXdataInfo,
    NXdataViolationKind,
    check_nxdata,
    classify_field,
    find_default_nxdata,
    find_default_nxentry,
    inspect_nxdata,
)


@pytest.fixture
def nxdata_factory(tmp_path):
    @contextlib.contextmanager
    def factory(name="data"):
        path = tmp_path / f"{name}.h5"

        with h5py.File(path, "w") as file:
            nxdata = file.create_group("entry/data")
            nxdata.attrs["NX_class"] = "NXdata"

            yield file, nxdata

    return factory


# ---------------------------------------------------------------------------
# classify_field — v3_make_nxdata
# ---------------------------------------------------------------------------


def test_classify_field_signal_v3(nxdata_factory):
    with nxdata_factory("v3_signal") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        ds = nxdata.create_dataset("I", data=np.zeros(10))
        assert classify_field(ds, "I") == "signal"


def test_classify_field_axis_v3_from_axes_array(nxdata_factory):
    with nxdata_factory("v3_axis_from_array") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.zeros(10))
        ds = nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


def test_classify_field_axis_v3_from_axes_string(nxdata_factory):
    with nxdata_factory("v3_axis_from_axes_str") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = "q"
        nxdata.create_dataset("I", data=np.zeros(10))
        ds = nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


def test_classify_field_axis_v3_via_indices_attr(nxdata_factory):
    with nxdata_factory("v3_via_indices_attr") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["q_indices"] = np.int32(0)
        nxdata.create_dataset("I", data=np.zeros(10))
        ds = nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


# ---------------------------------------------------------------------------
# classify_field — v2/v1
# ---------------------------------------------------------------------------


def test_classify_field_signal_v2(nxdata_factory):
    with nxdata_factory("v2_signal") as (_, nxdata):
        ds = nxdata.create_dataset("I", data=np.zeros(10))
        ds.attrs["signal"] = "1"
        assert classify_field(ds, "I") == "signal"


def test_classify_field_axis_v2_via_axis_attr(nxdata_factory):
    with nxdata_factory("v2_axis_via_axis_attr") as (_, nxdata):
        signal = nxdata.create_dataset("I", data=np.zeros(10))
        signal.attrs["signal"] = "1"
        ds = nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        ds.attrs["axis"] = np.int32(1)
        assert classify_field(ds, "q") == "axis"


def test_classify_field_axis_v2_via_colon_axes(nxdata_factory):
    with nxdata_factory("v2_axis_via_colon_axes") as (_, nxdata):
        signal = nxdata.create_dataset("I", data=np.zeros(10))
        signal.attrs["signal"] = "1"
        signal.attrs["axes"] = "q"
        ds = nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


def test_classify_field_none_for_non_nxdata(nxdata_factory):
    with nxdata_factory("v2_none_for_non_nxdata") as (file, nxdata):
        instrument = file.create_group("entry/instrument")
        instrument.attrs["NX_class"] = "NXinstrument"
        ds = nxdata.create_dataset("value", data=1.0)
        assert classify_field(ds, "value") is None


def test_classify_field_none_for_non_dataset(nxdata_factory):
    with nxdata_factory("v2_none_for_non_dataset") as (_, nxdata):
        sub = nxdata.create_group("subgroup")
        assert classify_field(sub, "subgroup") is None  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# find_default_nxentry
# ---------------------------------------------------------------------------


def test_find_default_nxentry_via_default_attr(tmp_path):
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        file.attrs["default"] = "scan"
        scan = file.create_group("scan")
        scan.attrs["NX_class"] = "NXentry"
        first = file.create_group("first")
        first.attrs["NX_class"] = "NXentry"
        result = find_default_nxentry(file)
        assert result is not None
        assert result.name == "/scan"


def test_find_default_nxentry_fallback_to_first(tmp_path):
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        entry = file.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        result = find_default_nxentry(file)
        assert result is not None
        assert result.name == "/entry"


def test_find_default_nxentry_returns_none_if_absent(tmp_path):
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        file.create_group("not_an_entry")
        assert find_default_nxentry(file) is None


# ---------------------------------------------------------------------------
# find_default_nxdata
# ---------------------------------------------------------------------------


def test_find_default_nxdata_v3_full_chain(tmp_path):
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        file.attrs["default"] = "entry"
        entry = file.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        entry.attrs["default"] = "data"
        nxdata = entry.create_group("data")
        nxdata.attrs["NX_class"] = "NXdata"
        nxdata.attrs["signal"] = "I"
        nxdata.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(file)
        assert result is not None
        assert result.name == "/entry/data"


def test_find_default_nxdata_v3_deep_chain(tmp_path):
    """@default chain through an intermediate group."""
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        file.attrs["default"] = "entry"
        entry = file.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        entry.attrs["default"] = "detector"
        det = entry.create_group("detector")
        det.attrs["default"] = "data"
        nxdata = det.create_group("data")
        nxdata.attrs["NX_class"] = "NXdata"
        nxdata.attrs["signal"] = "I"
        nxdata.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(file)
        assert result is not None
        assert result.name == "/entry/detector/data"


def test_find_default_nxdata_v1_fallback(tmp_path):
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        entry = file.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        nxdata = entry.create_group("data")
        nxdata.attrs["NX_class"] = "NXdata"
        nxdata.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(file)
        assert result is not None
        assert result.name == "/entry/data"


def test_find_default_nxdata_returns_none_if_absent(tmp_path):
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        entry = file.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        assert find_default_nxdata(file) is None


def test_find_default_nxdata_broken_default_attr(tmp_path):
    """Broken @default pointing to nonexistent group falls through to first NXdata."""
    with h5py.File(tmp_path / "file.nxs", "w") as file:
        file.attrs["default"] = "entry"
        entry = file.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        entry.attrs["default"] = "nonexistent"
        nxdata = entry.create_group("data")
        nxdata.attrs["NX_class"] = "NXdata"
        nxdata.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(file)
        # broken chain → first NXdata fallback
        assert result is not None


# ---------------------------------------------------------------------------
# inspect_nxdata — v3
# ---------------------------------------------------------------------------


def test_inspect_nxdata_v3_signal_and_axis(nxdata_factory):
    with nxdata_factory("v3_signal_and_axis") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.zeros(10))
        nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        info = inspect_nxdata(nxdata)
        assert info.convention == "v3"
        assert info.signal_name == "I"
        assert len(info.axes) == 1
        assert len(info.axes[0]) == 1
        assert info.axes[0][0].name.endswith("q")


def test_inspect_nxdata_v3_auxiliary_signals(nxdata_factory):
    with nxdata_factory("v3_auxiliary_signals") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["auxiliary_signals"] = np.array(["I2", "I3"], dtype="S10")
        nxdata.create_dataset("I", data=np.zeros(10))
        nxdata.create_dataset("I2", data=np.ones(10))
        nxdata.create_dataset("I3", data=np.ones(10))
        info = inspect_nxdata(nxdata)
        assert info.convention == "v3"
        assert set(info.aux_signals) == {"I2", "I3"}


def test_inspect_nxdata_v3_multi_dim_axes(nxdata_factory):
    with nxdata_factory("v3_multi_dim_axes") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["x", "y"], dtype="S10")
        nxdata.create_dataset("I", data=np.zeros((5, 3)))
        nxdata.create_dataset("x", data=np.arange(5, dtype=float))
        nxdata.create_dataset("y", data=np.arange(3, dtype=float))
        info = inspect_nxdata(nxdata)
        assert info.convention == "v3"
        assert len(info.axes) == 2


def test_inspect_nxdata_v3_signal_missing_returns_none(nxdata_factory):
    with nxdata_factory("v3_signal_missing_returns_none") as (_, nxdata):
        nxdata.attrs["signal"] = "missing"
        info = inspect_nxdata(nxdata)
        # v3 fails, v2 also fails, v1 fails (no datasets)
        assert info.signal is None


# ---------------------------------------------------------------------------
# inspect_nxdata — v2
# ---------------------------------------------------------------------------


def test_inspect_nxdata_v2(nxdata_factory):
    with nxdata_factory("v2_inspect") as (_, nxdata):
        ds = nxdata.create_dataset("I", data=np.zeros(10))
        ds.attrs["signal"] = "1"
        ds.attrs["axes"] = "q"
        nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        info = inspect_nxdata(nxdata)
        assert info.convention == "v2"
        assert info.signal_name == "I"
        assert len(info.axes) == 1


# ---------------------------------------------------------------------------
# inspect_nxdata — v1
# ---------------------------------------------------------------------------


def test_inspect_nxdata_v1_single_dataset(nxdata_factory):
    with nxdata_factory("v1_inspect_single_dataset") as (_, nxdata):
        nxdata.create_dataset("I", data=np.zeros(5))
        info = inspect_nxdata(nxdata)
        assert info.convention == "v1"
        assert info.signal_name == "I"


def test_inspect_nxdata_no_convention_multiple_datasets_no_signal(nxdata_factory):
    with nxdata_factory("v1_inspect_no_convention_multiple_datasets_no_signal") as (
        _,
        nxdata,
    ):
        nxdata.create_dataset("I", data=np.zeros(5))
        nxdata.create_dataset("I2", data=np.zeros(5))
        info = inspect_nxdata(nxdata)
        # multiple datasets with no signal attr → no convention
        assert info.signal is None
        assert info.convention is None


# ---------------------------------------------------------------------------
# check_nxdata — constraint checks defined in NXdata docstring
# ---------------------------------------------------------------------------


def test_check_nxdata_valid_simple(nxdata_factory):
    """No violations for a well-formed 1D NXdata group."""
    with nxdata_factory("simple") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.ones(10))
        nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        assert check_nxdata(nxdata) == []


def test_check_nxdata_valid_histogram_bin_edges(nxdata_factory):
    """len(axis) == len(signal) + 1 is valid (histogram bin edges)."""
    with nxdata_factory("histogram") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.ones(10))
        nxdata.create_dataset("q", data=np.arange(11, dtype=float))  # bin edges: +1
        assert check_nxdata(nxdata) == []


# Rule 1: @axes rank mismatch
def test_check_nxdata_axes_rank_mismatch(nxdata_factory):
    """@axes has wrong length relative to signal rank."""
    with nxdata_factory("axes_rank_mismatch") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(
            ["q"], dtype="S10"
        )  # length 1, but signal is 2D
        nxdata.create_dataset("I", data=np.ones((10, 20)))
        nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.AxesRankMismatch in kinds


# Rule 2: AXISNAME_indices count mismatch
def test_check_nxdata_indices_count_mismatch(nxdata_factory):
    """AXISNAME_indices has wrong count relative to AXISNAME rank."""
    with nxdata_factory("indices_count_mismatch") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        # x_encoder is 2D but its _indices has only one entry
        nxdata.attrs["x_encoder_indices"] = np.array([0], dtype=np.int32)
        nxdata.create_dataset("I", data=np.ones((10, 7)))
        nxdata.create_dataset("x_encoder", data=np.ones((10, 7)))  # rank 2
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.IndicesCountMismatch in kinds


# Rule 5: @axes positions not a subset of AXISNAME_indices
def test_check_nxdata_indices_not_subset(nxdata_factory):
    """@axes position of an axis is not included in AXISNAME_indices."""
    with nxdata_factory("indices_not_subset") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q", "."], dtype="S10")  # q at position 0
        nxdata.attrs["q_indices"] = np.array(
            [1], dtype=np.int32
        )  # but indices says dim 1
        nxdata.create_dataset("I", data=np.ones((10, 20)))
        nxdata.create_dataset("q", data=np.arange(20, dtype=float))
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.IndicesNotSubset in kinds


# Rule 6: axis shape mismatch
def test_check_nxdata_axis_shape_mismatch(nxdata_factory):
    """Axis length doesn't match signal dimension and isn't bin-edge +1."""
    with nxdata_factory("axis_shape_mismatch") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.ones(10))
        nxdata.create_dataset("q", data=np.arange(8, dtype=float))  # wrong length
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.AxisShapeMismatch in kinds


# Rule 6: multi-dimensional axis with array AXISNAME_indices
def test_check_nxdata_multi_dim_axis_valid(nxdata_factory):
    """Multi-dimensional axis with correct array AXISNAME_indices — no violations."""
    with nxdata_factory("multi_dim_axis_valid") as (_, nxdata):
        nxdata.attrs["signal"] = "data"
        nxdata.attrs["axes"] = np.array(["x_set", "y_set", "."], dtype="S10")
        nxdata.attrs["x_encoder_indices"] = np.array([0, 1], dtype=np.int32)
        nxdata.attrs["y_encoder_indices"] = np.array([1], dtype=np.int32)
        nxdata.create_dataset("data", data=np.ones((10, 7, 1024)))
        nxdata.create_dataset("x_encoder", data=np.ones((10, 7)))
        nxdata.create_dataset("y_encoder", data=np.ones(7))
        nxdata.create_dataset("x_set", data=np.arange(10, dtype=float))
        nxdata.create_dataset("y_set", data=np.arange(7, dtype=float))
        assert check_nxdata(nxdata) == []


def test_check_nxdata_multi_dim_axis_shape_mismatch(nxdata_factory):
    """Multi-dimensional axis shape mismatch detected via array AXISNAME_indices."""
    with nxdata_factory("dim_axis_shape_mismatch") as (_, nxdata):
        nxdata.attrs["signal"] = "data"
        nxdata.attrs["x_encoder_indices"] = np.array([0, 1], dtype=np.int32)
        nxdata.create_dataset("data", data=np.ones((10, 7, 1024)))
        nxdata.create_dataset("x_encoder", data=np.ones((9, 7)))  # dim0=9, expected 10
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.AxisShapeMismatch in kinds


# Missing axis referenced in @axes
def test_check_nxdata_missing_axis_in_axes(nxdata_factory):
    """@axes references a field that does not exist."""
    with nxdata_factory("missing_axis_in_axes") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.ones(10))
        # 'q' not created
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.MissingAxisData in kinds


# Missing axis referenced only via AXISNAME_indices
def test_check_nxdata_missing_axis_via_indices(nxdata_factory):
    """AXISNAME_indices references a field that does not exist."""
    with nxdata_factory("missing_axis_via_indices") as (_, nxdata):
        nxdata.attrs["NX_class"] = "NXdata"
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["q_indices"] = np.int32(0)
        nxdata.create_dataset("I", data=np.ones(10))
        # 'q' not created
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.MissingAxisData in kinds


# Auxiliary signal shape mismatch
def test_check_nxdata_aux_signal_shape_mismatch(nxdata_factory):
    """Auxiliary signal has wrong shape."""
    with nxdata_factory("aux_signal_shape_mismatch") as (_, nxdata):
        nxdata.attrs["signal"] = "I1"
        nxdata.attrs["auxiliary_signals"] = np.array(["I2"], dtype="S10")
        nxdata.create_dataset("I1", data=np.ones((10, 20)))
        nxdata.create_dataset("I2", data=np.ones((10, 30)))  # wrong shape
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.AuxSignalShapeMismatch in kinds


def test_check_nxdata_aux_signal_valid(nxdata_factory):
    """Multiple auxiliary signals with matching shapes produce no violations."""
    with nxdata_factory("aux_signal_valid") as (_, nxdata):
        nxdata.attrs["signal"] = "I1"
        nxdata.attrs["auxiliary_signals"] = np.array(["I2", "I3"], dtype="S10")
        nxdata.create_dataset("I1", data=np.ones((10, 20)))
        nxdata.create_dataset("I2", data=np.ones((10, 20)))
        nxdata.create_dataset("I3", data=np.ones((10, 20)))
        assert check_nxdata(nxdata) == []


# classify_field: array AXISNAME_indices
def test_classify_field_axis_via_array_indices(nxdata_factory):
    """classify_field recognizes axes declared with array AXISNAME_indices."""
    with nxdata_factory("field_axis_via_array_indices") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["x_encoder_indices"] = np.array([0, 1], dtype=np.int32)
        nxdata.create_dataset("I", data=np.ones((10, 7)))
        ds = nxdata.create_dataset("x_encoder", data=np.ones((10, 7)))
        assert classify_field(ds, "x_encoder") == "axis"


# No convention, no @signal attr → empty violations (group may be a non-plotting NXdata container)
def test_check_nxdata_no_signal_convention_returns_empty(nxdata_factory):
    """NXdata group with multiple datasets but no signal convention → no violation."""
    with nxdata_factory("no_convention") as (_, nxdata):
        nxdata.create_dataset("I", data=np.ones(10))
        nxdata.create_dataset("I2", data=np.ones(10))
        violations = check_nxdata(nxdata)
        assert violations == []


def test_check_nxdata_empty_group_no_violation(nxdata_factory):
    """An NXdata group with no datasets at all produces no violations."""
    with nxdata_factory("empty_group") as (_, nxdata):
        assert check_nxdata(nxdata) == []


def test_check_nxdata_missing_primary_signal_dataset(nxdata_factory):
    """@signal attr present but dataset missing → MissingSignalData violation."""
    with nxdata_factory("missing_primary_dataset") as (_, nxdata):
        nxdata.attrs["signal"] = "I"  # attr present, no dataset created
        violations = check_nxdata(nxdata)
        assert len(violations) == 1
        assert violations[0].kind == NXdataViolationKind.MissingSignalData
        assert "I" in violations[0].message


def test_inspect_nxdata_errors_populated(nxdata_factory):
    """inspect_nxdata populates NXdataInfo.errors for {name}_errors datasets."""
    with nxdata_factory("errors_populated") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.ones(10))
        nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        nxdata.create_dataset("I_errors", data=np.ones(10))
        nxdata.create_dataset("q_errors", data=np.ones(10))
        info = inspect_nxdata(nxdata)
        assert "I" in info.errors
        assert "q" in info.errors


def test_check_nxdata_errors_shape_mismatch(nxdata_factory):
    """FIELDNAME_errors with wrong shape → AxisShapeMismatch violation."""
    with nxdata_factory("errors_shape_mismatch") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.ones(10))
        nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        nxdata.create_dataset("I_errors", data=np.ones(5))  # wrong shape
        violations = check_nxdata(nxdata)
        kinds = {v.kind for v in violations}
        assert NXdataViolationKind.AxisShapeMismatch in kinds
        assert any("I_errors" in v.subject for v in violations)


def test_check_nxdata_errors_shape_valid(nxdata_factory):
    """FIELDNAME_errors with matching shape → no violation."""
    with nxdata_factory("errors_shape_valid") as (_, nxdata):
        nxdata.attrs["signal"] = "I"
        nxdata.attrs["axes"] = np.array(["q"], dtype="S10")
        nxdata.create_dataset("I", data=np.ones(10))
        nxdata.create_dataset("q", data=np.arange(10, dtype=float))
        nxdata.create_dataset("I_errors", data=np.ones(10))
        assert check_nxdata(nxdata) == []
