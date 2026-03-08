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
"""NXdata axis/signal inspection helpers.

These utilities detect whether a dataset participates in an NXdata
group as a signal or axis, implementing the NeXus Data Plotting
Standard (v2 from ~2004 and v3 from 2014).  They also provide helpers
for walking the NXentry → NXdata → signal chain.

None of these functions import from other pynxtools sub-modules aside
from `nexus.utils`, so they can be imported at any level without risk
of circular imports.
"""

from __future__ import annotations

import logging

import h5py
import numpy as np

from pynxtools.nexus.utils import decode_if_string


def chk_nxdata_axis_v2(
    hdf_node: h5py.Dataset, name: str, logger: logging.Logger
) -> None:
    """Check if *hdf_node* is referenced as an axis under the older NXdata conventions (v2)."""
    own_signal = hdf_node.attrs.get("signal")  # check for being a Signal
    if own_signal is str and own_signal == "1":
        logger.debug("Dataset referenced (v2) as NXdata SIGNAL")
    own_axes = hdf_node.attrs.get("axes")  # check for being an axis
    if own_axes is str:
        axes = own_axes.split(":")
        for i in range(len(axes)):
            if axes[i] and name == axes[i]:
                logger.debug("Dataset referenced (v2) as NXdata AXIS #%d", i)
                return None
    own_primary_axis = hdf_node.attrs.get("primary")
    own_axis = hdf_node.attrs.get("axis")
    if own_axis is int:
        # also convention v1
        if own_primary_axis is int and own_primary_axis == 1:
            logger.debug("Dataset referenced (v2) as NXdata AXIS #%d", own_axis - 1)
        else:
            logger.debug(
                "Dataset referenced (v2) as NXdata (primary/alternative) AXIS #%d",
                own_axis - 1,
            )
    return None


def chk_nxdata_axis(hdf_node: h5py.Dataset, name: str, logger: logging.Logger) -> None:
    """Check if *hdf_node* is referenced as a signal or axis in an NXdata group.

    Implements the NeXus Data Plotting Standard v3 (2014).  Falls back to v2
    conventions via :func:`chk_nxdata_axis_v2`.
    """
    if not isinstance(hdf_node, h5py.Dataset):
        return None
    parent = hdf_node.parent
    if not parent or (parent and not parent.attrs.get("NX_class") == "NXdata"):
        return None
    signal = parent.attrs.get("signal")  # check for Signal
    if signal and name == signal:
        logger.debug("Dataset referenced as NXdata SIGNAL")
        return None
    axes = parent.attrs.get("axes")  # check for default Axes
    if axes is str:
        if name == axes:
            logger.debug("Dataset referenced as NXdata AXIS")
            return None
    elif axes is not None:
        for i, j in enumerate(axes):
            if name == j:
                indices = parent.attrs.get(j + "_indices")
                if indices is int:
                    logger.debug(f"Dataset referenced as NXdata AXIS #{indices}")
                else:
                    logger.debug(f"Dataset referenced as NXdata AXIS #{i}")
                return None
    indices = parent.attrs.get(name + "_indices")  # check for alternative Axes
    if indices is int:
        logger.debug(f"Dataset referenced as NXdata alternative AXIS #{indices}")
    return chk_nxdata_axis_v2(hdf_node, name, logger)  # check for older conventions


def logger_auxiliary_signal(
    logger: logging.Logger, nxdata: h5py.Group
) -> logging.Logger:
    """Log any auxiliary signals declared in *nxdata*."""
    aux = decode_if_string(nxdata.attrs.get("auxiliary_signals"))
    if aux is not None:
        if isinstance(aux, str):
            aux = [aux]
        for aux_sig in aux:
            logger.debug(f"Further auxiliary signal has been identified: {aux_sig}")
    return logger


def print_default_plottable_header(logger: logging.Logger) -> None:
    """Emit a three-line visual separator before the default-plottable block."""
    logger.debug("========================")
    logger.debug("=== Default Plottable ===")
    logger.debug("========================")


def entry_helper(root: h5py.Group) -> h5py.Group | None:
    """Return the first NXentry group found directly under *root*, or ``None``."""
    nxentries = []
    for key in root.keys():
        if (
            isinstance(root[key], h5py.Group)
            and root[key].attrs.get("NX_class")
            and decode_if_string(root[key].attrs["NX_class"]) == "NXentry"
        ):
            nxentries.append(root[key])
    if len(nxentries) >= 1:
        return nxentries[0]
    return None


def nxdata_helper(nxentry: h5py.Group) -> h5py.Group | None:
    """Return the first NXdata group found directly under *nxentry*, or ``None``."""
    nxdata_list = []
    for key in nxentry.keys():
        if (
            isinstance(nxentry[key], h5py.Group)
            and nxentry[key].attrs.get("NX_class")
            and decode_if_string(nxentry[key].attrs["NX_class"]) == "NXdata"
        ):
            nxdata_list.append(nxentry[key])
    if len(nxdata_list) >= 1:
        return nxdata_list[0]
    return None


def signal_helper(nxdata: h5py.Group) -> h5py.Dataset | None:
    """Return the signal dataset for *nxdata*, or ``None`` if ambiguous."""
    signals = []
    for key in nxdata.keys():
        if isinstance(nxdata[key], h5py.Dataset):
            signals.append(nxdata[key])
    if (
        len(signals) == 1
    ):  # v3: as there was no selection given, only 1 data field shall exist
        return signals[0]
    if len(signals) > 1:  # v2: select the one with an attribute signal="1" attribute
        for sig in signals:
            signal_attr = decode_if_string(sig.attrs.get("signal"))
            if signal_attr and isinstance(signal_attr, str) and signal_attr == "1":
                return sig
    return None


def find_attrib_axis_actual_dim_num(
    nxdata: h5py.Group, a_item: int, ax_list: list
) -> None:
    """Append datasets that declare ``axis == a_item + 1`` to *ax_list* (in-place)."""
    lax = []
    for key in nxdata.keys():
        if isinstance(nxdata[key], h5py.Dataset):
            try:
                if nxdata[key].attrs["axis"] == a_item + 1:
                    lax.append(nxdata[key])
            except KeyError:
                pass
    if len(lax) == 1:
        ax_list.append(lax[0])
    # if there are more alternatives, prioritize the one with an attribute primary="1"
    elif len(lax) > 1:
        for sax in lax:
            if sax.attrs.get("primary") and sax.attrs.get("primary") == 1:
                ax_list.insert(0, sax)
            else:
                ax_list.append(sax)


def get_single_or_multiple_axes(
    nxdata: h5py.Group,
    ax_datasets: str | list | np.ndarray | None,
    a_item: int,
    ax_list: list,
    logger: logging.Logger,
) -> list:
    """Resolve axis datasets for dimension *a_item* from the ``axes`` attribute."""
    try:
        if isinstance(ax_datasets, str):  # single axis is defined
            # explicit definition of dimension number
            ind = decode_if_string(nxdata.attrs.get(ax_datasets + "_indices"))
            if ind and ind is int:
                if ind == a_item:
                    ax_list.append(nxdata[ax_datasets])
            elif a_item == 0:  # positional determination of the dimension number
                ax_list.append(nxdata[ax_datasets])
        elif isinstance(ax_datasets, list | np.ndarray):  # multiple axes are listed
            # explicit definition of dimension number
            for aax in ax_datasets:
                ind = decode_if_string(nxdata.attrs.get(aax + "_indices"))
                if ind and isinstance(ind, int):
                    if ind == a_item:
                        ax_list.append(nxdata[aax])
            if not ax_list and a_item < len(
                ax_datasets
            ):  # positional determination of the dimension number
                ax_list.append(nxdata[ax_datasets[a_item]])
        else:
            logger.warning(
                f"The 'axes' attribute is neither a string or a list or an np.ndarray "
                f"of strings, check {nxdata.name}"
            )
    except KeyError:
        logger.warning(
            f"Individual axis in 'axes' attribute for NXdata {nxdata.name} is not found"
        )
    return ax_list


def axis_helper(
    dim: int,
    nxdata: h5py.Group,
    signal: h5py.Dataset,
    axes: list,
    logger: logging.Logger,
) -> None:
    """Collect axis datasets for each dimension of *signal* (in-place into *axes*)."""
    for a_item in range(dim):
        ax_list: list = []
        # primary axes listed in attribute axes
        ax_datasets = decode_if_string(nxdata.attrs.get("axes"))
        ax_list = get_single_or_multiple_axes(
            nxdata, ax_datasets, a_item, ax_list, logger
        )
        for attr in nxdata.attrs.keys():  # check for corresponding AXISNAME_indices
            if (
                attr.endswith("_indices")
                and decode_if_string(nxdata.attrs[attr]) == a_item
                and nxdata[attr.split("_indices")[0]] not in ax_list
            ):
                ax_list.append(nxdata[attr.split("_indices")[0]])
        # v2  # check for ':' separated axes defined in Signal
        if not ax_list:
            try:
                ax_datasets = decode_if_string(signal.attrs.get("axes")).split(":")
                ax_list.append(nxdata[ax_datasets[a_item]])
            except (KeyError, AttributeError):
                pass
        if not ax_list:  # check for axis/primary specifications
            find_attrib_axis_actual_dim_num(nxdata, a_item, ax_list)
        axes.append(ax_list)
        logger.debug("")
        logger.debug(
            f"For Axis #{a_item}, {len(ax_list)} axes have been identified: {ax_list!s}"
        )
