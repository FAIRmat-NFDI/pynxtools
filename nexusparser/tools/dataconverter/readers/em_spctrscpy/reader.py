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

import datetime

from typing import Tuple, Any, Dict

import numpy as np

import hyperspy.api as hs

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader

from nexusparser.tools.dataconverter.readers.em_spctrscpy.utils.em_use_case_selector \
    import EmUseCaseSelector

from nexusparser.tools.dataconverter.readers.em_spctrscpy.utils.em_nexus_base_classes \
    import NxObject

from nexusparser.tools.dataconverter.readers.em_spctrscpy.utils.em_nomad_oasis_eln \
    import NxEmNomadOasisElnSchemaParser

# from nexusparser.tools.dataconverter.readers.em_spctrscpy.utils.oina.em_oina_xray \
#     import NxOinaSpectrumSetEmXray

from nexusparser.tools.dataconverter.readers.em_spctrscpy.utils.hspy.em_hspy_xray \
    import NxSpectrumSetEmXray

from nexusparser.tools.dataconverter.readers.em_spctrscpy.utils.hspy.em_hspy_eels \
    import NxSpectrumSetEmEels

from nexusparser.tools.dataconverter.readers.em_spctrscpy.utils.hspy.em_hspy_adf \
    import NxImageSetEmAdf


class NxEventDataEm:
    """Representing a data collection event with a single detector.

    During this data collection event, the microscope
    was considered stable enough.
    """

    def __init__(self, file_name: str):
        self.meta: Dict[str, NxObject] = {}
        self.meta["start_time"] = NxObject('non_recoverable')
        self.meta["end_time"] = NxObject('non_recoverable')
        self.meta["event_identifier"] = NxObject()
        self.meta["event_type"] = NxObject()
        self.meta["detector_identifier"] = NxObject()
        # ##MK::the following list is not complete
        # but brings an example how NXem can be used disentangle
        # data and processing when, at a given point in time,
        # multiple detectors have been used
        self.spectrum_set_em_xray = None
        self.spectrum_set_em_eels = None
        self.image_set_em_adf = None

        self.parse_hspy_analysis_results(file_name)

    def parse_hspy_analysis_results(self, file_name: str):
        """Parse the individual hyperspy-specific data.

        Route these respective classes of an NxEventDataEm instance.
        """
        hspy_objs = hs.load(file_name)
        # ##MK::this logic is too simplistic e.g. what if the dataset is TBs?
        # because file_name is usually the file from the microscope session...

        # developers can here switch easily one and off certain sub-parsers
        if isinstance(hspy_objs, list):
            print("Processing a list of hspy_objs...")
            self.spectrum_set_em_xray = NxSpectrumSetEmXray(hspy_objs)
            self.spectrum_set_em_eels = NxSpectrumSetEmEels(hspy_objs)
            self.image_set_em_adf = NxImageSetEmAdf(hspy_objs)
        else:
            print("Converting (a single hspy obj) into a list, processing it...")
            self.spectrum_set_em_xray = NxSpectrumSetEmXray([hspy_objs])
            self.spectrum_set_em_eels = NxSpectrumSetEmEels([hspy_objs])
            self.image_set_em_adf = NxImageSetEmAdf([hspy_objs])

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        prefix = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
        prefix += "/EVENT_DATA_EM[event_data_em_1]"

        # ##MK::dummies for now
        now = datetime.datetime.now().astimezone().isoformat()
        template[prefix + "/detector_identifier"] = now
        # self.meta["detector_identifier"].value
        # ##MK::hyperspy cannot implement per-event time stamping especially
        # not for time-zones because time data are vendor-specifically formatted
        # not always reported in which case hspy replaces missing vendor timestamps
        # with system time at runtime of the script !
        template[prefix + "/start_time"] = now
        # self.meta["start_time"].value
        template[prefix + "/end_time"] = now
        # self.meta["end_time"].value
        template[prefix + "/event_identifier"] = now
        # self.meta["event_identifier"].value
        template[prefix + "/event_type"] = now
        # self.meta["event_type"].value
        # ##MK::dummies for now end

        # if True is False:  # for development purposes to reduce nxs content
        prefix = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
        prefix += "/EVENT_DATA_EM[event_data_em_1]/"
        # ##MK::connect and compare frame_id with that of hspy
        if self.spectrum_set_em_xray is not None:
            if isinstance(self.spectrum_set_em_xray,
                          NxSpectrumSetEmXray) is True:
                self.spectrum_set_em_xray.report(prefix, 1, template)

        prefix = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
        prefix += "/EVENT_DATA_EM[event_data_em_1]/"
        if self.spectrum_set_em_eels is not None:
            if isinstance(self.spectrum_set_em_eels,
                          NxSpectrumSetEmEels) is True:
                self.spectrum_set_em_eels.report(prefix, 1, template)

        prefix = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
        prefix += "/EVENT_DATA_EM[event_data_em_1]/"
        # ##MK::connect and compare frame_id with that of hspy
        if self.image_set_em_adf is not None:
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
    # should point to an existent plot, in this example we use the
    # NxSpectrumSetEmXray stack_data instance in the first event ...

    trg = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
    trg += "/EVENT_DATA_EM[event_data_em_1]/"
    trg += "NX_SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray_1]/"
    trg += "DATA[stack]/counts"  # "DATA[stack]/counts"
    if trg in template.keys():
        assert isinstance(template[trg]["compress"], np.ndarray), \
            "EDS data which should support the default plot are not existent!"
        trg = "/ENTRY[entry]/"
        template[trg + "@default"] = "measurement"
        trg += "EVENT_DATA_EM_SET[measurement]/"
        template[trg + "@default"] = "event_data_em_1"
        trg += "EVENT_DATA_EM[event_data_em_1]/"
        template[trg + "@default"] = "spectrum_set_em_xray_1"
        trg += "NX_SPECTRUM_SET_EM[spectrum_set_em_xray_1]/"
        template[trg + "@default"] = "stack"  # "summary"  # "stack"
        return template

    # ... if the data are EELS though, we use the EELSSpectrum summary,
    # also in the first event
    trg = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
    trg += "/EVENT_DATA_EM[event_data_em_1]/"
    trg += "NX_SPECTRUM_SET_EM_EELS[spectrum_set_em_eels_1]/"
    trg += "DATA[stack]/counts"  # "DATA[stack]/counts"
    if trg in template.keys():
        assert isinstance(template[trg]["compress"], np.ndarray), \
            "EELS data which should support the default plot are not existent!"
        trg = "/ENTRY[entry]/"
        template[trg + "@default"] = "measurement"
        trg += "EVENT_DATA_EM_SET[measurement]/"
        template[trg + "@default"] = "event_data_em_1"
        trg += "EVENT_DATA_EM[event_data_em_1]/"
        template[trg + "@default"] = "spectrum_set_em_eels_1"
        trg += "NX_SPECTRUM_SET_EM_EELS[spectrum_set_em_eels_1]/"
        template[trg + "@default"] = "stack"  # "summary"  # "stack"
        return template

    # ##MK::if no stack data are available implement fallback to use or
    # compute the summary or some other mapping

    # print("WARNING::Creating the default plot found no relevant to pick!")
    return template


class EmSpctrscpyReader(BaseReader):
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
        template.clear()

        case = EmUseCaseSelector(file_paths)
        assert case.is_valid is True, \
            "Such a combination of input-file(s, if any) is not supported !"

        # nx_em_header = NxEmAppDefHeader()
        # prefix = "/ENTRY[entry]"
        # nx_em_header.report(prefix, template)

        print("Parsing numerical data and metadata with hyperspy...")
        if case.vendor_parser == 'oina':
            # oina_parser(case.vendor[0], template)
            return {}
        if case.vendor_parser == 'hspy':
            hyperspy_parser(case.vendor[0], template)
        else:
            print("No input-file defined for vendor data !")
            return {}

        print("Parsing metadata as well as numerical data from NOMAD OASIS ELN...")
        if case.eln_parser == 'nomad-oasis':
            nomad_oasis_eln_parser(case.eln[0], template)
        else:
            print("No input file defined for eln data !")
            return {}

        print("Creating default plottable data...")
        create_default_plottable_data(template)

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
READER = EmSpctrscpyReader
