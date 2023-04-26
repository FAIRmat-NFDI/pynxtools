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
"""Logic for annotating existent default plots in NXdata for NXem_ebsd for H5Web."""

# pylint: disable=no-member

HFIVE_WEB_MAX_SIZE = 2048


def roi_plot_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance either the ROI or IPF map."""
    # most interesting to show are three-dimensional orientation mappings ...
    trg = f"/ENTRY[entry{entry_id}]/correlation/region_of_interest/roi/data"
    if trg in template.keys():
        print(f"Found image default plot for entry{entry_id}")
        trg = "/"
        template[f"{trg}@default"] = f"entry{entry_id}"
        trg += f"ENTRY[entry{entry_id}]/"
        template[f"{trg}@default"] = "correlation"
        trg += "correlation/"
        template[f"{trg}@default"] = "region_of_interest"
        trg += "region_of_interest/"
        template[f"{trg}@default"] = "roi"
        return True

    # fall-back display an IPF mapping
    trg = f"/ENTRY[entry{entry_id}]/correlation/PROCESS[ipf_map1]/ipf_rgb_map/data"
    # by definition if there is one it will be always the first one and we use this IPF map
    if trg in template.keys():
        print(f"Found image default plot for entry{entry_id}")
        trg = "/"
        template[f"{trg}@default"] = f"entry{entry_id}"
        trg += f"ENTRY[entry{entry_id}]/"
        template[f"{trg}@default"] = "correlation"
        trg += "correlation/"
        template[f"{trg}@default"] = "ipf_map1"
        trg += "PROCESS[ipf_map1]/"
        template[f"{trg}@default"] = "ipf_rgb_map"
        return True

    # ... but in most practical cases we have two-dimensional EBSD maps only...
    trg = f"/ENTRY[entry{entry_id}]/experiment/indexing/region_of_interest/roi/data"
    if trg in template.keys():
        print(f"Found image default plot for entry{entry_id}")
        trg = "/"
        template[f"{trg}@default"] = f"entry{entry_id}"
        trg += f"ENTRY[entry{entry_id}]/"
        template[f"{trg}@default"] = "experiment"
        trg += "experiment/"
        template[f"{trg}@default"] = "indexing"
        trg += "indexing/"
        template[f"{trg}@default"] = "region_of_interest"
        return True

    # fall-back display an IPF mapping
    trg = f"/ENTRY[entry{entry_id}]/experiment/indexing" \
          f"/PROCESS[ipf_map1]/ipf_rgb_map/data"
    # by definition if there is one it will be always the first one and we use this IPF map
    if trg in template.keys():
        print(f"Found image default plot for entry{entry_id}")
        trg = "/"
        template[f"{trg}@default"] = f"entry{entry_id}"
        trg += f"ENTRY[entry{entry_id}]/"
        template[f"{trg}@default"] = "experiment"
        trg += "experiment/"
        template[f"{trg}@default"] = "indexing"
        trg += "indexing/"
        template[f"{trg}@default"] = "ipf_map1"
        trg += "PROCESS[ipf_map1]/"
        template[f"{trg}@default"] = "ipf_rgb_map"
        return True

    return False


def diffraction_pattern_available(template: dict, entry_id: int) -> bool:
    """Choose a preferred NXdata/data instance diffraction pattern."""
    trg = f"/ENTRY[entry{entry_id}]/simulation/IMAGE_SET_EM_KIKUCHI" \
          f"[image_set_em_kikuchi]/stack/data_counts"
    if trg in template.keys():
        print(f"Found image default plot for entry{entry_id}")
        trg = "/"
        template[f"{trg}@default"] = f"entry{entry_id}"
        trg += f"ENTRY[entry{entry_id}]/"
        template[f"{trg}@default"] = "simulation"
        trg += "simulation/"
        template[f"{trg}@default"] = "image_set_em_kikuchi"
        trg += "image_set_em_kikuchi/"
        template[f"{trg}@default"] = "stack"
        return True

    return False


def em_om_default_plot_generator(template: dict, entry_id: int) -> dict:
    """Identify and annotate default plot."""
    # prefer to show the region-of-interest overview as the default plot
    # if this does not exist, try to find one of the IPF color mappings
    if roi_plot_available(template, entry_id) is True:
        return template

    if diffraction_pattern_available(template, entry_id) is True:
        return template

    print(f"WARNING: No path to a default plot found for entry{entry_id} !")
    return template
