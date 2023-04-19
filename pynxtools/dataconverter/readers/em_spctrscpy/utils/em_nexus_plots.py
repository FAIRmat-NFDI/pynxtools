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
"""Parser for adding default plots and path to them to template."""

# pylint: disable=E1101

import numpy as np

# ##MK::for EDS use the spectrum stack, the more generic, the more complex
# ##MK::the logic has to be to infer a default plottable
# when using hyperspy and EDS data, the path to the default plottable
# should point to an existent plot, in this example we use the
# NxSpectrumSetEmXray stack_data instance in the first event ...
# default plot selection preference in decreasing order of relevance
# ebsd > xray > eels > adf > bse, se
# spectrum_set_ebsd: ipf > overview > stack
# spectrum_set_xray: stack > summary > overview
# spectrum_set_eels: stack > summary > overview
# image_set_adf: overview
# image_set_se/bse: overview


def xray_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance for Xray."""
    entry_name = "entry" + str(entry_id)
    trg = "/ENTRY[" + entry_name + "]/measurement/EVENT_DATA_EM[event_data_em1]/"
    trg += "SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray1]/"

    path = ""
    if trg + "stack/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[trg + "stack/DATA[data_counts]"]["compress"], np.ndarray), \
            "EDS data stack not existent!"
        path = "stack"
    if trg + "summary/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[trg + "summary/DATA[data_counts]"]["compress"], np.ndarray), \
            "EDS data summary not existent!"
        path = "summary"

    if path != "":
        print("Found xray default plot for entry " + entry_name + " at " + path)
        trg = "/"
        template[trg + "@default"] = entry_name
        trg += "ENTRY[" + entry_name + "]/"
        template[trg + "@default"] = "measurement"
        trg += "measurement/"
        template[trg + "@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[trg + "@default"] = "spectrum_set_em_xray1"
        trg += "SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray1]/"
        template[trg + "@default"] = path
        return True

    return False


def eels_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance for EELS."""
    entry_name = "entry" + str(entry_id)
    trg = "/ENTRY[" + entry_name + "]/measurement/EVENT_DATA_EM[event_data_em1]/"
    trg += "SPECTRUM_SET_EM_EELS[spectrum_set_em_eels1]/"

    path = ""
    if trg + "stack/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[trg + "stack/DATA[data_counts]"]["compress"], np.ndarray), \
            "EELS data stack not existent!"
        path = "stack"
    if trg + "summary/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[trg + "summary/DATA[data_counts]"]["compress"], np.ndarray), \
            "EELS data summary not existent!"
        path = "summary"

    if path != "":
        print("Found eels default plot for entry " + entry_name + " at " + path)
        trg = "/"
        template[trg + "@default"] = entry_name
        trg += "ENTRY[" + entry_name + "]/"
        template[trg + "@default"] = "measurement"
        trg += "measurement/"
        template[trg + "@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[trg + "@default"] = "spectrum_set_em_eels1"
        trg += "SPECTRUM_SET_EM_EELS[spectrum_set_em_eels1]/"
        template[trg + "@default"] = path
        return True

    return False


def adf_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance for ADF."""
    entry_name = "entry" + str(entry_id)
    trg = "/ENTRY[" + entry_name + "]/measurement/EVENT_DATA_EM[event_data_em1]/"
    trg += "IMAGE_SET_EM_ADF[image_set_em_adf1]/"

    path = ""
    if trg + "stack/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[trg + "stack/DATA[data_counts]"]["compress"], np.ndarray), \
            "ADF data stack not existent!"
        path = "stack"

    if path != "":
        print("Found adf default plot for entry " + entry_name + " at " + path)
        trg = "/"
        template[trg + "@default"] = entry_name
        trg += "ENTRY[" + entry_name + "]/"
        template[trg + "@default"] = "measurement"
        trg += "measurement/"
        template[trg + "@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[trg + "@default"] = "image_set_em_adf1"
        trg += "IMAGE_SET_EM_ADF[image_set_em_adf1]/"
        template[trg + "@default"] = path
        return True

    return False


def image_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance for generic image."""
    entry_name = "entry" + str(entry_id)
    trg = "/ENTRY[" + entry_name + "]/measurement/EVENT_DATA_EM[event_data_em1]/"
    trg += "IMAGE_SET_EM[image_set_em1]/"

    path = ""
    if trg + "stack/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[trg + "stack/DATA[data_counts]"]["compress"], np.ndarray), \
            "Generic image data stack not existent!"
        path = "stack"

    if path != "":
        print("Found image default plot for entry " + entry_name + " at " + path)
        trg = "/"
        template[trg + "@default"] = entry_name
        trg += "ENTRY[" + entry_name + "]/"
        template[trg + "@default"] = "measurement"
        trg += "measurement/"
        template[trg + "@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[trg + "@default"] = "image_set_em1"
        trg += "IMAGE_SET_EM[image_set_em1]/"
        template[trg + "@default"] = path
        return True

    return False


def em_spctrscpy_default_plot_generator(template: dict, n_entries: int) -> dict:  # ignore:R0915
    """For a valid NXS file at least one default plot is required."""

    for entry_id in np.arange(1, n_entries + 1):
        # by convention showing always the first entry of an NXevent_data_em

        # add ebsd

        if xray_plot_available(template, entry_id) is True:
            continue

        if eels_plot_available(template, entry_id) is True:
            continue

        if adf_plot_available(template, entry_id) is True:
            continue

        # add bse, se

        if image_plot_available(template, entry_id) is True:
            continue

        print("WARNING: No path to a default plot found for entry" + str(entry_id) + "!")

    return template
