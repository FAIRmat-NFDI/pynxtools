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
from typing import Tuple

import h5py
import pyaml as yaml
import os
import pandas as pd

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader

default_header = {'sep': '\t', 'skip': 0}


def load_header(filename, default=default_header):
    """ load the yaml description file, and apply defaults as well
        Parameters:
        filename:           a yaml file containing the definitions
        default_header:     predefined default values
    """
    with open(filename, 'rt') as fp:
        header = yaml.yaml.safe_load(fp)

    for k in header:
        if "@" in k:
            header[k.replace("\@","@")] = header.pop(k)

    for k, v in default.items():
        if k not in header:
            header[k] = v

    return header
# end load_header


def load_as_blocks(fn, header):
    """ load a CSV output file using the header dict
    """
    required_parameters = ("colnames", "skip", "sep")
    for required_parameter in required_parameters:
        if required_parameter not in header:
            raise ValueError('colnames, skip and sep are required header parameters!')

    if not os.path.isfile(fn):
        raise IOError(f'File not found error: {fn}')

    data = pd.read_csv(fn,
                       # use header = None and names to define custom column names
                       header=None,
                       names=header['colnames'],
                       skiprows=header['skip'],
                       delimiter=header['sep'])

    # if our table has a block structure, we hav to
    # handle it in a special way
    dt = data.to_numpy()
    keylist = []
    res = {}
    if 'blocks' in header:
        for head in header['blocks']:
            indx = data.columns == head
            icol = indx.nonzero()[0][0]
            searcharray = dt.take(icol, axis=len(dt.shape) - 1)
            dt = dt.compress(~indx, axis=len(dt.shape) - 1)
            while (len(searcharray.shape) > 1):
                searcharray = searcharray.take(0, axis=0)

            bkeys = data[head].unique()
            lens = [(searcharray == i).sum() for i in bkeys]
            data = data.drop(head, axis=1)

            if (lens == lens[0]).all():
                newshape = list(dt.shape)
                # dt.shape = (lens[0], int(dt.shape[0]/lens[0]), dt.shape[1])
                i = newshape.index(max(newshape))
                newshape[i] = lens[0]
                newshape.insert(i, int(dt.shape[i] / lens[0]))
                dt.shape = tuple(newshape)
                # dt.shape = (int(dt.shape[0]/lens[0]), lens[0], dt.shape[1])
                keylist.append(bkeys)
                res[head] = bkeys

    res['data'] = dt.astype("f")
    res['keys'] = keylist
    if "wavelength" in data.columns:
        i = (data.columns == "wavelength").nonzero()[0][0]
        searcharray = dt.take(i, axis=len(dt.shape) - 1)
        while (len(searcharray.shape) > 1):
            searcharray = searcharray.take(0, axis=0)
        res["wavelength"] = searcharray
    return res
# end of load_as_blocks


def load_as_array(fn, header):
    """ load a CSV output file using the header dict
    """
    required_parameters = ("colnames", "skip", "sep")
    for required_parameter in required_parameters:
        if required_parameter not in header:
            raise ValueError('colnames, skip and sep are required header parameters!')

    if not os.path.isfile(fn):
        raise IOError(f'File not found error: {fn}')

    whole_data = pd.read_csv(fn,
                             # use header = None and names to define custom column names
                             header=None,
                             names=header['colnames'],
                             skiprows=header['skip'],
                             delimiter=header['sep'])

    # if our table has a block structure, we hav to
    # handle it in a special way
    dt_header = whole_data['type'].astype(str).values.tolist()
    energy = dt_header.count("E")
    dt = whole_data.to_numpy()[0:energy, 1:].astype("float64")
    return dt

