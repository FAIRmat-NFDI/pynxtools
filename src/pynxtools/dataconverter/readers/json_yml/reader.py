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
"""A reader for YAML/JSON-based ELN and config data, built on MultiFormatReader.

.. deprecated::
    ``YamlJsonReader`` is deprecated and will be removed in a future release.
    Use ``MultiFormatReader`` directly instead — it provides identical
    functionality with no additional overhead.
"""

import logging
import warnings

from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader

logger = logging.getLogger("pynxtools")

_DEPRECATION_MSG = (
    "YamlJsonReader is deprecated and will be removed in a future release. "
    "Use MultiFormatReader directly instead."
)


class YamlJsonReader(MultiFormatReader):
    """
    .. deprecated::
        Use ``MultiFormatReader`` directly.

    A thin alias for ``MultiFormatReader`` with no additional behavior.
    All functionality is inherited unchanged.
    """

    supported_nxdls: list[str] = ["*"]

    def __init__(self, *args, **kwargs):
        logger.warning(_DEPRECATION_MSG)
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)


READER = YamlJsonReader
