# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""A script to create mock data for the example reader."""

import numpy as np
import h5py


# Function to generate a Gaussian curve
def gaussian(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2)


# Define the x-axis (evenly spaced)
x_values = np.linspace(-10, 10, 100)

# Generate Gaussian y-values
y_gaussian = gaussian(x_values, mu=0, sigma=1)

# Define the structure of the HDF5 file as a nested dictionary
data_structure = {
    "data": {
        "x_values": x_values,
        "y_values": y_gaussian,
        "x_units": "eV",
        "y_units": "counts_per_second",
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
