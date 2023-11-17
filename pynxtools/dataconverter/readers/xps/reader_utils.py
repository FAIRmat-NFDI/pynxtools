"""
Helper functions for populating NXmpes template
"""
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

def construct_data_key(spectrum):
    """
    Construct a key for the 'data' field of the xps_dict.
    Output example: cycle0_scan0.

    """
    if 'loop_no' in spectrum:
        cycle_key = f'cycle{spectrum["loop_no"]}'
    else:
        cycle_key = 'cycle0'

    if 'scan_no' in spectrum:
        scan_key = f'scan{spectrum["scan_no"]}'
    else:
        scan_key = 'scan0'

    return f'{cycle_key}_{scan_key}'


def construct_detector_data_key(spectrum):
    """
    Construct a key for the detector data fields of the xps_dict.
    Output example: 'cycles/Cycle_0/scans/Scan_0'

    """
    if 'loop_no' in spectrum:
        cycle_key = f'cycles/Cycle_{spectrum["loop_no"]}'
    else:
        cycle_key = 'cycles/Cycle_0'

    if 'scan_no' in spectrum:
        scan_key = f'scans/Scan_{spectrum["scan_no"]}'
    else:
        scan_key = 'scans/Scan_0'

    return f'{cycle_key}/{scan_key}'


def construct_entry_name(key):
    """Construction entry name."""
    key_parts = key.split("/")
    try:
        # entry example : vendor__sample__name_of_scan_region
        entry_name = (f'{key_parts[2]}'
                      f'__'
                      f'{key_parts[3].split("_", 1)[1]}'
                      f'__'
                      f'{key_parts[5].split("_", 1)[1]}'
                      )
    except IndexError:
        entry_name = ""
    return entry_name