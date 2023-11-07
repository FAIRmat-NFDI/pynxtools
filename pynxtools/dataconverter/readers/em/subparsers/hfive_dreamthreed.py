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
"""(Sub-)parser mapping concepts and content from community *.dream3d files on NXem."""

import os
from typing import Dict, Any, List
import numpy as np
import h5py
# import imageio.v3 as iio
from PIL import Image as pil

import diffsims
import orix
from diffpy.structure import Lattice, Structure
from orix import plot
from orix.crystal_map import create_coordinate_arrays, CrystalMap, PhaseList
from orix.quaternion import Rotation
from orix.vector import Vector3d

import matplotlib.pyplot as plt

from pynxtools.dataconverter.readers.em.subparsers.hfive_base import HdfFiveBaseParser
from pynxtools.dataconverter.readers.em.utils.hfive_utils import \
    EBSD_MAP_SPACEGROUP, read_strings_from_dataset, all_equal, format_euler_parameterization
from pynxtools.dataconverter.readers.em.examples.ebsd_database import \
    ASSUME_PHASE_NAME_TO_SPACE_GROUP

# DREAM3D implements essentially a data analysis workflow with individual steps
# in the DREAM3D jargon each step is referred to as a filter, filters have well-defined
# name and version, each filter takes dependent on its version specific input and
# generates predictable output, this is a benefit and signature of the professional
# design and idea behind DREAM3D
# in effect, the combination of versioned filters used in combination with the DREAM3D
# software version and file version defines how results end up in a DREAM3D file

# TODO::to capture every possible output one would keep a record of the individual
# schemes for each filter and the differences in these between versions
# considering the fact that DREAM3D is still in a process of migrating from previous
# versions to a so-called DREAM3DNX (more professional) version we do not wish to explore
# for now how this filter-based schema version can be implemented
# instead we leave it with a few examples, here specifically how to extract if
# available inverse pole figure maps for the reconstructed discretized three-dimensional
# microstructure which is the key task that DREAM3D enables users to generate from a
# collection of EBSD mappings obtained via serial-sectioning

# idea behind this implementation:
# e.g. a materials scientists/engineer working in the field of e.g. ICME
# generating N microstructure reconstructions from M measurements
# in general N and M >= 1 and N can be N >> M i.e. one serial-section study with
# hundreds of different microstructures, typical case for exploring phase space
# of thermo-chemo-mechanical material response effect of structure on properties
# in this case each DREAM3D run should be supplemented with contextualizing metadata
# e.g. collected via an ELN e.g. user, material, measurement used, etc. i.e. all those
# pieces of information which are not documented by or not documentable currently by
# the DREAM3D software within its own realm
# in effect a research may have say N ~= 1000 uploads with one DREAM3D instance each
# benefits: i) for the researcher search across explore, ii) for many researchers explore
# and contextualize


