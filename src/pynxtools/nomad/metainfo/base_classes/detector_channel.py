# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXdetector_channel (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXdetector_channel` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    SchemaAnnotation,
)
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
        unit="joule",
        description=("Energy at which a photon will be recorded"),
        a_nexus_field=NeXusField(
            name="threshold_energy",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
