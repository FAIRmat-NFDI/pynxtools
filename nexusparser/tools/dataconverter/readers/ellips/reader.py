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
"""An example reader implementation for the DataConverter."""
import os
from typing import Tuple

import h5py
import pyaml as yaml
import pandas as pd
import numpy as np

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader

DEFAULT_HEADER = {'sep': '\t', 'skip': 0}


def load_header(filename, default):
    """ load the yaml description file, and apply defaults as well
        Parameters:
        filename:           a yaml file containing the definitions
        default_header:     predefined default values
    """
    with open(filename, 'rt') as file:
        header = yaml.yaml.safe_load(file)

    for attr in header:
        if "@" in attr:
            header[attr.replace("\\@", "@")] = header.pop(attr)

    for key, value in default.items():
        if key not in header:
            header[key] = value
    return header


def load_as_array(my_file, header):
    """ Load a CSV output file using the header dict.

    """
    required_parameters = ("colnames", "skip", "sep")
    for required_parameter in required_parameters:
        if required_parameter not in header:
            raise ValueError('colnames, skip and sep are required header parameters!')

    if not os.path.isfile(my_file):
        raise IOError(f'File not found error: {my_file}')

    whole_data = pd.read_csv(my_file,
                             # use header = None and names to define custom column names
                             header=None,
                             names=header['colnames'],
                             skiprows=header['skip'],
                             delimiter=header['sep'])
    return whole_data


def slice_shape_definition(my_numpy_array):
    """This is an ellipsometry-specific slicing procedure of data.

The virtual datasets are created in the NeXus file
by the writer.py according to the shapes we define here.

The my_numpy_array[:, 1] column of source array my_numpy_array contains the incidence angles,
it is read to obtain the values of incidence_angles and their index in the source array.
These parameters will be used to define intervals to slice the source array
and create separate datasets for each incidence angle.
The intervals are defined in interval_list variable.
The datasets we want to create are:
- Wavelength
- Psi values
- Delta value
These parameters are stored in lists and then passed to the writer.py
"""
    unique_angles, counts = np.unique(my_numpy_array[:, 1], return_counts=True)
    wavelengthlist = []
    psilist = []
    deltalist = []
    index = 0
    interval_list = [np.int64(0)]
    for angle_no, angle in enumerate(unique_angles):
        angle = int(angle)
        psilist.append(f"psi_{angle}deg")
        deltalist.append(f"delta_{angle}deg")
        wavelengthlist.append(f"wavelength_{angle}deg")
        index += counts[angle_no]
        interval_list.append(index)
    return wavelengthlist, psilist, deltalist, interval_list


def virtual_dataset_generation(my_source_file, my_numpy_array):
    """This is an ellipsometry-specific slicing procedure of data.

The virtual datasets are created IN THE ROOT LEVEL of SOURCE FILE
according to the shapes we define here.

The strategy Is the following:
An array of data is saved in a HDF file as a dataset.
Virtual datasets are created in the same file in the root level.
Virtual datasets are then linked in the NeXus file as external links by the writer.py.

"""
    hdf_source_file = h5py.File(my_source_file, 'w')
    single_array_data = hdf_source_file.create_group('single_array_data')
    single_array_data.create_dataset('ellips_data', data=my_numpy_array)
    # Ellipsometry-specific handling: search for number of incidence angles
    incidence_angles = h5py.File(my_source_file,
                                 'r')['/single_array_data/ellips_data'][:, 1]
    unique_angles, counts = np.unique(incidence_angles, return_counts=True)
    layout = h5py.VirtualLayout(shape=(counts[0],), dtype=np.float64)
    # Virtual datasets are created in the source file at the root level
    initial = 0
    wavelengthlist = []
    psilist = []
    deltalist = []
    for index, angle in enumerate(unique_angles):
        angle = int(angle)
        #
        vsource = h5py.VirtualSource(my_source_file,
                                     '/single_array_data/ellips_data',
                                     shape=(incidence_angles.shape[0], 6)
                                     )[initial:initial + counts[index], 2]
        layout[:] = vsource
        hdf_source_file.create_virtual_dataset(f"psi_{angle}deg", layout)
        psilist.append(f"psi_{angle}deg")
        #
        vsource = h5py.VirtualSource(my_source_file,
                                     '/single_array_data/ellips_data',
                                     shape=(incidence_angles.shape[0], 6)
                                     )[initial:initial + counts[index], 3]
        layout[:] = vsource
        hdf_source_file.create_virtual_dataset(f"delta_{angle}deg", layout)
        deltalist.append(f"delta_{angle}deg")
        #
        vsource = h5py.VirtualSource(my_source_file,
                                     '/single_array_data/ellips_data',
                                     shape=(incidence_angles.shape[0], 6)
                                     )[initial:initial + counts[index], 0]
        layout[:] = vsource
        hdf_source_file.create_virtual_dataset(f"wavelength_{angle}deg", layout)
        wavelengthlist.append(f"wavelength_{angle}deg")
        #
        initial += counts[index]
    return wavelengthlist, psilist, deltalist


