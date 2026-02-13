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
"""Test cases chunking and compression."""

import numpy as np

from pynxtools.dataconverter.chunk import prioritized_axes_heuristic


def test_prioritized_axes_heuristic():
    pass
    # array = np.zeros((8, 1024, 1024), np.float64)
    # intentional usage
    # assert () == prioritized_axes_heuristic(array, (0, 1, 2))
    # awkward
    # assert () == prioritized_axes_heuristic(array, (0, 2, 1))
    # assert () == prioritized_axes_heuristic(array, (1, 2, 0))
    # assert () == prioritized_axes_heuristic(array, (1, 0, 2))
    # assert () == prioritized_axes_heuristic(array, (2, 0, 1))
    # assert () == prioritized_axes_heuristic(array, (2, 1, 0))
    # scalar
    # assert prioritized_axes_heuristic(2, (0,))
    # unlimited axis
    # assert prioritized_axes_heuristic(???, (0,))
    # multiples
    # assert prioritized_axes_heuristic(array, ())
    # assert prioritized_axes_heuristic(array, (0,))
    # assert prioritized_axes_heuristic(array, (0, 1,))
    # assert prioritized_axes_heuristic(array, (0, 0,))
    # assert prioritized_axes_heuristic(array, (0, 1, 1))
    # assert prioritized_axes_heuristic(array, (0, 1, 2, 2))
