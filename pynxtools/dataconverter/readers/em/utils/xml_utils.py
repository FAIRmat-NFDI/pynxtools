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
"""Flatten content of an XML tree into a Python dictionary."""

from collections import OrderedDict


def flatten_xml_to_dict(xml_content) -> dict:
    """Flatten content of an XML tree into a Python dictionary."""
    # https://codereview.stackexchange.com/a/21035
    # https://stackoverflow.com/questions/38852822/how-to-flatten-xml-file-in-python
    def items():
        for key, value in xml_content.items():
            # nested subtree
            if isinstance(value, dict):
                for subkey, subvalue in flatten_xml_to_dict(value).items():
                    yield '{}.{}'.format(key, subkey), subvalue
            # nested list
            elif isinstance(value, list):
                for num, elem in enumerate(value):
                    for subkey, subvalue in flatten_xml_to_dict(elem).items():
                        yield '{}.[{}].{}'.format(key, num, subkey), subvalue
            # everything else (only leafs should remain)
            else:
                yield key, value
    return OrderedDict(items())
