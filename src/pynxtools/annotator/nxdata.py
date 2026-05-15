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
"""NXdata annotation helpers — logging wrappers around ``nexus.nxdata``.

Pure detection logic lives in :mod:`pynxtools.nexus.nxdata`. This module
exposes logging-aware wrappers used by the annotator and re-exports the
shared helpers for backward compatibility.
"""

from __future__ import annotations

import logging
import numbers
from typing import Literal

import h5py
import numpy as np

from pynxtools.nexus.nxdata import classify_field as _classify_field
from pynxtools.nexus.nxdata import (
    entry_helper,
    find_attrib_axis_actual_dim_num,
    nxdata_helper,
    signal_helper,
)
from pynxtools.nexus.utils import decode_if_string

_logger = logging.getLogger(__file__)

# Re-export helpers that callers may import from this module
__all__ = [
    "chk_nxdata_axis_v2",
    "chk_nxdata_axis",
    "logger_auxiliary_signal",
    "print_default_plottable_header",
    "entry_helper",
    "nxdata_helper",
    "signal_helper",
    "find_attrib_axis_actual_dim_num",
    "get_single_or_multiple_axes",
    "axis_helper",
]


def chk_nxdata_axis_v2(
    hdf_node: h5py.Dataset,
    name: str,
    indent: str = "",
    logger: logging.Logger | None = None,
) -> Literal["axis", "signal"] | None:
    """Check if *hdf_node* is referenced as an axis under the older NXdata conventions (v2).

    Delegates detection to :func:`~pynxtools.nexus.nxdata.classify_field`.
    Returns ``'signal'``, ``'axis'``, or ``None``.
    """
    logger = logger or _logger
    result = _classify_field(hdf_node, name)
    if result == "signal":
        logger.debug(f"{indent}Dataset referenced (v2) as NXdata SIGNAL")
    elif result == "axis":
        own_axis = hdf_node.attrs.get("axis")
        own_primary = hdf_node.attrs.get("primary")
        if isinstance(own_axis, int):
            if isinstance(own_primary, int) and own_primary == 1:
                logger.debug(
                    f"{indent}Dataset referenced (v2) as NXdata AXIS #%d",
                    own_axis - 1,
                )
            else:
                logger.debug(
                    f"{indent}Dataset referenced (v2) as NXdata (primary/alternative) AXIS #%d",
                    own_axis - 1,
                )
        else:
            logger.debug(f"{indent}Dataset referenced (v2) as NXdata AXIS")
    return result


def chk_nxdata_axis(
    hdf_node: h5py.Dataset,
    name: str,
    indent: str = "",
    logger: logging.Logger | None = None,
) -> Literal["axis", "signal"] | None:
    """Check if *hdf_node* is referenced as a signal or axis in an NXdata group.

    Implements v3 (NIAC2014) first, falling back to v2/v1 via
    :func:`~pynxtools.nexus.nxdata.classify_field`.
    Returns ``'signal'``, ``'axis'``, or ``None``.
    """
    logger = logger or _logger

    if not isinstance(hdf_node, h5py.Dataset):
        return None
    parent = hdf_node.parent
    if not parent or parent.attrs.get("NX_class") != "NXdata":
        return None

    result = _classify_field(hdf_node, name)
    if result == "signal":
        logger.debug(f"{indent}Dataset referenced as NXdata SIGNAL")
    elif result == "axis":
        # Preserve index-number in the log message where we can derive it
        parent_signal = decode_if_string(parent.attrs.get("signal"))
        axes = parent.attrs.get("axes")
        indices_key = f"{name}_indices"
        if isinstance(axes, str):
            logger.debug(f"{indent}Dataset referenced as NXdata AXIS")
        elif axes is not None:
            matched = False
            for i, axis_name in enumerate(axes):
                if name == decode_if_string(axis_name):
                    indices = parent.attrs.get(f"{decode_if_string(axis_name)}_indices")
                    if isinstance(indices, numbers.Integral):
                        logger.debug(
                            f"{indent}Dataset referenced as NXdata AXIS #%d",
                            int(indices),
                        )
                    else:
                        logger.debug(
                            f"{indent}Dataset referenced as NXdata AXIS #%d",
                            i,
                        )
                    matched = True
                    break
            if not matched:
                logger.debug(f"{indent}Dataset referenced as NXdata AXIS")
        elif isinstance(parent.attrs.get(indices_key), numbers.Integral):
            logger.debug(
                f"{indent}Dataset referenced as NXdata alternative AXIS #%d",
                int(parent.attrs[indices_key]),
            )
        else:
            # v2/v1 fallback — let chk_nxdata_axis_v2 log the appropriate message
            return chk_nxdata_axis_v2(hdf_node, name, indent=indent, logger=logger)
    return result


def logger_auxiliary_signal(
    nxdata: h5py.Group, logger: logging.Logger | None = None
) -> None:
    """Log any auxiliary signals declared in *nxdata*."""
    logger = logger or _logger
    aux = decode_if_string(nxdata.attrs.get("auxiliary_signals"))
    if aux is not None:
        if isinstance(aux, str):
            aux = [aux]
        for aux_sig in aux:
            logger.debug(f"Further auxiliary signal has been identified: {aux_sig}")


def print_default_plottable_header(logger: logging.Logger | None = None) -> None:
    """Print a three-line header for the default plottable section."""
    logger = logger or _logger
    logger.debug("")
    logger.debug("========================")
    logger.debug("=== Default Plottable ===")
    logger.debug("========================")


def get_single_or_multiple_axes(
    nxdata: h5py.Group,
    ax_datasets: str | list | np.ndarray | None,
    a_item: int,
    ax_list: list,
    logger: logging.Logger | None = None,
) -> list:
    """Resolve axis datasets for dimension *a_item* from the ``axes`` attribute."""
    logger = logger or _logger
    try:
        if isinstance(ax_datasets, str):
            ind = decode_if_string(nxdata.attrs.get(ax_datasets + "_indices"))
            if ind and isinstance(ind, int):
                if ind == a_item:
                    ax_list.append(nxdata[ax_datasets])
            elif a_item == 0:
                ax_list.append(nxdata[ax_datasets])
        elif isinstance(ax_datasets, list | np.ndarray):
            for aax in ax_datasets:
                ind = decode_if_string(nxdata.attrs.get(aax + "_indices"))
                if ind and isinstance(ind, int):
                    if ind == a_item:
                        ax_list.append(nxdata[aax])
            if not ax_list and a_item < len(ax_datasets):
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
    logger: logging.Logger | None = None,
) -> None:
    """Collect axis datasets for each dimension of *signal* (in-place into *axes*)."""
    logger = logger or _logger
    for a_item in range(dim):
        ax_list: list = []
        ax_datasets = decode_if_string(nxdata.attrs.get("axes"))
        ax_list = get_single_or_multiple_axes(
            nxdata, ax_datasets, a_item, ax_list, logger
        )
        for attr in nxdata.attrs.keys():
            if (
                attr.endswith("_indices")
                and decode_if_string(nxdata.attrs[attr]) == a_item
                and nxdata[attr.split("_indices")[0]] not in ax_list
            ):
                ax_list.append(nxdata[attr.split("_indices")[0]])
        if not ax_list:
            try:
                ax_datasets = decode_if_string(signal.attrs.get("axes")).split(":")
                ax_list.append(nxdata[ax_datasets[a_item]])
            except (KeyError, AttributeError):
                pass
        if not ax_list:
            find_attrib_axis_actual_dim_num(nxdata, a_item, ax_list)
        axes.append(ax_list)
        logger.debug("")
        logger.debug(
            f"For Axis #{a_item}, {len(ax_list)} axes have been identified: {ax_list!s}"
        )
