#
# Copyright The pynxtools Authors.
#
# This file is part of pynxtools.
# See https://github.com/FAIRmat-NFDI/pynxtools for further info.
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
"""Pure NXdata detection and constraint-checking utilities — no logging dependency.

This module implements the three NeXus Data Plotting Standard conventions
(v3 from NIAC2014, v2 from ~2004, v1 oldest) for identifying the default
plottable signal and its axes in an HDF5/NeXus file.

It also implements the six NXdata structural constraints from NXdata.nxdl.xml
as a pure ``check_nxdata`` function so that both the validator and the
annotator can surface consistent, actionable messages without duplicating logic.

Public API:
    NXdataInfo          — structured result of inspecting an NXdata group
    NXdataViolation     — a single constraint violation found by check_nxdata
    classify_field      — return 'signal', 'axis', or None for a dataset
    find_default_nxdata — walk the default chain to find the NXdata group
    inspect_nxdata      — return NXdataInfo for an NXdata group
    check_nxdata     — return list[NXdataViolation] for an NXdata group

These functions carry no logging dependency and can be reused by both the
annotator and the validator (fixes https://github.com/FAIRmat-NFDI/pynxtools/issues/795).
"""

from __future__ import annotations

import numbers
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Literal

import h5py
import numpy as np

from pynxtools.nexus.utils import decode_if_string


@dataclass
class NXdataInfo:
    """Structured description of an NXdata group.

    Attributes:
        signal:       The primary signal dataset, or None if not found.
        signal_name:  Name of the signal dataset within the group.
        axes:         ``axes[dim]`` is a list of candidate axis datasets for
                      dimension *dim* of the signal.  Multi-dimensional axes
                      (those with array ``AXISNAME_indices``) appear in every
                      dimension slot they span.
        axes_indices: ``axes_indices[dim]`` is the list of ``AXISNAME_indices``
                      arrays (as Python lists of ints) for each axis in
                      ``axes[dim]``, parallel to ``axes[dim]``.
        aux_signals:  Names of auxiliary signal datasets (v3 only).
        convention:   Which plottable convention was detected: ``'v3'``,
                      ``'v2'``, ``'v1'``, or ``None`` if nothing was found.
        errors:       Maps field name (signal, axis, or aux signal name) to its
                      ``{name}_errors`` dataset when present in the group.
    """

    signal: h5py.Dataset | None = None
    signal_name: str | None = None
    axes: list[list[h5py.Dataset]] = field(default_factory=list)
    axes_indices: list[list[list[int]]] = field(default_factory=list)
    aux_signals: list[str] = field(default_factory=list)
    convention: Literal["v3", "v2", "v1"] | None = None
    errors: dict[str, h5py.Dataset] = field(default_factory=dict)
    """Maps field name (signal, axis, or aux signal) to its ``{name}_errors`` dataset."""


class NXdataViolationKind(Enum):
    """Enumeration of NXdata structural constraint violations."""

    AxesRankMismatch = auto()
    """@axes length ≠ signal rank."""

    IndicesCountMismatch = auto()
    """AXISNAME_indices count ≠ AXISNAME rank."""

    IndicesNotSubset = auto()
    """@axes positions for AXISNAME are not a subset of AXISNAME_indices."""

    AxisShapeMismatch = auto()
    """AXISNAME.shape[i] ≠ DATA.shape[AXISNAME_indices[i]] or +1."""

    AuxSignalShapeMismatch = auto()
    """Auxiliary signal shape ≠ primary signal shape."""

    MissingSignalData = auto()
    """@signal names a field that does not exist."""

    MissingAxisData = auto()
    """@axes or AXISNAME_indices references a field that does not exist."""

    NoSignalConvention = auto()
    """NXdata group has datasets but no identifiable signal by any plottable convention (v1/v2/v3)."""


