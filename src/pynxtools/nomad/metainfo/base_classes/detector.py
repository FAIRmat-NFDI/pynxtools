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
# Run `pynx nomad generate-metainfo --nxdl NXdetector` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
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
from pynxtools.nomad.metainfo.base_classes.data import Data

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Detector"]


class Detector(Component):
    """
    A detector, detector bank, or multidetector.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXdetector",
            category="base",
            symbols={
                "nP": "number of scan points (only present in scanning measurements)",
                "i": "number of detector pixels in the first (slowest) direction",
                "j": "number of detector pixels in the second (faster) direction",
                "k": "number of detector pixels in the third (if necessary, fastest) direction",
                "tof": "number of bins in the time-of-flight histogram",
            },
        ),
    )

    geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.geometry.Geometry",
        repeats=True,
        variable=True,
        description=("Position and orientation of detector"),
        a_nexus_group=NeXusGroup(
            nx_class="NXgeometry",
            name=None,
            name_type="any",
            optionality="optional",
            deprecated="Use the field `depends_on` and :ref:`NXtransformations` to position the detector and NXoff_geometry to describe its shape instead",
        ),
    )
    CHANNELNAME_channel = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector_channel.DetectorChannel",
        repeats=True,
        variable=True,
        description=(
            "Group containing the description and metadata for a single channel "
            "from a multi-channel detector. Given an :ref:`NXdata` group linked "
            "as part of an NXdetector group that has an axis with named channels "
            "(see the example in :ref:`NXdata "
            "</NXdata@default_slice-attribute>`), the NXdetector will have a "
            "series of NXdetector_channel groups, one for each channel, named "
            "CHANNELNAME_channel."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector_channel",
            name="CHANNELNAME_channel",
            name_type="partial",
            optionality="optional",
        ),
    )
    efficiency = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector.DetectorEfficiency",
        repeats=False,
        description=("Spectral efficiency of detector with respect to e.g. wavelength"),
    )
    calibration_method = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=(
            "summary of conversion of array data to pixels (e.g. polynomial "
            "approximations) and location of details of the calibrations"
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="calibration_method",
            name_type="specified",
            optionality="optional",
        ),
    )
    data_file = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="data_file",
            name_type="specified",
            optionality="optional",
        ),
    )
    collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=True,
        variable=True,
        description=(
            "Use this group to provide other data related to this NXdetector group."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )
    detector_module = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector_module.DetectorModule",
        repeats=True,
        variable=True,
        description=(
            "For use in special cases where the data in NXdetector is "
            "represented in several parts, each with a separate geometry."
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector_module",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    time_of_flight = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-time-of-flight-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=("Total time of flight"),
        a_nexus_field=NeXusField(
            name="time_of_flight",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME_OF_FLIGHT",
        ),
    )
    time_of_flight__axis = Quantity(
        type=MEnum(["3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-time-of-flight-axis-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="axis",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="time_of_flight",
            enumeration=["3"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="3",
        ),
    )
    time_of_flight__primary = Quantity(
        type=MEnum(["1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-time-of-flight-primary-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="primary",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="time_of_flight",
            enumeration=["1"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="1",
        ),
    )
    time_of_flight__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-time-of-flight-long-name-attribute"
        ],
        description=("Total time of flight"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="time_of_flight",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    raw_time_of_flight = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-raw-time-of-flight-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*"],
        description=("In DAQ clock pulses"),
        a_nexus_field=NeXusField(
            name="raw_time_of_flight",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_PULSES",
        ),
    )
    raw_time_of_flight__frequency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-raw-time-of-flight-frequency-attribute"
        ],
        description=("Clock frequency in Hz"),
        a_nexus_attribute=NeXusAttribute(
            name="frequency",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            parent_field="raw_time_of_flight",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    detector_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-detector-number-field"
        ],
        description=(
            "Identifier for detector (pixels) Can be multidimensional, if needed"
        ),
        a_nexus_field=NeXusField(
            name="detector_number",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    data_quantity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-data-field"
        ],
        shape=["*", "*", "*", "*"],
        description=(
            "Data values from the detector. The rank and dimension ordering "
            "should follow a principle of slowest to fastest measurement axes "
            "and may be explicitly specified in application definitions. "
            "Mechanical scanning of objects (e.g. sample position/angle, "
            "incident beam energy, etc) tends to be the slowest part of an "
            "experiment and so any such scan axes should be allocated to the "
            "first dimensions of the array. Note that in some cases it may be "
            "useful to represent a 2D set of scan points as a single scan-axis "
            "in the data array, especially if the scan pattern doesn't fit a "
            "rectangular array nicely. Repetition of an experiment in a time "
            "series tends to be used similar to a slow scan axis and so will "
            "often be in the first dimension of the data array. The next fastest "
            "axes are typically the readout of the detector. A point detector "
            "will not add any dimensions (as it is just a single value per scan "
            "point) to the data array, a strip detector will add one dimension, "
            "an imaging detector will add two dimensions (e.g. X, Y axes) and "
            "detectors outputting higher dimensional data will add the "
            "corresponding number of dimensions. Note that the detector "
            "dimensions don't necessarily have to be written in order of the "
            "actual readout speeds - the slowest to fastest rule principle is "
            "only a guide. Finally, detectors that operate in a time-of-flight "
            "mode, such as a neutron spectrometer or a silicon drift detector "
            "(used for X-ray fluorescence) tend to have their dimension(s) added "
            "to the last dimensions in the data array. The type of each "
            "dimension should should follow the order of scan points, detector "
            "pixels, then time-of-flight (i.e. spectroscopy, spectrometry). The "
            "rank and dimension sizes (see symbol list) shown here are merely "
            "illustrative of coordination between related datasets."
        ),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    data_quantity__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-data-long-name-attribute"
        ],
        description=("Title of measurement"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="data",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    data_quantity__check_sum = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-data-check-sum-attribute"
        ],
        description=("Integral of data as check of data integrity"),
        a_nexus_attribute=NeXusAttribute(
            name="check_sum",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            parent_field="data",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    data_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-data-errors-field"
        ],
        shape=["*", "*", "*", "*"],
        description=(
            "The best estimate of the uncertainty in the data value (array size "
            "should match the data field). Where possible, this should be the "
            "standard deviation, which has the same units as the data. The form "
            "data_error is deprecated."
        ),
        a_nexus_field=NeXusField(
            name="data_errors",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    x_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-x-pixel-offset-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "Offset from the detector center in x-direction. Can be "
            "multidimensional when needed."
        ),
        a_nexus_field=NeXusField(
            name="x_pixel_offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    x_pixel_offset__axis = Quantity(
        type=MEnum(["1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-x-pixel-offset-axis-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="axis",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="x_pixel_offset",
            enumeration=["1"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="1",
        ),
    )
    x_pixel_offset__primary = Quantity(
        type=MEnum(["1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-x-pixel-offset-primary-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="primary",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="x_pixel_offset",
            enumeration=["1"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="1",
        ),
    )
    x_pixel_offset__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-x-pixel-offset-long-name-attribute"
        ],
        description=("x-axis offset from detector center"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="x_pixel_offset",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    y_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-y-pixel-offset-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "Offset from the detector center in the y-direction. Can be "
            "multidimensional when different values are required for each pixel."
        ),
        a_nexus_field=NeXusField(
            name="y_pixel_offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y_pixel_offset__axis = Quantity(
        type=MEnum(["2"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-y-pixel-offset-axis-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="axis",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="y_pixel_offset",
            enumeration=["2"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="2",
        ),
    )
    y_pixel_offset__primary = Quantity(
        type=MEnum(["1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-y-pixel-offset-primary-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="primary",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="y_pixel_offset",
            enumeration=["1"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="1",
        ),
    )
    y_pixel_offset__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-y-pixel-offset-long-name-attribute"
        ],
        description=("y-axis offset from detector center"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="y_pixel_offset",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    z_pixel_offset = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-z-pixel-offset-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "Offset from the detector center in the z-direction. Can be "
            "multidimensional when different values are required for each pixel."
        ),
        a_nexus_field=NeXusField(
            name="z_pixel_offset",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    z_pixel_offset__axis = Quantity(
        type=MEnum(["3"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-z-pixel-offset-axis-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="axis",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="z_pixel_offset",
            enumeration=["3"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="3",
        ),
    )
    z_pixel_offset__primary = Quantity(
        type=MEnum(["1"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-z-pixel-offset-primary-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="primary",
            type="NX_POSINT",
            name_type="specified",
            optionality="optional",
            parent_field="z_pixel_offset",
            enumeration=["1"],
            deprecated="see: https://github.com/nexusformat/definitions/issues/436",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="1",
        ),
    )
    z_pixel_offset__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-z-pixel-offset-long-name-attribute"
        ],
        description=("y-axis offset from detector center"),
        a_nexus_attribute=NeXusAttribute(
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="z_pixel_offset",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    distance = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-distance-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*", "*"],
        description=(
            "This is the distance to the previous component in the instrument; "
            "most often the sample. The usage depends on the nature of the "
            "detector: Most often it is the distance of the detector assembly. "
            "But there are irregular detectors. In this case the distance must "
            "be specified for each detector pixel. Note, it is recommended to "
            "use NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="distance",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    polar_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-polar-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", "*", "*"],
        description=(
            "This is the polar angle of the detector towards the previous "
            "component in the instrument; most often the sample. The usage "
            "depends on the nature of the detector. Most often it is the "
            "polar_angle of the detector assembly. But there are irregular "
            "detectors. In this case, the polar_angle must be specified for each "
            "detector pixel. Note, it is recommended to use NXtransformations "
            "instead."
        ),
        a_nexus_field=NeXusField(
            name="polar_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    azimuthal_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-azimuthal-angle-field"
        ],
        dimensionality="[angle]",
        unit="radian",
        shape=["*", "*", "*"],
        description=(
            "This is the azimuthal angle angle of the detector towards the "
            "previous component in the instrument; most often the sample. The "
            "usage depends on the nature of the detector. Most often it is the "
            "azimuthal_angle of the detector assembly. But there are irregular "
            "detectors. In this case, the azimuthal_angle must be specified for "
            "each detector pixel. Note, it is recommended to use "
            "NXtransformations instead."
        ),
        a_nexus_field=NeXusField(
            name="azimuthal_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANGLE",
        ),
    )
    description_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-description-field"
        ],
        description=("name/manufacturer/model/etc. information"),
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
    serial_number = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-serial-number-field"
        ],
        description=("Serial number for the detector"),
        a_nexus_field=NeXusField(
            name="serial_number",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    local_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-local-name-field"
        ],
        description=("Local name for the detector"),
        a_nexus_field=NeXusField(
            name="local_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    solid_angle = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-solid-angle-field"
        ],
        dimensionality="[angle] ** 2",
        unit="steradian",
        shape=["*", "*"],
        description=("Solid angle subtended by the detector at the sample"),
        a_nexus_field=NeXusField(
            name="solid_angle",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_SOLID_ANGLE",
        ),
    )
    x_pixel_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-x-pixel-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "Size of each detector pixel. If it is scalar all pixels are the same size."
        ),
        a_nexus_field=NeXusField(
            name="x_pixel_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    y_pixel_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-y-pixel-size-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*"],
        description=(
            "Size of each detector pixel. If it is scalar all pixels are the same size"
        ),
        a_nexus_field=NeXusField(
            name="y_pixel_size",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
    )
    dead_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-dead-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*", "*", "*"],
        description=("Detector dead time"),
        a_nexus_field=NeXusField(
            name="dead_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    gas_pressure = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-gas-pressure-field"
        ],
        dimensionality="[mass] / [length] / [time] ** 2",
        unit="pascal",
        shape=["*", "*"],
        description=("Detector gas pressure"),
        a_nexus_field=NeXusField(
            name="gas_pressure",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_PRESSURE",
        ),
    )
    detection_gas_path = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-detection-gas-path-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("maximum drift space dimension"),
        a_nexus_field=NeXusField(
            name="detection_gas_path",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    crate = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-crate-field"
        ],
        shape=["*", "*"],
        description=("Crate number of detector"),
        a_nexus_field=NeXusField(
            name="crate",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    crate__local_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-crate-local-name-attribute"
        ],
        description=("Equivalent local term"),
        a_nexus_attribute=NeXusAttribute(
            name="local_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="crate",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    slot = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-slot-field"
        ],
        shape=["*", "*"],
        description=("Slot number of detector"),
        a_nexus_field=NeXusField(
            name="slot",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    slot__local_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-slot-local-name-attribute"
        ],
        description=("Equivalent local term"),
        a_nexus_attribute=NeXusAttribute(
            name="local_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="slot",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    input = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-input-field"
        ],
        shape=["*", "*"],
        description=("Input number of detector"),
        a_nexus_field=NeXusField(
            name="input",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    input__local_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-input-local-name-attribute"
        ],
        description=("Equivalent local term"),
        a_nexus_attribute=NeXusAttribute(
            name="local_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="input",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-type-field"
        ],
        description=(
            "Description of type such as He3 gas cylinder, He3 PSD, "
            "scintillator, fission chamber, proportion counter, ion chamber, "
            "ccd, pixel, image plate, CMOS, ..."
        ),
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    real_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-real-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*", "*", "*"],
        description=(
            "Real-time of the exposure (use this if exposure time varies for "
            "each array element, otherwise use ``count_time`` field). Most often "
            "there is a single real time value that is constant across an entire "
            "image frame. In such cases, only a 1-D array is needed. But there "
            "are detectors in which the real time changes per pixel. In that "
            "case, more than one dimension is needed. Therefore the rank of this "
            "field should be less than or equal to (detector rank + 1)."
        ),
        a_nexus_field=NeXusField(
            name="real_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    start_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-start-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "start time for each frame, with the ``start`` attribute as absolute "
            "reference"
        ),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    start_time__start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-start-time-start-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="start_time",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    stop_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-stop-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "stop time for each frame, with the ``start`` attribute as absolute "
            "reference"
        ),
        a_nexus_field=NeXusField(
            name="stop_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    stop_time__start = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-stop-time-start-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="start",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
            parent_field="stop_time",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    calibration_date = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-calibration-date-field"
        ],
        description=(
            "date of last calibration (geometry and/or efficiency) measurements"
        ),
        a_nexus_field=NeXusField(
            name="calibration_date",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    layout = Quantity(
        type=MEnum(["point", "linear", "area"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-layout-field"
        ],
        description=("How the detector is represented"),
        a_nexus_field=NeXusField(
            name="layout",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["point", "linear", "area"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    count_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-count-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=("Elapsed actual counting time"),
        a_nexus_field=NeXusField(
            name="count_time",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    sequence_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-sequence-number-field"
        ],
        shape=["*"],
        description=(
            "In order to properly sort the order of the images taken in (for "
            "example) a tomography experiment, a sequence number is stored with "
            "each image."
        ),
        a_nexus_field=NeXusField(
            name="sequence_number",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    beam_center_x = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-beam-center-x-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the x position where the direct beam would hit the "
            "detector. This is a length and can be outside of the actual "
            "detector. The length can be in physical units or pixels as "
            "documented by the units attribute."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_x",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    beam_center_y = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-beam-center-y-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "This is the y position where the direct beam would hit the "
            "detector. This is a length and can be outside of the actual "
            "detector. The length can be in physical units or pixels as "
            "documented by the units attribute."
        ),
        a_nexus_field=NeXusField(
            name="beam_center_y",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    frame_start_number = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-frame-start-number-field"
        ],
        description=(
            "This is the start number of the first frame of a scan. In protein "
            "crystallography measurements one often scans a couple of frames on "
            "a give sample, then does something else, then returns to the same "
            "sample and scans some more frames. Each time with a new data file. "
            "This number helps concatenating such measurements."
        ),
        a_nexus_field=NeXusField(
            name="frame_start_number",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    diameter = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-diameter-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("The diameter of a cylindrical detector"),
        a_nexus_field=NeXusField(
            name="diameter",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    acquisition_mode = Quantity(
        type=MEnum(
            [
                "gated",
                "triggered",
                "summed",
                "event",
                "histogrammed",
                "decimated",
                "pulse counting",
            ]
        ),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-acquisition-mode-field"
        ],
        description=("The acquisition mode of the detector."),
        a_nexus_field=NeXusField(
            name="acquisition_mode",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[
                "gated",
                "triggered",
                "summed",
                "event",
                "histogrammed",
                "decimated",
                "pulse counting",
            ],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    angular_calibration_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-angular-calibration-applied-field"
        ],
        description=(
            "True when the angular calibration has been applied in the "
            "electronics, false otherwise."
        ),
        a_nexus_field=NeXusField(
            name="angular_calibration_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    angular_calibration = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-angular-calibration-field"
        ],
        shape=["*", "*"],
        description=("Angular calibration data."),
        a_nexus_field=NeXusField(
            name="angular_calibration",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    flatfield_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-flatfield-applied-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-flatfield-field"
        ],
        shape=["*", "*"],
        description=("Flat field correction data."),
        a_nexus_field=NeXusField(
            name="flatfield",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    flatfield_errors = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-flatfield-errors-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-pixel-mask-applied-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-pixel-mask-field"
        ],
        shape=["*", "*"],
        description=(
            "The 32-bit pixel mask for the detector. Can be either one mask for "
            "the whole dataset (i.e. an array with indices i, j) or each frame "
            "can have its own mask (in which case it would be an array with "
            "indices np, i, j). Contains a bit field for each pixel to signal "
            "dead, blind or high or otherwise unwanted or undesirable pixels. "
            "They have the following meaning: .. can't make a table here, a "
            "bullet list will have to do for now * bit 0: gap (pixel with no "
            "sensor) * bit 1: dead * bit 2: under responding * bit 3: over "
            "responding * bit 4: noisy * bit 5: -undefined- * bit 6: pixel is "
            "part of a cluster of problematic pixels (bit set in addition to "
            "others) * bit 7: -undefined- * bit 8: user defined mask (e.g. "
            "around beamstop) * bits 9-30: -undefined- * bit 31: virtual pixel "
            "(corner pixel with interpolated value) Normal data analysis "
            "software would not take pixels into account when a bit in (mask & "
            "0x0000FFFF) is set. Tag bit in the upper two bytes would indicate "
            "special pixel properties that normally would not be a sole reason "
            "to reject the intensity value (unless lower bits are set. If the "
            "full bit depths is not required, providing a mask with fewer bits "
            "is permissible. If needed, additional pixel masks can be specified "
            "by including additional entries named pixel_mask_N, where N is an "
            "integer. For example, a general bad pixel mask could be specified "
            "in pixel_mask that indicates noisy and dead pixels, and an "
            "additional pixel mask from experiment-specific shadowing could be "
            "specified in pixel_mask_2. The cumulative mask is the bitwise OR of "
            "pixel_mask and any pixel_mask_N entries."
        ),
        a_nexus_field=NeXusField(
            name="pixel_mask",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    image_key = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-image-key-field"
        ],
        shape=["*"],
        description=(
            "This field allow to distinguish different types of exposure to the "
            'same detector "data" field. Some techniques require frequent '
            "(re-)calibration inbetween measurements and this way of recording "
            "the different measurements preserves the chronological order with "
            "is important for correct processing. This is used for example in "
            "tomography (:ref:`NXtomo`) sample projections, dark and flat "
            "images, a magic number is recorded per frame. The key is as "
            "follows: * projection (sample) = 0 * flat field = 1 * dark field = "
            "2 * invalid = 3 * background (no sample, but buffer where "
            "applicable) = 4 In cases where the data is of type :ref:`NXlog` "
            "this can also be an NXlog."
        ),
        a_nexus_field=NeXusField(
            name="image_key",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
    )
    countrate_correction_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-countrate-correction-applied-field"
        ],
        description=(
            "Counting detectors usually are not able to measure all incoming "
            "particles, especially at higher count-rates. Count-rate correction "
            "is applied to account for these errors. True when count-rate "
            "correction has been applied, false otherwise."
        ),
        a_nexus_field=NeXusField(
            name="countrate_correction_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    countrate_correction_lookup_table = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-countrate-correction-lookup-table-field"
        ],
        shape=["*"],
        description=(
            "The countrate_correction_lookup_table defines the LUT used for "
            "count-rate correction. It maps a measured count :math:`c` to its "
            "corrected value :math:`countrate\\_correction\\_lookup\\_table[c]`. "
            ":math:`m` denotes the length of the table."
        ),
        a_nexus_field=NeXusField(
            name="countrate_correction_lookup_table",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
    )
    virtual_pixel_interpolation_applied = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-virtual-pixel-interpolation-applied-field"
        ],
        description=(
            "True when virtual pixel interpolation has been applied, false "
            "otherwise. When virtual pixel interpolation is applied, values of "
            "some pixels may contain interpolated values. For example, to "
            "account for space between readout chips on a module, physical "
            "pixels on edges and corners between chips may have larger sensor "
            "areas and counts may be distributed between their logical pixels."
        ),
        a_nexus_field=NeXusField(
            name="virtual_pixel_interpolation_applied",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    bit_depth_readout = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-bit-depth-readout-field"
        ],
        description=(
            "How many bits the electronics reads per pixel. With CCD's and "
            "single photon counting detectors, this must not align with "
            "traditional integer sizes. This can be 4, 8, 12, 14, 16, ..."
        ),
        a_nexus_field=NeXusField(
            name="bit_depth_readout",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    detector_readout_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-detector-readout-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Time it takes to read the detector (typically milliseconds). This "
            "is important to know for time resolved experiments."
        ),
        a_nexus_field=NeXusField(
            name="detector_readout_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    trigger_delay_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-trigger-delay-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Time it takes to start exposure after a trigger signal has been "
            "received. This is the reaction time of the detector firmware after "
            "receiving the trigger signal to when the detector starts to acquire "
            "the exposure, including any user set delay.. This is important to "
            "know for time resolved experiments."
        ),
        a_nexus_field=NeXusField(
            name="trigger_delay_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    trigger_delay_time_set = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-trigger-delay-time-set-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=("User-specified trigger delay."),
        a_nexus_field=NeXusField(
            name="trigger_delay_time_set",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    trigger_internal_delay_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-trigger-internal-delay-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Time it takes to start exposure after a trigger signal has been "
            "received. This is the reaction time of the detector hardware after "
            "receiving the trigger signal to when the detector starts to acquire "
            "the exposure. It forms the lower boundary of the trigger_delay_time "
            "when the user does not request an additional delay."
        ),
        a_nexus_field=NeXusField(
            name="trigger_internal_delay_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    trigger_dead_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-trigger-dead-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        description=(
            "Time during which no new trigger signal can be accepted. Typically "
            "this is the trigger_delay_time + exposure_time + readout_time. This "
            "is important to know for time resolved experiments."
        ),
        a_nexus_field=NeXusField(
            name="trigger_dead_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "second"},
    )
    frame_time = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-frame-time-field"
        ],
        dimensionality="[time]",
        unit="second",
        shape=["*"],
        description=(
            "This is time for each frame. This is exposure_time + readout time."
        ),
        a_nexus_field=NeXusField(
            name="frame_time",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_TIME",
        ),
    )
    gain_setting = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-gain-setting-field"
        ],
        description=(
            "The gain setting of the detector. This is a detector-specific value "
            "meant to document the gain setting of the detector during data "
            "collection, for detectors with multiple available gain settings. "
            "Examples of gain settings include: * ``standard`` * ``fast`` * "
            "``auto`` * ``high`` * ``medium`` * ``low`` * ``mixed high to "
            "medium`` * ``mixed medium to low`` Developers are encouraged to use "
            "one of these terms, or to submit additional terms to add to the "
            "list."
        ),
        a_nexus_field=NeXusField(
            name="gain_setting",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    saturation_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-saturation-value-field"
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
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-underload-value-field"
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
    number_of_cycles = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-number-of-cycles-field"
        ],
        description=(
            "CCD images are sometimes constructed by summing together multiple "
            "short exposures in the electronics. This reduces background etc. "
            "This is the number of short exposures used to sum images for an "
            "image."
        ),
        a_nexus_field=NeXusField(
            name="number_of_cycles",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    sensor_material = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-sensor-material-field"
        ],
        description=(
            "At times, radiation is not directly sensed by the detector. Rather, "
            "the detector might sense the output from some converter like a "
            "scintillator. This is the name of this converter material."
        ),
        a_nexus_field=NeXusField(
            name="sensor_material",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    sensor_thickness = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-sensor-thickness-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=(
            "At times, radiation is not directly sensed by the detector. Rather, "
            "the detector might sense the output from some converter like a "
            "scintillator. This is the thickness of this converter material."
        ),
        a_nexus_field=NeXusField(
            name="sensor_thickness",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    threshold_energy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-threshold-energy-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="joule",
        description=(
            "Single photon counter detectors can be adjusted for a certain "
            "energy range in which they work optimally. This is the energy "
            "setting for this."
        ),
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
    depends_on = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-depends-on-field"
        ],
        description=(
            "The reference point of the detector is the center of the first "
            "pixel. In complex geometries the NXoff_geometry groups can be used "
            "to provide an unambiguous reference."
        ),
        a_nexus_field=NeXusField(
            name="depends_on",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    pixel_shape_off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        description=(
            "Shape description of each pixel. Use only if all pixels in the "
            "detector are of uniform shape."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXoff_geometry",
            group_name="pixel_shape",
            optionality="optional",
        ),
    )
    pixel_shape_cylindrical_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cylindrical_geometry.CylindricalGeometry",
        description=(
            "Shape description of each pixel. Use only if all pixels in the "
            "detector are of uniform shape and require being described by "
            "cylinders."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXcylindrical_geometry",
            group_name="pixel_shape",
            optionality="optional",
        ),
    )
    detector_shape_off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        description=(
            "Shape description of the whole detector. Use only if pixels in the "
            "detector are not of uniform shape."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXoff_geometry",
            group_name="detector_shape",
            optionality="optional",
        ),
    )
    detector_shape_cylindrical_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cylindrical_geometry.CylindricalGeometry",
        description=(
            "Shape description of the whole detector. Use only if pixels in the "
            "detector are not of uniform shape and require being described by "
            "cylinders."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXcylindrical_geometry",
            group_name="detector_shape",
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


class DetectorEfficiency(Data):
    """
    Spectral efficiency of detector with respect to e.g. wavelength
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-efficiency-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="efficiency",
            name_type="specified",
            optionality="optional",
        ),
    )

    signal = Quantity(
        type=MEnum(["efficiency"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-efficiency-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["efficiency"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="efficiency",
        ),
    )
    axes = Quantity(
        type=MEnum([".", ". .", ". . .", ". . . .", "wavelength"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-efficiency-axes-attribute"
        ],
        shape=["*"],
        a_nexus_attribute=NeXusAttribute(
            name="axes",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=[".", ". .", ". . .", ". . . .", "wavelength"],
        ),
    )
    wavelength_indices = Quantity(
        type=MEnum(["0"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-efficiency-wavelength-indices-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="wavelength_indices",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["0"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="0",
        ),
    )
    efficiency = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-efficiency-efficiency-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", "*", "*"],
        description=("efficiency of the detector"),
        a_nexus_field=NeXusField(
            name="efficiency",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_DIMENSIONLESS",
        ),
    )
    wavelength = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector-efficiency-wavelength-field"
        ],
        dimensionality="[length]",
        unit="m",
        shape=["*", "*", "*"],
        description=(
            "This field can be two things: #. For a pixel detector it provides "
            "the nominal wavelength for which the detector has been calibrated. "
            "#. For other detectors this field has to be seen together with the "
            "efficiency field above. For some detectors, the efficiency is "
            "wavelength dependent. Thus this field provides the wavelength axis "
            "for the efficiency field. In this use case, the efficiency and "
            "wavelength arrays must have the same dimensionality."
        ),
        a_nexus_field=NeXusField(
            name="wavelength",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_WAVELENGTH",
        ),
    )

    pixel_shape_off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        description=(
            "Shape description of each pixel. Use only if all pixels in the "
            "detector are of uniform shape."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXoff_geometry",
            group_name="pixel_shape",
            optionality="optional",
        ),
    )
    pixel_shape_cylindrical_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cylindrical_geometry.CylindricalGeometry",
        description=(
            "Shape description of each pixel. Use only if all pixels in the "
            "detector are of uniform shape and require being described by "
            "cylinders."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXcylindrical_geometry",
            group_name="pixel_shape",
            optionality="optional",
        ),
    )
    detector_shape_off_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.off_geometry.OffGeometry",
        description=(
            "Shape description of the whole detector. Use only if pixels in the "
            "detector are not of uniform shape."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXoff_geometry",
            group_name="detector_shape",
            optionality="optional",
        ),
    )
    detector_shape_cylindrical_geometry = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.cylindrical_geometry.CylindricalGeometry",
        description=(
            "Shape description of the whole detector. Use only if pixels in the "
            "detector are not of uniform shape and require being described by "
            "cylinders."
        ),
        a_nexus_choice=NeXusChoice(
            nx_class="NXcylindrical_geometry",
            group_name="detector_shape",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
