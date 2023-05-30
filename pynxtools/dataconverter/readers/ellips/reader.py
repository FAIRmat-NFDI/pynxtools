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
from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.ellips.mock import MockEllips
from pynxtools.dataconverter.helpers import extract_atom_types
from pynxtools.dataconverter.readers.utils import flatten_and_replace, FlattenSettings

DEFAULT_HEADER = {'sep': '\t', 'skip': 0}


CONVERT_DICT = {
    'angle_of_incidence': 'INSTRUMENT[instrument]/angle_of_incidence',
    'angle_of_incidence/@units': 'INSTRUMENT[instrument]/angle_of_incidence/@units',
    'angular_spread':
        'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/focussing_probes/angular_spread',
    'angular_spread/@units':
        'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/focussing_probes/angular_spread/@units',
    'atom_types': 'SAMPLE[sample]/atom_types',
    'backside_roughness': 'SAMPLE[sample]/backside_roughness',
    'calibration_status': 'INSTRUMENT[instrument]/calibration_status',
    'chemical_formula': 'SAMPLE[sample]/chemical_formula',
    'column_names': 'data_collection/column_names',
    'company': 'INSTRUMENT[instrument]/company',
    'count_time': 'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/DETECTOR[detector]/count_time',
    'count_time/@units':
        'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/DETECTOR[detector]/count_time/@units',
    'data_correction':
        'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/focussing_probes/data_correction',
    'data_error': 'data_collection/data_error',
    'data_identifier': 'data_collection/data_identifier',
    'data_software/@url': 'data_collection/data_software/@url',
    'data_software/program': 'data_collection/data_software/program',
    'data_software/version': 'data_collection/data_software/version',
    'data_type': 'data_collection/data_type',
    'depends_on': 'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/depends_on',
    'depolarization': 'derived_parameters/depolarization',
    'detector_type':
        'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/DETECTOR[detector]/detector_type',
    'ellipsometer_type': 'INSTRUMENT[instrument]/ellipsometer_type',
    'layer_structure': 'SAMPLE[sample]/layer_structure',
    'light_source': 'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/light_source',
    'medium': 'INSTRUMENT[instrument]/sample_stage/environment_conditions/medium',
    'measured_data': 'data_collection/measured_data',
    'model': 'INSTRUMENT[instrument]/model',
    'model/@version': 'INSTRUMENT[instrument]/model/@version',
    'real_time': 'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/DETECTOR[detector]/real_time',
    'revolutions': 'INSTRUMENT[instrument]/BEAM_PATH[beam_path]/rotating_element/revolutions',
    'rotating_element_type': 'INSTRUMENT[instrument]/rotating_element_type',
    'sample_history': 'SAMPLE[sample]/sample_history',
    'sample_name': 'SAMPLE[sample]/sample_name',
    'sample_type': 'SAMPLE[sample]/sample_type',
    'software/@url': 'INSTRUMENT[instrument]/software/@url',
    'software/program': 'INSTRUMENT[instrument]/software/program',
    'software/version': 'INSTRUMENT[instrument]/software/version',
    'stage_type': 'INSTRUMENT[instrument]/sample_stage/stage_type',
    'substrate': 'SAMPLE[sample]/substrate',
}

CONFIG_KEYS = [
    'blocks',
    'colnames',
    'derived_parameter_type',
    'err-var',
    'filename',
    'parameters',
    'plot_name',
    'sep',
    'skip',
    'spectrum_type',
    'spectrum_unit'
]

REPLACE_NESTED = {
    # 'SOURCE[source]/Probe': 'SOURCE[source]',
    # 'SOURCE[source]/Pump': 'SOURCE[source_pump]',
    # 'BEAM[beam]/Probe': 'BEAM[beam]',
    # 'BEAM[beam]/Pump': 'BEAM[beam_pump]',
}


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

    eln_data_dict = flatten_and_replace(
        FlattenSettings(
            dic=header,
            convert_dict=CONVERT_DICT,
            replace_nested=REPLACE_NESTED,
            black_list=CONFIG_KEYS
        )
    )
    template.update(eln_data_dict)

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


def header_labels(header, unique_angles):
    """ Define data labels (column names)

    """

    if header["data_type"] == "Psi/Delta":
        labels = {"Psi": [], "Delta": []}
    elif header["data_type"] == "tan(Psi)/cos(Delta)":
        labels = {"tan(Psi)": [], "cos(Delta)": []}
    else:
        labels = {}
        for i in range(1, 5):
            for j in range(1, 5):
                labels.update({f"m{i}{j}": []})

    for angle in enumerate(unique_angles):
        for key, val in labels.items():
            val.append(f"{key}_{int(angle[1])}deg")

    return labels


def mock_function(header):
    """ Mock ellipsometry data

    """

    mock_header = MockEllips(header)
    mock_header.mock_template(header)

    # Defining labels:
    mock_angles = header["angle_of_incidence"]

    labels = header_labels(header, mock_angles)

    for angle in enumerate(header["angle_of_incidence"]):
        for key, val in labels.items():
            val.append(f"{key}_{int(angle[1])}deg")

    # Atom types: Convert str to list if atom_types is not a list:
    # if isinstance(header["atom_types"], str):
    #     header["atom_types"] = header["atom_types"].split(",")

    # header["column_names"] = list(labels.keys())

    return header, labels


def data_set_dims(whole_data):
    """ User defined variables to produce slices of the whole data set

    """
    energy = whole_data['type'].astype(str).values.tolist().count("E")
    unique_angles, counts = np.unique(whole_data["angle_of_incidence"
                                                 ].to_numpy()[0:energy].astype("int64"),
                                      return_counts=True
                                      )

    return unique_angles, counts


