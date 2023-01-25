#!/usr/bin/env python3
"""Parser for adding default plots and path to them to template."""

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

import numpy as np


def em_spctrscpy_default_plot_generator(template: dict) -> dict:
    """For a valid NXS file at least one default plot is required."""
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

    # add ebsd

    trg = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
    trg += "/EVENT_DATA_EM[event_data_em1]/"
    trg += "NX_SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray1]/DATA"
    endpoint = ""
    if trg + "[stack]/counts" in template.keys():
        assert isinstance(template[trg + "[stack]/counts"]["compress"], np.ndarray), \
            "EDS data stack not existent!"
        endpoint = "stack"
    if trg + "[summary]/counts" in template.keys():
        assert isinstance(template[trg + "[summary]/counts"]["compress"], np.ndarray), \
            "EDS data summary not existent!"
        endpoint = "summary"
    if endpoint != "":  # one exists, so build path
        print("Found xray default data plot endpoint named " + endpoint)
        trg = "/ENTRY[entry]/"
        template[trg + "@default"] = "measurement"
        trg += "EVENT_DATA_EM_SET[measurement]/"
        template[trg + "@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[trg + "@default"] = "spectrum_set_em_xray1"
        trg += "NX_SPECTRUM_SET_EM[spectrum_set_em_xray1]/"
        template[trg + "@default"] = endpoint
        return template

    trg = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
    trg += "/EVENT_DATA_EM[event_data_em1]/"
    trg += "NX_SPECTRUM_SET_EM_EELS[spectrum_set_em_eels1]/DATA"
    endpoint = ""
    if trg + "[stack]/counts" in template.keys():
        assert isinstance(template[trg + "[stack]/counts"]["compress"], np.ndarray), \
            "EELS data stack not existent!"
        endpoint = "stack"
    if trg + "[summary]/counts" in template.keys():
        assert isinstance(template[trg + "[summary]/counts"]["compress"], np.ndarray), \
            "EELS data summary not existent!"
        endpoint = "summary"
    if endpoint != "":
        print("Found eels default data plot endpoint named " + endpoint)
        trg = "/ENTRY[entry]/"
        template[trg + "@default"] = "measurement"
        trg += "EVENT_DATA_EM_SET[measurement]/"
        template[trg + "@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[trg + "@default"] = "spectrum_set_em_eels1"
        trg += "NX_SPECTRUM_SET_EM_EELS[spectrum_set_em_eels1]/"
        template[trg + "@default"] = "stack"
        return template

    trg = "/ENTRY[entry]/EVENT_DATA_EM_SET[measurement]"
    trg += "/EVENT_DATA_EM[event_data_em1]/"
    trg += "NX_IMAGE_SET_EM_ADF[image_set_em_adf1]/DATA"
    endpoint = ""
    if trg + "[adf]/intensity" in template.keys():
        assert isinstance(template[trg + "[adf]/intensity"]["compress"], np.ndarray), \
            "ADF data intensity not existent!"
        endpoint = "intensity"
    if endpoint != "":
        print("Found adf default data plot endpoint named " + endpoint)
        trg = "/ENTRY[entry]/"
        template[trg + "@default"] = "measurement"
        trg += "EVENT_DATA_EM_SET[measurement]/"
        template[trg + "@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[trg + "@default"] = "image_set_em_adf1"
        trg += "NX_IMAGE_SET_EM_ADF[image_set_em_adf1]/"
        template[trg + "@default"] = "intensity"
        return template

    # bse, se

    print("WARNING: No relevant endpoint found which could point to a default plot!")
    return template
