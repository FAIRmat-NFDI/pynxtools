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
# Run `pynx nomad generate-metainfo --nxdl NXapm_measurement` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

from nomad.metainfo import MEnum, Quantity, Section, SubSection

from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.object import Object

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmMeasurement"]


class ApmMeasurement(Object):
    """
    Base class for collecting a run with a real or a simulated atom probe or
    field-ion microscope.

    The term run is understood as an exact synonym for session, i.e. the usage
    of a real or simulated tomograph or microscope for a certain amount of time
    during which one characterizes a single specimen.

    Research workflows for experiments and simulations of atom probe and
    related field-evaporation evolve continuously and become increasingly
    connected with other methods used for material characterization
    specifically electron microscopy. A few examples in this direction are:

    * `T. Kelly et al. <https://doi.org/10.1017/S1431927620022205>`_ * `C.
    Fleischmann et al. <https://doi.org/10.1016/j.ultramic.2018.08.010>`_ * `W.
    Windl et al. <https://doi.org/10.1093/micmic/ozad067.294>`_ * `C. Freysoldt
    et al. <https://doi.org/10.1103/PhysRevLett.124.176801>`_ * `G. da Costa et
    al. <https://doi.org/10.1038/s41467-024-54169-2>`_

    The majority of atom probe research is performed using the so-called Local
    Electrode Atom Probe (LEAP) instruments from AMETEK/Cameca. In addition,
    several research groups have built their own instruments and shared
    different aspects of the technical specifications and approaches including
    how these groups apply data processing e.g.:

    * `M. Monajem et al. <https://doi.org/10.1017/S1431927622003397>`_ * `P.
    Stender et al. <https://doi.org/10.1017/S1431927621013982>`_ * `I. Dimkou
    et al. <https://doi.org/10.1093/micmic/ozac051>`_

    to name but a few.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_measurement.html#nxapm_measurement"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_measurement",
            category="base",
        ),
    )

    apm_instrument = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_instrument.ApmInstrument",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_instrument",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    apm_event_data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_event_data.ApmEventData",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXapm_event_data",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    status = Quantity(
        type=MEnum(["success", "aborted"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_measurement.html#nxapm_measurement-status-field"
        ],
        description=(
            "A statement whether the measurement completed successfully, or was "
            "aborted."
        ),
        a_nexus_field=NeXusField(
            name="status",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["success", "aborted"],
        ),
    )
    quality = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_measurement.html#nxapm_measurement-quality-field"
        ],
        description=(
            "Statement about the quality of the measurement. The value can be "
            "extracted from the CAnalysis.CResults.fQuality field of a "
            "CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="quality",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
