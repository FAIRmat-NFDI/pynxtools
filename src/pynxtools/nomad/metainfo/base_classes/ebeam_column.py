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
# Run `pynx nomad generate-metainfo --nx-class NXebeam_column` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.component import Component
from pynxtools.nomad.metainfo.base_classes.monochromator import Monochromator
from pynxtools.nomad.metainfo.base_classes.source import Source

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["EbeamColumn"]


class EbeamColumn(Component):
    """
    Base class for a set of components providing a controllable electron beam.

    The idea behind defining :ref:`NXebeam_column` as an own base class vs.
    adding these concepts in :ref:`NXem_instrument` is that the electron beam
    generating component might be worthwhile to use also in other types of
    experiments.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXebeam_column",
            category="base",
        ),
    )

    electron_source = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.ebeam_column.EbeamColumnElectronSource",
        repeats=False,
        description=(
            "A physical part of an electron or ion microscope from which the "
            "particles that form the beam are emitted. The hardware for an "
            "electron source in an electron microscope may contain several "
            "components which affect the beam path. This concept is related to "
            "term `Source`_ of the EMglossary standard. .. _Source: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000045"
        ),
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
            "A component for blanking the beam or generating pulsed electron "
            "beams. See e.g . `I. G. C. Weppelman et al. "
            "<https://doi.org/10.1016/j.ultramic.2017.10.002>`_ or `Y. Liao "
            "<https://www.globalsino.com/EM/page2464.html>`_ for details."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdeflector",
            name="blankerID",
            name_type="partial",
            optionality="optional",
        ),
    )
    monochromator = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.ebeam_column.EbeamColumnMonochromator",
        repeats=True,
        variable=True,
        description=(
            "Device to improve energy resolution or chromatic aberration. "
            "Examples are Wien, $\\textalpha$-, or $\\Omega$- energy filter or "
            "`cc corrector like "
            "<https://www.ceos-gmbh.de/en/basics/cc-corrector>`_"
        ),
    )
    corrector_cs = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.corrector_cs.CorrectorCs",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcorrector_cs",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    corrector_ax = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.ebeam_column.EbeamColumnCorrectorAx",
        repeats=False,
        description=(
            "Component that reshapes an ellipse-shaped electron beam into a "
            "circular one. * `L. Reimer 1998, Springer, 1998 "
            "<https://dx.doi.org/10.1007/978-3-540-3896>`_ * `M. Tanaka et al., "
            "Electron Microscopy Glossary, 2024 "
            "<https://www.jeol.com/words/semterms/20201020.111014.php#gsc.tab=0>`_ "
            "Stigmator is an exact synonym."
        ),
    )
    biprismID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.component.Component",
        repeats=True,
        variable=True,
        description=("Electron biprism as it is used e.g. for electron holography."),
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="biprismID",
            name_type="partial",
            optionality="optional",
        ),
    )
    phaseplateID = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.ebeam_column.EbeamColumnPhaseplateID",
        repeats=True,
        variable=True,
        description=(
            "Device that causes a change in the phase of an electron wave. * `M. "
            "Malac et al. <https://doi.org/10.1093/jmicro/dfaa070>`_ * `R. R. "
            "Schröder et al. <https://www.lem.kit.edu/152.php>`_"
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
            "characteristics of the electron beam at a given location. "
            ":ref:`NXtransformations` should be used to specify the location or "
            "the position at which details about the beam were probed. This "
            "concept is related to term `Electron Beam`_ of the EMglossary "
            "standard. .. _Electron Beam: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000021"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-operation-mode-field"
        ],
        description=(
            "Tech-partner, microscope-, and control-software-specific name of "
            "the specific operation mode how the ebeam_column and its components "
            "are controlled to achieve specific illumination conditions. In many "
            "cases the users of an instrument do not or can not be expected to "
            "know all intricate spatiotemporal dynamics of their hardware. "
            "Instead, they rely on assumptions that the instrument, its control "
            "software, and components work as expected to focus on their "
            "research questions. For these cases, having a place for documenting "
            "the operation_mode is useful in as much as at least some "
            "constraints on how the illumination conditions were is documented."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="operation_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
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


class EbeamColumnElectronSource(Source):
    """
    A physical part of an electron or ion microscope from which the particles
    that form the beam are emitted.

    The hardware for an electron source in an electron microscope may contain
    several components which affect the beam path.

    This concept is related to term `Source`_ of the EMglossary standard.

    .. _Source: https://purls.helmholtz-metadaten.de/emg/EMG_00000045
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXsource",
            name="electron_source",
            name_type="specified",
            optionality="optional",
        ),
    )

    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "The potential difference between anode and cathode. This concept is "
            "related to term `Acceleration Voltage`_ of the EMglossary standard. "
            ".. _Acceleration Voltage: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000004"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    extraction_voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-extraction-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Voltage which is used to create an electric field that draws "
            "particles from the source. This concept is related to term "
            "`Extraction Voltage`_ of the EMglossary standard. .. _Extraction "
            "Voltage: https://purls.helmholtz-metadaten.de/emg/EMG_00000025"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="extraction_voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    emission_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-emission-current-field"
        ],
        dimensionality="[current]",
        description=(
            "Electrical current which is released from the source. This concept "
            "is related to term `Emission Current`_ of the EMglossary standard. "
            ".. _Emission Current: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000025"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="emission_current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    filament_current = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-filament-current-field"
        ],
        dimensionality="[current]",
        description=(
            "Electrical current which flows through the source. This concept is "
            "related to term `Filament Current`_ of the EMglossary standard. .. "
            "_Filament Current: "
            "https://purls.helmholtz-metadaten.de/emg/EMG_00000027"
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="filament_current",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_CURRENT",
        ),
    )
    probe = Quantity(
        type=MEnum(["electron"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-probe-field"
        ],
        description=("Type of radiation."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="probe",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["electron"],
        ),
    )
    emitter_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-emitter-type-field"
        ],
        description=(
            "Emitter type used to create the beam. If the emitter type is other, "
            "give further details in the description field."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="emitter_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    emitter_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-emitter-material-field"
        ],
        description=(
            "Material of which the emitter is build, e.g. the filament material."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="emitter_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    lifetime = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-electron-source-lifetime-field"
        ],
        dimensionality="[time]",
        description=("How long has the source been in operation."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="lifetime",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EbeamColumnMonochromator(Monochromator):
    """
    Device to improve energy resolution or chromatic aberration.

    Examples are Wien, $\textalpha$-, or $\\Omega$- energy filter or `cc
    corrector like <https://www.ceos-gmbh.de/en/basics/cc-corrector>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-monochromator-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXmonochromator",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(
            [
                "wien",
                "alfa",
                "omega",
                "castaing_henry",
                "gatan_imaging",
                "sector_analyzer",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-monochromator-type-field"
        ],
        description=("Qualitative type of the component."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "wien",
                "alfa",
                "omega",
                "castaing_henry",
                "gatan_imaging",
                "sector_analyzer",
            ],
        ),
    )
    applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-monochromator-applied-field"
        ],
        description=("Was the corrector used?"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
    )
    dispersion = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-monochromator-dispersion-field"
        ],
        description=("Energy dispersion in e.g. µm/eV."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="dispersion",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    voltage = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-monochromator-voltage-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=("Corresponding voltage for that energy dispersion."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="voltage",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EbeamColumnCorrectorAx(Component):
    """
    Component that reshapes an ellipse-shaped electron beam into a circular
    one.

    * `L. Reimer 1998, Springer, 1998
    <https://dx.doi.org/10.1007/978-3-540-3896>`_ * `M. Tanaka et al., Electron
    Microscopy Glossary, 2024
    <https://www.jeol.com/words/semterms/20201020.111014.php#gsc.tab=0>`_

    Stigmator is an exact synonym.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-corrector-ax-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="corrector_ax",
            name_type="specified",
            optionality="optional",
        ),
    )

    value_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-corrector-ax-value-x-field"
        ],
        description=(
            "Descriptor for the correction strength along the first direction "
            "when exact technical details are unknown or not directly "
            "controllable as the control software of the microscope does not "
            "enable or was not configured to display these values for users."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="value_x",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    value_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-corrector-ax-value-y-field"
        ],
        description=(
            "Descriptor for the correction strength along the second direction "
            "when exact technical details are unknown or not directly "
            "controllable as the control software of the microscope does not "
            "enable or was not configured to display these values for users."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="value_y",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EbeamColumnPhaseplateID(Component):
    """
    Device that causes a change in the phase of an electron wave.

    * `M. Malac et al. <https://doi.org/10.1093/jmicro/dfaa070>`_ * `R. R.
    Schröder et al. <https://www.lem.kit.edu/152.php>`_
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-phaseplateid-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXcomponent",
            name="phaseplateID",
            name_type="partial",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXebeam_column.html#nxebeam_column-phaseplateid-type-field"
        ],
        description=("Qualitative type"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["thin_film", "electrostatic"],
            open_enum=True,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
