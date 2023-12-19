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
"""Utilities for working with NeXus concepts encoded as Python dicts in the concepts dir."""

# pylint: disable=no-member

import pytz

from datetime import datetime


def load_from_modifier(terms, fd_dct):
    """Implement modifier which reads values of different type from fd_dct."""
    if isinstance(terms, str):
        if terms in fd_dct.keys():
            return fd_dct[terms]
    if all(isinstance(entry, str) for entry in terms) is True:
        if isinstance(terms, list):
            lst = []
            for entry in terms:
                lst.append(fd_dct[entry])
            return lst
    return None


def convert_iso8601_modifier(terms, dct: dict):
    """Implement modifier which transforms nionswift time stamps to proper UTC ISO8601."""
    if terms is not None:
        if isinstance(terms, str):
            if terms in dct.keys():
                return None
        elif (isinstance(terms, list)) and (len(terms) == 2) \
                and (all(isinstance(entry, str) for entry in terms) is True):
            # assume the first argument is a local time
            # assume the second argument is a timezone string
            if terms[0] in dct.keys() and terms[1] in dct.keys():
                # handle the case that these times can be arbitrarily formatted
                # for now we let ourselves be guided
                # by how time stamps are returned in Christoph Koch's
                # nionswift instances also formatting-wise
                date_time_str = dct[terms[0]].replace("T", " ")
                time_zone_str = dct[terms[1]]
                if time_zone_str in pytz.all_timezones:
                    date_time_obj \
                        = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
                    utc_time_zone_aware \
                        = pytz.timezone(time_zone_str).localize(date_time_obj)
                    return utc_time_zone_aware
                else:
                    raise ValueError('Invalid timezone string!')
                return None
        else:
            return None
    return None


def apply_modifier(modifier, dct: dict):
    """Interpret a functional mapping using data from dct via calling modifiers."""
    if isinstance(modifier, dict):
        # different commands are available
        if set(["fun", "terms"]) == set(modifier.keys()):
            if modifier["fun"] == "load_from":
                return load_from_modifier(modifier["terms"], dct)
            if modifier["fun"] == "convert_iso8601":
                return convert_iso8601_modifier(modifier["terms"], dct)
        else:
            print(f"WARNING::Modifier {modifier} is currently not implemented !")
            # elif set(["link"]) == set(modifier.keys()), with the jsonmap reader Sherjeel conceptualized "link"
            return None
    if isinstance(modifier, str):
        return modifier
    return None


# examples/tests how to use modifiers
# modd = "µs"
# modd = {"link": "some_link_to_somewhere"}
# modd = {"fun": "load_from", "terms": "metadata/scan/scan_device_properties/mag_boards/MagBoard 1 DAC 11"}
# modd = {"fun": "load_from", "terms": ["metadata/scan/scan_device_properties/mag_boards/MagBoard 1 DAC 11",
#     "metadata/scan/scan_device_properties/mag_boards/MagBoard 1 Relay"]}
# modd = {"fun": "convert_iso8601", "terms": ["data_modified", "timezone"]}
# print(apply_modifier(modd, yml))

def variadic_path_to_specific_path(path, instance_identifier: list):
    """Transforms a variadic path to an actual path with instances."""
    if (path is not None) and (path != ""):
        narguments = path.count("*")
        if narguments == 0:  # path is not variadic
            return path
        if len(instance_identifier) >= narguments:
            tmp = path.split("*")
            if len(tmp) == narguments + 1:
                nx_specific_path = ""
                for idx in range(0, narguments):
                    nx_specific_path += f"{tmp[idx]}{instance_identifier[idx]}"
                    idx += 1
                nx_specific_path += f"{tmp[-1]}"
                return nx_specific_path
    return None
