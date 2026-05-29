"""Unit tests for pynxtools.nexus.nxdata — pure NXdata detection."""

import h5py
import numpy as np
import pytest

from pynxtools.nexus.nxdata import (
    NXdataInfo,
    classify_field,
    find_default_nxdata,
    find_default_nxentry,
    inspect_nxdata,
)

# ---------------------------------------------------------------------------
# classify_field — v3
# ---------------------------------------------------------------------------


def test_classify_field_signal_v3(tmp_path):
    with h5py.File(tmp_path / "classify_field_signal_v3.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "I"
        ds = g.create_dataset("I", data=np.zeros(10))
        assert classify_field(ds, "I") == "signal"


def test_classify_field_axis_v3_from_axes_array(tmp_path):
    with h5py.File(tmp_path / "classify_field_axis_v3_from_axes_array.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "I"
        g.attrs["axes"] = np.array(["q"], dtype="S10")
        g.create_dataset("I", data=np.zeros(10))
        ds = g.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


def test_classify_field_axis_v3_from_axes_string(tmp_path):
    with h5py.File(tmp_path / "classify_field_axis_v3_from_axes_string.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "I"
        g.attrs["axes"] = "q"
        g.create_dataset("I", data=np.zeros(10))
        ds = g.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


def test_classify_field_axis_v3_via_indices_attr(tmp_path):
    with h5py.File(tmp_path / "classify_field_axis_v3_via_indices_attr.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "I"
        g.attrs["q_indices"] = np.int32(0)
        g.create_dataset("I", data=np.zeros(10))
        ds = g.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


# ---------------------------------------------------------------------------
# classify_field — v2/v1
# ---------------------------------------------------------------------------


def test_classify_field_signal_v2(tmp_path):
    with h5py.File(tmp_path / "classify_field_signal_v2.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        ds = g.create_dataset("I", data=np.zeros(10))
        ds.attrs["signal"] = "1"
        assert classify_field(ds, "I") == "signal"


def test_classify_field_axis_v2_via_axis_attr(tmp_path):
    with h5py.File(tmp_path / "classify_field_axis_v2_via_axis_attr.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        sig = g.create_dataset("I", data=np.zeros(10))
        sig.attrs["signal"] = "1"
        ds = g.create_dataset("q", data=np.arange(10, dtype=float))
        ds.attrs["axis"] = np.int32(1)
        assert classify_field(ds, "q") == "axis"


def test_classify_field_axis_v2_via_colon_axes(tmp_path):
    with h5py.File(tmp_path / "classify_field_axis_v2_via_colon_axes.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        sig = g.create_dataset("I", data=np.zeros(10))
        sig.attrs["signal"] = "1"
        sig.attrs["axes"] = "q"
        ds = g.create_dataset("q", data=np.arange(10, dtype=float))
        assert classify_field(ds, "q") == "axis"


def test_classify_field_none_for_non_nxdata(tmp_path):
    with h5py.File(tmp_path / "classify_field_none_for_non_nxdata.nxs", "w") as f:
        g = f.create_group("entry/instrument")
        g.attrs["NX_class"] = "NXinstrument"
        ds = g.create_dataset("value", data=1.0)
        assert classify_field(ds, "value") is None


def test_classify_field_none_for_non_dataset(tmp_path):
    with h5py.File(tmp_path / "classify_field_none_for_non_dataset.nxs", "w") as f:
        g = f.create_group("entry/data")
        g.attrs["NX_class"] = "NXdata"
        sub = g.create_group("subgroup")
        assert classify_field(sub, "subgroup") is None  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# find_default_nxentry
# ---------------------------------------------------------------------------


def test_find_default_nxentry_via_default_attr(tmp_path):
    with h5py.File(tmp_path / "find_default_nxentry_via_default_attr.nxs", "w") as f:
        f.attrs["default"] = "scan"
        scan = f.create_group("scan")
        scan.attrs["NX_class"] = "NXentry"
        first = f.create_group("first")
        first.attrs["NX_class"] = "NXentry"
        result = find_default_nxentry(f)
        assert result is not None
        assert result.name == "/scan"


def test_find_default_nxentry_fallback_to_first(tmp_path):
    with h5py.File(tmp_path / "find_default_nxentry_fallback_to_first.nxs", "w") as f:
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        result = find_default_nxentry(f)
        assert result is not None
        assert result.name == "/entry"


def test_find_default_nxentry_returns_none_if_absent(tmp_path):
    with h5py.File(
        tmp_path / "find_default_nxentry_returns_none_if_absent.nxs", "w"
    ) as f:
        f.create_group("not_an_entry")
        assert find_default_nxentry(f) is None


# ---------------------------------------------------------------------------
# find_default_nxdata
# ---------------------------------------------------------------------------


def test_find_default_nxdata_v3_full_chain(tmp_path):
    with h5py.File(tmp_path / "find_default_nxdata_v3_full_chain.nxs", "w") as f:
        f.attrs["default"] = "entry"
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        entry.attrs["default"] = "data"
        data = entry.create_group("data")
        data.attrs["NX_class"] = "NXdata"
        data.attrs["signal"] = "I"
        data.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(f)
        assert result is not None
        assert result.name == "/entry/data"


def test_find_default_nxdata_v3_deep_chain(tmp_path):
    """@default chain through an intermediate group."""
    with h5py.File(tmp_path / "find_default_nxdata_v3_deep_chain.nxs", "w") as f:
        f.attrs["default"] = "entry"
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        entry.attrs["default"] = "detector"
        det = entry.create_group("detector")
        det.attrs["default"] = "data"
        data = det.create_group("data")
        data.attrs["NX_class"] = "NXdata"
        data.attrs["signal"] = "I"
        data.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(f)
        assert result is not None
        assert result.name == "/entry/detector/data"


def test_find_default_nxdata_v1_fallback(tmp_path):
    with h5py.File(tmp_path / "find_default_nxdata_v1_fallback.nxs", "w") as f:
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        data = entry.create_group("data")
        data.attrs["NX_class"] = "NXdata"
        data.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(f)
        assert result is not None
        assert result.name == "/entry/data"


def test_find_default_nxdata_returns_none_if_absent(tmp_path):
    with h5py.File(
        tmp_path / "find_default_nxdata_returns_none_if_absent.nxs", "w"
    ) as f:
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        assert find_default_nxdata(f) is None


def test_find_default_nxdata_broken_default_attr(tmp_path):
    """Broken @default pointing to nonexistent group falls through to first NXdata."""
    with h5py.File(tmp_path / "find_default_nxdata_broken_default_attr.nxs", "w") as f:
        f.attrs["default"] = "entry"
        entry = f.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        entry.attrs["default"] = "nonexistent"
        data = entry.create_group("data")
        data.attrs["NX_class"] = "NXdata"
        data.create_dataset("I", data=np.zeros(5))
        result = find_default_nxdata(f)
        # broken chain → first NXdata fallback
        assert result is not None


# ---------------------------------------------------------------------------
# inspect_nxdata — v3
# ---------------------------------------------------------------------------


def test_inspect_nxdata_v3_signal_and_axis(tmp_path):
    with h5py.File(tmp_path / "inspect_nxdata_v3_signal_and_axis.nxs", "w") as f:
        g = f.create_group("data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "I"
        g.attrs["axes"] = np.array(["q"], dtype="S10")
        g.create_dataset("I", data=np.zeros(10))
        g.create_dataset("q", data=np.arange(10, dtype=float))
        info = inspect_nxdata(g)
        assert info.convention == "v3"
        assert info.signal_name == "I"
        assert len(info.axes) == 1
        assert len(info.axes[0]) == 1
        assert info.axes[0][0].name.endswith("q")


def test_inspect_nxdata_v3_auxiliary_signals(tmp_path):
    with h5py.File(tmp_path / "inspect_nxdata_v3_auxiliary_signals.nxs", "w") as f:
        g = f.create_group("data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "I"
        g.attrs["auxiliary_signals"] = np.array(["I2", "I3"], dtype="S10")
        g.create_dataset("I", data=np.zeros(10))
        g.create_dataset("I2", data=np.ones(10))
        g.create_dataset("I3", data=np.ones(10))
        info = inspect_nxdata(g)
        assert info.convention == "v3"
        assert set(info.aux_signals) == {"I2", "I3"}


def test_inspect_nxdata_v3_multi_dim_axes(tmp_path):
    with h5py.File(tmp_path / "inspect_nxdata_v3_multi_dim_axes.nxs", "w") as f:
        g = f.create_group("data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "I"
        g.attrs["axes"] = np.array(["x", "y"], dtype="S10")
        g.create_dataset("I", data=np.zeros((5, 3)))
        g.create_dataset("x", data=np.arange(5, dtype=float))
        g.create_dataset("y", data=np.arange(3, dtype=float))
        info = inspect_nxdata(g)
        assert info.convention == "v3"
        assert len(info.axes) == 2


def test_inspect_nxdata_v3_signal_missing_returns_none(tmp_path):
    with h5py.File(
        tmp_path / "inspect_nxdata_v3_signal_missing_returns_none.nxs", "w"
    ) as f:
        g = f.create_group("data")
        g.attrs["NX_class"] = "NXdata"
        g.attrs["signal"] = "missing"
        info = inspect_nxdata(g)
        # v3 fails, v2 also fails, v1 fails (no datasets)
        assert info.signal is None


# ---------------------------------------------------------------------------
# inspect_nxdata — v2
# ---------------------------------------------------------------------------


def test_inspect_nxdata_v2(tmp_path):
    with h5py.File(tmp_path / "inspect_nxdata_v2.nxs", "w") as f:
        g = f.create_group("data")
        g.attrs["NX_class"] = "NXdata"
        ds = g.create_dataset("I", data=np.zeros(10))
        ds.attrs["signal"] = "1"
        ds.attrs["axes"] = "q"
        g.create_dataset("q", data=np.arange(10, dtype=float))
        info = inspect_nxdata(g)
        assert info.convention == "v2"
        assert info.signal_name == "I"
        assert len(info.axes) == 1


# ---------------------------------------------------------------------------
# inspect_nxdata — v1
# ---------------------------------------------------------------------------


def test_inspect_nxdata_v1_single_dataset(tmp_path):
    with h5py.File(tmp_path / "inspect_nxdata_v1_single_dataset.nxs", "w") as f:
        g = f.create_group("data")
        g.attrs["NX_class"] = "NXdata"
        g.create_dataset("I", data=np.zeros(5))
        info = inspect_nxdata(g)
        assert info.convention == "v1"
        assert info.signal_name == "I"


def test_inspect_nxdata_no_convention_multiple_datasets_no_signal(tmp_path):
    with h5py.File(
        tmp_path / "inspect_nxdata_no_convention_multiple_datasets_no_signal.nxs", "w"
    ) as f:
        g = f.create_group("data")
        g.attrs["NX_class"] = "NXdata"
        g.create_dataset("I", data=np.zeros(5))
        g.create_dataset("I2", data=np.zeros(5))
        info = inspect_nxdata(g)
        # multiple datasets with no signal attr → no convention
        assert info.signal is None
        assert info.convention is None
