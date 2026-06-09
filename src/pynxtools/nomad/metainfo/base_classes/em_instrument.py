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
# Run `pynx nomad generate-metainfo --nxdl NXem_instrument` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.instrument import Instrument
from pynxtools.nomad.metainfo.base_classes.manipulator import Manipulator

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EmInstrument"]


class EmInstrument(Instrument):
    """
    Base class for instrument-related details of a real or simulated electron
    microscope.

    For collecting data and experiments which are simulations of an electron
    microscope (or such session) use the :ref:`NXem` application definition and
    the :ref:`NXem_event_data` groups it provides.

    This base class implements the concept of :ref:`NXem` whereby (meta)data
    are distinguished whether these typically change during a session (dynamic)
    or not (static metadata). This design allows to store e.g. hardware related
    concepts only once instead of demanding that each image or spectrum from
    the session needs to be stored also with the static metadata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXem_instrument",
            category="base",
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
    ebeam_column = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.ebeam_column.EbeamColumn",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXebeam_column",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    ibeam_column = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.ibeam_column.IbeamColumn",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXibeam_column",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    em_optical_system = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_optical_system.EmOpticalSystem",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXem_optical_system",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector.Detector",
        repeats=True,
        variable=True,
        description=(
            "Description of the type of the detector. Electron microscopes have "
            "typically multiple detectors. Different technologies are in use "
            "like CCD, scintillator, direct electron, CMOS, or image plate to "
            "name but a few."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    stageID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.em_instrument.EmInstrumentStageID",
        repeats=True,
        variable=True,
        description=(
            "Stages in an electron microscope are multi-functional devices. "
            "Stages enable experimentalists the application of controlled "
            "external stimuli on the specimen. Modern stages realize a hierarchy "
            "of components. A multi-axial tilt rotation holder is a good example "
            "where the control of each degree of freedom is technically "
            "implemented via providing instances of e.g. :ref:`NXpositioner` or "
            ":ref:`NXactuator` that achieve the rotating and positioning of the "
            "specimen. The physical process of mounting a specimen on a stage in "
            "practice often comes with an own hierarchy of fixtures to bridge "
            "e.g. length scales technically. An example from atom probe "
            "microscopy is that researchers may work with wire samples which are "
            "clipped into a larger fixing unit to enable careful specimen "
            "handling. Alternatively, a microtip is a silicon post upon which "
            "e.g. an atom probe specimen is mounted. Multiple of such microtips "
            "are then grouped into a microtip array to conveniently enable "
            "loading of multiple specimens into the instrument with fewer "
            "operations. There are further scenarios typically encountered "
            "related to mounting and locating specimens inside an electron "
            "microscope, a few examples follow: * A nanoparticle on a copper "
            "grid. The copper grid is the holder. This grid itself is fixed to a "
            "stage. * An atom probe specimen fixed in a stub. In this case the "
            "stub can be considered the holder, while the cryostat temperature "
            "control unit is a component of the stage. * For in-situ experiments "
            "with e.g. chips with read-out electronics as actuators, the chips "
            "are again placed in a larger unit. A typical example are in-situ "
            "experiments using e.g. the tools of `Protochips "
            "<https://www.protochips.com>`_. * Other examples are (quasi) "
            "in-situ experiments where experimentalists anneal or deform the "
            "specimen via e.g. in-situ tensile testing machines which are "
            "mounted on the specimen holder. For specific details and "
            "inspiration about stages in electron microscopes: * `Holders with "
            "multiple axes <https://www.nanotechnik.com/e5as.html>`_ * "
            "`Chip-based designs "
            "<https://www.protochips.com/products/fusion/fusion-select-components/>`_ "
            "* `Further chip-based designs "
            "<https://www.nanoprobetech.com/about>`_ * `Stages in transmission "
            "electron microscopy <https://doi.org/10.1007/978-3-662-14824-2>`_ "
            "(page 103, table 4.2) * `Further stages in transmission electron "
            "microscopy <https://doi.org/10.1007/978-1-4757-2519-3>`_ (page "
            "124ff) * `Specimens in atom probe "
            "<https://doi.org/10.1007/978-1-4614-8721-0>`_ (page 47ff) * "
            "`Exemplar micro-manipulators "
            "<https://nano.oxinst.com/products/omniprobe/omniprobe-200>`_"
        ),
    )
    nanoprobeID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.manipulator.Manipulator",
        repeats=True,
        variable=True,
        description=(
            "In contrast to the stage, the nanoprobe is an additional "
            "manipulator that is a specifically frequently found component of "
            "FIB/SEM instruments. A nanoprobe is used to pick up and relocated "
            "portions of the specimen that have been cut off during "
            "site-specific lift-outs and specimen preparation."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="nanoprobeID",
            name_type="partial",
            optionality="optional",
        ),
    )
    gas_injector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
        repeats=False,
        description=(
            "Gas injection systems (GIS) are components of microscopes that are "
            "equipped with focused-ion beam capabilities. The component is used "
            "to introduce reactive neutral gases to the sample surface for "
            "enhanced etching, preferential etching, or material deposition."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="gas_injector",
            name_type="specified",
            optionality="optional",
        ),
    )
    pump = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.pump.Pump",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXpump",
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

    name_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-name-field"
        ],
        description=(
            "Given name of the microscope at the hosting institution. This is an "
            "alias. Examples could be NionHermes, Titan, JEOL, Gemini, etc."
        ),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    location = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-location-field"
        ],
        description=(
            "Location of the lab or place where the instrument is installed. "
            "Using GEOREF is preferred."
        ),
        a_nexus_field=NeXusField(
            name="location",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    type = Quantity(
        type=MEnum(["sem", "fib", "tem"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-type-field"
        ],
        description=(
            "Different types of electron microscopes exist: * sem, a scanning "
            "electron microscope without focused-ion beam capabilities * fib, a "
            "scanning electron microscope with focused-ion beam capabilities "
            "irrespective whether these were used or not * tem, a transmission "
            "electron microscope NXem is one joint data model that can be used "
            "to document research that is performed with several of these types "
            "of microscopes (SEM, TEM, or FIB). The NXem data model stresses "
            "that these types of instruments despite having several differences "
            "are still all electron beamlines with which to probe electron "
            "and/or ion matter interaction and in fact in practice have many "
            "similarities in how they are used, the components, they contain, "
            "etc. This field can be used in research data management systems for "
            "enabling a categorization or tagging of experiments without having "
            "to analyze if groups like NXibeam_column are present (which would "
            "indicate type is fib) or if certain lens configurations or "
            "instrument models are used which suggests the microscope is a "
            "scanning (sem) or transmission electron microscope (tem):"
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="recommended",
            enumeration=["sem", "fib", "tem"],
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named concept groups — only when the group element defines own quantities that
# differ from the generic class (changed optionality, extra fields, different
# type/units/enumeration). These inherit from the specific generic class so all
# base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class EmInstrumentStageID(Manipulator):
    """
    Stages in an electron microscope are multi-functional devices.

    Stages enable experimentalists the application of controlled external
    stimuli on the specimen. Modern stages realize a hierarchy of components. A
    multi-axial tilt rotation holder is a good example where the control of
    each degree of freedom is technically implemented via providing instances
    of e.g. :ref:`NXpositioner` or :ref:`NXactuator` that achieve the rotating
    and positioning of the specimen.

    The physical process of mounting a specimen on a stage in practice often
    comes with an own hierarchy of fixtures to bridge e.g. length scales
    technically. An example from atom probe microscopy is that researchers may
    work with wire samples which are clipped into a larger fixing unit to
    enable careful specimen handling. Alternatively, a microtip is a silicon
    post upon which e.g. an atom probe specimen is mounted. Multiple of such
    microtips are then grouped into a microtip array to conveniently enable
    loading of multiple specimens into the instrument with fewer operations.
    There are further scenarios typically encountered related to mounting and
    locating specimens inside an electron microscope, a few examples follow:

    * A nanoparticle on a copper grid. The copper grid is the holder. This grid
    itself is fixed to a stage. * An atom probe specimen fixed in a stub. In
    this case the stub can be considered the holder, while the cryostat
    temperature control unit is a component of the stage. * For in-situ
    experiments with e.g. chips with read-out electronics as actuators, the
    chips are again placed in a larger unit. A typical example are in-situ
    experiments using e.g. the tools of `Protochips
    <https://www.protochips.com>`_. * Other examples are (quasi) in-situ
    experiments where experimentalists anneal or deform the specimen via e.g.
    in-situ tensile testing machines which are mounted on the specimen holder.

    For specific details and inspiration about stages in electron microscopes:

    * `Holders with multiple axes <https://www.nanotechnik.com/e5as.html>`_ *
    `Chip-based designs
    <https://www.protochips.com/products/fusion/fusion-select-components/>`_ *
    `Further chip-based designs <https://www.nanoprobetech.com/about>`_ *
    `Stages in transmission electron microscopy
    <https://doi.org/10.1007/978-3-662-14824-2>`_ (page 103, table 4.2) *
    `Further stages in transmission electron microscopy
    <https://doi.org/10.1007/978-1-4757-2519-3>`_ (page 124ff) * `Specimens in
    atom probe <https://doi.org/10.1007/978-1-4614-8721-0>`_ (page 47ff) *
    `Exemplar micro-manipulators
    <https://nano.oxinst.com/products/omniprobe/omniprobe-200>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmanipulator",
            name="stageID",
            name_type="partial",
            optionality="optional",
        ),
    )

    design = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-design-field"
        ],
        description=(
            "Principal design of the stage. Exemplar terms could be side_entry, "
            "top_entry, single_tilt, quick_change, multiple_specimen, "
            "bulk_specimen, double_tilt, tilt_rotate, heating_chip, "
            "atmosphere_chip, electrical_biasing_chip, liquid_cell_chip"
        ),
        a_nexus_field=NeXusField(
            name="design",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    alias = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-alias-field"
        ],
        description=(
            "Free-text field to give a term how that a stage_lab at this level "
            "of the stage_lab hierarchy is commonly referred to. Examples could "
            "be stub, puck, carousel, microtip, clip, holder, etc."
        ),
        a_nexus_field=NeXusField(
            name="alias",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    tilt1 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-tilt1-field"
        ],
        dimensionality="[angle]",
        description=(
            "The interpretation of this tilt1 value can be contextualized via "
            "the comment attribute. However, it is better to describe the "
            "reference frame in which the tilt is defined explicitly using "
            "instances of :ref:`NXtransformations` and respective instances of "
            ":ref:`NXcoordinate_system`. Especially when this NXem_instrument "
            "base class is used in an application definition like NXem."
        ),
        a_nexus_field=NeXusField(
            name="tilt1",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    tilt1__comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-tilt1-comment-attribute"
        ],
        description=(
            "Discouraged free-text field to provide details about how to "
            "interpret tilt1."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="tilt1",
        ),
    )
    tilt2 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-tilt2-field"
        ],
        dimensionality="[angle]",
        description=(
            "The interpretation of this tilt2 value can be contextualized via "
            "the comment attribute. However, it is better to describe the "
            "reference frame in which the tilt is defined explicitly using "
            "instances of :ref:`NXtransformations` and respective instances of "
            ":ref:`NXcoordinate_system`. Especially when this NXem_instrument "
            "base class is used in an application definition like NXem."
        ),
        a_nexus_field=NeXusField(
            name="tilt2",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    tilt2__comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-tilt2-comment-attribute"
        ],
        description=(
            "Discouraged free-text field to provide details about how to "
            "interpret tilt2."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="tilt2",
        ),
    )
    rotation = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-rotation-field"
        ],
        dimensionality="[angle]",
        description=(
            "The interpretation of this rotation value can be contextualized via "
            "the comment attribute. However, it is better to describe the "
            "reference frame in which the rotation is defined explicitly using "
            "instances of :ref:`NXtransformations` and respective instances of "
            ":ref:`NXcoordinate_system`. Especially when this NXem_instrument "
            "base class is used in an application definition like NXem."
        ),
        a_nexus_field=NeXusField(
            name="rotation",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    rotation__comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-rotation-comment-attribute"
        ],
        description=(
            "Discouraged free-text field to provide details about how to "
            "interpret rotation."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="rotation",
        ),
    )
    position = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXem_instrument.html#nxem_instrument-stageid-position-field"
        ],
        dimensionality="[length]",
        shape=[3],
        description=(
            "The interpretation of these position values can be contextualized "
            "via the comment attribute. However, it is better to describe the "
            "reference frame in which the position values are defined explicitly "
            "using instances of :ref:`NXtransformations` and respective "
            "instances of :ref:`NXcoordinate_system`. Especially when this "
            "NXem_instrument base class is used in an application definition "
            "like NXem."
        ),
        a_nexus_field=NeXusField(
            name="position",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
