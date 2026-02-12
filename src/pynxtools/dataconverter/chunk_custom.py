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

"""Utilities for overwriting h5py chunking heuristic to consider domain-specific access pattern."""

import numpy as np

from pynxtools.dataconverter.chunk_cache import CHUNK_CONFIG_DEFAULT
from pynxtools.dataconverter.helpers import logger


def prioritized_axes_heuristic(
    data: np.ndarray,
    priority: tuple[int, ...],
) -> tuple[int, ...] | bool:
    """Define an explicit tuple[int] how to chunk data with shape

    Parameter:
    * data, a numpy array
    * priority, all dimension scale axes indices, arranged
    in increasing priority which axes should not be as strongly splitted into chunks.
    the later the index in priority, the more likely this axis will be splitted
    into fewer chunks, if any.

    Examples substantiating this heuristic:
    * Electron microscopy, a stack of 100,000 x 1024 x 1024 2D images, 4B int itemsize:
    Chunking should keep dim 1 and especially dim 2 (especially for C-style storage, i.e.,
    when dim 2 changes fastest, as contiguous as possible, and chunk mainly on dim 0,
    Reason is often users wish to read entire images completely than slicing thin
    pixel slabs in other (orthogonal viewing directions)
    * Reconstructed ion positions in atom probe 1,000,000 x 3, 4B itemsize,
    users wish to read entire position triplets in contiguous blocks of triplets
    rather than reading fast a single column. Therefore, dim 0 should be chunked
    with higher priority while trying to keep dim 1 intact.

    By contrast, h5py current auto-chunking guess_chunk function e.g., https://github.com/h5py/h5py/blob/
    706755340058c8e8000ed769d4f5ad3571e4dfce/h5py/_hl/filters.py#L361
    splits alternatingly across all dims. In effect, arrays get chunked more regularly,
    useful especially when all three orthogonal viewing directions are roughly equally
    important for slicing but for the above-mentioned examples such strategy can easily
    cause that even a single 1024 x 1024 image will be distributed across dozens of
    chunks, making data retrieval unnecessarily slower. Note that the proposal here,
    is like the guess_chunk from h5py a heuristic, the latter ought to apply to many
    cases but that must not be understood as it is at all a useful solution to go with
    if the display/usage pattern of an array is well-known a priori and biased frequently
    towards slicing across a specific direction. Currently, guess_chunk offers
    a compromise for slicing about equally all three orthogonal
    directions.

    Examples:
    * prioritized_axes_heuristic((100000, 2048, 2048), (0, 1, 2))
    * prioritized_axes_heuristic((1000000, 3), (0, 1))
    * prioritized_axes_heuristic((60, 60, 180), (2, 1, 0))

    Returns value for the chunks parameter of h5py create_dataset
    * tuple[int, ...], explicit chunk size
    * True, the fallback to h5py guess_chunk auto-chunking."""
    if not isinstance(data, np.ndarray):  # only np.ndarray supported
        logger.info(f"chunk strategy h5py auto used for non-numpy array")
        return True
    shape: tuple[int, ...] = np.shape(data)
    if any(extent == 0 for extent in shape):  # unlimited axis not supported
        logger.info(f"chunk strategy h5py auto used for datasets with unlimited axes")
        return True
    if set(priority) != set(range(len(priority))):  # all dim indices need to be present
        logger.info(
            f"chunk strategy h5py auto used for incorrect axes priority setting"
        )
        return True
    if len(shape) == 0:
        raise ValueError("chunk_shape not allowed for scalar datasets.")
        # also h5py by default would raise in such a case
    chunk_shape: list[float] = list(float(extent) for extent in shape)
    max_byte_per_chunk: int = int(CHUNK_CONFIG_DEFAULT["byte_size"])
    byte_per_item: int = data.itemsize

    dim = 0
    idx = 0
    logger.debug(
        f"chunk strategy, prioritized_axes_heuristic analyzing for shape {shape} and byte_per_item {byte_per_item} ..."
    )  # allow monitoring if we ever run into an infinite loop
    while True:
        idx += 1
        byte_per_chunk = np.prod(chunk_shape) * byte_per_item
        logger.debug(
            f"chunk strategy, while {idx}, {dim}, {chunk_shape}, {byte_per_chunk}"
        )
        if byte_per_chunk < max_byte_per_chunk:
            # one issue with splitting always in half is that when we break out
            # here it can happen that max_byte_per_chunk - byte_per_chunk is large
            # enough that one could still pack another slice of data across the
            # most prominent axis along we chopped initially, e.g.
            # say 1000 * extent(dim1) * extent(dim2) with dim0 the most prominent axis
            # is not yet full-filling the condition but 1000 / 2 does leading to 500
            # although still say 100 * extent(dim1) * extent(dim2) would fit
            logger.debug(
                f"chunk strategy, below max_byte {idx}, {dim}, {chunk_shape}, {byte_per_chunk}"
            )
            fill_up_along_most_prominent_axis = max_byte_per_chunk / byte_per_item
            logger.debug(
                f"chunk strategy, below max_byte {fill_up_along_most_prominent_axis}"
            )
            for dim_idx in np.arange(1, len(chunk_shape)):
                fill_up_along_most_prominent_axis = (
                    fill_up_along_most_prominent_axis / np.ceil(chunk_shape[dim_idx])
                )
                logger.debug(
                    f"chunk strategy, below_max_byte {fill_up_along_most_prominent_axis}, {dim_idx}, {np.ceil(chunk_shape[dim_idx])}"
                )
            if 0 < int(shape[0]) < int(fill_up_along_most_prominent_axis):
                chunk_shape[0] = shape[0]
                logger.debug(
                    f"chunk strategy, below max_byte, cap to shape[0] chunk_shape[0] {chunk_shape[0]}"
                )
            elif int(fill_up_along_most_prominent_axis) >= 1:
                chunk_shape[0] = fill_up_along_most_prominent_axis
                logger.debug(
                    f"chunk strategy, below max_byte, fill-up to max chunk_shape[0] {chunk_shape[0]}"
                )
            else:
                logger.debug(
                    f"chunk strategy, below max_byte, no further tweaking chunk_shape[0] {chunk_shape[0]}"
                )

            break
        if chunk_shape[dim] % 2 == 0:
            chunk_shape[dim] = chunk_shape[dim] / 2
        else:
            chunk_shape[dim] = (chunk_shape[dim] / 2) + 1

        if dim < (len(shape) - 1):
            if chunk_shape[dim] < 2:
                dim += 1
                # seems we cannot reduce byte_per_chunk further by splitting
                # along dim, so unfortunately need to consider splitting across
                # the next, less prioritized axis
        else:
            # continue splitting on the same axes irrespective if ndims == 1 or higher
            if chunk_shape[dim] >= 2:
                continue

            # can't figure something out that is anywhere smarter, go with h5py chunking heuristic
            logger.debug(
                f"chunk strategy h5py auto, no more axes can be splitted to reduce byte_per_chunk"
            )
            return True

    if all(int(extent) >= 1 for extent in chunk_shape):
        logger.debug(
            f"chunk strategy custom {tuple(int(extent) for extent in chunk_shape)} for shape {shape} with byte_per_item {byte_per_item} using chunk_shape {chunk_shape}, byte_per_chunk {byte_per_chunk}"
        )
        return tuple(int(extent) for extent in chunk_shape)
    logger.debug(f"chunk strategy h5py auto used")
    return True
