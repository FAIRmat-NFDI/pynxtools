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
"""Subparser for exemplar reading of raw PNG files collected on a TEM with Protochip heating_chip."""

import mmap
import re
import numpy as np
import xmltodict
from typing import Dict
from PIL import Image
from zipfile import ZipFile

from pynxtools.dataconverter.readers.em.subparsers.image_png_protochips_concepts import \
    get_protochips_variadic_concept
from pynxtools.dataconverter.readers.em.subparsers.image_png_protochips_cfg import \
    PNG_PROTOCHIPS_TO_NEXUS_CFG
from pynxtools.dataconverter.readers.shared.map_concepts.mapping_functors \
    import variadic_path_to_specific_path
from pynxtools.dataconverter.readers.em.subparsers.image_png_protochips_modifier import \
    get_nexus_value
from pynxtools.dataconverter.readers.em.subparsers.image_base import ImgsBaseParser
from pynxtools.dataconverter.readers.em.utils.xml_utils import flatten_xml_to_dict
from pynxtools.dataconverter.readers.shared.shared_utils import get_sha256_of_file_content


class ProtochipsPngSetSubParser(ImgsBaseParser):
    def __init__(self, file_path: str = "", entry_id: int = 1):
        super().__init__(file_path)
        self.entry_id = entry_id
        self.event_id = 1
        self.prfx = None
        self.tmp: Dict = {"data": None,
                          "meta": {}}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.png_info: Dict = {}
        self.supported = False
        self.check_if_zipped_png_protochips()

    def check_if_zipped_png_protochips(self):
        """Check if resource behind self.file_path is a TaggedImageFormat file."""
        # all tests have to be passed before the input self.file_path
        # can at all be processed with this parser
        # test 1: check if file is a zipfile
        with open(self.file_path, 'rb', 0) as file:
            s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            magic = s.read(8)
            if magic != b'PK\x03\x04\x14\x00\x08\x00':  # https://en.wikipedia.org/wiki/List_of_file_signatures
                print(f"Test 1 failed, {self.file_path} is not a ZIP archive !")
                return
        # test 2: check if there are at all PNG files with iTXt metadata from Protochips in this zip file
        # collect all those PNGs to work with and write a tuple of their image dimensions
        with ZipFile(self.file_path) as zip_file_hdl:
            for file in zip_file_hdl.namelist():
                if file.lower().endswith(".png") is True:
                    with zip_file_hdl.open(file) as fp:
                        magic = fp.read(8)
                        if magic == b'\x89PNG\r\n\x1a\n':
                            method = "smart"  # "lazy"
                            # get image dimensions
                            if method == "lazy":  # lazy but paid with the price of reading the image content
                                fp.seek(0)  # seek back to beginning of file required because fp.read advanced fp implicitly!
                                with Image.open(fp) as png:
                                    try:
                                        nparr = np.array(png)
                                        self.png_info[file] = np.shape(nparr)
                                    except IOError:
                                        print(f"Loading image data in-place from {self.file_path}:{file} failed !")
                            if method == "smart":  # knowing where to hunt width and height in PNG metadata
                                # https://dev.exiv2.org/projects/exiv2/wiki/The_Metadata_in_PNG_files
                                magic = fp.read(8)
                                self.png_info[file] = (np.frombuffer(fp.read(4), dtype=">i4"),
                                                       np.frombuffer(fp.read(4), dtype=">i4"))

        # test 3: check there are some PNGs
        if len(self.png_info.keys()) == 0:
            print("Test 3 failed, there are no PNGs !")
            return
        # test 4: check that all PNGs have the same dimensions, TODO::could check for other things here
        target_dims = None
        for file_name, tpl in self.png_info.items():
            if target_dims is not None:
                if tpl == target_dims:
                    continue
                else:
                    print("Test 4 failed, not all PNGs have the same dimensions")
                    return
            else:
                target_dims = tpl
        print("All tests passed successfully")
        self.supported = True

    def get_xml_metadata(self, file, fp):
        try:
            fp.seek(0)
            with Image.open(fp) as png:
                png.load()
                if "MicroscopeControlImage" in png.info.keys():
                    meta = flatten_xml_to_dict(
                        xmltodict.parse(png.info["MicroscopeControlImage"]))
                    # first phase analyse the collection of Protochips metadata concept instance symbols and reduce to unique concepts
                    grpnm_lookup = {}
                    for concept, value in meta.items():
                        # not every key is allowed to define a concept
                        # print(f"{concept}: {value}")
                        idxs = re.finditer(r".\[[0-9]+\].", concept)
                        if (sum(1 for _ in idxs) > 0):  # is_variadic
                            markers = [".Name", ".PositionerName"]
                            for marker in markers:
                                if concept.endswith(marker):
                                    grpnm_lookup[f"{concept[0:len(concept)-len(marker)]}"] = value
                        else:
                            grpnm_lookup[concept] = value
                    # second phase, evaluate each concept instance symbol wrt to its prefix coming from the unique concept
                    self.tmp["meta"][file] = {}
                    for k, v in meta.items():
                        grpnms = None
                        idxs = re.finditer(r".\[[0-9]+\].", k)
                        if (sum(1 for _ in idxs) > 0):  # is variadic
                            search_argument = k[0:k.rfind("].") + 1]
                            for parent_grpnm, child_grpnm in grpnm_lookup.items():
                                if parent_grpnm.startswith(search_argument):
                                    grpnms = (parent_grpnm, child_grpnm)
                                    break
                            if grpnms is not None:
                                if len(grpnms) == 2:
                                    if "PositionerSettings" in k and k.endswith(".PositionerName") is False:
                                        self.tmp["meta"][file][f"{grpnms[0]}.{grpnms[1]}{k[k.rfind('.') + 1:]}"] = v
                                    if k.endswith(".Value"):
                                        self.tmp["meta"][file][f"{grpnms[0]}.{grpnms[1]}"] = v
                        else:
                            self.tmp["meta"][file][f"{k}"] = v
                        # TODO::simplify and check that metadata end up correctly in self.tmp["meta"][file]
        except ValueError:
            print(f"Flattening XML metadata content {self.file_path}:{file} failed !")

    def get_file_hash(self, file, fp):
        self.tmp["meta"][file]["sha256"] = get_sha256_of_file_content(fp)

    def parse_and_normalize(self):
        """Perform actual parsing filling cache self.tmp."""
        if self.supported is True:
            print(f"Parsing via Protochips-specific metadata...")
            # may need to set self.supported = False on error
            with ZipFile(self.file_path) as zip_file_hdl:
                for file in self.png_info.keys():
                    with zip_file_hdl.open(file) as fp:
                        self.get_xml_metadata(file, fp)
                        self.get_file_hash(file, fp)
                        # print(f"Debugging self.tmp.file.items {file}")
                        # for k, v in self.tmp["meta"][file].items():
                        #    print(f"{k}: {v}")
            print(f"{self.file_path} metadata within PNG collection processed "
                  f"successfully ({len(self.tmp['meta'].keys())} PNGs evaluated).")
        else:
            print(f"{self.file_path} is not a Protochips-specific "
                  f"PNG file that this parser can process !")

    def process_into_template(self, template: dict) -> dict:
        if self.supported is True:
            self.process_event_data_em_metadata(template)
            # self.process_event_data_em_data(template)
        return template

    def process_event_data_em_metadata(self, template: dict) -> dict:
        """Add respective metadata."""
        # contextualization to understand how the image relates to the EM session
        print(f"Mapping some of the Protochips-specific metadata on respective NeXus concept instance")
        identifier = [self.entry_id, self.event_id, 1]
        for tpl in PNG_PROTOCHIPS_TO_NEXUS_CFG:
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

    def process_event_data_em_data(self, template: dict) -> dict:
        """Add respective heavy data."""
        # default display of the image(s) representing the data collected in this event
        print(f"Writing Protochips PNG image into a respective NeXus concept instance")
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
