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
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nx-class NXdetector_channel` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import (
    NeXusAttribute,
    NeXusChoice,
    NeXusDefinition,
    NeXusField,
    NeXusGroup,
    NeXusLink,
)
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["DetectorChannel"]


class DetectorChannel(Object):
    """
    Description and metadata for a single channel from a multi-channel
    detector.

    Given an :ref:`NXdata` group linked as part of an NXdetector group that has
    an axis with named channels (see the example in :ref:`NXdata
    </NXdata@default_slice-attribute>`), the NXdetector will have a series of
    NXdetector_channel groups, one for each channel, named CHANNELNAME_channel.

    Example, given these axes in the NXdata group::

    @axes = ["image_id", "channel", ".", "."]

    And this list of channels in the NXdata group::

    channel = ["threshold_1", "threshold_2", "difference"]

    The NXdetector group would have three NXdetector_channel groups::

    detector:NXdetector ... threshold_1_channel:NXdetector_channel
    threshold_energy = float flatfield = float[i, j] pixel_mask = uint[i, j]
    flatfield_applied = bool pixel_mask_applied = bool
    threshold_2_channel:NXdetector_channel threshold_energy = float flatfield =
    float[i, j] pixel_mask = uint[i, j] flatfield_applied = bool
    pixel_mask_applied = bool difference_channel:NXdetector_channel
    threshold_energy = float[2]
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdetector_channel",
            category="base",
            symbols={
                "dataRank": "Rank of the ``data`` field associated with this detector",
                "nP": "number of scan points",
                "i": "number of detector pixels in the slowest direction",
                "j": "number of detector pixels in the second slowest direction",
                "k": "number of detector pixels in the third slowest direction",
            },
        ),
    )

    threshold_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-threshold-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        description=("Energy at which a photon will be recorded"),
        a_nexus_field=NeXusField(
            name="threshold_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
    )
    flatfield_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-flatfield-applied-field"
        ],
        description=(
            "True when the flat field correction has been applied in the "
            "electronics, false otherwise."
        ),
        a_nexus_field=NeXusField(
            name="flatfield_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    flatfield = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-flatfield-field"
        ],
        description=("Response of each pixel given a constant input"),
        a_nexus_field=NeXusField(
            name="flatfield",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    flatfield_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-flatfield-errors-field"
        ],
        shape=["*", "*"],
        description=(
            "Errors of the flat field correction data. The form flatfield_error "
            "is deprecated."
        ),
        a_nexus_field=NeXusField(
            name="flatfield_errors",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    pixel_mask_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-pixel-mask-applied-field"
        ],
        description=(
            "True when the pixel mask correction has been applied in the "
            "electronics, false otherwise."
        ),
        a_nexus_field=NeXusField(
            name="pixel_mask_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    pixel_mask = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-pixel-mask-field"
        ],
        description=(
            "Custom pixel mask for this channel. May include nP as the first "
            "dimension for masks that vary for each scan point."
        ),
        a_nexus_field=NeXusField(
            name="pixel_mask",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    saturation_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-saturation-value-field"
        ],
        description=(
            "The value at which the detector goes into saturation. Especially "
            "common to CCD detectors, the data is known to be invalid above this "
            "value. For example, given a saturation_value and an "
            "underload_value, the valid pixels are those less than or equal to "
            "the saturation_value and greater than or equal to the "
            "underload_value. The precise type should match the type of the "
            "data."
        ),
        a_nexus_field=NeXusField(
            name="saturation_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    underload_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector_channel.html#nxdetector_channel-underload-value-field"
        ],
        description=(
            "The lowest value at which pixels for this detector would be "
            "reasonably measured. The data is known to be invalid below this "
            "value. For example, given a saturation_value and an "
            "underload_value, the valid pixels are those less than or equal to "
            "the saturation_value and greater than or equal to the "
            "underload_value. The precise type should match the type of the "
            "data."
        ),
        a_nexus_field=NeXusField(
            name="underload_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
