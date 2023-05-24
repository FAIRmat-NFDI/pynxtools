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
"""Parse display_items inside a zip file generated from compressing a swift project dir."""

# pylint: disable=no-member

# from typing import Dict, Any, List, Tuple

import yaml

import json

import flatdict as fd

import nion.swift.model.NDataHandler as nsnd

import numpy as np

import h5py

from zipfile37 import ZipFile

from pynxtools.dataconverter.readers.em_nion.utils.swift_uuid_to_file_name \
    import uuid_to_file_name

from pynxtools.dataconverter.readers.em_nion.concepts.swift_display_items_to_nx_concepts \
    import nexus_concept_dict, identify_nexus_concept_key


class NxEmNionSwiftProjectParser:
    """Parse NionSwift project file.

    """

    def __init__(self, file_name, entry_id):
        """Class wrapping swift parser."""
        self.file_name = file_name
        self.entry_id = entry_id
        # counters which keep track of how many instances of NXevent_data_em have
        # been instantiated, this implementation currently maps each display_items
        # onto an own NXevent_data_em instance
        self.event_data_em_id = 1
        self.image_id = 1
        self.spectrum_id = 1
        self.proj_file_names = []
        # assure that there is exactly one *.nsproj file only to parse from
        self.ndata_file_dict = {}
        # just get the *.ndata files irrespective whether they will be parsed later
        self.hdf_file_dict = {}
        # just get the *.h5 files irrespective whether they will be interpreted

    def add_nx_image_real_space(self, flat_metadata, template: dict) -> dict:
        """Add data and metadata for an instance of concept NxImageRealSpace."""
        for key, val in flat_metadata.items():
            print (f"{key}, {val}")
        return template

    def check_project_file(self):
        """Inspect the content of the compressed project file to check if supported."""
        # file_name = "2022-02-18_Metadata_Kuehbach.zip.nionswift"
        with ZipFile(self.file_name) as zip_file_hdl:
            for file in zip_file_hdl.namelist():
                if file.endswith(".h5"):
                    key = file[file.rfind("/")+1:].replace(".h5", "")
                    if key not in self.hdf_file_dict:
                        self.hdf_file_dict[key] = file
                elif file.endswith(".ndata"):
                    key = file[file.rfind("/")+1:].replace(".ndata", "")
                    if key not in self.ndata_file_dict:
                        self.ndata_file_dict[key] = file
                elif file.endswith(".nsproj"):
                    self.proj_file_names.append(file)
                else:
                    continue
        if not self.ndata_file_dict.keys().isdisjoint(self.hdf_file_dict.keys()):
            print("Keys of *.ndata and *.h5 files in project are not disjoint!")
            return False
        if len(self.proj_file_names) != 1:
            print("The project contains either no or more than one nsproj file!")
            return False
        print(self.proj_file_names)
        for key, val in self.ndata_file_dict.items():
            print(f"{key}, {val}")
        for key, val in self.hdf_file_dict.items():
            print(f"{key}, {val}")
        return True

    def map_to_nexus(self, mdat, dat, full_path, nx_concept_name, template):
        print("Skipping actual processing of the mdat and dat")
        del mdat
        del dat
        return template

    def process_ndata(self, file_hdl, full_path, template):
        """Handle reading and processing of opened *.ndata inside the ZIP file."""
        # assure that we start reading that file_hdl/pointer from the beginning...
        file_hdl.seek(0)
        local_files, dir_files, eocd = nsnd.parse_zip(file_hdl)
        # ...now that pointer might point somewhere...
        flat_metadata_dict = {}
        data_arr = None

        for offset, tpl in local_files.items():
            print(f"{tpl}")
            if tpl[0] == b'metadata.json':
                print(f"Extract metadata.json from {full_path} at offset {offset}")
                # ... explicit jump back to beginning of the file
                file_hdl.seek(0)
                metadata_dict = nsnd.read_json(file_hdl,
                                               local_files,
                                               dir_files,
                                               b'metadata.json')

                nx_concept_key = identify_nexus_concept_key(metadata_dict)
                nx_concept_name = nexus_concept_dict[nx_concept_key]
                print(f"Display_item {full_path}, concept {nx_concept_key}, maps {nx_concept_name}")

                flat_metadata_dict = fd.FlatDict(metadata_dict, delimiter='/')
                break
                # because we expect (based on Benedikt's example) to find only one json file
                # in that *.ndata file pointed to by file_hdl

        if flat_metadata_dict == {}:  # only continue if some metadata were retrieved
            return template

        for offset, tpl in local_files.items():
            print(f"{tpl}")
            if tpl[0] == b'data.npy':
                file_hdl.seek(0)
                data_arr = nsnd.read_data(file_hdl,
                                          local_files,
                                          dir_files,
                                          b'data.npy')
                break
                # because we expect (based on Benedikt's example) to find only one npy file
                # in that *.ndata file pointed to by file_hdl

        print(f"data_arr type {data_arr.dtype}, shape {np.shape(data_arr)}")
        # check on the integriety of the data_arr array that it is not None or empty
        # this should be done more elegantly by just writing the
        # data directly into the template and not creating another copy

        self.map_to_nexus(flat_metadata_dict, data_arr,
                          full_path, nx_concept_name, template)
        return template

    def process_hdf(self, file_hdl, full_path, template):
        """Handle reading and processing of opened *.h5 inside the ZIP file."""
        flat_metadata_dict = {}
        data_arr = None

        file_hdl.seek(0)
        h5r = h5py.File(file_hdl, "r")
        metadata_dict = json.loads(h5r["data"].attrs["properties"])

        nx_concept_key = identify_nexus_concept_key(metadata_dict)
        nx_concept_name = nexus_concept_dict[nx_concept_key]
        print(f"Display_item {full_path}, concept {nx_concept_key}, maps {nx_concept_name}")

        flat_metadata_dict = fd.FlatDict(metadata_dict, delimiter='/')

        if flat_metadata_dict == {}:  # only continue if some metadata were retrieved
            return template

        data_arr = h5r["data"]
        # h5r.close()

        print(f"data_arr type {data_arr.dtype}, shape {np.shape(data_arr)}")
        # check on the integriety of the data_arr array that it is not None or empty
        # this should be done more elegantly by just writing the
        # data directly into the template and not creating another copy
        self.map_to_nexus(flat_metadata_dict, data_arr,
                          full_path, nx_concept_name, template)
        return template

    def parse_project_file(self, template: dict) -> dict:
        """Parse lazily from compressed NionSwift project (nsproj + directory)."""
        swift_proj_dict = {}
        with ZipFile(self.file_name) as zip_file_hdl:
            with zip_file_hdl.open(self.proj_file_names[0]) as file_hdl:
                # with open(file_name, 'r') as stream:
                swift_proj_dict = fd.FlatDict(yaml.safe_load(file_hdl), delimiter='/')
                for entry in swift_proj_dict["display_items"]:
                    if isinstance(entry, dict):
                        for key, val in entry.items():
                            print(f"{key}, {val}")
        if swift_proj_dict == {}:
            return template

        for itm in swift_proj_dict["display_items"]:
            if set(["type", "uuid", "created", "display_data_channels"]).issubset(itm.keys()):
                if len(itm["display_data_channels"]) == 1:
                    if "data_item_reference" in itm["display_data_channels"][0].keys():
                        key = uuid_to_file_name(
                            itm["display_data_channels"][0]["data_item_reference"])
                        # file_name without the mime type
                        if key in self.ndata_file_dict:
                            print(f"Key {key} is *.ndata maps to {self.ndata_file_dict[key]}")
                            with ZipFile(self.file_name) as zip_file_hdl:
                                print(f"Parsing {self.ndata_file_dict[key]}...")
                                with zip_file_hdl.open(self.ndata_file_dict[key]) as file_hdl:
                                    self.process_ndata(
                                        file_hdl,
                                        self.ndata_file_dict[key],
                                        template)
                        elif key in self.hdf_file_dict:
                            print(f"Key {key} is *.h5 maps to {self.hdf_file_dict[key]}")
                            with ZipFile(self.file_name) as zip_file_hdl:
                                print(f"Parsing {self.hdf_file_dict[key]}...")
                                with zip_file_hdl.open(self.hdf_file_dict[key]) as file_hdl:
                                    self.process_hdf(
                                        file_hdl,
                                        self.hdf_file_dict[key],
                                        template)
                        else:
                            print(f"Key {key} has no corresponding data file")
        return template

    def parse(self, template: dict) -> dict:
        """Parse NOMAD OASIS relevant data and metadata from swift project."""
        print("Parsing lazily from compressed NionSwift project (nsproj + directory)...")
        print(self.file_name)
        print(f"{self.entry_id}")
        if self.check_project_file() is False:
            return template

        self.parse_project_file(template)
        return template
