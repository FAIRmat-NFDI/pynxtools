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
"""Parser for loading generic orientation microscopy data based on ."""

# pylint: disable=no-member

from typing import Tuple, Any

from pynxtools.dataconverter.readers.base.reader import BaseReader

from pynxtools.dataconverter.readers.em_nion.utils.swift_define_io_cases \
    import EmNionUseCaseSelector

from pynxtools.dataconverter.readers.em_nion.utils.swift_load_generic_eln \
    import NxEmNionElnSchemaParser

from pynxtools.dataconverter.readers.em_nion.utils.swift_zipped_project_parser \
    import NxEmNionSwiftProjectParser

from pynxtools.dataconverter.readers.em_spctrscpy.utils.em_nexus_plots \
    import em_spctrscpy_default_plot_generator


class EmNionReader(BaseReader):
    """Parse content from nionswift projects.

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

        # this em_om parser combines multiple sub-parsers
        # so we need the following input:
        # logical analysis which use case
        # data input from an ELN (using an ELN-agnostic) YAML representation
        # data input from technology partner files, here zipped nionswift project
        # directory and file renamed from ending with zip to nszip
        # functionalities for creating default plots

        entry_id = 1

        print("Parse ELN and compressed nionswift project content...")
        case = EmNionUseCaseSelector(file_paths)
        if case.is_valid is False:
            print("Such a combination of input-file(s, if any) is not supported !")
            return {}

        print("Parse (meta)data coming from an ELN...")
        if case.eln_parser_type == "generic":
            eln = NxEmNionElnSchemaParser(case.eln[0], entry_id)
            eln.parse(template)
        else:
            print("No interpretable ELN input found!")
            return {}

        print("Parse (numerical) data and metadata from nionswift project...")
        if case.prj_parser_type == "nionswift":
            swift_parser = NxEmNionSwiftProjectParser(case.prj[0], entry_id)
            swift_parser.parse(template)
        else:
            print("No input-file defined for technology partner data !")

        # at this point the default plots exist already
        # we only need to decorate the template to point to the mandatory ROI overview
        print("Create NeXus default plottable data...")
        em_spctrscpy_default_plot_generator(template, entry_id)

        debugging = False
        if debugging is True:
            print("Reporting state of template before passing to HDF5 writing...")
            for keyword in template.keys():
                print(keyword)
                # print(type(template[keyword]))
                # print(f"{keyword}, {template[keyword]}")

        print("Forward instantiated template to the NXS writer...")
        return template


# This has to be set to allow the convert script to use this reader.
READER = EmNionReader
