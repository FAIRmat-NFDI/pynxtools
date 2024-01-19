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

# pylint: disable=no-member,fixme

from typing import Tuple, Any

from pynxtools.dataconverter.readers.base.reader import BaseReader
# from pynxtools.dataconverter.readers.em.concepts.nxs_concepts import NxEmAppDef
# from pynxtools.dataconverter.readers.em.subparsers.nxs_mtex import NxEmNxsMTexSubParser
from pynxtools.dataconverter.readers.em.subparsers.nxs_pyxem import NxEmNxsPyxemSubParser
# from pynxtools.dataconverter.readers.em.subparsers.nxs_imgs import NxEmImagesSubParser
# from pynxtools.dataconverter.readers.em.subparsers.nxs_nion import NxEmZippedNionProjectSubParser
from pynxtools.dataconverter.readers.em.subparsers.rsciio_velox import RsciioVeloxSubParser
from pynxtools.dataconverter.readers.em.utils.default_plots import NxEmDefaultPlotResolver
# from pynxtools.dataconverter.readers.em.geometry.convention_mapper import NxEmConventionMapper

# remaining subparsers to be implemented and merged into this one
# from pynxtools.dataconverter.readers.em_om.utils.generic_eln_io \
#     import NxEmOmGenericElnSchemaParser
# from pynxtools.dataconverter.readers.em_om.utils.orix_ebsd_parser \
#     import NxEmOmOrixEbsdParser
# from pynxtools.dataconverter.readers.em_om.utils.mtex_ebsd_parser \
#     import NxEmOmMtexEbsdParser
# from pynxtools.dataconverter.readers.em_om.utils.zip_ebsd_parser \
#     import NxEmOmZipEbsdParser
# from pynxtools.dataconverter.readers.em_om.utils.dream3d_ebsd_parser \
#     import NxEmOmDreamThreedEbsdParser
# from pynxtools.dataconverter.readers.em_om.utils.em_nexus_plots \
#     import em_om_default_plot_generator


class EmReader(BaseReader):
    """Parse content from file formats of the electron microscopy community."""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXem", "NXroot"]

    # pylint: disable=duplicate-code
    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Read data from given file, return filled template dictionary em."""
        # pylint: disable=duplicate-code
        template.clear()

        # debug_id = 3
        # template[f"/ENTRY[entry1]/test{debug_id}"] = f"test{debug_id}"
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

        print("Identify information sources (ELN, RDM config, tech files) to deal with...")
        # case = EmUseCaseSelector(file_paths)
        # if case.is_valid is False:
        #     print("Such a combination of input (file) is not supported !")
        #    return {}

        print("Process pieces of information within RDM-specific ELN export file...")
        # if case.eln_parser_type == "oasis":
        #     # pattern_simulation = False
        #     # if case.dat_parser_type == "zip":
        #     #     pattern_simulation = True
        #     eln = OasisCustomSchemaInstanceFileParser(case.eln[0], entry_id)
        #     eln.parse(template)
        # else:
        #     print("No interpretable ELN input found!")

        # print("Process pieces of information in RDM-specific configuration files...")
        # if case.cfg_parser_type == "oasis":
        #     cfg = OasisSpecificConfigInstanceFileParser(case.cfg[0], entry_id)
        #     cfg.parse(template)
        # else:
        #     print("No interpretable configuration file offered")

        input_file_names = []
        for file_path in file_paths:
            if file_path != "":
                input_file_names.append(file_path)
        print("Parse NeXus appdef-specific content...")
        # nxs = NxEmAppDef()
        # nxs.parse(template, entry_id, input_file_names)

        print("Parse conventions of reference frames...")
        # conventions = NxEmConventionMapper(entry_id)
        # conventions.parse(template)

        print("Parse and map pieces of information within files from tech partners...")
        # sub_parser = "nxs_mtex"
        # subparser = NxEmNxsMTexSubParser(entry_id, file_paths[0])
        # subparser.parse(template)
        # TODO::check correct loop through!

        # add further with resolving cases
        # if file_path is an HDF5 will use hfive parser
        # sub_parser = "nxs_pyxem"
        # subparser = NxEmNxsPyxemSubParser(entry_id, file_paths[0])
        # subparser.parse(template)
        # TODO::check correct loop through!

        # sub_parser = "image_tiff"
        # subparser = NxEmImagesSubParser(entry_id, file_paths[0])
        # subparser.parse(template)
        # TODO::check correct loop through!

        # sub_parser = "zipped_nion_project"
        # subparser = NxEmZippedNionProjectSubParser(entry_id, file_paths[0])
        # subparser.parse(template, verbose=True)
        # TODO::check correct loop through!

        # sub_parser = "velox_emd"
        subparser = RsciioVeloxSubParser(entry_id, file_paths[0], verbose=False)
        subparser.parse(template)

        # for dat_instance in case.dat_parser_type:
        #     print(f"Process pieces of information in {dat_instance} tech partner file...")
        #    continue
        #    # elif case.dat_parser_type == "zip":
        #    #     zip_parser = NxEmOmZipEbsdParser(case.dat[0], entry_id)
        #    #     zip_parser.parse(template)
        #    # elif case.dat_parser_type == "dream3d":
        #    #     dream_parser = NxEmOmDreamThreedEbsdParser(case.dat[0], entry_id)
        #    #     dream_parser.parse(template)
        #    # elif case.dat_parser_type == "kikuchipy":
        #    # elif case.dat_parser_type == "pyxem":
        #    # elif case.dat_parser_type == "score":
        #    # elif case.dat_parser_type == "qube":
        #    # elif case.dat_parser_type == "paradis":
        #    # elif case.dat_parser_type == "brinckmann":
        # at this point the data for the default plots should already exist
        # we only need to decorate the template to point to the mandatory ROI overview
        # print("Create NeXus default plottable data...")
        # em_default_plot_generator(template, 1)

        run_block = False
        if run_block is True:
            nxs_plt = NxEmDefaultPlotResolver()
            # if nxs_mtex is the sub-parser
            resolved_path = nxs_plt.nxs_mtex_get_nxpath_to_default_plot(
                entry_id, file_paths[0])
            # print(f"DEFAULT PLOT IS {resolved_path}")
            if resolved_path != "":
                nxs_plt.annotate_default_plot(template, resolved_path)

        debugging = False
        if debugging is True:
            print("Reporting state of template before passing to HDF5 writing...")
            for keyword in template.keys():
                print(keyword)
                # print(type(template[keyword]))
                print(template[keyword])

        print("Forward instantiated template to the NXS writer...")
        return template


# This has to be set to allow the convert script to use this reader.
READER = EmReader
