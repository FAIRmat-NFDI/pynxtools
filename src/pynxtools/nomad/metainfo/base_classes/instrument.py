# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXinstrument (see
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
# Run `pynx nomad generate-metainfo --nxdl NXinstrument` to regenerate.
# Hand edits are preserved across regeneration via the sidecar
# generated_manifest.json.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    SchemaAnnotation,
)
from nomad.metainfo import Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import (
    NeXusAttribute,
    NeXusDefinition,
    NeXusField,
    NeXusGroup,
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

    actuators = SubSection(
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
    apertures = SubSection(
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
    attenuators = SubSection(
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
    beams = SubSection(
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
    beam_stops = SubSection(
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
    bending_magnets = SubSection(
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
    collimators = SubSection(
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
    collections = SubSection(
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
    capillaries = SubSection(
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
    crystals = SubSection(
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
    detectors = SubSection(
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
    detector_groups = SubSection(
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
    disk_choppers = SubSection(
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
    fabrications = SubSection(
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
    fermi_choppers = SubSection(
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
    filters = SubSection(
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
    flippers = SubSection(
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
    guides = SubSection(
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
    histories = SubSection(
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
    insertion_devices = SubSection(
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
    mirrors = SubSection(
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
    moderators = SubSection(
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
    monochromators = SubSection(
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
    polarizers = SubSection(
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
    positioners = SubSection(
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
    sensors = SubSection(
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
    sources = SubSection(
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
    velocity_selectors = SubSection(
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
    xraylenses = SubSection(
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

    name = Quantity(
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    name__short_name = Quantity(
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
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