class EllipsometryReader(BaseReader):
    """
        An example reader implementation for the DataConverter.
        Importing metadata from the yaml file based on the last
        two parts of the key in the application definition.
    """
    def __init__(self):
        self.default_header = DEFAULT_HEADER
        self.my_source_file = str(f"{os.path.dirname(__file__)}/../../../../../tests/"
                                  f"data/tools/dataconverter/readers/ellips/test.h5")

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXellipsometry"]

    def read_and_populate_template(self, file_paths, template):
        """This function is creating and populating the header dictionary reading the yaml file.

The template dictionary is then populated according to the content of header dictionary.
"""
        header = self.default_header
        for file_path in file_paths:
            if os.path.splitext(file_path)[1].lower() in [".yaml", ".yml"]:
                header = load_header(file_path, header)
                if "filename" not in header:
                    raise KeyError("filename is missing from", file_path)
                tempfile = os.path.join(os.path.split(file_path)[0], header["filename"])
        if os.path.isfile(tempfile):
            whole_data = load_as_array(tempfile, header)
        else:
            whole_data = load_as_array(header["filename"], header)
        # extrapolate only the "E" portion of data
        energy = whole_data['type'].astype(str).values.tolist().count("E")
        my_numpy_array = whole_data.to_numpy()[0:energy, 1:].astype("float64")
        del whole_data["type"]
        # measured_data is a required field
        header["measured_data"] = my_numpy_array
        for k in whole_data:
            header[k] = whole_data[k].to_numpy()[0:energy].astype("float64")
        if "calibration_filename" in header:
            calibration = load_as_array(header["calibration_filename"], header)
            for k in calibration:
                header[f"calibration_{k}"] = calibration[k]
        # For loop handling attributes from yaml to appdef:
        for k in template.keys():
            k_list = k.rsplit("/", 2)
            long_k = "/".join(k_list[-2:]) if len(k_list) > 2 else ""
            short_k = k_list[-1]
            if len(k_list) > 2 and long_k in header:
                template[k] = header.pop(long_k)
            elif short_k in header:
                template[k] = header.pop(short_k)
        return template, my_numpy_array

    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary.

Two handling of virtual datasets are implemented:

METHOD 1: virtual datasets are in the source file and they are linked via external link
(requires definition of virtual datasets via "virtual_dataset_generation").
It is usefull for particular slicings that are not accounted in method 2

METHOD 2: virtual dataset are created inside the NeXus file
(requires definition of the slices' shapes we want to pick from the whole dataset
via "slice_shape_definition").

"""
        if not file_paths:
            raise Exception("No input files were given to Ellipsometry Reader.")

        # The template is filled with default entries.
        template, my_numpy_array = self.read_and_populate_template(file_paths, template)

        # METHOD 1:
        wavelengthlist, psilist, deltalist = virtual_dataset_generation(self.my_source_file,
                                                                        my_numpy_array
                                                                        )
        for wavelength in wavelengthlist:
            template[f"/ENTRY[entry]/plot/{wavelength}"] = {"external_link": f"/{wavelength}",
                                                            "file_link": self.my_source_file
                                                            }
            template[f"/ENTRY[entry]/plot/{wavelength}/@units"] = "angstrom"
        for psi in psilist:
            template[f"/ENTRY[entry]/plot/{psi}"] = {"external_link": f"/{psi}",
                                                     "file_link": self.my_source_file
                                                     }
            template[f"/ENTRY[entry]/plot/{psi}/@units"] = "degrees"
        for delta in deltalist:
            template[f"/ENTRY[entry]/plot/{delta}"] = {"external_link": f"/{delta}",
                                                       "file_link": self.my_source_file
                                                       }
            template[f"/ENTRY[entry]/plot/{delta}/@units"] = "degrees"

        # METHOD 2:
        wavelengthlist, psilist, deltalist, interval_list = slice_shape_definition(my_numpy_array)
        for index, wavy in enumerate(wavelengthlist):
            template[f"/ENTRY[entry]/plot/{wavy}_test2"] = {"external_link":
                                                            f"/single_array_data/ellips_data",
                                                            "file_link":
                                                            self.my_source_file,
                                                            "slice_column":
                                                            [0],
                                                            "slice_row":
                                                            [interval_list[index],
                                                             interval_list[index + 1]
                                                             ]
                                                            }
            template[f"/ENTRY[entry]/plot/{wavy}_test2/@units"] = "degrees"
        for index, psi in enumerate(psilist):
            template[f"/ENTRY[entry]/plot/{psi}_test2"] = {"external_link":
                                                           f"/single_array_data/ellips_data",
                                                           "file_link":
                                                           self.my_source_file,
                                                           "slice_column":
                                                           [2],
                                                           "slice_row":
                                                           [interval_list[index],
                                                            interval_list[index + 1]
                                                            ]
                                                           }
            template[f"/ENTRY[entry]/plot/{psi}_test2/@units"] = "degrees"
        for index, delta in enumerate(deltalist):
            template[f"/ENTRY[entry]/plot/{delta}_test2"] = {"external_link":
                                                             f"/single_array_data/ellips_data",
                                                             "file_link":
                                                             self.my_source_file,
                                                             "slice_column":
                                                             [3],
                                                             "slice_row":
                                                             [interval_list[index],
                                                              interval_list[index + 1]
                                                              ]
                                                             }
            template[f"/ENTRY[entry]/plot/{delta}_test2/@units"] = "degrees"

        # Define default plot showing psi and delta at all angles:
        template["/@default"] = "entry"
        template["/ENTRY[entry]/@default"] = "plot"
        template["/ENTRY[entry]/plot/@signal"] = f"{psilist[0]}_test2"
        template["/ENTRY[entry]/plot/@axes"] = "wavelength_50deg_test2"
        if len(psilist) > 1:
            test_psi = [s + "_test2" for s in psilist[1:]]
            test_delta = [s + "_test2" for s in deltalist[1:]]
            template["/ENTRY[entry]/plot/@auxiliary_signals"] = test_psi + test_delta
        else:
            template["/ENTRY[entry]/plot/@auxiliary_signals"] = [s + "_test2" for s in deltalist]

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = EllipsometryReader
