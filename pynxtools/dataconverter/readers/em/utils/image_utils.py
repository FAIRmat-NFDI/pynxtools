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

import numpy as np


# https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
def sort_ascendingly_by_second_argument(tup):
    # convert the list of tuples to a numpy array with data type (object, int)
    arr = np.array(tup, dtype=[('col1', object), ('col2', int)])
    # get the indices that would sort the array based on the second column
    indices = np.argsort(arr['col2'])
    # use the resulting indices to sort the array
    sorted_arr = arr[indices]
    # convert the sorted numpy array back to a list of tuples
    sorted_tup = [(row['col1'], row['col2']) for row in sorted_arr]
    return sorted_tup


def if_str_represents_float(s):
    try:
        return isinstance(float(s), float)
    except ValueError:
        return False
