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
# Run `pynx nomad generate-metainfo --nxdl NXem_event_data` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
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

__all__ = ["EmEventData"]


class EmEventData(Object):
    """
    Base class to store state and (meta)data of events for electron microscopy.

    Event-related (meta)data, typically measured datasets like images and
    spectra. To avoid repetitively storing static instrument-related metadata,
    the dynamic (meta)data that typically changes for each image and spectrum
    is split from the static (meta)data.

    Which temporal granularity is adequate to log events depends on the
    situation and research question. Using a model which enables a collection
    of events offers the most flexible way to cater for both experiments with
    controlled electron beams in a real microscope or the simulation of such
    experiments or individual aspects of such experiments.

    Electron microscopes are dynamic. Scientists often report that microscopes
    *perform differently* across sessions. That *they* perform differently from
    one day or another. In some cases, root causes for performance differences
    are unclear. Users of the instrument may consider such conditions
    impractical, or *too poor*, and thus abort their session. Alternatively,
    users may try to bring the microscope into a state where conditions are
    considered better or of whatever high enough quality for starting or
    continuing the measurement.

    In all these use cases it is useful to have a mechanism whereby
    time-dependent data of the instrument state can be stored and documented in
    an representation that facilitates interoperability. This is the idea
    behind this base class.

    :ref:`NXem_event_data` represents an instance to describe and serialize
    flexibly whatever is considered a time interval during which the instrument
    is considered stable enough for allowing any working on tasks with it.
    Examples of such tasks are the collecting of data (images and spectra) or
    the calibrating the instrument or individual of its components. Users may
    wish to take only a single scan or image and complete their session
    thereafter. Alternatively, users are working for much longer time at the
    instrument, perform recalibrations in between and take several scans (of
    different ROIs on the specimen), or they explore the state of the
    microscope for service or maintenance tasks.

    :ref:`NXem_event_data` serves the harmonization and documentation of these
    cases:

    * Firstly, via a header section whose purpose is to contextualize and
    identify the event instance in time. * Secondly, via a data and metadata
    section where individual data collections can be stored in a standardized
    representation.

    We are aware of the fact that given the variety how an electron microscope
    is used, there is a need for a flexible and adaptive documentation system.
    At the same time we are also convinced though that just because one has
    different requirements for some specific aspect under the umbrella of
    settings to an electron microscope, this does not necessarily warrant that
    one has to cook up an own data schema.

    Instead, the electron microscopy community should work towards reusing
    schema components as frequently as possible. This will enable that there is
    at all not only a value of harmonizing electron microscopy research content
    but also there is a technical possibility to build services around such
    harmonized data.

    Arguably it is oftentimes tricky to specify a clear time interval when the
    microscope is *stable enough*. Take for instance the acquisition of an
    image or a stack of spectra. Having to deal with instabilities is a common
    theme in electron microscopy practice. Numerical protocols can be used
    during data post-processing to correct for some of the instabilities. A few
    exemplar references provide an overview on the subject:

    * `C. Ophus et al. <https://dx.doi.org/10.1016/j.ultramic.2015.12.002>`_ *
    `B. Berkels et al. <https://doi.org/10.1016/j.ultramic.2018.12.016>`_ * `L.
    Jones et al.
    <https://link.springer.com/article/10.1186/s40679-015-0008-4>`_

    For specific simulation purposes, mainly in an effort to digitally repeat
    or simulate the experiment (digital twin), it is tempting to consider
    dynamics of the instrument, implemented as time-dependent functional
    descriptions of e.g. lens excitations, beam shape functions, trajectories
    of groups of electrons and ions, or detector noise models. This also
    warrants to document the time-dependent details of individual components of
    the microscope via the here implemented class :ref:`NXem_event_data`.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_event_data.html#nxem_event_data"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_event_data",
            category="base",
        ),
    )

    user = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.user.User",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    em_instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_instrument.EmInstrument",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_instrument",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    image = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.Image",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXimage",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    spectrum = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.spectrum.Spectrum",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXspectrum",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_event_data.html#nxem_event_data-start-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the snapshot time interval started. If users wish to "
            "specify an interval of time that the snapshot should represent "
            "during which the instrument was stable and configured using "
            "specific settings and calibrations, the start_time is the start "
            "(left bound of the time interval) while the end_time specifies the "
            "end (right bound) of the time interval."
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    end_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_event_data.html#nxem_event_data-end-time-field"
        ],
        description=(
            "ISO 8601 time code with local time zone offset to UTC information "
            "included when the snapshot time interval ended."
        ),
        a_nexus_field=NeXusField(
            name="end_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
    )
    identifier_event = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_event_data.html#nxem_event_data-identifier-event-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Identifier of a specific state and setting of the microscope."),
        a_nexus_field=NeXusField(
            name="identifier_event",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    identifier_sample = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_event_data.html#nxem_event_data-identifier-sample-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("The name of the sample to resolve ambiguities."),
        a_nexus_field=NeXusField(
            name="identifier_sample",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_event_data.html#nxem_event_data-type-field"
        ],
        description=(
            "Which specific event/measurement type. Examples are: * "
            "In-lens/backscattered electron, usually has quadrants * "
            "Secondary_electron, image, topography, fractography, overview "
            "images * Backscattered_electron, image, Z or channeling contrast "
            "(ECCI) * Bright_field, image, TEM * Dark_field, image, crystal "
            "defects * Annular dark field, image (medium- or high-angle), TEM * "
            "Diffraction, image, TEM, or a comparable technique in the SEM * "
            "Kikuchi, image, SEM EBSD and TEM diffraction * X-ray spectra "
            "(point, line, surface, volume), composition EDS/EDX(S) * Electron "
            "energy loss spectra for points, lines, surfaces, TEM * Auger, "
            "spectrum, (low Z contrast element composition) * "
            "Cathodoluminescence (optical spectra) * Ronchigram, image, "
            "alignment utility specifically in TEM * Chamber, e.g. TV camera "
            "inside the chamber, education purposes. This field may also be used "
            "for storing additional information about the event for which there "
            "is at the moment no other place. In the long run such free-text "
            "field description should be avoided as it is difficult to "
            "machine-interpret. Instead, an enumeration should be used."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
