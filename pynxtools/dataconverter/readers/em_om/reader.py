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

from pynxtools.dataconverter.readers.em_om.utils.use_case_selector \
    import EmOmUseCaseSelector

from pynxtools.dataconverter.readers.em_om.utils.generic_eln_io \
    import NxEmOmGenericElnSchemaParser

from pynxtools.dataconverter.readers.em_om.utils.orix_ebsd_parser \
    import NxEmOmOrixEbsdParser

from pynxtools.dataconverter.readers.em_om.utils.mtex_ebsd_parser \
    import NxEmOmMtexEbsdParser

from pynxtools.dataconverter.readers.em_om.utils.zip_ebsd_parser \
    import NxEmOmZipEbsdParser

from pynxtools.dataconverter.readers.em_om.utils.dream3d_ebsd_parser \
    import NxEmOmDreamThreedEbsdParser

from pynxtools.dataconverter.readers.em_om.utils.em_nexus_plots \
    import em_om_default_plot_generator


class EmOmReader(BaseReader):
    """Parse content from file formats of the electron-backscatter community.

    Specifically, electron microscopy
    towards a NXem_ebsd.nxdl-compliant NeXus file.
    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXem_ebsd"]  # how to combine with "NXem"?

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
        # data input from technology partner files
        # functionalities for creating default plots

        entry_id = 1
        # if len(file_paths) != 2:
        #     print("Generation of example data not implemented yet...!")
        #     return {}

        print("Parse ELN and technology partner file(s)...")
        case = EmOmUseCaseSelector(file_paths)
        if case.is_valid is False:
            print("Such a combination of input-file(s, if any) is not supported !")
            return {}

        print("Parse (meta)data coming from an ELN...")
        if case.eln_parser_type == "generic":
            pattern_simulation = False
            if case.dat_parser_type == "zip":
                pattern_simulation = True
            eln = NxEmOmGenericElnSchemaParser(case.eln[0], entry_id, pattern_simulation)
            eln.parse(template)
        else:
            print("No interpretable ELN input found!")
            return {}

        print("Parse (numerical) data and metadata from technology partner files...")
        if case.dat_parser_type == "orix":
            orix_parser = NxEmOmOrixEbsdParser(case.dat[0], entry_id)
            # h5oina parser evaluating content and plotting with orix on the fly
            orix_parser.parse(template)
        elif case.dat_parser_type == "mtex":
            mtex_parser = NxEmOmMtexEbsdParser(case.dat[0], entry_id)
            # ebsd parser because concept suggested for MTex by M. Kühbach
            # would include different HDF5 dumps for different MTex classes
            mtex_parser.parse(template)
        elif case.dat_parser_type == "zip":
            zip_parser = NxEmOmZipEbsdParser(case.dat[0], entry_id)
            zip_parser.parse(template)
        elif case.dat_parser_type == "dream3d":
            dream_parser = NxEmOmDreamThreedEbsdParser(case.dat[0], entry_id)
            dream_parser.parse(template)
        # elif case.dat_parser_type == "kikuchipy":
        # elif case.dat_parser_type == "pyxem":
        # elif case.dat_parser_type == "score":
        # elif case.dat_parser_type == "qube":
        # elif case.dat_parser_type == "paradis":
        # elif case.dat_parser_type == "brinckmann":
        else:
            print("No input-file defined for technology partner data !")

        # at this point the default plots exist already
        # we only need to decorate the template to point to the mandatory ROI overview
        print("Create NeXus default plottable data...")
        em_om_default_plot_generator(template, 1)

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
READER = EmOmReader
