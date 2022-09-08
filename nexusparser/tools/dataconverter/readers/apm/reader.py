#!/usr/bin/env python3
"""Generic parser for loading atom probe microscopy data into NXapm."""

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
# pylint: disable=duplicate-code
# pylint: disable=R0801

from typing import Tuple, Any

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader

from nexusparser.tools.dataconverter.readers.apm.utils.apm_use_case_selector \
    import ApmUseCaseSelector

from nexusparser.tools.dataconverter.readers.apm.utils.apm_reconstruction_io \
    import ApmReconstructionParser

from nexusparser.tools.dataconverter.readers.apm.utils.apm_ranging_io \
    import ApmRangingDefinitionsParser

from nexusparser.tools.dataconverter.readers.apm.utils.apm_nomad_oasis_eln_io \
    import NxApmNomadOasisElnSchemaParser

from nexusparser.tools.dataconverter.readers.apm.utils.apm_nexus_plots \
    import apm_default_plot_generator

# each reconstruction should be stored as an own file because for commercial
# atom probe microscopes it is currently impossible to get less processed data
# from the microscopes


class ApmReader(BaseReader):
    """Parse content from community file formats.

    Specifically, (local electrode) atom probe microscopy and field-ion microscopy
    towards a NXapm.nxdl-compliant NeXus file.

    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXapm"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        # pylint: disable=duplicate-code
        # pylint: disable=R0801
        """Read data from given file, return filled template dictionary apm."""
        template.clear()  # pylint: disable=duplicate-code

        case = ApmUseCaseSelector(file_paths)
        assert case.is_valid is True, \
            "Such a combination of input-file(s, if any) is not supported !"

        # nx_apm_header = NxApmAppDefHeader()
        # prefix = "/ENTRY[entry]"
        # nx_apm_header.report(prefix, template)

        print("Parsing numerical data and metadata from reconstructed dataset...")
        if len(case.reconstruction) == 1:
            nx_apm_recon = ApmReconstructionParser(case.reconstruction[0])
            nx_apm_recon.report(template)
        else:
            print("No input-file defined for reconstructed dataset!")
            return {}

        print("Parsing numerical data and metadata from ranging definitions file...")
        if len(case.ranging) == 1:
            nx_apm_range = ApmRangingDefinitionsParser(case.ranging[0])
            nx_apm_range.report(template)
        else:
            print("No input-file defined for ranging definitions!")
            return {}

        print("Parsing metadata as well as numerical data from NOMAD OASIS ELN...")
        if len(case.eln) == 1:
            nx_apm_eln = NxApmNomadOasisElnSchemaParser(case.eln[0])
            nx_apm_eln.report(template)
        else:
            print("No input file defined for eln data !")
            return {}

        print("Creating default plottable data...")
        apm_default_plot_generator(template)

        # if True is True:
        # reporting of what has not been properly defined at the reader level
        # print("\n\nDebugging...")
        # for keyword in template.keys():
        #     # if template[keyword] is None:
        #     print(keyword + "...")
        #     print(template[keyword])
        #     # if template[keyword] is None:
        #     #     print("Entry: " + keyword + " is not properly defined yet!")

        print("Forwarding the instantiated template to the NXS writer...")

        return template


# This has to be set to allow the convert script to use this reader.
READER = ApmReader
