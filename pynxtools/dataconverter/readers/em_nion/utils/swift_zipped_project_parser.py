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

from pynxtools.dataconverter.readers.em_nion.utils.swift_generate_dimscale_axes \
    import get_list_of_dimension_scale_axes

from pynxtools.dataconverter.readers.em_nion.map_concepts.swift_display_items_to_nx \
    import nexus_concept_dict, identify_nexus_concept_key

from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import apply_modifier, variadic_path_to_specific_path

from pynxtools.dataconverter.readers.em_nion.map_concepts.swift_to_nx_image_real_space \
    import NxImageRealSpaceDict

from pynxtools.dataconverter.readers.em_nion.utils.em_nion_versioning \
    import NX_EM_NION_SWIFT_NAME, NX_EM_NION_SWIFT_VERSION
from pynxtools.dataconverter.readers.em_nion.utils.em_nion_versioning \
    import NX_EM_NION_EXEC_NAME, NX_EM_NION_EXEC_VERSION


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
        self.event_data_written = False
        self.event_data_em_id = 1
        self.image_id = 1
        self.spectrum_id = 1
        self.proj_file_names = []
        # assure that there is exactly one *.nsproj file only to parse from
        self.ndata_file_dict = {}
        # just get the *.ndata files irrespective whether they will be parsed later
        self.hdf_file_dict = {}
        # just get the *.h5 files irrespective whether they will be interpreted

    def check_project_file(self):
        """Inspect the content of the compressed project file to check if supported."""
        # file_name = "2022-02-18_Metadata_Kuehbach.zip.nionswift"
        with ZipFile(self.file_name) as zip_file_hdl:
            for file in zip_file_hdl.namelist():
                if file.endswith(".h5"):
                    key = file[file.rfind("/") + 1:].replace(".h5", "")
                    if key not in self.hdf_file_dict:
                        self.hdf_file_dict[key] = file
                elif file.endswith(".ndata"):
                    key = file[file.rfind("/") + 1:].replace(".ndata", "")
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

    def add_nx_image_real_space(self, meta, arr, template):
        """Add data and metadata for an instance of concept NxImageRealSpace."""
        # metadata
        identifier = [self.entry_id, self.event_data_em_id, self.image_id]
        for nx_path, modifier in NxImageRealSpaceDict.items():
            if (nx_path != "IGNORE") and (nx_path != "UNCLEAR"):
                # print(nx_path)
                # instance_identifier = list(np.repeat(1, nx_path.count("*")))
                # print(instance_identifier)
                trg = variadic_path_to_specific_path(nx_path, identifier)
                # print(trg)
                template[trg] = apply_modifier(modifier, meta)

        # array data
        axes_lst = get_list_of_dimension_scale_axes(meta)
        # print(axes_lst)

        axes_names = [("axis_image_identifier", "image_identifier", 2),
                      ("axis_y", "y", 1),
                      ("axis_x", "x", 0)]
        print(f"Add NXdata len(axes_lst) {len(axes_lst)}, len(axes_names) {len(axes_names)}")
        if 2 <= len(axes_lst) <= len(axes_names):
            trg = f"/ENTRY[entry{self.entry_id}]/measurement/EVENT_DATA_EM[event_data_em" \
                  f"{self.event_data_em_id}]/IMAGE_SET[image_set{self.image_id}]/" \
                  f"PROCESS[process]"
            template[f"{trg}/source"] = "n/a"
            template[f"{trg}/source/@version"] = "n/a"
            template[f"{trg}/PROGRAM[program1]/program"] \
                = f"We do not know because the nsproj file does not store it explicitly "\
                  f"which nionswift version and dependencies are used when writing "\
                  f"the nsproj file!"
            template[f"{trg}/PROGRAM[program1]/program/@version"] = "not recoverable"
            template[f"{trg}/PROGRAM[program2]/program"] \
                = f"{NX_EM_NION_SWIFT_NAME}"
            template[f"{trg}/PROGRAM[program2]/program/@version"] \
                = f"{NX_EM_NION_SWIFT_VERSION}"
            template[f"{trg}/PROGRAM[program3]/program"] \
                = f"{NX_EM_NION_EXEC_NAME}"
            template[f"{trg}/PROGRAM[program3]/program/@version"] \
                = f"{NX_EM_NION_EXEC_VERSION}"

            trg = f"/ENTRY[entry{self.entry_id}]/measurement/EVENT_DATA_EM[event_data_em" \
                  f"{self.event_data_em_id}]/IMAGE_SET[image_set{self.image_id}]/DATA[stack]"
            template[f"{trg}/@NX_class"] = "NXdata"  # ##TODO one should not need to add this manually
            template[f"{trg}/title"] = str("Should come from NionSwift directly")
            template[f"{trg}/@signal"] = "data_counts"
            template[f"{trg}/@axes"] = ["axis_image_identifier", "axis_y", "axis_x"]
            for idx in np.arange(0, 3):
                template[f"{trg}/@AXISNAME_indices[{axes_names[idx][0]}_indices]"] \
                    = np.uint32(axes_names[idx][2])
            # the following three lines would be required by H5Web to plot RGB maps
            # template[f"{trg}/@CLASS"] = "IMAGE"
            # template[f"{trg}/@IMAGE_VERSION"] = "1.2"
            # template[f"{trg}/@SUBCLASS_VERSION"] = np.int64(15)

            if len(axes_lst) == 2:
                ny, nx = np.shape(arr)
                template[f"{trg}/data_counts"] \
                    = {"compress": np.reshape(arr, (1, ny, nx), order="C"), "strength": 1}
                template[f"{trg}/data_counts/@long_name"] = "Signal"
                # no image_identifier axis available
                template[f"{trg}/AXISNAME[{axes_names[0][0]}]"] \
                    = {"compress": np.asarray([1], np.uint32), "strength": 1}
                template[f"{trg}/AXISNAME[{axes_names[0][0]}]/@long_name"] \
                    = f"Image identifier (a. u.)"
                template[f"{trg}/AXISNAME[{axes_names[0][0]}]/@units"] = ""
                for idx in [1, 2]:
                    template[f"{trg}/AXISNAME[{axes_names[idx][0]}]"] \
                        = {"compress": axes_lst[idx - 1]["value"], "strength": 1}
                    template[f"{trg}/AXISNAME[{axes_names[idx][0]}]/@long_name"] \
                        = f"Calibrated position along {axes_names[idx][1]}-axis " \
                          f"({axes_lst[idx - 1]['unit']})"
                    template[f"{trg}/AXISNAME[{axes_names[idx][0]}]/@units"] \
                        = f"{axes_lst[idx - 1]['unit']}"
            else:  # len(axes_lst) == 3
                template[f"{trg}/data_counts"] = {"compress": arr, "strength": 1}
                for idx in [0, 1, 2]:
                    # TODO check that casting works properly
                    template[f"{trg}/AXISNAME[{axes_names[idx][0]}]"] \
                        = {"compress": np.asarray(axes_lst[idx]["value"], np.uint32),
                           "strength": 1}
                    template[f"{trg}/AXISNAME[{axes_names[idx][0]}]/@long_name"] \
                        = f"Calibrated position along {axes_names[idx][1]}-axis " \
                          f"({axes_lst[idx]['unit']})"
                    template[f"{trg}/AXISNAME[{axes_names[idx][0]}]/@units"] \
                        = f"{axes_lst[idx]['unit']}"

        self.image_id += 1
        self.event_data_written = True
        return template

    def update_event_identifier(self):
        """Advance and reset bookkeeping of event data em and data instances."""
        if self.event_data_written is True:
            self.event_data_em_id += 1
            self.event_data_written = False
        self.image_id = 1
        self.spectrum_id = 1
        # because either we found that the display item is fed from an H5 or from an NDATA
        # print(f"Identifier at {self.entry_id}, {self.event_data_em_id}, {self.image_id}, {self.spectrum_id}")

    def map_to_nexus(self, meta, arr, concept_name, template):
        """Create the actual instance of a specific set of NeXus concepts in template."""
        # meta is an flatdict
        # arr is a numpy array
        if concept_name == "NxImageSetRealSpace":
            print(f"Adding an instance of concept {concept_name}")
            self.add_nx_image_real_space(meta, arr, template)
        else:
            print(f"Ignoring concept {concept_name} because not yet implemented")

        self.update_event_identifier()
        return template

    def process_ndata(self, file_hdl, full_path, template):
        """Handle reading and processing of opened *.ndata inside the ZIP file."""
        # assure that we start reading that file_hdl/pointer from the beginning...
        file_hdl.seek(0)
        local_files, dir_files, eocd = nsnd.parse_zip(file_hdl)
        # ...now that pointer might point somewhere...
        flat_metadata_dict = {}
        data_arr = None
        nx_concept_name = ""

        for offset, tpl in local_files.items():
            # print(f"{tpl}")
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
            # print(f"{tpl}")
            if tpl[0] == b'data.npy':
                print(f"Extract data.npy from {full_path} at offset {offset}")
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

        self.map_to_nexus(flat_metadata_dict, data_arr, nx_concept_name, template)
        del flat_metadata_dict
        del data_arr
        del nx_concept_name
        return template

    def process_hdf(self, file_hdl, full_path, template):
        """Handle reading and processing of opened *.h5 inside the ZIP file."""
        flat_metadata_dict = {}
        data_arr = None
        nx_concept_name = ""

        file_hdl.seek(0)
        h5r = h5py.File(file_hdl, "r")
        metadata_dict = json.loads(h5r["data"].attrs["properties"])

        nx_concept_key = identify_nexus_concept_key(metadata_dict)
        nx_concept_name = nexus_concept_dict[nx_concept_key]
        print(f"Display_item {full_path}, concept {nx_concept_key}, maps {nx_concept_name}")

        flat_metadata_dict = fd.FlatDict(metadata_dict, delimiter='/')

        if flat_metadata_dict == {}:  # only continue if some metadata were retrieved
            return template

        data_arr = h5r["data"][()]
        h5r.close()

        print(f"data_arr type {data_arr.dtype}, shape {np.shape(data_arr)}")
        # check on the integriety of the data_arr array that it is not None or empty
        # this should be done more elegantly by just writing the
        # data directly into the template and not creating another copy
        self.map_to_nexus(flat_metadata_dict, data_arr, nx_concept_name, template)
        del flat_metadata_dict
        del data_arr
        del nx_concept_name
        return template

    def parse_project_file(self, template: dict) -> dict:
        """Parse lazily from compressed NionSwift project (nsproj + directory)."""
        swift_proj_dict = {}
        with ZipFile(self.file_name) as zip_file_hdl:
            with zip_file_hdl.open(self.proj_file_names[0]) as file_hdl:
                # with open(file_name, 'r') as stream:
                swift_proj_dict = fd.FlatDict(yaml.safe_load(file_hdl), delimiter='/')
                # for entry in swift_proj_dict["display_items"]:
                #     if isinstance(entry, dict):
                #         for key, val in entry.items():
                #             print(f"{key}, {val}")
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
