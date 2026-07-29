# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

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
