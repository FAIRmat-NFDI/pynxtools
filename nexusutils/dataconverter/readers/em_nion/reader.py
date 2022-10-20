#!/usr/bin/env python3
"""Nion/NionSwift EM reader."""

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

import re

import json

from typing import Tuple, Any

import numpy as np

from nexusutils.dataconverter.readers.base.reader import BaseReader

from nexusutils.dataconverter.readers.em_nion.utils.em_io_utils_misc \
    import recursive_query_nested_dict, assess_situation_with_input_files, NION_ERROR_CODES

from nexusutils.dataconverter.readers.em_nion.utils.em_io_utils_ods2dct \
    import ods_to_json_routing_dict

# each experiment on a given sample should be stored in an own file


def report_appdef_version(template: dict) -> dict:
    """Specify which application definition version is used."""
    template["/ENTRY[entry]/definition"] = "NXem_nion"
    template["/ENTRY[entry]/definition/@version"] = "1"

    return template


def extract_data_from_json_file(file_name: str, template: dict) -> dict:
    """Query those data which a NionSwift json file has."""
    # file_name = 'HAADF_01.json'
    print('Extracting data from NionSwift JSON file: ' + file_name)

    with open(file_name, 'r', encoding='utf-8') as infile:
        jsn = json.load(infile)

    json_to_nxdl_path = ods_to_json_routing_dict()

    # extract quantities
    for keyword, value in json_to_nxdl_path.items():
        assert isinstance(value, tuple), \
            'Keyword: ' + keyword + '\n' + 'Value is not a tuple!'
        assert len(value) == 2, \
            'Keyword: ' + keyword + '\n' + 'Value is not a duplett!'

        nxdl_path, nxdl_unit = value

        if nxdl_path in template.keys():
            tmp = recursive_query_nested_dict(keyword, jsn)

            assert tmp is not None, \
                'Keyword: ' + keyword + '\n' + 'Value is None!'
            template[nxdl_path] = tmp

        if nxdl_path + '/@units' in template.keys():
            template[nxdl_path + '/@units'] = nxdl_unit

    # extract quantities for which the nionswift json document
    # formats/distributes the pieces of information across multiple keywords,
    # so that to format them according to what the application definition,
    # it is required a hard coding for now
    # NEW ISSUE: discuss with nion for formatting alternatives
    # NEW ISSUE: write NXDL from within nionswift and append missing metadata

    # nionswift json does not explicitly report start_time, end_time and
    # preparation_time but gives a time stamp, according to the suggestion
    # how start_time should be used in such case we infer the time from
    # this nionswift time stamp
    date_time = recursive_query_nested_dict("datetime_original/local_datetime", jsn)
    time_zone = recursive_query_nested_dict("datetime_original/tz", jsn)
    tmp = re.compile(r"^(\+|-)(\d{2})00$")
    assert tmp.search(time_zone) is not None, \
        'nionswift time zone formatting ' + time_zone + ' is not valid!'

    template["/ENTRY[entry]/start_time"] \
        = value = date_time + time_zone[0:3] + ':' + time_zone[3:5]
    # NEW ISSUE:
    template["/ENTRY[entry]/end_time"] \
        = template["/ENTRY[entry]/start_time"]
    template["/ENTRY[entry]/SAMPLE[sample]/preparation_date"] \
        = template["/ENTRY[entry]/start_time"]

    # NEW ISSUE: this should better be stored with each image
    center_positions = recursive_query_nested_dict(
        "metadata/scan/scan_device_parameters/center_nm", jsn)
    assert isinstance(center_positions, list), \
        'Value for center positions is not a list!'
    assert center_positions != [], \
        'Value for center positions is an empty list!'
    assert len(center_positions) == 2, \
        'Value for center positions is not a duplett!'

    template["/ENTRY[entry]/em_lab/hadf/SCANBOX_EM[scanbox_em]/center"] \
        = np.asarray(center_positions, np.float64)
    template["/ENTRY[entry]/em_lab/hadf/SCANBOX_EM[scanbox_em]/center/@units"] \
        = "nm"
    # NEW ISSUE: center and their units is currently hardcoded
    # NEW ISSUE: nionswift json metadata document is inconsistent here

    positions = np.zeros((3,), np.float64)
    for axis in [0, 1, 2]:
        tmp = recursive_query_nested_dict(
            ["metadata/instrument/ImageScanned/StageOutX",
             "metadata/instrument/ImageScanned/StageOutY",
             "metadata/instrument/ImageScanned/StageOutZ"][axis], jsn)
        assert isinstance(tmp, float), 'Coordinate value is not a float!'
        positions[axis] = tmp
    template["/ENTRY[entry]/em_lab/STAGE_LAB[stage_lab]/position"] \
        = positions
    template["/ENTRY[entry]/em_lab/STAGE_LAB[stage_lab]/position/@units"] = "m"
    # NEW ISSUE: positions and their units are currently hardcoded

    # NEW ISSUE: probe_ha should better be stored only within each scan
    # and not in misc
    tmp = recursive_query_nested_dict("metadata/instrument/ImageScanned/probe_ha", jsn)
    template["/ENTRY[entry]/em_lab/miscellaneous/semi_convergence_angle"] \
        = tmp
    template["/ENTRY[entry]/em_lab/miscellaneous/semi_convergence_angle/@units"] \
        = "rad"

    return template


