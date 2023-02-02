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
"""Representation of an NXevent_data_em class."""

# pylint: disable=E1101

import datetime

from typing import Dict

import hyperspy.api as hs

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_nexus_base_classes \
    import NxObject

from nexusutils.dataconverter.readers.em_spctrscpy.utils.hspy.em_hspy_xray \
    import NxSpectrumSetEmXray

from nexusutils.dataconverter.readers.em_spctrscpy.utils.hspy.em_hspy_eels \
    import NxSpectrumSetEmEels

from nexusutils.dataconverter.readers.em_spctrscpy.utils.hspy.em_hspy_adf \
    import NxImageSetEmAdf


class NxEventDataEm:
    """Representing a data collection event with a single detector.

    During this data collection event, the microscope
    was considered stable enough.
    """

    def __init__(self, file_name: str, entry_id: int):
        assert file_name != "", "Argument file_name must not be empty !"
        assert entry_id > 0, "Argument entry_id has to be > 0 !"
        self.entry_id = entry_id
        self.file_name = file_name
        self.meta: Dict[str, NxObject] = {}
        self.meta["start_time"] = NxObject("non_recoverable")
        self.meta["end_time"] = NxObject("non_recoverable")
        self.meta["event_identifier"] = NxObject()
        self.meta["event_type"] = NxObject()
        self.meta["detector_identifier"] = NxObject()
        # the following list is not complete
        # but brings an example how NXem can be used disentangle
        # data and processing when, at a given point in time,
        # multiple detectors have been used
        self.spectrum_set_em_xray = NxSpectrumSetEmXray([])
        self.spectrum_set_em_eels = NxSpectrumSetEmEels([])
        self.image_set_em_adf = NxImageSetEmAdf([])

        self.parse_hspy_analysis_results()

    def parse_hspy_analysis_results(self):
        """Parse the individual hyperspy-specific data.

        Route these respective classes of an NxEventDataEm instance.
        """
        hspy_objs = hs.load(self.file_name)
        # this logic is too simplistic e.g. what if the dataset is TBs?
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
        prefix = f"/ENTRY[entry{self.entry_id}]/measurement/"
        prefix += "EVENT_DATA_EM[event_data_em1]/"

        # dummies for now
        now = datetime.datetime.now().astimezone().isoformat()
        template[prefix + "detector_identifier"] = now
        # hyperspy cannot implement per-event time stamping especially
        # not for time-zones because time data are vendor-specifically formatted
        # not always reported in which case hspy replaces missing vendor timestamps
        # with system time at runtime of the script !
        template[prefix + "start_time"] = now
        template[prefix + "end_time"] = now
        template[prefix + "event_identifier"] = now
        template[prefix + "event_type"] = now

        prefix = f"/ENTRY[entry{self.entry_id}]/measurement/"
        prefix += "EVENT_DATA_EM[event_data_em1]/"
        # connect and compare frame_id with that of hspy
        if self.spectrum_set_em_xray is not None:
            if isinstance(self.spectrum_set_em_xray,
                          NxSpectrumSetEmXray) is True:
                self.spectrum_set_em_xray.report(prefix, 1, template)

        prefix = f"/ENTRY[entry{self.entry_id}]/measurement/"
        prefix += "EVENT_DATA_EM[event_data_em1]/"
        if self.spectrum_set_em_eels is not None:
            if isinstance(self.spectrum_set_em_eels,
                          NxSpectrumSetEmEels) is True:
                self.spectrum_set_em_eels.report(prefix, 1, template)

        prefix = f"/ENTRY[entry{self.entry_id}]/measurement/"
        prefix += "EVENT_DATA_EM[event_data_em1]/"
        # connect and compare frame_id with that of hspy
        if self.image_set_em_adf is not None:
            if isinstance(self.image_set_em_adf,
                          NxImageSetEmAdf) is True:
                self.image_set_em_adf.report(prefix, 1, template)

        # add generic images

        return template
