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
"""(Sub-)parser for reading content from ThermoFisher Velox *.emd (HDF5) via rosettasciio."""

import flatdict as fd
import numpy as np

from typing import Dict, List
from rsciio import emd
from ase.data import chemical_symbols

from pynxtools.dataconverter.readers.em.subparsers.rsciio_base import RsciioBaseParser
from pynxtools.dataconverter.readers.em.utils.rsciio_hyperspy_utils \
    import get_named_axis, get_axes_dims, get_axes_units
from pynxtools.dataconverter.readers.shared.shared_utils \
    import get_sha256_of_file_content

REAL_SPACE = 0
COMPLEX_SPACE = 1


class RsciioVeloxSubParser(RsciioBaseParser):
    """Read Velox EMD File Format emd."""
    def __init__(self, entry_id: int = 1, file_path: str = ""):
        super().__init__(file_path)
        if entry_id > 0:
            self.entry_id = entry_id
        else:
            self.entry_id = 1
        self.id_mgn: Dict = {"event": 1,
                             "event_img": 1,
                             "event_spc": 1,
                             "roi": 1,
                             "eds_img": 1}
        self.file_path_sha256 = None
        self.tmp: Dict = {}
        self.supported_version: Dict = {}
        self.version: Dict = {}
        self.supported = False
        self.check_if_supported()

    def check_if_supported(self):
        try:
            self.objs = emd.file_reader(self.file_path)
            # TODO::what to do if the content of the file is larger than the available
            # main memory, one approach to handle this is to have the file_reader parsing
            # only the collection of the concepts without the actual instance data
            # based on this one could then plan how much memory has to be reserved
            # in the template and stream out accordingly
            with open(self.file_path, "rb", 0) as fp:
                self.file_path_sha256 = get_sha256_of_file_content(fp)

            print(f"Parsing {self.file_path} with SHA256 {self.file_path_sha256} ...")
            self.supported = True
        except IOError:
            print(f"Loading {self.file_path} using {self.__name__} is not supported !")

    def parse(self, template: dict, verbose=False) -> dict:
        """Perform actual parsing filling cache self.tmp."""
        if self.supported is True:
            self.tech_partner_to_nexus_normalization(template)
        else:
            print(f"{self.file_path} is not a Velox-specific "
                  f"EMD file that this parser can process !")
        return template

    def tech_partner_to_nexus_normalization(self, template: dict) -> dict:
        """Translate tech partner concepts to NeXus concepts."""
        reqs = ["data", "axes", "metadata", "original_metadata", "mapping"]
        for idx, obj in enumerate(self.objs):
            if not isinstance(obj, dict):
                continue
            parse = True
            for req in reqs:
                if req not in obj:
                    parse = False
            if parse is False:
                continue

            content_type = self.content_resolver(obj)
            print(f"Parsing {idx}-th object in {self.file_path} content type is {content_type}")
            print(f"dims: {obj['axes']}")
            if content_type == "imgs":
                self.normalize_imgs_content(obj, template)  # generic imaging modes
                # TODO:: could later make an own one for bright/dark field, but
                # currently no distinction in hyperspy
            elif content_type == "adf":
                self.normalize_adf_content(obj, template)  # (high-angle) annular dark field
            elif content_type == "diff":  # diffraction image in reciprocal space
                self.normalize_diff_content(obj, template)  # diffraction images
            elif content_type == "eds_map":
                self.normalize_eds_map_content(obj, template)  # ED(X)S in the TEM
            elif content_type == "eds_spc":
                self.normalize_eds_spc_content(obj, template)  # EDS spectrum/(a)
            elif content_type == "eels":
                self.normalize_eels_content(obj, template)  # electron energy loss spectroscopy
            else:  # == "n/a"
                print(f"WARNING::Unable to resolve content of {idx}-th object in {self.file_path}!")
        return template

    def content_resolver(self, obj: dict) -> str:
        """Try to identify which content the obj describes best."""
        # assume rosettasciio-specific formatting of the emd parser
        # i.e. a dictionary with the following keys:
        # "data", "axes", "metadata", "original_metadata", "mapping"
        meta = fd.FlatDict(obj["metadata"], "/")
        # orgmeta = fd.FlatDict(obj["original_metadata"], "/")
        dims = get_axes_dims(obj["axes"])
        units = get_axes_units(obj["axes"])

        if "General/title" not in meta.keys():
            return "n/a"

        if (meta["General/title"] in ("BF")) or (meta["General/title"].startswith("DF")):
            uniq = set()
            for dim in dims:
                uniq.add(dim[0])
            # TODO::the problem with using here the explicit name DF4 is that this may only
            # work for a particular microscope:
            # Core/MetadataDefinitionVersion: 7.9, Core/MetadataSchemaVersion: v1/2013/07
            # Instrument/ControlSoftwareVersion: 1.15.4, Instrument/Manufacturer: FEI Company
            # Instrument/InstrumentId: 6338, Instrument/InstrumentModel: Talos F200X
            # instead there should be a logic added which resolves which concept
            # the data in this obj are best described by when asking a community-wide
            # glossary but not the FEI-specific glossary
            # all that logic is unneeded and thereby the data more interoperable
            # if FEI would harmonize their obvious company metadata standard with the
            # electron microscopy community!
            if sorted(uniq) == ["x", "y"]:
                return "imgs"

        if meta["General/title"] in ("HAADF"):
            return "adf"

        # all units indicating we are in real or complex i.e. reciprocal space
        if meta["General/title"] in ("EDS"):
            return "eds_spc"
            # applies to multiple cases, sum spectrum, spectrum stack etc.

        for symbol in chemical_symbols[1::]:  # an eds_map
            # TODO::does rosettasciio via hyperspy identify the symbol or is the
            # title by default already in Velox set (by default) to the chemical symbol?
            if meta["General/title"] != symbol:
                continue
            return "eds_map"

        vote_r_c = [0, 0]  # real space, complex space
        for unit in units:
            if unit.lower().replace(" ", "") \
                    in ["m", "cm", "mm", "µm", "nm", "pm"]:
                vote_r_c[REAL_SPACE] += 1
            if unit.lower().replace(" ", "") \
                    in ["1/m", "1/cm", "1/mm", "1/µm", "1/nm", "1/pm"]:
                vote_r_c[COMPLEX_SPACE] += 1

        if (vote_r_c[0] == len(units)) and (vote_r_c[1] == 0):
            return "imgs"
        if (vote_r_c[0] == 0) and (vote_r_c[1] == len(units)):
            return "diff"

        return "n/a"

    def normalize_imgs_content(self, obj: dict, template: dict) -> dict:
        """Map generic scanned images (e.g. BF/DF) to NeXus."""
        meta = fd.FlatDict(obj["metadata"], "/")
        dims = get_axes_dims(obj["axes"])
        if len(dims) != 2:
            raise ValueError(f"{obj['axes']}")
        trg = f"/ENTRY[entry{self.entry_id}]/measurement/event_data_em_set/" \
              f"EVENT_DATA_EM[event_data_em{self.id_mgn['event']}]/" \
              f"IMAGE_R_SET[image_r_set{self.id_mgn['event_img']}]"
        template[f"{trg}/PROCESS[process]/source/type"] = "file"
        template[f"{trg}/PROCESS[process]/source/path"] = self.file_path
        template[f"{trg}/PROCESS[process]/source/checksum"] = self.file_path_sha256
        template[f"{trg}/PROCESS[process]/source/algorithm"] = "SHA256"
        template[f"{trg}/PROCESS[process]/detector_identifier"] = meta["General/title"]
        template[f"{trg}/image_twod/@NX_class"] = "NXdata"  # TODO::writer should do!
        template[f"{trg}/image_twod/@signal"] = "intensity"
        template[f"{trg}/image_twod/@axes"] = []
        for dim in dims:
            template[f"{trg}/image_twod/@axes"].append(f"axis_{dim[0]}")
            template[f"{trg}/image_twod/@AXISNAME_indices[axis_{dim[0]}]"] \
                = np.uint32(dim[1])
            support, unit = get_named_axis(obj["axes"], dim[0])
            if support is not None and unit is not None:
                template[f"{trg}/image_twod/axis_{dim[0]}"] \
                    = {"compress": support, "strength": 1}
                template[f"{trg}/image_twod/axis_{dim[0]}/@long_name"] \
                    = f"{dim[0]}-axis position ({unit})"
        template[f"{trg}/image_twod/title"] = meta["General/title"]
        template[f"{trg}/image_twod/intensity"] \
            = {"compress": np.asarray(obj["data"]), "strength": 1}
        # template[f"{trg}/image_twod/intensity/@units"]
        # TODO::add metadata
        self.id_mgn["event_img"] += 1
        self.id_mgn["event"] += 1
        return template

    def normalize_adf_content(self, obj: dict, template: dict) -> dict:
        """Map relevant (high-angle) annular dark field images to NeXus."""
        meta = fd.FlatDict(obj["metadata"], "/")
        dims = get_axes_dims(obj["axes"])
        if len(dims) != 2:
            raise ValueError(f"{obj['axes']}")
        trg = f"/ENTRY[entry{self.entry_id}]/measurement/event_data_em_set/" \
              f"EVENT_DATA_EM[event_data_em{self.id_mgn['event']}]/" \
              f"IMAGE_R_SET[image_r_set{self.id_mgn['event_img']}]"
        template[f"{trg}/PROCESS[process]/source/type"] = "file"
        template[f"{trg}/PROCESS[process]/source/path"] = self.file_path
        template[f"{trg}/PROCESS[process]/source/checksum"] = self.file_path_sha256
        template[f"{trg}/PROCESS[process]/source/algorithm"] = "SHA256"
        template[f"{trg}/PROCESS[process]/detector_identifier"] = meta["General/title"]
        template[f"{trg}/image_twod/@NX_class"] = "NXdata"  # TODO::writer should do!
        template[f"{trg}/image_twod/@signal"] = "intensity"
        template[f"{trg}/image_twod/@axes"] = []
        for dim in dims:
            template[f"{trg}/image_twod/@axes"].append(f"axis_{dim[0]}")
            template[f"{trg}/image_twod/@AXISNAME_indices[axis_{dim[0]}]"] \
                = np.uint32(dim[1])
            support, unit = get_named_axis(obj["axes"], dim[0])
            if support is not None and unit is not None:
                template[f"{trg}/image_twod/axis_{dim[0]}"] \
                    = {"compress": support, "strength": 1}
                template[f"{trg}/image_twod/axis_{dim[0]}/@long_name"] \
                    = f"{dim[0]}-axis position ({unit})"
        template[f"{trg}/image_twod/title"] = meta["General/title"]
        template[f"{trg}/image_twod/intensity"] \
            = {"compress": np.asarray(obj["data"]), "strength": 1}
        # template[f"{trg}/image_twod/intensity/@units"]
        # TODO::coll. angles given in original_metadata map to half_angle_interval
        # TODO::add metadata
        self.id_mgn["event_img"] += 1
        self.id_mgn["event"] += 1
        return template

    def normalize_diff_content(self, obj: dict, template: dict) -> dict:
        """Map relevant diffraction images to NeXus."""
        # TODO::the above-mentioned constraint is not general enough
        # this can work only for cases where we know that we not only have a
        # Ceta camera but also use it for taking diffraction pattern
        # TODO::this is an example that more logic is needed to identify whether
        # the information inside obj really has a similarity with the concept of
        # somebody having taken a diffraction image
        # one can compare the situation with the following:
        # assume you wish to take pictures of apples and have an NXapple_picture
        # but all you get is an image from a digital camera where the dataset is
        # named maybe DCIM, without a logic one cannot make the mapping robustly!
        # can one map y, x, on j, i indices
        idx_map = {"y": "j", "x": "i"}
        meta = fd.FlatDict(obj["metadata"], "/")
        dims = get_axes_dims(obj["axes"])
        if len(dims) != 2:
            raise ValueError(f"{obj['axes']}")
        for dim in dims:
            if dim[0] not in idx_map.keys():
                raise ValueError(f"Unable to map index {dim[0]} on something!")

        trg = f"/ENTRY[entry{self.entry_id}]/measurement/event_data_em_set/" \
              f"EVENT_DATA_EM[event_data_em{self.id_mgn['event']}]/" \
              f"IMAGE_C_SET[image_c_set{self.id_mgn['event_img']}]"
        template[f"{trg}/PROCESS[process]/source/type"] = "file"
        template[f"{trg}/PROCESS[process]/source/path"] = self.file_path
        template[f"{trg}/PROCESS[process]/source/checksum"] = self.file_path_sha256
        template[f"{trg}/PROCESS[process]/source/algorithm"] = "SHA256"
        template[f"{trg}/PROCESS[process]/detector_identifier"] = meta["General/title"]
        template[f"{trg}/image_twod/@NX_class"] = "NXdata"  # TODO::writer should do!
        template[f"{trg}/image_twod/@signal"] = "magnitude"
        template[f"{trg}/image_twod/@axes"] = []
        for dim in dims:
            template[f"{trg}/image_twod/@axes"].append(f"axis_{idx_map[dim[0]]}")
            template[f"{trg}/image_twod/@AXISNAME_indices[axis_{idx_map[dim[0]]}]"] \
                = np.uint32(dim[1])
            support, unit = get_named_axis(obj["axes"], dim[0])
            if support is not None and unit is not None:
                template[f"{trg}/image_twod/axis_{idx_map[dim[0]]}"] \
                    = {"compress": support, "strength": 1}
                template[f"{trg}/image_twod/axis_{idx_map[dim[0]]}/@long_name"] \
                    = f"{idx_map[dim[0]]}-axis position ({unit})"
        template[f"{trg}/image_twod/title"] = meta["General/title"]
        template[f"{trg}/image_twod/magnitude"] \
            = {"compress": np.asarray(obj["data"]), "strength": 1}
        # template[f"{trg}/image_twod/magnitude/@units"]
        # TODO::add metadata
        self.id_mgn["event_img"] += 1
        self.id_mgn["event"] += 1
        return template

    def normalize_eds_spc_content(self, obj: dict, template: dict) -> dict:
        """Map relevant EDS spectrum/(a) to NeXus."""
        meta = fd.FlatDict(obj["metadata"], "/")
        dims = get_axes_dims(obj["axes"])
        n_dims = None
        if dims == [('Energy', 0)]:
            n_dims = 1
        elif dims == [('y', 0), ('x', 1), ('X-ray energy', 2)]:
            n_dims = 3
        else:
            print(f"WARNING eds_spc for {dims} is not implemented!")
            return
        trg = f"/ENTRY[entry{self.entry_id}]/measurement/event_data_em_set/" \
              f"EVENT_DATA_EM[event_data_em{self.id_mgn['event']}]/" \
              f"SPECTRUM_SET[spectrum_set{self.id_mgn['event_spc']}]"
        template[f"{trg}/source"] = meta["General/title"]
        template[f"{trg}/PROCESS[process]/source/type"] = "file"
        template[f"{trg}/PROCESS[process]/source/path"] = self.file_path
        template[f"{trg}/PROCESS[process]/source/checksum"] = self.file_path_sha256
        template[f"{trg}/PROCESS[process]/source/algorithm"] = "SHA256"
        template[f"{trg}/PROCESS[process]/detector_identifier"] \
            = f"Check carefully how rsciio/hyperspy knows this {meta['General/title']}!"
        trg = f"/ENTRY[entry{self.entry_id}]/measurement/event_data_em_set/" \
              f"EVENT_DATA_EM[event_data_em{self.id_mgn['event']}]/" \
              f"SPECTRUM_SET[spectrum_set{self.id_mgn['event_spc']}]" \
              f"DATA[spectrum_zerod]"
        template[f"{trg}/@NX_class"] = "NXdata"  # TODO::should be autodecorated
        template[f"{trg}/@signal"] = "intensity"
        if n_dims == 1:
            template[f"{trg}/@axes"] = ["axis_energy"]
            template[f"{trg}/@AXISNAME_indices[axis_energy_indices]"] = np.uint32(0)
            support, unit = get_named_axis(obj["axes"], "Energy")
            template[f"{trg}/AXISNAME[axis_energy]"] \
                = {"compress": support, "strength": 1}
            template[f"{trg}/AXISNAME[axis_energy]/@long_name"] \
                = f"Energy ({unit})"
        if n_dims == 3:
            template[f"{trg}/@axes"] = ["axis_y", "axis_x", "axis_energy"]
            template[f"{trg}/@AXISNAME_indices[axis_y_indices]"] = np.uint32(2)
            template[f"{trg}/@AXISNAME_indices[axis_x_indices]"] = np.uint32(1)
            template[f"{trg}/@AXISNAME_indices[axis_energy_indices]"] = np.uint32(0)
            support, unit = get_named_axis(obj["axes"], "y")
            template[f"{trg}/AXISNAME[axis_y]"] = {"compress": support, "strength": 1}
            template[f"{trg}/AXISNAME[axis_y]/@long_name"] = f"y-axis position ({unit})"
            support, unit = get_named_axis(obj["axes"], "x")
            template[f"{trg}/AXISNAME[axis_x]"] = {"compress": support, "strength": 1}
            template[f"{trg}/AXISNAME[axis_x]/@long_name"] = f"x-axis position ({unit})"
            support, unit = get_named_axis(obj["axes"], "X-ray energy")
            template[f"{trg}/AXISNAME[axis_energy]"] = {"compress": support, "strength": 1}
            template[f"{trg}/AXISNAME[axis_energy]/@long_name"] = f"Energy ({unit})"
        # template[f"{trg}/description"] = ""
        template[f"{trg}/title"] = f"EDS spectrum {meta['General/title']}"
        template[f"{trg}/intensity"] \
            = {"compress": np.asarray(obj["data"]), "strength": 1}
        # template[f"{trg}/intensity/@long_name"] = ""
        self.id_mgn["event_spc"] += 1
        self.id_mgn["event"] += 1
        return template

    def normalize_eds_map_content(self, obj: dict, template: dict) -> dict:
        """Map relevant EDS map to NeXus."""
        meta = fd.FlatDict(obj["metadata"], "/")
        dims = get_axes_dims(obj["axes"])
        if len(dims) != 2:
            raise ValueError(f"{obj['axes']}")
        trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{self.id_mgn['roi']}]/eds/indexing"
        template[f"{trg}/source"] = meta["General/title"]
        trg = f"/ENTRY[entry{self.entry_id}]/ROI[roi{self.id_mgn['roi']}]/eds/indexing/" \
              f"IMAGE_R_SET[image_r_set{self.id_mgn['eds_img']}]"
        template[f"{trg}/PROCESS[process]/source/type"] = "file"
        template[f"{trg}/PROCESS[process]/source/path"] = self.file_path
        template[f"{trg}/PROCESS[process]/source/checksum"] = self.file_path_sha256
        template[f"{trg}/PROCESS[process]/source/algorithm"] = "SHA256"
        template[f"{trg}/PROCESS[process]/detector_identifier"] \
            = f"Check carefully how rsciio/hyperspy knows this {meta['General/title']}!"
        # template[f"{trg}/description"] = ""
        # template[f"{trg}/energy_range"] = (0., 0.)
        # template[f"{trg}/energy_range/@units"] = "keV"
        # template[f"{trg}/iupac_line_candidates"] = ""
        template[f"{trg}/image_twod/@NX_class"] = "NXdata"  # TODO::should be autodecorated
        template[f"{trg}/image_twod/@signal"] = "intensity"
        template[f"{trg}/image_twod/@axes"] = []
        for dim in dims:
            template[f"{trg}/image_twod/@axes"].append(f"axis_{dim[0]}")
            template[f"{trg}/image_twod/@AXISNAME_indices[axis_{dim[0]}_indices]"] \
                = np.uint32(dim[1])
            support, unit = get_named_axis(obj["axes"], dim[0])
            if support is not None and unit is not None:
                template[f"{trg}/image_twod/AXISNAME[axis_{dim[0]}]"] \
                    = {"compress": support, "strength": 1}
                template[f"{trg}/image_twod/axis_{dim[0]}/@long_name"] \
                    = f"{dim[0]}-axis position ({unit})"
        template[f"{trg}/title"] = f"EDS map {meta['General/title']}"
        template[f"{trg}/image_twod/intensity"] \
            = {"compress": np.asarray(obj["data"]), "strength": 1}
        # template[f"{trg}/image_twod/intensity/@long_name"] = f"Signal"
        self.id_mgn["eds_img"] += 1
        self.id_mgn["roi"] += 1  # TODO not necessarily has to be incremented!
        return template

    def normalize_eels_content(self, obj: dict, template: dict) -> dict:
        return template
