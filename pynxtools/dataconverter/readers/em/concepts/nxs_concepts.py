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
"""Implement NeXus-specific groups and fields to document software and versions used."""

# pylint: disable=no-member,too-few-members

from typing import List
from pynxtools.dataconverter.readers.em.concepts.concept_mapper \
    import variadic_path_to_specific_path


PYNXTOOLS_VERSION = "n/a"
PYNXTOOLS_URL = "https://www.github.com/FAIRmat-NFDI/pynxtools"

NXEM_NAME = "NXem"
NXEM_VERSION = "n/a"
NXEM_URL = "https://www.github.com/FAIRmat-NFDI/nexus_definitions"

NxEmRoot = {"/ENTRY[entry*]/PROGRAM[program1]/program": "pynxtools/dataconverter/readers/em",
            "/ENTRY[entry*]/PROGRAM[program1]/program/@version": PYNXTOOLS_VERSION,
            "/ENTRY[entry*]/PROGRAM[program1]/program/@url": PYNXTOOLS_URL,
            "/ENTRY[entry*]/@url": NXEM_URL,
            "/ENTRY[entry*]/definition": NXEM_NAME,
            "/ENTRY[entry*]/definition/@version": NXEM_VERSION}
# alternatively the above-mentioned program1 entries to place under "/"


class NxEmAppDef():
    """Add NeXus NXem appdef specific contextualization.

    """
    def __init__(self):
        pass

    def parse(self, template: dict, entry_id: int = 1, cmd_line_args: List = []) -> dict:
        """Parse application definition."""
        for nx_path, value in NxEmRoot.items():
            if (nx_path != "IGNORE") and (nx_path != "UNCLEAR"):
                trg = variadic_path_to_specific_path(nx_path, [entry_id])
                res = value
                if res is not None:
                    template[trg] = res
        if cmd_line_args != [] and all(isinstance(item, str) for item in cmd_line_args):
            template["/cs_profiling/@NX_class"] = "NXcs_profiling"
            template["/cs_profiling/command_line_call"] = cmd_line_args
        return template


class NxConcept():
    """"Define a NeXus concept object to handle paths.

    """
    def __init__(self, hdf_paths: List = []):
        # TODO::remove redundant code for instantiating specific NxConcepts like
        # NxSpectrum, NxImageRealSpaceSet, NxEmEdsIndexing
        pass
