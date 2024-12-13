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
"""A script to create mock data for the example reader."""

import numpy as np
import h5py


# Function to generate a Gaussian curve
def gaussian_2d(x, y, mu_x, mu_y, sigma_x, sigma_y):
    """
    Computes a 2D Gaussian function.

    Parameters:
    - x: np.ndarray, 1D array representing the x-axis values.
    - y: np.ndarray, 1D array representing the y-axis values.
    - mu_x: float, mean along the x-axis.
    - mu_y: float, mean along the y-axis.
    - sigma_x: float, standard deviation along the x-axis.
    - sigma_y: float, standard deviation along the y-axis.

    Returns:
    - np.ndarray, 2D array of Gaussian values.
    """
    # Create 2D mesh grids for x and y
    X, Y = np.meshgrid(x, y, indexing="ij")  # 'ij' ensures x rows align with y cols
    # Compute the Gaussian in 2D
    return np.exp(-0.5 * (((X - mu_x) / sigma_x) ** 2 + ((Y - mu_y) / sigma_y) ** 2))


# Define the x-axis (evenly spaced)
x = np.linspace(-5, 5, 100)  # 100 points between -5 and 5
y = np.linspace(-5, 5, 100)

# Parameters for the Gaussian
mu_x = 0
mu_y = 0
sigma_x = 1
sigma_y = 2

# Generate the 2D Gaussian
gaussian_values = gaussian_2d(x, y, mu_x, mu_y, sigma_x, sigma_y)

# Define the structure of the HDF5 file as a nested dictionary
data_structure = {
    "axes": {
        "x_values": x,
        "y_values": y,
        "x_values/@units": "eV",
        "y_values/@units": "eV",
    },
    "data": {
        "intensity": gaussian_values,
        "intensity/@units": "counts_per_second",
    },
    "metadata": {
        "instrument": {
            "version": 1.0,
            "detector": {
                "name": "my_gaussian_detector",
                "count_time": 1.2,
                "count_time_units": "s",
            },
        },
    },
}


# Function to recursively create groups and datasets from the dictionary
def create_hdf5_group(group, structure):
    for key, value in structure.items():
        if isinstance(value, dict):
            # Create a subgroup and recursively add its contents
            subgroup = group.create_group(key)
            create_hdf5_group(subgroup, value)
        else:
            # Create a dataset
            if isinstance(value, str):
                value = np.bytes_(value)  # Convert strings to numpy strings
            group.create_dataset(key, data=value)


# Create a new HDF5 file and populate it using the dictionary structure
with h5py.File("mock_data.h5", "w") as hdf:
    create_hdf5_group(hdf, data_structure)