@dataclass
class NXdataViolation:
    """A single NXdata constraint violation.

    Attributes:
        kind:     Which rule was violated.
        message:  Human-readable description of the problem.
        subject:  HDF5 path or attribute name that triggered the violation.
    """

    kind: NXdataViolationKind
    message: str
    subject: str


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def classify_field(
    hdf_node: h5py.Dataset, name: str
) -> Literal["signal", "axis"] | None:
    """Return ``'signal'``, ``'axis'``, or ``None`` for *hdf_node*.

    Checks v3 parent attributes first, then falls back to v2/v1 own attributes.
    Returns ``None`` if *hdf_node* is not a dataset or its parent is not NXdata.
    """
    if not isinstance(hdf_node, h5py.Dataset):
        return None
    parent = hdf_node.parent
    if parent is None or decode_if_string(parent.attrs.get("NX_class")) != "NXdata":
        return None

    # v3: signal named in parent @signal attr
    signal = decode_if_string(parent.attrs.get("signal"))
    if signal and name == signal:
        return "signal"

    # v3: axis named in parent @axes attr (string or array)
    axes = parent.attrs.get("axes")
    if isinstance(axes, str):
        if name == axes:
            return "axis"
    elif axes is not None:
        for axis_name in axes:
            if name == decode_if_string(axis_name):
                return "axis"

    # v3: AXISNAME_indices attr on the parent (scalar or array)
    indices_key = f"{name}_indices"
    raw = parent.attrs.get(indices_key)
    if raw is not None and _to_indices(raw) is not None:
        return "axis"

    # v2: own @signal="1"
    own_signal = decode_if_string(hdf_node.attrs.get("signal"))
    if own_signal == "1":
        return "signal"

    # v2/v1: own @axis integer attribute
    own_axis = hdf_node.attrs.get("axis")
    if isinstance(own_axis, numbers.Integral):
        return "axis"

    # v2: colon-separated @axes on a sibling signal dataset
    for key in parent.keys():
        sibling = parent[key]
        if not isinstance(sibling, h5py.Dataset):
            continue
        sig_axes = decode_if_string(sibling.attrs.get("axes"))
        if isinstance(sig_axes, str):
            for ax in sig_axes.split(":"):
                if ax and ax == name:
                    return "axis"
    return None


def find_default_nxentry(root: h5py.File | h5py.Group) -> h5py.Group | None:
    """Return the default NXentry group under *root*, or the first NXentry found."""
    return _default_entry(root)


def find_default_nxdata(root: h5py.File | h5py.Group) -> h5py.Group | None:
    """Walk the NeXus default chain to find the default plottable NXdata group.

    Implements three conventions in preference order:

    * **v3 (NIAC2014)**: ``root@default`` → NXentry → ``@default`` chain →
      NXdata with a ``@signal`` attribute.
    * **v2 (~2004)** / **v1 (oldest)** fallback: first NXentry → first NXdata.
    """
    # v3: follow @default chain from root
    nxentry = _default_entry(root)
    if nxentry is not None:
        nxdata = _follow_default_chain(nxentry)
        if (
            nxdata is not None
            and decode_if_string(nxdata.attrs.get("signal")) is not None
        ):
            return nxdata

    # v2/v1 fallback: first NXentry → first NXdata
    if nxentry is None:
        nxentry = _first_nxentry(root)
    if nxentry is None:
        return None
    return _first_nxdata(nxentry)


def inspect_nxdata(group: h5py.Group) -> NXdataInfo:
    """Return a :class:`NXdataInfo` for *group*, implementing v3→v2→v1 conventions.

    Tries v3 first (``@signal`` attr on the group), then v2 (``@signal="1"`` on
    a field), then v1 (single dataset with no signal attribute required).
    """
    info = NXdataInfo()

    # v3: signal named by @signal attr on the group
    signal_name = decode_if_string(group.attrs.get("signal"))
    if signal_name and signal_name in group:
        dataset = group[signal_name]
        if isinstance(dataset, h5py.Dataset):
            info.signal = dataset
            info.signal_name = signal_name
            info.convention = "v3"
            info.aux_signals = _read_aux_signals(group)
            info.axes, info.axes_indices = _collect_axes_v3(group, dataset)
            info.errors = _collect_errors(
                group, info.signal_name, info.axes, info.aux_signals
            )
            return info

    # v2: field with own @signal="1" attribute
    for key in group.keys():
        if not isinstance(group[key], h5py.Dataset):
            continue
        if decode_if_string(group[key].attrs.get("signal")) == "1":
            info.signal = group[key]
            info.signal_name = key
            info.convention = "v2"
            info.axes, info.axes_indices = _collect_axes_v2(group, group[key])
            info.errors = _collect_errors(
                group, info.signal_name, info.axes, info.aux_signals
            )
            return info

    # v1: single dataset (no signal attribute required)
    datasets = [group[k] for k in group.keys() if isinstance(group[k], h5py.Dataset)]
    if len(datasets) == 1:
        info.signal = datasets[0]
        info.signal_name = datasets[0].name.split("/")[-1]
        info.convention = "v1"
        info.errors = _collect_errors(
            group, info.signal_name, info.axes, info.aux_signals
        )

    return info


