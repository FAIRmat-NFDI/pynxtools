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
"""Subparser for harmonizing ThermoFisher-specific content in TIFF files."""

import mmap
import numpy as np
from typing import Dict
from PIL import Image
from PIL.TiffTags import TAGS

from pynxtools.dataconverter.readers.em.subparsers.image_tiff import TiffSubParser
from pynxtools.dataconverter.readers.em.subparsers.image_tiff_tfs_concepts import \
    get_fei_parent_concepts, get_fei_childs
from pynxtools.dataconverter.readers.em.subparsers.image_tiff_tfs_cfg import \
    TIFF_TFS_TO_NEXUS_CFG
from pynxtools.dataconverter.readers.em.utils.image_utils import \
    sort_ascendingly_by_second_argument, if_str_represents_float
from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import variadic_path_to_specific_path
from pynxtools.dataconverter.readers.em.subparsers.image_tiff_tfs_modifier import \
    get_nexus_value


class TfsTiffSubParser(TiffSubParser):
    def __init__(self, file_path: str = "", entry_id: int = 1):
        super().__init__(file_path)
        self.entry_id = entry_id
        self.event_id = 1
        self.prfx = None
        self.tmp: Dict = {"data": None,
                          "meta": {}}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.tags: Dict = {}
        self.supported = False
        self.check_if_tiff()

    def check_if_tiff_tfs(self):
        """Check if resource behind self.file_path is a TaggedImageFormat file."""
        self.supported = 0  # voting-based
        with open(self.file_path, 'rb', 0) as file:
            s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            magic = s.read(4)
            if magic == b'II*\x00':  # https://en.wikipedia.org/wiki/TIFF
                self.supported += 1

        with Image.open(self.fiele_path, mode="r") as fp:
            tfs_keys = [34682]
            for tfs_key in tfs_keys:
                if tfs_key in fp.tag_v2:
                    if len(fp.tag[tfs_key]) == 1:
                        self.supported += 1  # found TFS-specific tag
        if self.supported == 2:
            self.supported = True
        else:
            self.supported = False

    def get_metadata(self):
        """Extract metadata in TFS specific tags if present."""
        print("Reporting the tags found in this TIFF file...")
        # for an overview of tags
        # https://www.loc.gov/preservation/digital/formats/content/tiff_tags.shtml
        # with Image.open(self.file_path, mode="r") as fp:
        #     self.tags = {TAGS[key] : fp.tag[key] for key in fp.tag_v2}
        #     for key, val in self.tags.items():
        #         print(f"{key}, {val}")
        tfs_parent_concepts = get_fei_parent_concepts()
        tfs_parent_concepts_byte_offset = {}
        for concept in tfs_parent_concepts:
            tfs_parent_concepts_byte_offset[concept] = None
        with open(self.file_path, 'rb', 0) as fp:
            s = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)
            for concept in tfs_parent_concepts:
                pos = s.find(bytes(f"[{concept}]", "utf8"))  # != -1
                if pos != -1:
                    tfs_parent_concepts_byte_offset[concept] = pos
                else:
                    print(f"Instance of concept [{concept}] was not found !")
            print(tfs_parent_concepts_byte_offset)

            sequence = []  # decide I/O order in which metadata for childs of parent concepts will be read
            for key, value in tfs_parent_concepts_byte_offset.items():
                if value is not None:
                    sequence.append((key, value))
                    # tuple of parent_concept name and byte offset
            sequence = sort_ascendingly_by_second_argument(sequence)
            print(sequence)

            idx = 0
            for parent, byte_offset in sequence:
                pos_s = byte_offset
                pos_e = None
                if idx < len(sequence) - 1:
                    pos_e = sequence[idx + 1][1]
                else:
                    pos_e = np.iinfo(np.uint64).max
                    # TODO::better use official convention to not read beyond the end of file
                idx += 1
                if pos_s is None or pos_e is None:
                    raise ValueError(f"Definition of byte boundaries for reading childs of [{parent}] was unsuccessful !")
                # print(f"Search for [{parent}] in between byte offsets {pos_s} and {pos_e}")

                # fish metadata of e.g. the system section
                for term in get_fei_childs(parent):
                    s.seek(pos_s, 0)
                    pos = s.find(bytes(f"{term}=", "utf8"))
                    if pos < pos_e:  # check if pos_e is None
                        s.seek(pos, 0)
                        value = f"{s.readline().strip().decode('utf8').replace(f'{term}=', '')}"
                        self.tmp["meta"][f"{parent}/{term}"] = None
                        if isinstance(value, str):
                            if value != "":
                                # execution order of the check here matters!
                                if value.isdigit() is True:
                                    self.tmp["meta"][f"{parent}/{term}"] = np.int64(value)
                                elif if_str_represents_float(value) is True:
                                    self.tmp["meta"][f"{parent}/{term}"] = np.float64(value)
                                else:
                                    self.tmp["meta"][f"{parent}/{term}"] = value
                        else:
                            raise ValueError(f"Detected an unexpected case {parent}/{term}, type: {type(value)} !")
                    else:
                        pass

    def parse_and_normalize(self):
        """Perform actual parsing filling cache self.tmp."""
        if self.supported is True:
            print(f"Parsing via ThermoFisher-specific metadata...")
            self.get_metadata()
            # for key in self.tmp["meta"].keys():
            #     print(f"{key}")
        else:
            print(f"{self.file_path} is not a ThermoFisher-specific "
                  f"TIFF file that this parser can process !")

    def process_into_template(self, template: dict) -> dict:
        if self.supported is True:
            self.process_event_data_em_metadata(template)
            self.process_event_data_em_data(template)
        return template

    def process_event_data_em_data(self, template: dict) -> dict:
        """Add respective heavy data."""
        # default display of the image(s) representing the data collected in this event
        print(f"Writing TFS/FEI TIFF image as a onto the respective NeXus concept")
        # read image in-place
        with Image.open(self.file_path, mode="r") as fp:
            nparr = np.array(fp)
            # print(f"type: {type(nparr)}, dtype: {nparr.dtype}, shape: {np.shape(nparr)}")
            # TODO::discussion points
            # - how do you know we have an image of real space vs. imaginary space (from the metadata?)
            # - how do deal with the (ugly) scale bar that is typically stamped into the TIFF image content?
            # with H5Web and NeXus most of this is obsolete unless there are metadata stamped which are not
            # available in NeXus or in the respective metadata in the metadata section of the TIFF image
            # remember H5Web images can be scaled based on the metadata allowing basically the same
            # explorative viewing using H5Web than what traditionally typical image viewers are meant for
            image_identifier = 1
            trg = f"/ENTRY[entry{self.entry_id}]/measurement/EVENT_DATA_EM_SET[event_data_em_set]/" \
                  f"EVENT_DATA_EM[event_data_em{self.event_id}]/" \
                  f"IMAGE_R_SET[image_r_set{image_identifier}]/DATA[image]"
            # TODO::writer should decorate automatically!
            template[f"{trg}/title"] = f"Image"
            template[f"{trg}/@NX_class"] = f"NXdata"  # TODO::writer should decorate automatically!
            template[f"{trg}/@signal"] = "intensity"
            dims = ["x", "y"]
            idx = 0
            for dim in dims:
                template[f"{trg}/@AXISNAME_indices[axis_{dim}_indices]"] = np.uint32(idx)
                idx += 1
            template[f"{trg}/@axes"] = []
            for dim in dims[::-1]:
                template[f"{trg}/@axes"].append(f"axis_{dim}")
            template[f"{trg}/intensity"] = {"compress": np.array(fp), "strength": 1}
            #  0 is y while 1 is x for 2d, 0 is z, 1 is y, while 2 is x for 3d
            template[f"{trg}/intensity/@long_name"] = f"Signal"

            sxy = {"x": 1., "y": 1.}
            scan_unit = {"x": "m", "y": "m"}  # assuming FEI reports SI units
            # we may face the CCD overview camera for the chamber for which there might not be a calibration!
            if ("EScan/PixelWidth" in self.tmp["meta"].keys()) and ("EScan/PixelHeight" in self.tmp["meta"].keys()):
                sxy = {"x": self.tmp["meta"]["EScan/PixelWidth"],
                       "y": self.tmp["meta"]["EScan/PixelHeight"]}
                scan_unit = {"x": "px", "y": "px"}
            nxy = {"x": np.shape(np.array(fp))[1], "y": np.shape(np.array(fp))[0]}
            # TODO::be careful we assume here a very specific coordinate system
            # however the TIFF file gives no clue, TIFF just documents in which order
            # it arranges a bunch of pixels that have stream in into a n-d tiling
            # e.g. a 2D image
            # also we have to be careful because TFS just gives us here
            # typical case of an image without an information without its location
            # on the physical sample surface, therefore we can only scale
            # pixel_identifier by physical scaling quantities s_x, s_y
            # also the dimensions of the image are on us to fish with the image
            # reading library instead of TFS for consistency checks adding these
            # to the metadata the reason is that TFS TIFF use the TIFF tagging mechanism
            # and there is already a proper TIFF tag for the width and height of an
            # image in number of pixel
            for dim in dims:
                template[f"{trg}/AXISNAME[axis_{dim}]"] \
                    = {"compress": np.asarray(np.linspace(0,
                                                          nxy[dim] - 1,
                                                          num=nxy[dim],
                                                          endpoint=True) * sxy[dim], np.float64), "strength": 1}
                template[f"{trg}/AXISNAME[axis_{dim}]/@long_name"] \
                    = f"Coordinate along {dim}-axis ({scan_unit[dim]})"
                template[f"{trg}/AXISNAME[axis_{dim}]/@units"] = f"{scan_unit[dim]}"
        return template

    def process_event_data_em_metadata(self, template: dict) -> dict:
        """Add respective metadata."""
        # contextualization to understand how the image relates to the EM session
        print(f"Mapping some of the TFS/FEI metadata concepts onto NeXus concepts")
        identifier = [self.entry_id, self.event_id, 1]
        for tpl in TIFF_TFS_TO_NEXUS_CFG:
            if isinstance(tpl, tuple):
                trg = variadic_path_to_specific_path(tpl[0], identifier)
                if len(tpl) == 2:
                    template[trg] = tpl[1]
                if len(tpl) == 3:
                    # nxpath, modifier, value to load from and eventually to be modified
                    retval = get_nexus_value(tpl[1], tpl[2], self.tmp["meta"])
                    if retval is not None:
                        template[trg] = retval
        return template
