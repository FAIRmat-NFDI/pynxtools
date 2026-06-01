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
"""Pure NXdata detection utilities — no logging dependency.

This module implements the three NeXus Data Plotting Standard conventions
for identifying the default plottable signal and its axes in an HDF5/NeXus
file, in order of preference:

- **v3 (NIAC2014)**: ``@signal`` attribute on the NXdata group names the
  signal; ``@axes`` or ``AXISNAME_indices`` group attributes name the axes.
- **v2 (~2004)**: a field carries ``signal="1"``; axes are named via a
  colon/comma-delimited ``@axes`` attribute on that field.
- **v1 (oldest)**: a field carries ``signal="1"``; axes are associated via
  ``axis=N`` integer attributes on the axis fields (and optionally
  ``primary=1`` to select the preferred axis for a given dimension).

If none of these spec-defined conventions is detected, ``convention=None``
is returned and the signal is left as ``None``.

Public API:
    NXdataInfo      — structured result of inspecting an NXdata group
    classify_field  — return 'signal', 'axis', or None for a dataset
    find_default_nxdata — walk the default chain to find the NXdata group
    inspect_nxdata  — return NXdataInfo for an NXdata group

These functions carry no logging dependency and can be reused by both the
annotator and the validator (see issue #519).
"""

from __future__ import annotations

import numbers
import re
from dataclasses import dataclass, field
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
                      dimension *dim* of the signal.
        aux_signals:  Names of auxiliary signal datasets (v3 only).
        convention:   Which plottable convention was detected: ``'v3'``
                      (NIAC2014 group-level ``@signal``), ``'v2'`` (field-level
                      ``signal="1"`` with ``@axes`` on the signal), ``'v1'``
                      (field-level ``signal="1"`` with ``axis=N`` on axis
                      fields), or ``None`` if no spec-defined convention found.
    """

    signal: h5py.Dataset | None = None
    signal_name: str | None = None
    axes: list[list[h5py.Dataset]] = field(default_factory=list)
    aux_signals: list[str] = field(default_factory=list)
    convention: Literal["v3", "v2", "v1"] | None = None


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

    # v3: AXISNAME_indices attr on the parent
    indices_key = f"{name}_indices"
    if isinstance(parent.attrs.get(indices_key), numbers.Integral):
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
    """Return a :class:`NXdataInfo` for *group*, implementing v3 → v2 → v1 conventions.

    Tries v3 first (``@signal`` attr on the group), then v2 (field-level
    ``signal="1"`` with ``@axes`` on that field), then v1 (field-level
    ``signal="1"`` with ``axis=N`` attributes on axis fields).  Returns
    ``NXdataInfo()`` with ``convention=None`` if no spec-defined convention
    is satisfied.
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
            info.axes = _collect_axes_v3(group, dataset)
            return info

    # v2 / v1: field with own @signal="1" attribute
    # v2 if that field also carries @axes (colon/comma-delimited axis names);
    # v1 if axes are associated via axis=N integer attributes on axis fields.
    for key in group.keys():
        if not isinstance(group[key], h5py.Dataset):
            continue
        if decode_if_string(group[key].attrs.get("signal")) == "1":
            ds = group[key]
            info.signal = ds
            info.signal_name = key
            info.convention = "v2" if ds.attrs.get("axes") is not None else "v1"
            info.axes = _collect_axes_v2(group, ds)
            return info

    return info


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _default_entry(root: h5py.File | h5py.Group) -> h5py.Group | None:
    """Return the default entry group or the first NXentry group if no default is set."""
    name = decode_if_string(root.attrs.get("default"))
    if name and name in root and isinstance(root[name], h5py.Group):
        return root[name]
    return _first_nxentry(root)


def _first_nxentry(root: h5py.File | h5py.Group) -> h5py.Group | None:
    """Return the first NXentry encountered in HDF5 iteration order under *root*."""
    for key in root.keys():
        hdf_node = root[key]
        if (
            isinstance(hdf_node, h5py.Group)
            and decode_if_string(hdf_node.attrs.get("NX_class")) == "NXentry"
        ):
            return hdf_node
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
    """Find the first NXdata with an NXentry"""
    for key in nxentry.keys():
        grp = nxentry[key]
        if (
            isinstance(grp, h5py.Group)
            and decode_if_string(grp.attrs.get("NX_class")) == "NXdata"
        ):
            return grp
    return None


def _read_aux_signals(group: h5py.Group) -> list[str]:
    """Read the aux_signals from an NXdata group"""
    aux = decode_if_string(group.attrs.get("auxiliary_signals"))
    if aux is None:
        return []
    return [aux] if isinstance(aux, str) else list(aux)


def _collect_axes_v3(
    group: h5py.Group, signal: h5py.Dataset
) -> list[list[h5py.Dataset]]:
    """Collect axis datasets per signal dimension using v3 convention."""
    dim = len(signal.shape)
    axes_attr = group.attrs.get("axes")
    result = []
    for a_item in range(dim):
        ax_list: list[h5py.Dataset] = []
        # Per the NeXus manual, @axes should be a list; the str branch handles
        # single-axis files where HDF5 stores a scalar string instead of a 1-element array.
        if isinstance(axes_attr, str):
            ind = group.attrs.get(f"{axes_attr}_indices")
            if (isinstance(ind, numbers.Integral) and ind == a_item) or (
                ind is None and a_item == 0
            ):
                if axes_attr in group and isinstance(group[axes_attr], h5py.Dataset):
                    ax_list.append(group[axes_attr])
        elif isinstance(axes_attr, (list, np.ndarray)):
            for ax_name_raw in axes_attr:
                ax_name = decode_if_string(ax_name_raw)
                if not isinstance(ax_name, str):
                    continue
                if ax_name == ".":
                    continue
                ind = group.attrs.get(f"{ax_name}_indices")
                if isinstance(ind, numbers.Integral) and ind == a_item:
                    if ax_name in group and isinstance(group[ax_name], h5py.Dataset):
                        ax_list.append(group[ax_name])
            if not ax_list and a_item < len(axes_attr):
                ax_name = decode_if_string(axes_attr[a_item])
                if (
                    ax_name != "."
                    and ax_name in group
                    and isinstance(group[ax_name], h5py.Dataset)
                ):
                    ax_list.append(group[ax_name])
        # AXISNAME_indices attrs on the group for axes not in @axes
        for attr in group.attrs:
            if attr.endswith("_indices") and isinstance(
                group.attrs[attr], numbers.Integral
            ):
                if group.attrs[attr] == a_item:
                    ax_field_name = attr[: -len("_indices")]
                    if (
                        ax_field_name in group
                        and isinstance(group[ax_field_name], h5py.Dataset)
                        and group[ax_field_name] not in ax_list
                    ):
                        ax_list.append(group[ax_field_name])
        result.append(ax_list)
    return result


def _collect_axes_v2(
    group: h5py.Group, signal_dataset: h5py.Dataset
) -> list[list[h5py.Dataset]]:
    """Collect axis datasets per signal dimension using v2/v1 conventions."""
    own_axes = decode_if_string(signal_dataset.attrs.get("axes"))
    axes_names = re.split(r"[:,]", own_axes) if isinstance(own_axes, str) else []
    dim = len(signal_dataset.shape)
    result = []
    for a_item in range(dim):
        ax_list: list[h5py.Dataset] = []
        if a_item < len(axes_names) and axes_names[a_item] in group:
            ds = group[axes_names[a_item]]
            if isinstance(ds, h5py.Dataset):
                ax_list.append(ds)
        if not ax_list:
            for key in group.keys():
                ds = group[key]
                if isinstance(ds, h5py.Dataset) and ds.attrs.get("axis") == a_item + 1:
                    if ds.attrs.get("primary") == 1:
                        ax_list.insert(0, ds)
                    else:
                        ax_list.append(ds)
        result.append(ax_list)
    return result
