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

# pylint: disable=no-member

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
    entry_name = f"entry{entry_id}"
    trg = f"/ENTRY[{entry_name}]/measurement/" \
          f"EVENT_DATA_EM[event_data_em1]/xray/"

    path = ""
    if f"{trg}stack/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[f"{trg}stack/DATA[data_counts]"]["compress"], np.ndarray), \
            "EDS data stack not existent!"
        path = "stack"
    if f"{trg}summary/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[f"{trg}summary/DATA[data_counts]"]["compress"], np.ndarray), \
            "EDS data summary not existent!"
        path = "summary"

    if path != "":
        print(f"Found xray default plot for {entry_name} at {path}")
        trg = "/"
        template[f"{trg}@default"] = entry_name
        trg = f"/ENTRY[{entry_name}]/"
        template[f"{trg}@default"] = "measurement"
        trg += "measurement/"
        template[f"{trg}@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[f"{trg}@default"] = "xray"
        trg += "xray/"
        template[f"{trg}@default"] = path
        return True

    return False


def eels_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance for EELS."""
    entry_name = f"entry{entry_id}"
    trg = f"/ENTRY[{entry_name}]/measurement/" \
          f"EVENT_DATA_EM[event_data_em1]/eels/"

    path = ""
    if f"{trg}stack/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[f"{trg}stack/DATA[data_counts]"]["compress"], np.ndarray), \
            "EELS data stack not existent!"
        path = "stack"
    if f"{trg}summary/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[f"{trg}summary/DATA[data_counts]"]["compress"], np.ndarray), \
            "EELS data summary not existent!"
        path = "summary"

    if path != "":
        print(f"Found eels default plot for {entry_name} at {path}")
        trg = "/"
        template[f"{trg}@default"] = entry_name
        trg = f"/ENTRY[{entry_name}]/"
        template[f"{trg}@default"] = "measurement"
        trg += "measurement/"
        template[f"{trg}@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[f"{trg}@default"] = "eels"
        trg += "eels/"
        template[f"{trg}@default"] = path
        return True

    return False


def adf_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance for ADF."""
    entry_name = f"entry{entry_id}"
    trg = f"/ENTRY[{entry_name}]/measurement/" \
          f"EVENT_DATA_EM[event_data_em1]/adf/"

    path = ""
    if f"{trg}stack/DATA[data_counts]" in template.keys():
        assert isinstance(
            template[f"{trg}stack/DATA[data_counts]"]["compress"], np.ndarray), \
            "ADF data stack not existent!"
        path = "stack"

    if path != "":
        print(f"Found adf default plot for entry {entry_name} at {path}")
        trg = "/"
        template[f"{trg}@default"] = entry_name
        trg = f"/ENTRY[{entry_name}]/"
        template[f"{trg}@default"] = "measurement"
        trg += "measurement/"
        template[f"{trg}@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[f"{trg}@default"] = "adf"
        trg += "adf/"
        template[f"{trg}@default"] = path
        return True

    return False


def image_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance for generic image."""
    entry_name = f"entry{entry_id}"
    trg = f"/ENTRY[{entry_name}]/measurement/EVENT_DATA_EM[event_data_em1]/" \
          f"IMAGE_SET[image_set1]/"

    path = ""
    if f"{trg}DATA[stack]/data_counts" in template.keys():
        assert isinstance(
            template[f"{trg}DATA[stack]/data_counts"]["compress"], np.ndarray), \
            "Generic image data stack not existent!"
        path = "stack"

    if path != "":
        print(f"Found image default plot for {entry_name} at {path}")
        trg = "/"
        template[f"{trg}@default"] = entry_name
        trg = f"/ENTRY[{entry_name}]/"
        template[f"{trg}@default"] = "measurement"
        trg += "measurement/"
        template[f"{trg}@default"] = "event_data_em1"
        trg += "EVENT_DATA_EM[event_data_em1]/"
        template[f"{trg}@default"] = "image_set1"
        trg += "IMAGE_SET[image_set1]/"
        template[f"{trg}@default"] = path
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

        print(f"WARNING: No path to a default plot found for entry{entry_id} !")

    return template