class EllipsometryReader(BaseReader):
    """
        An example reader implementation for the DataConverter.
        Importing metadata from the yaml file based on the last
        two parts of the key in the application definition.
    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXellipsometry"]

    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""

        if not file_paths:
            raise Exception("No input files were given to Ellipsometry Reader.")

        header = default_header
        for file_path in file_paths:
            file_extension = os.path.splitext(file_path)[1]
            if file_extension.lower() in [".yaml", ".yml"]:
                header = load_header(file_path, header)

        if "filename" not in header:
            raise KeyError("filename is missing")

        tempfile = os.path.join(os.path.split(file_path)[0], header["filename"])
        if os.path.isfile(tempfile):
            tempdata = load_as_blocks(tempfile, header)
            my_tempdata = load_as_array(tempfile, header)
        else:
            tempdata = load_as_blocks(header["filename"], header)
            my_tempdata = load_as_array(header["filename"], header)

        header["measured_data"] = tempdata["data"]
        data_to_plot = tempdata["data"]
        del tempdata["keys"]
        del tempdata["data"]
        for k in tempdata:
            header[k] = tempdata[k]
        if "calibration_filename" in header:
            calibration = load_as_blocks(header["calibration_filename"], header)
            for k in calibration:
                header[f"calibration_{k}"] = calibration[k]
        dk = ["filename", "skip", "sep", "blocks", "colnames", "x-var", "y-var", "type"]

        for k in dk:
            if k in header:
                del header[k]

        # return_data = {}
        # for k in template.keys():
        #     if "@units" in k:
        #         continue
        #     short_k = k.rsplit("/", 1)[1]
        #     k_units = f"{k}/@units"
        #     if short_k in header:
        #         if k_units in template:
        #             if isinstance(header[short_k], str) and " " in header[short_k]:
        #                 val = header.pop(short_k).rsplit(" ", 1)
        #                 return_data[k_units] = val[-1]
        #                 return_data[k] = val[0]
        #                 sys.stdout.write("val0", val[0], type(val[0]), short_k)
        #                 with open('/home/carola/NOMAD/nomad2/testlog.txt', "w") as file:
        #                     #file.write("val0", val[0], type(val[0]), short_k)
        #                     file.write("val0")
        #                 try:
        #                     return_data[k] = float(val[0])
        #                 except ValueError:
        #                     pass
        #             else:
        #                 # we did not find unit but we assigned a value
        #                 return_data[k] = header.pop(short_k)
        #         else:
        #             return_data[k] = header.pop(short_k)
            # The entries in the template dict should correspond with what the dataconverter
            # outputs with --generate-template for a provided NXDL file
            # field_name = k[k.rfind("/") + 1:]
            # if field_name[0] != "@":
            #     template[k] = data[field_name]
            #     if f"{field_name}_units" in data.keys() and f"{k}/@units" in template.keys():


        ## For loop handling attributes from yaml to appdef:
        for k in template.keys():
            k_list = k.rsplit("/", 2)
            long_k = "/".join(k_list[-2:]) if len(k_list) > 2 else ""
            short_k = k_list[-1]
            if len(k_list) > 2 and long_k in header:
                template[k] = header.pop(long_k)
            elif short_k in header:
                template[k] = header.pop(short_k)

        # Because plot fields do not exist in template,
        # we check for the keys which contain plot in the header
        for k in header.keys():
            if k[0:4] != "plot":
                continue
            tk = f"/ENTRY[entry]/{k}"
            template[tk] = header[k]

        wave_length = data_to_plot[0, 0, :, 0]

        # Wavelength should be of type float. Pandas sends it back as Python object aka dtype('O')
        template["/ENTRY[entry]/SAMPLE[sample]/wavelength"] = template["/ENTRY[entry]/SAMPLE[sample]/wavelength"].astype("float64")

        # psi and delta for plots:
        psilist=[]
        deltalist=[]
        for k in range(data_to_plot.shape[1]):
            this_k = f"psi ({int(tempdata['angle_of_incidence'][k])}deg)" if "angle_of_incidence" in tempdata else f"psi{k}"
            template[f"/ENTRY[entry]/plot/{this_k}"] = data_to_plot[0, k, :, 1]
            psilist.append(this_k)
            this_k = f"delta ({int(tempdata['angle_of_incidence'][k])}deg)" if "angle_of_incidence" in tempdata else f"delta{k}"
            template[f"/ENTRY[entry]/plot/{this_k}"] = data_to_plot[0, k, :, 2]
            deltalist.append(this_k)

        # Define default plot showing psi and delta at all angles:
        template["/@default"] = "entry"
        template["/ENTRY[entry]/@default"] = "plot"
        template["/ENTRY[entry]/plot/@signal"] = psilist[0]
        if len(psilist) > 1:
            template["/ENTRY[entry]/plot/@auxiliary_signals"] = psilist[1:]+deltalist
        else:
            template["/ENTRY[entry]/plot/@auxiliary_signals"] = deltalist

        template["/ENTRY[entry]/plot/wavelength"] = wave_length
        template["/ENTRY[entry]/plot/@axes"] = "wavelength"

        template[f"/ENTRY[entry]/plot/psi/@units"] = "degrees"
        for k in range(data_to_plot.shape[1]):
            template[f"/ENTRY[entry]/plot/{psilist[k]}/@units"] = "degrees"
            template[f"/ENTRY[entry]/plot/{deltalist[k]}/@units"] = "degrees"

        my_source_path = str(f"{os.path.dirname(__file__)}/../../../../../tests/"
                             f"data/tools/dataconverter/readers/ellips")
        test_h5_file = h5py.File(f"{my_source_path}/test.h5", 'w')
        test_h5_file.create_dataset('my_test_vds', data=my_tempdata)
        my_raw_array = {"technique": "ellipsometry",
                        "raw_dataset": test_h5_file,
                        "path": f"{my_source_path}/test.h5"}
        template["/ENTRY[entry]/plot/whole_dataset"] = my_raw_array

        # for k in template:
        #     if "@" in k:
        #         print(k, template[k])

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = EllipsometryReader
