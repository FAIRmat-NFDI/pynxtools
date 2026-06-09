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
# Run `pynx nomad generate-metainfo --nxdl NXapm_reconstruction` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["ApmReconstruction"]


class ApmReconstruction(Process):
    """
    Base class for the configuration and results of a reconstruction algorithm.

    Generating a tomographic reconstruction of the specimen uses selected and
    calibrated ion hit positions, the evaporation sequence, and voltage curve
    data. Very often scientists use own software scripts according to published
    procedures, so-called reconstruction protocols.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXapm_reconstruction",
            category="base",
            symbols={
                "n": "Number of ions spatially filtered from results of the hit_finding algorithm\n                from which an instance of a reconstructed volume has been generated.\n                These ions get new identifier assigned in the process - the so-called\n                evaporation_id, which must not be confused with the pulse_id!"
            },
        ),
    )

    program = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.program.Program",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprogram",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    note = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=True,
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    config = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_reconstruction.ApmReconstructionConfig",
        repeats=False,
        description=(
            "Parameters that configure a reconstruction algorithm which takes "
            "hit data and mass-to-charge-state ratio values to construct a model "
            "of the evaporated specimen. This model is called the reconstructed "
            "volume. Researchers in the field of atom probe call these "
            "algorithms reconstruction protocols. Different such protocols "
            "exist. Although these are qualitatively similar, each protocol uses "
            "and interprets the parameters slightly differently. The majority of "
            "reconstructions is performed with the proprietary software APSuite "
            "/ IVAS, the source code for the reconstruction protocols that this "
            "software implements in detail is not open but the parameters and "
            "their qualitative effect on the reconstructed volume follows the "
            "protocols that are discussed in the atom probe literature. This "
            "group allows to document these parameters in a standardized manner."
        ),
    )
    naive_discretization = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.process.Process",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name="naive_discretization",
            name_type="specified",
            optionality="optional",
        ),
    )
    obb = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.apm_reconstruction.ApmReconstructionObb",
        repeats=False,
        description=(
            "Tight, axis-aligned bounding box about the point cloud of the "
            "reconstruction."
        ),
    )

    reconstructed_positions = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-reconstructed-positions-field"
        ],
        dimensionality="[length]",
        shape=["*", 3],
        description=(
            "Three-dimensional positions of the ions in the reconstructed volume."
        ),
        a_nexus_field=NeXusField(
            name="reconstructed_positions",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    reconstructed_positions__depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-reconstructed-positions-depends-on-attribute"
        ],
        description=(
            "The instance of :ref:`NXcoordinate_system` in which the positions "
            "are defined."
        ),
        a_nexus_attribute=NeXusAttribute(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="reconstructed_positions",
        ),
    )
    quality = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-quality-field"
        ],
        description=(
            "Qualitative statement about the reconstruction. The value can be "
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
    volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-volume-field"
        ],
        dimensionality="[length] ** 3",
        description=(
            "Sum of ion volumes The value can be extracted from the "
            "CAnalysis.CSpatial.fRecoVolume field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )
    field_of_view = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-field-of-view-field"
        ],
        dimensionality="[length]",
        description=(
            "The nominal diameter of the specimen ROI which is measured in the "
            "experiment. The physical specimen cannot be measured completely "
            "because ions may launch but hit in locations other than the "
            "detector."
        ),
        a_nexus_field=NeXusField(
            name="field_of_view",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
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


class ApmReconstructionConfig(Parameters):
    """
    Parameters that configure a reconstruction algorithm which takes hit data
    and mass-to-charge-state ratio values to construct a model of the
    evaporated specimen. This model is called the reconstructed volume.
    Researchers in the field of atom probe call these algorithms reconstruction
    protocols.

    Different such protocols exist. Although these are qualitatively similar,
    each protocol uses and interprets the parameters slightly differently.

    The majority of reconstructions is performed with the proprietary software
    APSuite / IVAS, the source code for the reconstruction protocols that this
    software implements in detail is not open but the parameters and their
    qualitative effect on the reconstructed volume follows the protocols that
    are discussed in the atom probe literature. This group allows to document
    these parameters in a standardized manner.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXparameters",
            name="config",
            name_type="specified",
            optionality="optional",
        ),
    )

    voltage_filter_initial = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-voltage-filter-initial-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Lowest voltage at which an ion that is considered in the "
            "reconstructed volume has been extracted from the specimen."
        ),
        a_nexus_field=NeXusField(
            name="voltage_filter_initial",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    voltage_filter_final = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-voltage-filter-final-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "Highest voltage at which an ion that is considered in the "
            "reconstructed volume has been extracted from the specimen."
        ),
        a_nexus_field=NeXusField(
            name="voltage_filter_final",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    protocol_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-protocol-name-field"
        ],
        description=(
            "Qualitative statement about which reconstruction protocol was used. "
            "For reconstructions performed with APSuite / IVAS the value "
            '"cameca" should be used.'
        ),
        a_nexus_field=NeXusField(
            name="protocol_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["bas", "geiser", "gault", "cameca"],
            open_enum=True,
        ),
    )
    primary_element = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-primary-element-field"
        ],
        description=(
            "Assumed primary element based on which the reconstruction is "
            "calibrated. The value can be extracted from the "
            "CAnalysis.CSpatial.fPrimaryElement field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="primary_element",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    efficiency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-efficiency-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Assumed detection efficiency The value can be extracted from the "
            "CAnalysis.CSpatial.fEfficiency field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="efficiency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    flight_path = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-flight-path-field"
        ],
        dimensionality="[length]",
        description=(
            "Nominal flight path The value can be extracted from the "
            "CAnalysis.CSpatial.fFlightPath field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="flight_path",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    evaporation_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-evaporation-field-field"
        ],
        description=(
            "Assumed evaporation electric field The value can be extracted from "
            "the CAnalysis.CSpatial.fEvaporationField field of a CamecaRoot ROOT "
            "file."
        ),
        a_nexus_field=NeXusField(
            name="evaporation_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    image_compression = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-image-compression-field"
        ],
        dimensionality="dimensionless",
        description=(
            "Image compression factor (ICF) The value can be extracted from the "
            "CAnalysis.CSpatial.fImageCompression field of a CamecaRoot ROOT "
            "file."
        ),
        a_nexus_field=NeXusField(
            name="image_compression",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    kfactor = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-kfactor-field"
        ],
        dimensionality="dimensionless",
        description=(
            "The factor :math:`k` in :math:`R_0 = \\frac{V}{kF}` with "
            ":math:`R_0` tip_radius_zero :math:`V` the voltage and :math:`F` the "
            "evaporation field. The value can be extracted from the "
            "CAnalysis.CSpatial.fKfactor field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="kfactor",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    shank_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-shank-angle-field"
        ],
        dimensionality="[angle]",
        description=(
            "Shank angle The value can be extracted from the "
            "CAnalysis.CSpatial.fShankAngle field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="shank_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    ion_volume = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-ion-volume-field"
        ],
        dimensionality="[length] ** 3",
        description=("Assumed atomic volume"),
        a_nexus_field=NeXusField(
            name="ion_volume",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLUME",
        ),
    )
    tip_radius = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-tip-radius-field"
        ],
        dimensionality="[length]",
        description=(
            "The value can be extracted from the CAnalysis.CSpatial.fTipRadius "
            "field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="tip_radius",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    tip_radius_zero = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-tip-radius-zero-field"
        ],
        dimensionality="[length]",
        description=(
            "The value can be extracted from the CAnalysis.CSpatial.fTipRadius0 "
            "field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="tip_radius_zero",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    voltage_zero = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-voltage-zero-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 3 / [current]",
        description=(
            "The value can be extracted from the CAnalysis.CSpatial.fVoltage0 "
            "field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="voltage_zero",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_VOLTAGE",
        ),
    )
    crystallographic_calibration = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-crystallographic-calibration-field"
        ],
        description=(
            "Different strategies for crystallographic calibration of the "
            "reconstruction are possible. Therefore, we collect first such "
            "feedback before parametrizing this further. If no crystallographic "
            "calibration was performed, the field should be filled with the n/a, "
            "meaning not applied."
        ),
        a_nexus_field=NeXusField(
            name="crystallographic_calibration",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )
    comment = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-config-comment-field"
        ],
        description=(
            "Possibility of a free text field that allows to report additional "
            "details related to the reconstruction protocol. For LEAP systems "
            "and reconstructions that are performed with APSuite / IVAS see also "
            "`B. Gault et al. <https://doi.org/10.1093/mam/ozae081>_` and `T. "
            "Blum et al. <https://doi.org/10.1002/9781119227250.ch18>`_ (page "
            "371). for best practices on the reporting of metadata in atom probe "
            "tomography. The value can be extracted from the "
            "CAnalysis.CResults.fComments field of a CamecaRoot ROOT file."
        ),
        a_nexus_field=NeXusField(
            name="comment",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ApmReconstructionObb(Collection):
    """
    Tight, axis-aligned bounding box about the point cloud of the
    reconstruction.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-obb-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="obb",
            name_type="specified",
            optionality="optional",
        ),
    )

    xmin = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-obb-xmin-field"
        ],
        dimensionality="[length]",
        description=("Minimum coordinate value along the x-direction"),
        a_nexus_field=NeXusField(
            name="xmin",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    xmax = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-obb-xmax-field"
        ],
        dimensionality="[length]",
        description=("Maximum coordinate value along the x-direction"),
        a_nexus_field=NeXusField(
            name="xmax",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    ymin = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-obb-ymin-field"
        ],
        dimensionality="[length]",
        description=("Minimum coordinate value along the y-direction"),
        a_nexus_field=NeXusField(
            name="ymin",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    ymax = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-obb-ymax-field"
        ],
        dimensionality="[length]",
        description=("Maximum coordinate value along the y-direction"),
        a_nexus_field=NeXusField(
            name="ymax",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    zmin = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-obb-zmin-field"
        ],
        dimensionality="[length]",
        description=("Minimum coordinate value along the z-direction"),
        a_nexus_field=NeXusField(
            name="zmin",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    zmax = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXapm_reconstruction.html#nxapm_reconstruction-obb-zmax-field"
        ],
        dimensionality="[length]",
        description=("Maximum coordinate value along the z-direction"),
        a_nexus_field=NeXusField(
            name="zmax",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
