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
# Run `pynx nomad generate-metainfo --nxdl NXibeam_column` to regenerate.
# Additive-only: the generator will never remove or rename existing class members.
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
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["IbeamColumn"]


class IbeamColumn(Component):
    """
    Base class for a set of components equipping an instrument with FIB
    capabilities.

    Focused-ion-beam (FIB) capabilities turn especially scanning electron
    microscopes into specimen preparation labs. FIB is a material preparation
    technique whereby portions of the sample are illuminated with a focused ion
    beam with controlled intensity. The beam is controlled such that it is
    intense, focused, and equipped with sufficient ion having sufficient
    momentum to remove material in a controlled manner.

    The fact that an electron microscope with FIB capabilities achieves these
    functionalities via a second component (aka the ion gun) that has its own
    relevant control circuits, focusing lenses, and other components, warrants
    the definition of an own base class to group these components and
    distinguish them from the lenses and components for creating and shaping
    the electron beam.

    For more details about the relevant physics and application examples
    consult the literature, for example:

    * `L. A. Giannuzzi et al. <https://doi.org/10.1007/b101190>`_ * `E. I.
    Preiß et al.
    <https://link.springer.com/content/pdf/10.1557/s43578-020-00045-w.pdf>`_ *
    `J. F. Ziegler et al.
    <https://www.sciencedirect.com/science/article/pii/S0168583X10001862>`_ *
    `J. Lili <https://www.osti.gov/servlets/purl/924801>`_ * `N. Yao
    <https://doi.org/10.1017/CBO9780511600302>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXibeam_column",
            category="base",
        ),
    )

    ion_source = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.ibeam_column.IbeamColumnIonSource",
        repeats=False,
        description=("The source which creates the ion beam."),
    )
    electromagnetic_lens = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.electromagnetic_lens.ElectromagneticLens",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXelectromagnetic_lens",
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
    deflector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    blankerID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.deflector.Deflector",
        repeats=True,
        variable=True,
        description=(
            "A component for blanking the ion beam or generating pulsed ion beams."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="blankerID",
            name_type="partial",
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
    beam = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.beam.Beam",
        repeats=True,
        variable=True,
        description=(
            "Individual characterization results for the position, shape, and "
            "characteristics of the ion beam. :ref:`NXtransformations` should be "
            "used to specify the location or position at which details about the "
            "ion beam are probed."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXbeam",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    component = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    scan_controller = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.scan_controller.ScanController",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXscan_controller",
            name="scan_controller",
            name_type="specified",
            optionality="optional",
        ),
    )

    operation_mode = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-operation-mode-field"
        ],
        description=(
            "Tech-partner, microscope-, and control-software-specific name of "
            "the specific operation mode how the ibeam_column and its components "
            "are controlled to achieve specific illumination conditions. In many "
            "cases the users of an instrument do not or can not be expected to "
            "know all intricate spatiotemporal dynamics of their hardware. "
            "Instead, they rely on assumptions that the instrument, its control "
            "software, and components work as expected to focus on their "
            "research questions. For these cases, having a place for documenting "
            "the operation_mode is useful in as much as at least some "
            "constraints on how the illumination conditions were is documented."
        ),
        a_nexus_field=NeXusField(
            name="operation_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class IbeamColumnIonSource(Source):
    """
    The source which creates the ion beam.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="ion_source",
            name_type="specified",
            optionality="optional",
        ),
    )

    emitter_type = Quantity(
        type=MEnum(["liquid_metal", "plasma", "gas_field", "other"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-emitter-type-field"
        ],
        description=(
            "Emitter type used to create the ion beam. If the emitter type is "
            "other, give further details in the description field."
        ),
        a_nexus_field=NeXusField(
            name="emitter_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["liquid_metal", "plasma", "gas_field", "other"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    description = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-description-field"
        ],
        description=(
            "Ideally, a (globally) unique persistent identifier, link, or text "
            "to a resource which gives further details."
        ),
        a_nexus_field=NeXusField(
            name="description",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    flux = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-flux-field"
        ],
        flexible_unit=True,
        description=("Average/nominal flux"),
        a_nexus_field=NeXusField(
            name="flux",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    brightness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-brightness-field"
        ],
        flexible_unit=True,
        description=("Average/nominal brightness"),
        a_nexus_field=NeXusField(
            name="brightness",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-current-field"
        ],
        dimensionality="[current]",
        unit="ampere",
        description=("Charge current"),
        a_nexus_field=NeXusField(
            name="current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "ampere"},
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        unit="volt",
        description=(
            "Ion acceleration voltage upon source exit and entering the vacuum "
            "flight path."
        ),
        a_nexus_field=NeXusField(
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "volt"},
    )
    ion_energy_profile = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXibeam_column.html#nxibeam_column-ion-source-ion-energy-profile-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "To be defined more specifically. Community suggestions are welcome."
        ),
        a_nexus_field=NeXusField(
            name="ion_energy_profile",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "joule"},
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