class HdfFiveDreamThreedReader(HdfFiveBaseParser):
    """Read DREAM3D HDF5 files (from Bluequartz's DREAM3D)"""
    def __init__(self, file_path: str = ""):
        super().__init__(file_path)
        self.prfx = None
        self.tmp = {}
        self.supported_version = {}
        self.version = {}
        self.init_support()
        self.supported = False
        self.check_if_supported()

    def init_support(self):
        """Init supported versions."""
        self.supported_version = {}
        self.version = {}
        self.supported_version["tech_partner"] = ["Bluequartz"]
        self.supported_version["schema_name"] = ["DREAM3D"]
        self.supported_version["schema_version"] = ["6.0", "7.0"]
        # strictly speaking Bluequartz refers the above-mentioned here as File Version
        # but content is expected adaptive depends on filters used, their versions, and
        # the sequence in which the execution of these filters was instructed
        self.supported_version["writer_name"] = ["DREAM3D"]
        self.supported_version["writer_version"] = [
            "1.2.812.508bf5f37",
            "2.0.170.4eecce207",
            "1.0.107.2080f4e",
            "2014.03.05",
            "2014.03.13",
            "2014.03.15",
            "2014.03.16",
            "4.3.6052.263064d",
            "1.2.828.f45085c83",
            "2.0.170.4eecce207",
            "1.2.826.7c66a0e77"]

    def check_if_supported(self):
        # check if instance to process matches any of these constraints
        self.supported = 0  # voting-based
        with h5py.File(self.file_path, "r") as h5r:
            if len(h5r["/"].attrs.keys()) < 2:
                self.supported = False
                return
            req_fields = ["DREAM3D Version", "FileVersion"]
            for req_field in req_fields:
                if f"{req_field}" not in h5r["/"].attrs.keys():
                    self.supported = False
                    return
            if read_strings_from_dataset(h5r["/"].attrs["DREAM3D Version"]) in self.supported_version["writer_version"]:
                self.supported += 1
            if read_strings_from_dataset(h5r["/"].attrs["FileVersion"]) in self.supported_version["schema_version"]:
                self.supported += 1

            if self.supported == 2:
                self.supported = True
                self.version = self.supported_version.copy()
            else:
                self.supported = False

    def search_normalizable_content(self):
        """Check if that highly customizable DREAM3D file has here supported content."""
        super().open()
        super().get_content()
        # super().report_content()
        super().close()
        # the logic to find if there is at all a 3D EBSD reconstruction in it
        # search for a node:
        target_path = []
        #    named _SIMPL_GEOMETRY
        candidate_paths = []
        for hdf_node_path in self.datasets.keys():
            idx = hdf_node_path.find("/_SIMPL_GEOMETRY")
            if idx > -1:
                candidate_paths.append((hdf_node_path, idx))
        #    which has childs "DIMENSIONS, ORIGIN, SPACING"
        for path_idx in candidate_paths:
            head = path_idx[0][0:path_idx[1]]
            tail = path_idx[0][path_idx[1]:]
            found = 0
            req_fields = ["DIMENSIONS", "ORIGIN", "SPACING"]
            for req_field in req_fields:
                if f"{head}/_SIMPL_GEOMETRY/{req_field}" in self.datasets.keys():
                    found += 1
            if found == 3:
                target_path.append(head)
                break
        del candidate_paths
        # if only one such node found parse only if
        if len(target_path) != 1:
            return
        else:
            target_path = target_path[0]
        #    that node has one sibling node called CellData
        found = 0
        i_j_k = (None, None, None)
        group_name = None
        for entry in self.datasets.keys():
            if entry.startswith(f"{target_path}") is True and entry.endswith(f"EulerAngles") is True:
                group_name = entry[0:-12]  # removing the trailing fwslash
        #       which has a dset of named EulerAngles shape 4d, (i, j, k, 1) +
                shp = self.datasets[entry][2]
                if isinstance(shp, tuple) and len(shp) == 4:
                    if shp[3] == 3:
                        i_j_k = (shp[0], shp[1], shp[2])
                        found += 1
                        break
        if group_name is None:
            return
        #       which has a dset named BC or CI or MAD shape 4d (i, j, k, 1) +
        one_key_required = ["BC", "Band Contrast", "CI", "Confidence Index", "MAD"]
        for key in one_key_required:
            if f"{group_name}/{key}" in self.datasets.keys():
                shp = self.datasets[f"{group_name}/{key}"][2]
                if isinstance(shp, tuple) and len(shp) == 4:
                    if (shp[0], shp[1], shp[2]) == i_j_k:
                        found += 1
                        break
        #       which has a dset named Phases shape 4d (i, j, k, 1) +
        if f"{group_name}/Phases" in self.datasets.keys():
            shp = self.datasets[f"{group_name}/Phases"][2]
            if isinstance(shp, tuple) and len(shp) == 4:
                if (shp[0], shp[1], shp[2]) == i_j_k:
                    found += 1
        #    that node has one sibling node called Phase Data
        if found != 3:
            return
        #       which has a dset named CrystalStructures, LatticeConstants, MaterialName
        req_fields = ["CrystalStructures", "LatticeConstants", "MaterialName"]
        found = 0
        possible_locs = ["Phase Data", "CellEnsembleData"]
        # TODO::these group names were found in the examples but likely they can be changed depending on how the filters are set
        for req_field in req_fields:
            for loc in possible_locs:
                if f"{target_path}/{loc}/{req_field}" in self.datasets.keys():
        #           (which should also have specific shape)
                    found += 1
                    if found != 3:
                        print(f"Relevant 3D EBSD content found")
                        print(f"{target_path}")
                        print(f"{group_name}")
                        return
        print(f"No relevant 3D EBSD content found!")

        # but see if that logic does not also check the shape and numerical content
        # there are still possibilities where this logic fails to detect a concept
        # reliably, this shows clearly that documenting and offering versioned description
        # of content is the key barrier to implement more sophisticated conceptual
        # normalization and assuring that content from other data providers (like DREAM3D)
        # is understood before being normalized so that results in the RDMS are really
        # useful and comparable

        # this is one approach how to find relevant groups
        # another would be to interpret really the filters applied and hunt
        # for the output within the parameters of a specific filter

    def parse_and_normalize(self):
        """Read and normalize away community-specific formatting with an equivalent in NXem."""
        self.search_normalizable_content()

        # how to find if at all relevant
        # search for a node:
        #    named _SIMPL_GEOMETRY
        #    which has childs "DIMENSIONS, ORIGIN, SPACING"
        # if only one such node found
        #    check that this node has one sibling node called CellData
        #    which has a group of shape 4d, (>=1, >=1, >=1, 3) uint8 surplus
        #    a group named either BC, CI or MAD, shape 4d (i, j, k, 1), name
        """
        with h5py.File(f"{self.file_path}", "r") as h5r:
            tmp = HdfFiveBaseParser()

            cache_id = 1
            grp_names = list(h5r["/"])
            for grp_name in grp_names:
                if grp_name not in ["Version", "Manufacturer"]:
                    self.prfx = f"/{grp_name}"
                    ckey = self.init_named_cache(f"ebsd{cache_id}")
                    self.parse_and_normalize_group_ebsd_header(h5r, ckey)
                    self.parse_and_normalize_group_ebsd_phases(h5r, ckey)
                    self.parse_and_normalize_group_ebsd_data(h5r, ckey)
                    # add more information to pass to hfive parser
                    cache_id += 1
        """
        # from hfive_ebsd
