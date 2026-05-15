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
"""NXdata axis/signal helpers re-exported from ``nexus.nxdata`` for backward compat.

Pure detection logic lives in :mod:`pynxtools.nexus.nxdata`. This module
re-exports the legacy helpers still imported by :mod:`pynxtools.nexus.nexus`.
"""

from __future__ import annotations

import logging

import h5py
import numpy as np

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
    "entry_helper",
    "nxdata_helper",
    "signal_helper",
    "find_attrib_axis_actual_dim_num",
    "get_single_or_multiple_axes",
    "axis_helper",
]


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
