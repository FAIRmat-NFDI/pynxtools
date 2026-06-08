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
# Run `pynx nomad generate-metainfo --nxdl NXinstrument` to regenerate.
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

__all__ = ["Instrument"]


class Instrument(Object):
    """
    Collection of the components of the instrument or beamline.

    Template of instrument descriptions comprising various beamline components.
    Each component will also be a NeXus group defined by its distance from the
    sample. Negative distances represent beamline components that are before
    the sample while positive distances represent components that are after the
    sample. This device allows the unique identification of beamline components
    in a way that is valid for both reactor and pulsed instrumentation.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXinstrument",
            category="base",
        ),
    )

    actuator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.actuator.Actuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXactuator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    aperture = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.aperture.Aperture",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXaperture",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    attenuator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.attenuator.Attenuator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXattenuator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    beam = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    beam_stop = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam_stop.BeamStop",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam_stop",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    bending_magnet = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.bending_magnet.BendingMagnet",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXbending_magnet",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    collimator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collimator.Collimator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollimator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    capillary = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.capillary.Capillary",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcapillary",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    crystal = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.crystal.Crystal",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcrystal",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector.Detector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    detector_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector_group.DetectorGroup",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector_group",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    disk_chopper = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.disk_chopper.DiskChopper",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdisk_chopper",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    event_data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.event_data.EventData",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXevent_data",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    fabrication = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fabrication.Fabrication",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfabrication",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    fermi_chopper = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.fermi_chopper.FermiChopper",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfermi_chopper",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    filter = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.filter.Filter",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXfilter",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    flipper = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.flipper.Flipper",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXflipper",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    guide = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.guide.Guide",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXguide",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    history = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.history.History",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXhistory",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    insertion_device = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.insertion_device.InsertionDevice",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXinsertion_device",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    mirror = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.mirror.Mirror",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmirror",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    moderator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.moderator.Moderator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmoderator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    monochromator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.monochromator.Monochromator",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    polarizer = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.polarizer.Polarizer",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpolarizer",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    positioner = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.positioner.Positioner",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpositioner",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    sensor = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.sensor.Sensor",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsensor",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    source = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.source.Source",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    DIFFRACTOMETER = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.transformations.Transformations",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXtransformations",
            name="DIFFRACTOMETER",
            name_type="specified",
            optionality="optional",
        ),
    )
    velocity_selector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.velocity_selector.VelocitySelector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXvelocity_selector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    xraylens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.xraylens.Xraylens",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXxraylens",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument-name-field"
        ],
        description=("Name of instrument"),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    name_quantity__short_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument-name-short-name-attribute"
        ],
        description=("short name for instrument, perhaps the acronym"),
        a_nexus_attribute=NeXusAttribute(
            name="short_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="name",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
