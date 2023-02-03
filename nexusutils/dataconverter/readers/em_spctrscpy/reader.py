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
"""Parser for loading generic X-ray spectroscopy and EELS data into NXem via hyperspy."""

# pylint: disable=E1101

from typing import Tuple, Any

from nexusutils.dataconverter.readers.base.reader import BaseReader


from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_use_case_selector \
    import EmUseCaseSelector

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_generic_eln_io \
    import NxEmNomadOasisElnSchemaParser

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_event_data \
    import NxEventDataEm

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_nexus_plots \
    import em_spctrscpy_default_plot_generator

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_example_data \
    import EmSpctrscpyCreateExampleData


def hyperspy_parser(file_name: str, template: dict, entry_id: int) -> dict:
    """Parse content from electron microscopy vendor files."""
    test = NxEventDataEm(file_name, entry_id)
    test.report(template)
    return template


def nomad_oasis_eln_parser(file_name: str, template: dict, entry_id: int) -> dict:
    """Parse out output from a YAML file from a NOMAD OASIS YAML."""
    test = NxEmNomadOasisElnSchemaParser(file_name, entry_id)
    test.report(template)
    return template


class EmSpctrscpyReader(BaseReader):
    """Parse content from community file formats.

    Specifically, electron microscopy
    towards a NXem.nxdl-compliant NeXus file.
    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXem"]

    # pylint: disable=duplicate-code
    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Read data from given file, return filled template dictionary em."""
        # pylint: disable=duplicate-code
        template.clear()

        # this em_spctrscpy parser combines multiple sub-parsers
        # so we need the following input:
        # logical analysis which use case
        # data input from an ELN (e.g. NOMAD OASIS)
        # data input from technology partner files
        # functionalities for creating default plots
        # developer functionalities for creating synthetic data

        n_entries = 1
        entry_id = 1
        if len(file_paths) == 1:
            if file_paths[0].startswith("synthesize"):
                synthesis_id = int(file_paths[0].replace("synthesize", ""))
                print(f"synthesis_id {synthesis_id}")
            else:
                synthesis_id = 1
            print("Create one synthetic entry in one NeXus file...")
            synthetic = EmSpctrscpyCreateExampleData(synthesis_id)
            synthetic.synthesize(template)
        else:
            print("Parse ELN and technology partner file(s)...")
            case = EmUseCaseSelector(file_paths)
            assert case.is_valid is True, \
                "Such a combination of input-file(s, if any) is not supported !"

            print("Parse (meta)data coming from an ELN...")
            if case.eln_parser == "nomad-oasis":
                nomad_oasis_eln_parser(case.eln[0], template, entry_id)
            else:
                print("No input file defined for eln data !")
                return {}

            print("Parse (numerical) data and metadata from technology partner files...")
            if case.vendor_parser == "oina":
                # oina_parser(case.vendor[0], template, entry_id)
                return {}
            if case.vendor_parser == "hspy":
                hyperspy_parser(case.vendor[0], template, entry_id)
            else:
                print("No input-file defined for technology partner data !")
                return {}

        print("Create NeXus default plottable data...")
        em_spctrscpy_default_plot_generator(template, n_entries)

        debugging = False
        if debugging is True:
            print("Reporting state of template before passing to HDF5 writing...")
            for keyword in template.keys():
                print(keyword)
                # print(type(template[keyword]))
                # print(template[keyword])

        print("Forward instantiated template to the NXS writer...")
        return template


# This has to be set to allow the convert script to use this reader.
READER = EmSpctrscpyReader