def extract_data_from_scans(
        npy_file_name: str, json_file_name: str,
        template: dict) -> dict:
    """Query those data which a NionSwift numpy file has.

    Add per scan metadata from json metadata file from nionswift.
    """
    # npy_file_name = 'HAADF_01.npy'
    # json_file_name = 'HAADF_01.json'
    print('Extracting data from NionSwift NPY file: ' + npy_file_name)

    # ##MK how will the numpy dump look like when there are multiple images?
    # ##MK how do images map to indices

    path_prefix = "/ENTRY[entry]/em_lab/hadf/DATA[data]/"

    template[path_prefix + "@axes"] = ["ypos", "xpos"]
    template[path_prefix + "@signal"] = "intensity"
    # here assuming h5py will encodes the str into an UTF-8
    template[path_prefix + "@ypos_indices"] = 0
    template[path_prefix + "@xpos_indices"] = 1

    npy = np.load(npy_file_name)
    template[path_prefix + "intensity"] = npy
    # NEW ISSUE: this needs to be disentangled for multiple scans

    with open(json_file_name, 'r', encoding='utf-8') as infile:
        jsn = json.load(infile)

    # NEW ISSUE: based on design for multiple scans reconstruct pixel
    # coordinates, currently hardcoded
    spatial_calibrations = recursive_query_nested_dict("spatial_calibrations", jsn)
    assert isinstance(spatial_calibrations, list), \
        'Value for spatial calibrations is not a list!'
    assert spatial_calibrations != [], \
        'Value for spatial calibrations is an empty list!'
    assert len(spatial_calibrations) == 2, \
        'Value for spatial calibrations is not a duplett!'

    center_positions = recursive_query_nested_dict(
        "metadata/scan/scan_device_parameters/center_nm", jsn)
    assert isinstance(center_positions, list), \
        'Value for center positions is not a list!'
    assert center_positions != [], \
        'Value for center positions is an empty list!'
    assert len(center_positions) == 2, \
        'Value for center positions is not a duplett!'

    scan_sizes = recursive_query_nested_dict(
        "metadata/scan/scan_device_parameters/size", jsn)
    assert isinstance(scan_sizes, list), \
        'Value for scan sizes is not a list!'
    assert scan_sizes != [], \
        'Value for scan sizes is an empty list!'
    assert len(scan_sizes) == 2, \
        'Value for scan sizes is not a duplett!'

    xmin = center_positions[0] + spatial_calibrations[0]['offset'] \
        + 0 * spatial_calibrations[0]['scale']
    xmax = center_positions[0] + spatial_calibrations[0]['offset'] \
        + scan_sizes[0] * spatial_calibrations[0]['scale']
    template[path_prefix + "xpos"] = np.linspace(
        xmin, xmax, scan_sizes[0], endpoint=True)
    template[path_prefix + "xpos/@units"] = "nm"

    ymin = center_positions[1] + spatial_calibrations[1]['offset'] \
        + 0 * spatial_calibrations[1]['scale']
    ymax = center_positions[1] + spatial_calibrations[1]['offset'] \
        + scan_sizes[1] * spatial_calibrations[1]['scale']
    template[path_prefix + "ypos"] = np.linspace(
        ymin, ymax, scan_sizes[1], endpoint=True)
    # NEW ISSUE: xpos/ypos units currently hardcoded, no explicit unit field

    template[path_prefix + "ypos/@units"] = "nm"
    template[path_prefix + "@long_name"] = "HADF image"

    return template


def extract_data_from_elabftw_file(file_name: str, template: dict) -> dict:
    """Query (meta)data from dumps of e.g. ELabFTW or lab-instrument configs."""
    # file_name = 'HAADF_01.ELabFTW.json'
    print('Extracting data from ELN/LIMS/others JSON file: ' + file_name)

    with open(file_name, 'r', encoding='utf-8') as infile:
        dct = json.load(infile)

    for nxdl_path, value in dct.items():
        if nxdl_path in template.keys():
            assert value is not None, \
                'Keyword: ' + nxdl_path + '\n' + 'Value is None!'
            template[nxdl_path] = value

    return template


class EmNionReader(BaseReader):
    """Parse content from community file formats.

    Specifically, of (transmission) electron microscopy from a Nion microscope
    to create a NXem_nion.nxdl-compliant NeXus file.

    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXem_nion"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Read data from given file, return filled template dictionary."""
        typed_files, case = assess_situation_with_input_files(file_paths)

        assert case != NION_ERROR_CODES[-1], \
            'Each nionswift record should have only one npy and json file!'

        report_appdef_version(template)

        print('Add metadata which come from other sources...')
        if 'json' in typed_files:
            assert len(typed_files['json']) == 1, \
                "List of json files is ambiguous!"

            extract_data_from_json_file(typed_files['json'][0], template)

        print('Add metadata/data from numpy array(s) representing scans...')
        if 'npy' in typed_files:
            assert len(typed_files['npy']) == 1, \
                "List of npy files is ambiguous!"
            assert len(typed_files['json']) == 1, \
                "List of json files is ambiguous!"

            extract_data_from_scans(
                typed_files['npy'][0],
                typed_files['json'][0],
                template)

        print('Add metadata from e.g.ELN/LIMS dump JSON files...')
        extract_data_from_elabftw_file(typed_files['dat'][0], template)

        # inspect the template for debugging purposes
        # for keyword, value in template.items():
        #     print('Keyword: ' + keyword + ' value: ' + str(value))

        # NEW ISSUE: add path to default plottable data
        template['/@default'] = "entry"
        template['/ENTRY[entry]/@default'] = "em_lab"
        template['/ENTRY[entry]/em_lab/@default'] = "hadf"
        template['/ENTRY[entry]/em_lab/hadf/@default'] = "data"

        return template


# This has to be set to allow the convert script to use this reader.
READER = EmNionReader