def check_nxdata(
    group: h5py.Group, info: NXdataInfo | None = None
) -> list[NXdataViolation]:
    """Check the six NXdata structural constraints from NXdata.nxdl.xml.

    Rules (numbered as in the NXDL doc):
      1. ``@axes`` length must equal the rank of DATA.
      2. ``AXISNAME_indices`` count must equal the rank of AXISNAME.
      3. When ``AXISNAME_indices`` is absent, fall back to position in ``@axes``.
         (Handled in inspect_nxdata — not re-checked here.)
      4. Corollary of 3 — no explicit check needed.
      5. Positions of AXISNAME in ``@axes`` must be a subset of ``AXISNAME_indices``.
      6. ``AXISNAME.shape[i]`` == ``DATA.shape[AXISNAME_indices[i]]`` or ``+1``
         (histogram bin edges).

    Additionally checks:
      - Auxiliary signal shapes must match the primary signal shape.

    Args:
        group: An h5py Group that is an NXdata group.
        info:  Pre-computed :class:`NXdataInfo` (from :func:`inspect_nxdata`).
               If *None*, ``inspect_nxdata(group)`` is called.

    Returns:
        A list of :class:`NXdataViolation` objects, empty when everything is valid.
    """
    if info is None:
        info = inspect_nxdata(group)

    if info.signal is None:
        signal_name = decode_if_string(group.attrs.get("signal"))
        if signal_name is not None:
            return [
                NXdataViolation(
                    kind=NXdataViolationKind.MissingSignalData,
                    message=(
                        f"@signal='{signal_name}' but no dataset '{signal_name}' "
                        f"exists in the group."
                    ),
                    subject=f"{group.name}/{signal_name}",
                )
            ]
        return []

    violations: list[NXdataViolation] = []
    group_path = group.name
    signal_shape = info.signal.shape
    signal_ndim = len(signal_shape)

    # Rule 1: @axes length == signal rank
    axes_attr = group.attrs.get("axes")
    if axes_attr is not None:
        axes_list = (
            [decode_if_string(axes_attr)]
            if isinstance(axes_attr, (str, bytes, np.bytes_))
            else [decode_if_string(a) for a in axes_attr]
        )
        if len(axes_list) != signal_ndim:
            violations.append(
                NXdataViolation(
                    kind=NXdataViolationKind.AxesRankMismatch,
                    message=(
                        f"@axes has {len(axes_list)} entries but signal "
                        f"'{info.signal_name}' has rank {signal_ndim}."
                    ),
                    subject=f"{group_path}@axes",
                )
            )
        axes_names = [a for a in axes_list if a != "."]
    else:
        axes_names = []

    # Rules 2, 5, 6: per-axis checks via AXISNAME_indices
    for attr_name in group.attrs.keys():
        if not attr_name.endswith("_indices"):
            continue
        ax_name = attr_name[: -len("_indices")]
        raw = group.attrs[attr_name]
        idx_list = _to_indices(raw)
        if idx_list is None:
            continue  # attribute present but not an integer or integer array

        # Rule 2: count of AXISNAME_indices must equal rank of AXISNAME field
        if ax_name in group and isinstance(group[ax_name], h5py.Dataset):
            ax_ds = group[ax_name]
            ax_ndim = len(ax_ds.shape)
            if len(idx_list) != ax_ndim:
                violations.append(
                    NXdataViolation(
                        kind=NXdataViolationKind.IndicesCountMismatch,
                        message=(
                            f"@{attr_name} has {len(idx_list)} index value(s) but "
                            f"'{ax_name}' has rank {ax_ndim}; they must be equal."
                        ),
                        subject=f"{group_path}@{attr_name}",
                    )
                )
            else:
                # Rule 6: shape correspondence
                for i, data_dim in enumerate(idx_list):
                    if data_dim < 0 or data_dim >= signal_ndim:
                        violations.append(
                            NXdataViolation(
                                kind=NXdataViolationKind.AxisShapeMismatch,
                                message=(
                                    f"@{attr_name}[{i}]={data_dim} is out of range "
                                    f"for signal rank {signal_ndim}."
                                ),
                                subject=f"{group_path}@{attr_name}",
                            )
                        )
                        continue
                    expected = signal_shape[data_dim]
                    actual = ax_ds.shape[i]
                    if actual != expected and actual != expected + 1:
                        violations.append(
                            NXdataViolation(
                                kind=NXdataViolationKind.AxisShapeMismatch,
                                message=(
                                    f"'{ax_name}'.shape[{i}]={actual} does not match "
                                    f"signal dimension {data_dim} (expected {expected} "
                                    f"or {expected + 1} for bin edges)."
                                ),
                                subject=f"{group_path}/{ax_name}",
                            )
                        )
        else:
            violations.append(
                NXdataViolation(
                    kind=NXdataViolationKind.MissingAxisData,
                    message=(
                        f"@{attr_name} references axis '{ax_name}' "
                        f"which does not exist in the group."
                    ),
                    subject=f"{group_path}/{ax_name}",
                )
            )

        # Rule 5: @axes positions of ax_name must be a subset of idx_list
        if ax_name in axes_names and axes_attr is not None:
            axes_positions = [
                i for i, a in enumerate(axes_list) if decode_if_string(a) == ax_name
            ]
            for pos in axes_positions:
                if pos not in idx_list:
                    violations.append(
                        NXdataViolation(
                            kind=NXdataViolationKind.IndicesNotSubset,
                            message=(
                                f"'{ax_name}' appears at position {pos} in @axes but "
                                f"@{attr_name}={idx_list} does not include {pos}."
                            ),
                            subject=f"{group_path}@{attr_name}",
                        )
                    )

    # Rule 6 for axes listed in @axes without an explicit AXISNAME_indices:
    # dimension index falls back to the position in @axes (rule 3).
    if axes_attr is not None:
        for pos, ax_name_raw in enumerate(axes_list):
            ax_name = decode_if_string(ax_name_raw)
            if ax_name == "." or ax_name is None:
                continue
            # Skip axes that have an explicit AXISNAME_indices (already checked above)
            if f"{ax_name}_indices" in group.attrs:
                continue
            if ax_name not in group or not isinstance(group[ax_name], h5py.Dataset):
                violations.append(
                    NXdataViolation(
                        kind=NXdataViolationKind.MissingAxisData,
                        message=(
                            f"@axes[{pos}] references axis '{ax_name}' "
                            f"which does not exist in the group."
                        ),
                        subject=f"{group_path}/{ax_name}",
                    )
                )
                continue
            ax_ds = group[ax_name]
            # For a 1D axis at position pos the expected size is signal_shape[pos]
            if pos < signal_ndim:
                expected = signal_shape[pos]
                actual = len(ax_ds)
                if actual != expected and actual != expected + 1:
                    violations.append(
                        NXdataViolation(
                            kind=NXdataViolationKind.AxisShapeMismatch,
                            message=(
                                f"'{ax_name}' at @axes[{pos}] has length {actual} but "
                                f"signal dimension {pos} has size {expected} "
                                f"(or {expected + 1} for bin edges)."
                            ),
                            subject=f"{group_path}/{ax_name}",
                        )
                    )

    # Auxiliary signal shape must match primary signal shape
    for aux_name in info.aux_signals:
        if aux_name not in group:
            violations.append(
                NXdataViolation(
                    kind=NXdataViolationKind.MissingSignalData,
                    message=f"@auxiliary_signals references '{aux_name}' which does not exist.",
                    subject=f"{group_path}/{aux_name}",
                )
            )
        elif isinstance(group[aux_name], h5py.Dataset):
            aux_shape = group[aux_name].shape
            if aux_shape != signal_shape:
                violations.append(
                    NXdataViolation(
                        kind=NXdataViolationKind.AuxSignalShapeMismatch,
                        message=(
                            f"Auxiliary signal '{aux_name}' has shape {aux_shape} "
                            f"but primary signal '{info.signal_name}' has shape "
                            f"{signal_shape}; they must be equal."
                        ),
                        subject=f"{group_path}/{aux_name}",
                    )
                )

    # FIELDNAME_errors shape must match the shape of its associated field
    for field_name, err_ds in info.errors.items():
        ref_shape = _ref_shape_for(field_name, info)
        if ref_shape is None and field_name in info.aux_signals and field_name in group:
            ref_shape = group[field_name].shape
        if ref_shape is not None and err_ds.shape != ref_shape:
            violations.append(
                NXdataViolation(
                    kind=NXdataViolationKind.AxisShapeMismatch,
                    message=(
                        f"'{field_name}_errors' has shape {err_ds.shape} but "
                        f"'{field_name}' has shape {ref_shape}; "
                        f"errors must have the same shape as their field."
                    ),
                    subject=f"{group_path}/{field_name}_errors",
                )
            )

    return violations


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _collect_errors(
    group: h5py.Group,
    signal_name: str | None,
    axes: list[list[h5py.Dataset]],
    aux_signals: list[str],
) -> dict[str, h5py.Dataset]:
    """Return ``{name: errors_dataset}`` for all detected signal/axis/aux names."""
    names: list[str] = []
    if signal_name:
        names.append(signal_name)
    seen: set[str] = set()
    for ax_list in axes:
        for ax_ds in ax_list:
            n = ax_ds.name.split("/")[-1]
            if n not in seen:
                seen.add(n)
                names.append(n)
    names.extend(aux_signals)
    return {
        n: group[f"{n}_errors"]
        for n in names
        if f"{n}_errors" in group and isinstance(group[f"{n}_errors"], h5py.Dataset)
    }


def _ref_shape_for(field_name: str, info: NXdataInfo) -> tuple[int, ...] | None:
    """Return the expected shape for a ``{field_name}_errors`` dataset.

    Returns the signal shape when *field_name* is the primary signal, the axis
    dataset shape when it matches an axis, and *None* for aux signals (caller
    resolves those via ``group[field_name].shape``).
    """
    if field_name == info.signal_name:
        return info.signal.shape if info.signal is not None else None
    for ax_list in info.axes:
        for ax_ds in ax_list:
            if ax_ds.name.split("/")[-1] == field_name:
                return ax_ds.shape
    return None


def _to_indices(raw) -> list[int] | None:
    """Convert a raw HDF5 attribute value to a list of integer indices.

    Accepts a scalar integer, a numpy integer, or a 1-D array of integers.
    Returns *None* for anything else.
    """
    if isinstance(raw, numbers.Integral):
        return [int(raw)]
    if isinstance(raw, np.ndarray):
        if raw.ndim == 0 and np.issubdtype(raw.dtype, np.integer):
            return [int(raw)]
        if raw.ndim == 1 and np.issubdtype(raw.dtype, np.integer):
            return [int(v) for v in raw]
    return None


def _default_entry(root: h5py.File | h5py.Group) -> h5py.Group | None:
    name = decode_if_string(root.attrs.get("default"))
    if name and name in root and isinstance(root[name], h5py.Group):
        return root[name]
    return _first_nxentry(root)


def _first_nxentry(root: h5py.File | h5py.Group) -> h5py.Group | None:
    for key in root.keys():
        grp = root[key]
        if (
            isinstance(grp, h5py.Group)
            and decode_if_string(grp.attrs.get("NX_class")) == "NXentry"
        ):
            return grp
    return None


def _follow_default_chain(group: h5py.Group) -> h5py.Group | None:
    """Follow ``@default`` attrs from *group* until landing on an NXdata or None."""
    current = group
    while True:
        default = decode_if_string(current.attrs.get("default"))
        if not default:
            if decode_if_string(current.attrs.get("NX_class")) == "NXdata":
                return current
            return None
        try:
            current = current[default]
        except KeyError:
            return None


def _first_nxdata(nxentry: h5py.Group) -> h5py.Group | None:
    for key in nxentry.keys():
        grp = nxentry[key]
        if (
            isinstance(grp, h5py.Group)
            and decode_if_string(grp.attrs.get("NX_class")) == "NXdata"
        ):
            return grp
    return None


def _read_aux_signals(group: h5py.Group) -> list[str]:
    aux = decode_if_string(group.attrs.get("auxiliary_signals"))
    if aux is None:
        return []
    return [aux] if isinstance(aux, str) else list(aux)


def _collect_axes_v3(
    group: h5py.Group, signal: h5py.Dataset
) -> tuple[list[list[h5py.Dataset]], list[list[list[int]]]]:
    """Collect axis datasets and their indices per signal dimension (v3 convention).

    Returns:
        axes:         ``axes[dim]`` → list of datasets spanning *dim*.
        axes_indices: ``axes_indices[dim]`` → parallel list of full index lists
                      (one per dataset in ``axes[dim]``).
    """
    dim = len(signal.shape)
    axes_attr = group.attrs.get("axes")
    axes_result: list[list[h5py.Dataset]] = [[] for _ in range(dim)]
    indices_result: list[list[list[int]]] = [[] for _ in range(dim)]

    # Build a name→indices map for all AXISNAME_indices attributes
    ax_indices_map: dict[str, list[int]] = {}
    for attr in group.attrs.keys():
        if attr.endswith("_indices"):
            ax_name = attr[: -len("_indices")]
            idx = _to_indices(group.attrs[attr])
            if idx is not None:
                ax_indices_map[ax_name] = idx

    # Collect axes named in @axes, using their explicit indices or fallback position
    if axes_attr is not None:
        axes_list = (
            [decode_if_string(axes_attr)]
            if isinstance(axes_attr, (str, bytes, np.bytes_))
            else [decode_if_string(a) for a in axes_attr]
        )
        for pos, ax_name in enumerate(axes_list):
            if ax_name == "." or ax_name is None:
                continue
            if ax_name not in group or not isinstance(group[ax_name], h5py.Dataset):
                continue
            ds = group[ax_name]
            idx_list = ax_indices_map.get(ax_name, [pos])
            for data_dim in idx_list:
                if 0 <= data_dim < dim:
                    if ds not in axes_result[data_dim]:
                        axes_result[data_dim].append(ds)
                        indices_result[data_dim].append(idx_list)

    # Collect additional axes declared only via AXISNAME_indices (not in @axes)
    for ax_name, idx_list in ax_indices_map.items():
        if ax_name not in group or not isinstance(group[ax_name], h5py.Dataset):
            continue
        ds = group[ax_name]
        for data_dim in idx_list:
            if 0 <= data_dim < dim:
                if ds not in axes_result[data_dim]:
                    axes_result[data_dim].append(ds)
                    indices_result[data_dim].append(idx_list)

    return axes_result, indices_result


def _collect_axes_v2(
    group: h5py.Group, signal_dataset: h5py.Dataset
) -> tuple[list[list[h5py.Dataset]], list[list[list[int]]]]:
    """Collect axis datasets per signal dimension using v2/v1 conventions."""
    own_axes = decode_if_string(signal_dataset.attrs.get("axes"))
    axes_names = own_axes.split(":") if isinstance(own_axes, str) else []
    dim = len(signal_dataset.shape)
    axes_result: list[list[h5py.Dataset]] = []
    indices_result: list[list[list[int]]] = []
    for a_item in range(dim):
        ax_list: list[h5py.Dataset] = []
        idx_list_list: list[list[int]] = []
        if a_item < len(axes_names) and axes_names[a_item] in group:
            ds = group[axes_names[a_item]]
            if isinstance(ds, h5py.Dataset):
                ax_list.append(ds)
                idx_list_list.append([a_item])
        if not ax_list:
            for key in group.keys():
                ds = group[key]
                if isinstance(ds, h5py.Dataset) and ds.attrs.get("axis") == a_item + 1:
                    if ds.attrs.get("primary") == 1:
                        ax_list.insert(0, ds)
                        idx_list_list.insert(0, [a_item])
                    else:
                        ax_list.append(ds)
                        idx_list_list.append([a_item])
        axes_result.append(ax_list)
        indices_result.append(idx_list_list)
    return axes_result, indices_result
