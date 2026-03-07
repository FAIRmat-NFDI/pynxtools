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
"""A reader for YAML/JSON-based ELN and config data, built on MultiFormatReader."""

from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader


class YamlJsonReader(MultiFormatReader):
    """
    A reader that dispatches YAML/JSON files to per-extension handlers.

    Subclasses define self.extensions in __init__ to map file suffixes to
    handler callables. All pipeline logic (file dispatch, template creation,
    config-file processing, logging) is inherited from MultiFormatReader.
    """

    supported_nxdls: list[str] = []


READER = YamlJsonReader
