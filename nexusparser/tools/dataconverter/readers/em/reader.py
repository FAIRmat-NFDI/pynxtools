#!/usr/bin/env python3
"""Parser for loading generic X-ray spectroscopy hyperspy data into NXem."""

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

import numpy as np

import hyperspy.api as hs

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader

from nexusparser.tools.dataconverter.readers.em.utils.em_use_case_selector \
    import EmUseCaseSelector

from nexusparser.tools.dataconverter.readers.em.utils.em_nexus_base_classes \
    import NxObject, NxAppDefHeader

from nexusparser.tools.dataconverter.readers.em.utils.em_nomad_oasis_eln \
    import NxEmNomadOasisElnSchemaParser

from nexusparser.tools.dataconverter.readers.em.utils.hspy.em_hspy_xray \
    import NxSpectrumSetEmXray

from nexusparser.tools.dataconverter.readers.em.utils.hspy.em_hspy_adf \
     import NxImageSetEmAdf


# example_file_name = "46_ES-LP_L1_brg.bcf"
# example_file_name = "1613_Si_HAADF_610_kx.emd"
# hspy_object_list = hs.load(example_file_name)


class NxEventDataEm:
    """Representing a data collection event with a single detector.

    During this data collection event, the microscope
    was considered stable enough.
    """

    def __init__(self, file_name: str):
        self.start_time = NxObject('non_recoverable')
        self.end_time = NxObject('non_recoverable')
        self.event_identifier = NxObject()
        self.event_type = NxObject()
        self.detector_identifier = NxObject()
        # ##MK::the following list is not complete
        # but brings an example how NXem can be used disentangle
        # data and processing when, at a given point in time,
        # multiple detectors have been used
        self.spectrum_set_em_xray = None
        self.image_set_em_adf = None

        self.parse_hspy_analysis_results(file_name)

    def parse_hspy_analysis_results(self, file_name: str):
        """Parse the individual hyperspy-specific data.

        Route these respective classes of an NxEventDataEm instance.
        """
        hspy_objs = hs.load(file_name)
        # ##MK::this logic is too simplistic e.g. what if the dataset is TBs?
        # because file_name is usually the file from the microscope session...
        self.spectrum_set_em_xray = NxSpectrumSetEmXray(hspy_objs)
        self.image_set_em_adf = NxImageSetEmAdf(hspy_objs)

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        prefix = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
        prefix += "/EVENT_DATA_EM[event_data_em_1]"

        # ##MK::dummies for now
        import datetime
        NOW = datetime.datetime.now().astimezone().isoformat()
        template[prefix + "/detector_identifier"] = NOW  # self.detector_identifier.value
        # ##MK::hyperspy cannot implement per-event time stamping especially
        # not for time-zones because time data are vendor-specifically formatted
        # not always reported in which case hspy replaces missing vendor timestamps
        # with system time at runtime of the script !
        template[prefix + "/start_time"] = NOW  # self.start_time.value
        template[prefix + "/end_time"] = NOW  # self.end_time.value
        template[prefix + "/event_identifier"] = NOW  # self.event_identifier.value
        template[prefix + "/event_type"] = NOW  # self.event_type.value
        # ##MK::dummies for now end

        # if True is False:  # for development purposes to reduce nxs content
        prefix = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
        prefix += "/EVENT_DATA_EM[event_data_em_1]/"
        # ##MK::connect and compare frame_id with that of hspy
        if isinstance(self.spectrum_set_em_xray,
                      NxSpectrumSetEmXray) is True:
            self.spectrum_set_em_xray.report(prefix, 1, template)

        prefix = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
        prefix += "/EVENT_DATA_EM[event_data_em_1]/"
        # ##MK::connect and compare frame_id with that of hspy
        if isinstance(self.image_set_em_adf,
                      NxImageSetEmAdf) is True:
            self.image_set_em_adf.report(prefix, 1, template)

        return template


def hyperspy_parser(file_name: str, template: dict) -> dict:
    """Parse content from electron microscopy vendor files."""
    test = NxEventDataEm(file_name)
    test.report(template)
    return template


def nomad_oasis_eln_parser(file_name: str, template: dict) -> dict:
    """Parse out output from a YAML file from a NOMAD OASIS YAML."""
    test = NxEmNomadOasisElnSchemaParser(file_name)
    test.report(template)
    return template


def create_default_plottable_data(template: dict) -> dict:
    """For a valid NXS file at least one default plot is required."""
    # ##MK::for EDS use the spectrum stack, the more generic, the more complex
    # ##MK::the logic has to be to infer a default plottable
    # when using hyperspy and EDS data, the path to the default plottable
    # needs to point to an existent plot, in this example we use the
    # NxSpectrumSetEmXray stack_data instance of the first event which
    # has such
    trg = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
    trg += "/EVENT_DATA_EM[event_data_em_1]/"
    trg += "NX_SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray_1]/"
    trg += "DATA[summary]/counts"  # "DATA[stack]/counts"
    assert isinstance(template[trg], np.ndarray), \
        "The data which should support the default plottable are not existent!"
    trg = "/ENTRY[entry]/"
    template[trg + "@default"] = "measurement"
    trg += "EVENT_DATA_EM_SET[measurement]/"
    template[trg + "@default"] = "event_data_em_1"
    trg += "EVENT_DATA_EM[event_data_em_1]/"
    template[trg + "@default"] = "spectrum_set_em_xray_1"
    trg += "NX_SPECTRUM_SET_EM[spectrum_set_em_xray_1]/"
    template[trg + "@default"] = "summary"  # "stack"
    return template


class EmReader(BaseReader):
    """Parse content from community file formats.

    Specifically, electron microscopy
    towards a NXem.nxdl-compliant NeXus file.
    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXem"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Read data from given file, return filled template dictionary."""
        case = EmUseCaseSelector(file_paths)
        assert case.is_valid is True, \
            'Such a combination of input-file if any is not supported !'

        nx_em_header = NxAppDefHeader()
        prefix = "/ENTRY[entry]"
        nx_em_header.report(prefix, template)

        print("Parsing numerical data and metadata with hyperspy...")
        if len(case.micr) == 1:
            hyperspy_parser(case.micr[0], template)
        else:
            print("No input-file defined for micr data !")
            return {}

        print("Parsing metadata as well as numerical data from NOMAD OASIS ELN...")
        if len(case.eln) == 1:
            nomad_oasis_eln_parser(case.eln[0], template)
        else:
            print("No input file defined for eln data !")

        print("Creating default plottable data...")
        create_default_plottable_data(template)

        # reporting of what has not been properly defined at the reader level
        print('\n\nDebugging...')
        for keyword in template.keys():
            # if template[keyword] is None:
            print(keyword + '...')
            print(template[keyword])
            # if template[keyword] is None:
            #     print("Entry: '" + keyword + " is not properly defined yet!")

        print("Forwarding the instantiated template to the NXS writer...")

        return template


# This has to be set to allow the convert script to use this reader.
READER = EmReader