class EllipsometryReader(BaseReader):
    """An example reader implementation for the DataConverter.
    Importing metadata from the yaml file based on the last
    two parts of the key in the application definition.
    """

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXellipsometry"]

    @staticmethod
    def populate_header_dict_with_datasets(file_paths, is_mock=False):
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

        # read first N lines of the data file:
        # with open(data_file) as input_file:
        #     file_header = [next(input_file) for _ in range(header["skip"])]

        if os.path.isfile(data_file):
            whole_data = load_as_pandas_array(data_file, header)
        else:
            # this we have tried, we should throw an error...
            whole_data = load_as_pandas_array(header["filename"], header)

        unique_angles, counts = data_set_dims(whole_data)

        labels = header_labels(header, unique_angles)

        block_idx = [np.int64(0)]
        index = 0
        while index < len(whole_data):
            index += counts[0]
            block_idx.append(index)

        # array that will be allocated in a HDF5 file
        my_numpy_array = np.empty([
            len(unique_angles),
            len(labels),
            counts[0]
        ])
        my_error_array = np.empty([
            len(unique_angles),
            len(labels),
            counts[0]
        ])
        derived_params = np.empty([
            len(unique_angles),
            1,
            counts[0]
        ])

        for index, angle in enumerate(unique_angles):
            my_numpy_array[
                index,
                :,
                :] = angle

        data_index = 0
        for key, val in labels.items():
            for index in range(len(val)):
                my_numpy_array[
                    index,
                    data_index,
                    :] = whole_data[key].to_numpy()[block_idx[index]:block_idx[index + 1]
                                                    ].astype("float64")
            data_index += 1

        data_index = 0
        for key, val in labels.items():
            for index in range(len(val)):
                my_error_array[
                    index,
                    data_index,
                    :] = whole_data[f"err.{key}"].to_numpy()[
                        block_idx[index]:block_idx[index + 1]].astype("float64")
            data_index += 1

        # derived parameters:
        # takes last but one column from the right (skips empty columns):
        # data_index = 1
        # temp = whole_data[header["colnames"][-data_index]].to_numpy()[
        #     block_idx[0]].astype("float64")
        # while temp * 0 != 0:
        #     temp = whole_data[header["colnames"][-data_index]].to_numpy()[
        #         block_idx[0]].astype("float64")
        #     data_index += 1

        for index in range(len(unique_angles)):
            derived_params[
                index,
                0,
                :] = whole_data[header["colnames"][3]].to_numpy()[
                    block_idx[index + 6]:block_idx[index + 7]].astype("float64")

        # measured_data is a required field
        header["measured_data"] = my_numpy_array
        # data_error and depolarization_values are optional
        header["data_error"] = my_error_array
        header[header["derived_parameter_type"]] = derived_params

        spectrum_type = header["spectrum_type"]
        if spectrum_type not in header["colnames"]:
            print("ERROR: spectrum type not found in 'colnames'")
        header[f"data_collection/NAME_spectrum[{spectrum_type}_spectrum]"] = (
            whole_data[spectrum_type].to_numpy()[0:counts[0]].astype("float64"))

        header["angle_of_incidence"] = unique_angles

        # Create mocked ellipsometry data template:
        if is_mock:
            header, labels = mock_function(header)

        if "atom_types" not in header:
            header["atom_types"] = extract_atom_types(header["chemical_formula"])
        # Atom types: Convert str to list if atom_types is not a list:
        # if isinstance(header["atom_types"], str):
        #     header["atom_types"] = header["atom_types"].split(",")

        # header["column_names"] = list(labels.keys())

        return header, labels

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None,
             is_mock: bool = False) -> dict:
        """ Reads data from given file and returns a filled template dictionary.

            A handlings of virtual datasets is implemented:

            virtual dataset are created inside the final NeXus file.

            The template entry is filled with a dictionary containing the following keys:
            - link: the path of the external data file and the path of desired dataset inside it
            - shape: numpy array slice object (according to array slice notation)
        """

        if not file_paths:
            raise IOError("No input files were given to Ellipsometry Reader.")

        # The header dictionary is filled with entries.
        header, labels = (
            EllipsometryReader.populate_header_dict_with_datasets(file_paths, is_mock)
        )

        data_list = []
        for val in labels.values():
            data_list.append(val)

        # The template dictionary is filled
        template = populate_template_dict(header, template)

        spectrum_type = header["spectrum_type"]
        spectrum_unit = header["spectrum_unit"]
        template[f"/ENTRY[entry]/plot/AXISNAME[{spectrum_type}]"] = \
            {"link": f"/entry/data_collection/{spectrum_type}_spectrum"}
        # template[f"/ENTRY[entry]/data_collection/DATA[data]/AXISNAME[{spectrum_type}]"] = \
        #     {"link": f"/entry/data_collection/{spectrum_type}_spectrum"}
        template[f"/ENTRY[entry]/data_collection/NAME_spectrum[{spectrum_type}_spectrum]/@units"] \
            = spectrum_unit
        template[
            f"/ENTRY[entry]/data_collection/NAME_spectrum[{spectrum_type}_spectrum]/@long_name"
        ] = f"{spectrum_type} ({spectrum_unit})"
        plot_name = header["plot_name"]
        for dindx in range(0, len(labels.keys())):
            for index, key in enumerate(data_list[dindx]):
                template[f"/ENTRY[entry]/plot/DATA[{key}]"] = \
                    {
                        "link": "/entry/data_collection/measured_data",
                        "shape": np.index_exp[index, dindx, :]
                }
                template[f"/ENTRY[entry]/plot/DATA[{key}]/@units"] = "degrees"
                if dindx == 0 and index == 0:
                    template[f"/ENTRY[entry]/plot/DATA[{key}]/@long_name"] = \
                        f"{plot_name} (degrees)"
                template[f"/ENTRY[entry]/plot/DATA[{key}_errors]"] = \
                    {
                        "link": "/entry/data_collection/data_error",
                        "shape": np.index_exp[index, dindx, :]
                }
                template[f"/ENTRY[entry]/plot/DATA[{key}_errors]/@units"] = "degrees"

        # Define default plot showing Psi and Delta at all angles:
        template["/@default"] = "entry"
        template["/ENTRY[entry]/@default"] = "plot"
        template["/ENTRY[entry]/plot/@signal"] = f"{data_list[0][0]}"
        template["/ENTRY[entry]/plot/@axes"] = spectrum_type
        template["/ENTRY[entry]/plot/title"] = plot_name

        # if len(data_list[0]) > 1:
        template["/ENTRY[entry]/plot/@auxiliary_signals"] = data_list[0][1:]
        for index in range(1, len(data_list)):
            template["/ENTRY[entry]/plot/@auxiliary_signals"] += data_list[index]

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = EllipsometryReader
