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

from typing import Tuple, Any

from nexusutils.dataconverter.readers.base.reader import BaseReader

# this apm parser combines multiple sub-parsers
# so we need the following input:
# logical analysis which use case
# data input from an ELN (e.g. NOMAD OASIS)
# data input from technology partner files
# functionalities for creating default plots
# developer functionalities for creating synthetic data

from nexusutils.dataconverter.readers.apm.utils.apm_use_case_selector \
    import ApmUseCaseSelector

from nexusutils.dataconverter.readers.apm.utils.apm_generic_eln_io \
    import NxApmNomadOasisElnSchemaParser

from nexusutils.dataconverter.readers.apm.utils.apm_reconstruction_io \
    import ApmReconstructionParser

from nexusutils.dataconverter.readers.apm.utils.apm_ranging_io \
    import ApmRangingDefinitionsParser

from nexusutils.dataconverter.readers.apm.utils.apm_nexus_plots \
    import apm_default_plot_generator

from nexusutils.dataconverter.readers.apm.utils.apm_example_data \
    import ApmCreateExampleData

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
        """Read data from given file, return filled template dictionary apm."""
        template.clear()

        create_example_data_for_dev_purposes = True
        if create_example_data_for_dev_purposes is True:
            print("Create synthetic data...")
            synthetic = ApmCreateExampleData()
            synthetic.composition_to_ranging_definitions(template)
            synthetic.report(template)
        else:
            print("Identify case...")
            case = ApmUseCaseSelector(file_paths)
            assert case.is_valid is True, \
                "Such a combination of input-file(s, if any) is not supported !"

            print("Parse (meta)data coming from an ELN...")
            if len(case.eln) == 1:
                nx_apm_eln = NxApmNomadOasisElnSchemaParser(case.eln[0])
                nx_apm_eln.report(template)
            else:
                print("No input file defined for eln data !")
                return {}

            print("Parse (numerical) data and metadata from ranging definitions file...")
            if len(case.reconstruction) == 1:
                nx_apm_recon = ApmReconstructionParser(case.reconstruction[0])
                nx_apm_recon.report(template)
            else:
                print("No input-file defined for reconstructed dataset!")
                return {}
            if len(case.ranging) == 1:
                nx_apm_range = ApmRangingDefinitionsParser(case.ranging[0])
                nx_apm_range.report(template)
            else:
                print("No input-file defined for ranging definitions!")
                return {}

        print("Create NeXus default plottable data...")
        apm_default_plot_generator(template)

        debugging = False
        if debugging is True:
            print("Reporting state of template before passing to HDF5 writing...")
            for keyword in template.keys():
                print(keyword)
                print(template[keyword])

        print("Forward instantiated template to the NXS writer...")
        return template


# This has to be set to allow the convert script to use this reader.
READER = ApmReader
