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
from typing import Tuple, Any
import yaml
import pandas as pd
import numpy as np
# import h5py
from nexusutils.dataconverter.readers.base.reader import BaseReader

DEFAULT_HEADER = {'sep': '\t', 'skip': 0}


def load_header(filename, default):
    """ load the yaml description file, and apply defaults from
        the defalut dict for all keys not found from the file.

        Parameters:
            filename:           a yaml file containing the definitions
            default_header:     predefined default values

        Returns:
            a dict containing the loaded information
    """
    with open(filename, 'rt', encoding='utf8') as file:
        header = yaml.safe_load(file)

    clean_header = {}
    for key, val in header.items():
        if "\\@" in key:
            clean_header[key.replace("\\@", "@")] = val
        elif key == 'sep':
            clean_header[key] = val.encode("utf-8").decode("unicode_escape")
        elif isinstance(val, dict):
            clean_header[key] = val.get('value')
            clean_header[f'{key}/@units'] = val.get('unit')
        else:
            clean_header[key] = val

    for key, value in default.items():
        if key not in clean_header:
            clean_header[key] = value
    return clean_header


def load_as_pandas_array(my_file, header):
    """ Load a CSV output file using the header dict.
        Use the fields: colnames, skip and sep from the header
        to instruct the csv reader about:
        colnames    -- column names
        skip        -- how many lines to skip
        sep         -- separator character in the file

        Parameters:
            my_file  string, file name
            header   dict header read from a yaml file

        Returns:
            A pandas array is returned.
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


def populate_header_dict(file_paths):
    """ This function creates and populates the header dictionary
        reading one or more yaml file.

        Parameters:
            file_paths  a list of file paths to be read

        Returns:
            a dict merging the content of all files
    """

    header = DEFAULT_HEADER

    for file_path in file_paths:
        if os.path.splitext(file_path)[1].lower() in [".yaml", ".yml"]:
            header = load_header(file_path, header)
            if "filename" not in header:
                raise KeyError("filename is missing from", file_path)
            data_file = os.path.join(os.path.split(file_path)[0], header["filename"])

            # if the path is not right, try the path provided directly
            if not os.path.isfile(data_file):
                data_file = header["filename"]

    return header, data_file


def populate_template_dict(header, template):
    """The template dictionary is then populated according to the content of header dictionary.

    """

    if "calibration_filename" in header:
        calibration = load_as_pandas_array(header["calibration_filename"], header)
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
    return template


class EllipsometryReader(BaseReader):
    """An example reader implementation for the DataConverter.

Importing metadata from the yaml file based on the last
two parts of the key in the application definition.
"""

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXellipsometry"]

    @staticmethod
    def populate_header_dict_with_datasets(file_paths):
        """This is an ellipsometry-specific processing of data.

    The procedure is the following:
    - the header dictionary is initialized reading a yaml file
    - the data are read from header["filename"] and saved in a pandas object
    - an array is shaped according to application definition in a 5D array (numpy array)
    - the array is saved in a HDF5 file as a dataset
    - virtual datasets instances are created in the header dictionary,
      referencing to data in the created HDF5 file.
    - the header is finally returned, ready to be parsed in the final template dictionary

    """
        header, data_file = populate_header_dict(file_paths)

        if os.path.isfile(data_file):
            whole_data = load_as_pandas_array(data_file, header)
        else:
            # this we have tried, we should throw an error...
            whole_data = load_as_pandas_array(header["filename"], header)

        # User defined variables to produce slices of the whole data set
        energy = whole_data['type'].astype(str).values.tolist().count("E")
        unique_angles, counts = np.unique(whole_data["angle_of_incidence"
                                                     ].to_numpy()[0:energy].astype("int64"),
                                          return_counts=True
                                          )
        labels = {"psi": [], "delta": []}
        block_idx = [np.int64(0)]
        index = 0
        for angle in enumerate(unique_angles):
            labels["psi"].append(f"psi_{int(angle[1])}deg")
            labels["delta"].append(f"delta_{int(angle[1])}deg")
            index += counts[angle[0]]
            block_idx.append(index)

        # array that will be allocated in a HDF5 file
        # counts[0] = N_wavelents*N_time*N_p1
        my_numpy_array = np.empty([1,
                                   1,
                                   len(unique_angles),
                                   len(['psi', 'delta']),
                                   counts[0]
                                   ])

        for index, unique_angle in enumerate(unique_angles):
            my_numpy_array[0,
                           0,
                           index,
                           :,
                           :] = unique_angle

        for index in range(len(labels["psi"])):
            my_numpy_array[0,
                           0,
                           index,
                           0,
                           :] = whole_data["psi"].to_numpy()[block_idx[index]:block_idx[index + 1]
                                                             ].astype("float64")

        for index in range(len(labels["delta"])):
            my_numpy_array[0,
                           0,
                           index,
                           1,
                           :] = whole_data["delta"].to_numpy()[block_idx[index]:block_idx[index + 1]
                                                               ].astype("float64")

        # measured_data is a required field
        header["measured_data"] = my_numpy_array
        header["spectrometer/wavelength"] = (
            whole_data["wavelength"].to_numpy()[0:counts[0]].astype("float64")
        )
        header["angle_of_incidence"] = unique_angles
        return header, labels["psi"], labels["delta"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """ Reads data from given file and returns a filled template dictionary.

            A handlings of virtual datasets is implemented:

            virtual dataset are created inside the final NeXus file.

            The template entry is filled with a dictionary containing the following keys:
            - link: the path of the external data file and the path of desired dataset inside it
            - shape: numpy array slice object (according to array slice notation)
        """

        if not file_paths:
            raise Exception("No input files were given to Ellipsometry Reader.")

        # The header dictionary is filled with entries.
        header, psilist, deltalist = (
            EllipsometryReader.populate_header_dict_with_datasets(file_paths)
        )

        # The template dictionary is filled
        template = populate_template_dict(header, template)

        template["/ENTRY[entry]/plot/wavelength"] = {"link":
                                                     "/entry/instrument/spectrometer/wavelength"
                                                     }
        template["/ENTRY[entry]/plot/wavelength/@units"] = "angstrom"

        for index, psi in enumerate(psilist):
            template[f"/ENTRY[entry]/plot/{psi}"] = {"link":
                                                     "/entry/sample/measured_data",
                                                     "shape":
                                                     np.index_exp[0, 0, index, 0, :]
                                                     }
            template[f"/ENTRY[entry]/plot/{psi}/@units"] = "degrees"

        for index, delta in enumerate(deltalist):
            template[f"/ENTRY[entry]/plot/{delta}"] = {"link":
                                                       "/entry/sample/measured_data",
                                                       "shape":
                                                       np.index_exp[0, 0, index, 1, :]
                                                       }
            template[f"/ENTRY[entry]/plot/{delta}/@units"] = "degrees"

        # Define default plot showing psi and delta at all angles:
        template["/@default"] = "entry"
        template["/ENTRY[entry]/@default"] = "plot"
        template["/ENTRY[entry]/plot/@signal"] = f"{psilist[0]}"
        template["/ENTRY[entry]/plot/@axes"] = "wavelength"
        if len(psilist) > 1:
            template["/ENTRY[entry]/plot/@auxiliary_signals"] = psilist[1:] + deltalist
        else:
            template["/ENTRY[entry]/plot/@auxiliary_signals"] = deltalist

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = EllipsometryReader
