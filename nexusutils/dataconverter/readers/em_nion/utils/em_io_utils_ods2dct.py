#!/usr/bin/env python3
"""Utility to create metadata/data routing table dictionary from spreadsheet."""

# -*- coding: utf-8 -*-
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

# pylint: disable=E1101

# import json

import os
from typing import Dict, Any

import pandas as pd

import numpy as np

# create a json dictionary with all those entries of the NXDL
# for which the metadata/data can not be extracted from files but
# need to be specified by other means (e.g. human, control software,
# external databases)

ROUTING_TABLE_FILE = 'NionSwiftJsonToNexusTranslationTable.ods'


def ods_to_json_routing_dict() -> dict:  # file_name: str) -> dict:
    """Parse LibreCalc/Excel table into dictionary.

    The dictionary how a path in a JSON document should be stored in a
    specific field in NeXus. The keyword of the dictionary is the flattened
    path in the JSON document, the value argument is a tuple of the path
    in NeXus and the specific SI/UniData unit that is to be used.
    """
    prefix = os.getcwd()
    prefix += "/readers/em_nion/utils/"
    print('Loading: ' + ROUTING_TABLE_FILE + ' from...')
    print(prefix)
    # no prefixing for jupyter-lab assuming datasets are in /
    prefix = ''
    tmp = pd.read_excel(prefix + ROUTING_TABLE_FILE,
                        sheet_name='JsonToNeXusRoutingTable',
                        engine="odf",
                        skiprows=7,
                        keep_default_na=False, na_values=['_'])

    dct: Dict[Any, Any] = {}

    for rowidx in np.arange(0, tmp.shape[0]):
        json_path = tmp.iloc[rowidx, 0]
        nxdl_path = tmp.iloc[rowidx, 1]
        nxdl_unit = tmp.iloc[rowidx, 2]
        status = tmp.iloc[rowidx, 3]

        assert status in [0, 1, 2, 3, 4, 5], \
            print("nxdl_use is not 0 or 1!")

        if status in [1, 3] and nxdl_path != 'None':
            assert json_path not in dct.keys(), \
                print(f'{json_path} has already been added to routing table!')

            dct[json_path] = (nxdl_path, nxdl_unit)

    return dct

    # NEW ISSUE: in case it is desirable to export the dictionary to a json file
    # with open(file_name + '.json', 'w', encoding='utf-8') \
    #         as file_handle:
    #     json.dump(dct, file_handle, ensure_ascii=False, indent=4)

# testing
# routing_table = ods_to_json_routing_dict()
