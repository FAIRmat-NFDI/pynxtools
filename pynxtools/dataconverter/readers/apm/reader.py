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
"""Generic parser for loading atom probe microscopy data into NXapm."""

# pylint: disable=no-member

from typing import Tuple, Any

from pynxtools.dataconverter.readers.base.reader import BaseReader

from pynxtools.dataconverter.readers.apm.utils.apm_define_io_cases \
    import ApmUseCaseSelector

from pynxtools.dataconverter.readers.apm.utils.apm_load_deployment_specifics \
    import NxApmNomadOasisConfigurationParser

from pynxtools.dataconverter.readers.apm.utils.apm_load_generic_eln \
    import NxApmNomadOasisElnSchemaParser

from pynxtools.dataconverter.readers.apm.utils.apm_load_reconstruction \
    import ApmReconstructionParser

from pynxtools.dataconverter.readers.apm.utils.apm_load_ranging \
    import ApmRangingDefinitionsParser

from pynxtools.dataconverter.readers.apm.utils.apm_create_nx_default_plots \
    import apm_default_plot_generator

from pynxtools.dataconverter.readers.apm.utils.apm_generate_synthetic_data \
    import ApmCreateExampleData

# this apm parser combines multiple sub-parsers
# so we need the following input:
# logical analysis which use case
# data input from an ELN (e.g. NOMAD OASIS)
# data input from technology partner files
# functionalities for creating default plots
# developer functionalities for creating synthetic data

# each reconstruction should be stored as an own file because for commercial
# atom probe microscopes it is currently impossible to get less processed data
# from the microscopes
# for development purposes synthetic datasets can be created which are
# for now stored all in the same file. As these use the same dictionary
# the template variable analyses of files larger than the physical main memory
# can currently not be handled


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

        n_entries = 1
        entry_id = 1
        if len(file_paths) == 1:
            if file_paths[0].startswith("synthesize"):
                synthesis_id = int(file_paths[0].replace("synthesize", ""))
                print(f"synthesis_id {synthesis_id}")
            else:
                synthesis_id = 1
            print("Create one synthetic entry in one NeXus file...")
            synthetic = ApmCreateExampleData(synthesis_id)
            synthetic.synthesize(template)
        else:  # eln_data, and ideally recon and ranging definitions from technology partner file
            print("Parse ELN and technology partner file(s)...")
            case = ApmUseCaseSelector(file_paths)
            assert case.is_valid is True, \
                "Such a combination of input-file(s, if any) is not supported !"

            print("Parse (meta)data coming from an ELN...")
            if len(case.eln) == 1:
                nx_apm_eln = NxApmNomadOasisElnSchemaParser(case.eln[0], entry_id)
                nx_apm_eln.report(template)
            else:
                print("No input file defined for eln data !")
                return {}

            print("Parse (meta)data coming from a configuration that specific OASIS...")
            if len(case.cfg) == 1:
                nx_apm_cfg = NxApmNomadOasisConfigurationParser(case.cfg[0], entry_id)
                nx_apm_cfg.report(template)
            # having and or using a deployment-specific configuration is optional

            print("Parse (numerical) data and metadata from ranging definitions file...")
            if len(case.reconstruction) == 1:
                nx_apm_recon = ApmReconstructionParser(case.reconstruction[0], entry_id)
                nx_apm_recon.report(template)
            else:
                print("No input-file defined for reconstructed dataset!")
                return {}
            if len(case.ranging) == 1:
                nx_apm_range = ApmRangingDefinitionsParser(case.ranging[0], entry_id)
                nx_apm_range.report(template)
            else:
                print("No input-file defined for ranging definitions!")
                return {}

        print("Create NeXus default plottable data...")
        apm_default_plot_generator(template, n_entries)

        # print("Reporting state of template before passing to HDF5 writing...")
        # for keyword in template.keys():
        #     print(keyword)
        #     print(template[keyword])

        print("Forward instantiated template to the NXS writer...")
        return template


# This has to be set to allow the convert script to use this reader.
READER = ApmReader
