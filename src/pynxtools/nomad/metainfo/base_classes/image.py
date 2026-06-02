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
# Run `pynx nomad generate-metainfo --nx-class NXimage` to regenerate.
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
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.process import Process

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Image"]


class Image(Object):
    """
    Base class for reporting a set of images representing specializations of
    NXdata.

    The most commonly used scanning methods are supported. That is one-, two-,
    three-dimensional ROIs discretized using regular Euclidean tilings.

    Colloquially, an image is understood as a discretized representation of
    intensity distribution detected or simulated for some ROI. When discretized
    with regular Euclidean tilings, the terms pixel and voxel identify the
    smallest discretization unit. In this case, pixel and voxel are polygonal
    or polyhedral unit cells respectively of the underlying tiling of the ROI
    within the reference space. For all other tilings e.g. non-equispaced, the
    shape and size of pixel and voxel differs. Using the term image point is
    eventually more appropriate when working with such tilings.

    Therefore, all docstrings in this base class refer to points. Points are
    considered exact synonyms for pixel and voxel, which are terms used for
    regular tilings.

    Point coordinates identify the location of the barycenter.

    For images in reciprocal space in practice, complex numbers are encoded via
    some formatted pair of real values. Typically, fast algorithms for
    computing Fourier transformations (FFT) are used to encode images in
    reciprocal (frequency) space. FFT libraries are used for implementing the
    key functionalities of these mathematical operations. Different libraries
    use different representations and encoding of the images. Details can be
    found in the respective sections of the typical FFT libraries
    documentations:

    * `FFTW by M. Frigo and S. G. Johnson
    <https://www.fftw.org/fftw3_doc/Tutorial.html#Tutorial>`_ * `Intel MKL by
    the Intel Co.
    <https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-c/2024-2/fourier-transform-functions.html>`_
    * `cuFFT by the NVidia Co.
    <https://docs.nvidia.com/cuda/cufft/index.html>`_ * `NFFT by the TU
    Chemnitz group <https://www-user.tu-chemnitz.de/~potts/nfft/>`_ for
    non-equispaced computations

    Users are strongly advised to inspect carefully which specific conventions
    their library uses to enable storing and modifying the implementation of
    their code such that the serialized representations as they are detailed
    here for NeXus match.

    It is often the case that several images are combined using processing. In
    this case, the number of images which are combined into collections is not
    necessarily the same for each collection. The NXimage base class addresses
    this logical distinction through the notation of indices_image and
    indices_group concepts. That is indices_image are always counting from
    offset in increments of one as each image is its own entity. By contrast, a
    group may contain no, or several images. Consequently, indices_group are
    not required to be contiguous.

    Classically, images depict objects in real space. Such usage of NXimage
    essentially is equivalent to storing pictures. For this purpose the
    image_1d, image_2d, or image_3d NXdata instances respectively should be
    used such that all their axes axis_i, axis_j, axis_k are constrained to
    NeXus Unit Category NX_LENGTH.

    Imaging modes in electron microscopy are typically more versatile,
    specifically for use cases in scanning transmission electron microscopy,
    so-called 4DSTEM. In this case, one two-dimensional diffraction image is
    taken for each point that gets scanned in real space. Consequently,
    image_3d and image_4d NXdata instances should be used for these cases with
    axis_k and axis_m respectively of NeXus Unit Category NX_LENGTH and axis_i
    and axis_j respectively of NeXus Unit Category NX_WAVENUMBER or
    NX_UNITLESS.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXimage",
            category="base",
            symbols={
                "n_img": "Number of images in the stack, for stacks the slowest dimension.",
                "n_m": "Number of image points along the slowest dimension.",
                "n_k": "Number of image points along the slow dimension (k equivalent to z).",
                "n_j": "Number of image points along the fast dimension (j equivalent to y).",
                "n_i": "Number of image points along the fastest dimension (i equivalent to x).",
            },
        ),
    )

    process = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageProcess",
        repeats=True,
        variable=True,
        description=(
            "Details how NXdata instance were processed from detector "
            "readings/raw data."
        ),
    )
    image_1d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageImage1d",
        repeats=False,
        description=("One-dimensional image."),
    )
    image_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageImage2d",
        repeats=False,
        description=("Two-dimensional image."),
    )
    image_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageImage3d",
        repeats=False,
        description=("Three-dimensional image."),
    )
    image_4d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageImage4d",
        repeats=False,
        description=("Four-dimensional image."),
    )
    stack_1d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageStack1d",
        repeats=False,
        description=("Collection of one-dimensional images."),
    )
    stack_2d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageStack2d",
        repeats=False,
        description=("Collection of two-dimensional images."),
    )
    stack_3d = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.image.ImageStack3d",
        repeats=False,
        description=("Collection of three-dimensional images."),
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


class ImageProcess(Process):
    """
    Details how NXdata instance were processed from detector readings/raw data.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-process-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXprocess",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    detector_identifier = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-process-detector-identifier-field"
        ],
        description=(
            "Link or name of an :ref:`NXdetector` instance with which the data "
            "were collected."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="detector_identifier",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ImageImage1d(Data):
    """
    One-dimensional image.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-1d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_1d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-1d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Intensity for real-valued images as an alternative for real. "
            "Magnitude of the image intensity for complex-valued data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-1d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Real part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-1d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Imaginary part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-1d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=(
            "Image intensity as a complex number as an alternative to real and "
            "imag fields if values are stored as interleaved complex numbers."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-1d-axis-i-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fastest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-1d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fastest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ImageImage2d(Data):
    """
    Two-dimensional image.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Intensity for real-valued images as an alternative for real. "
            "Magnitude of the image intensity for complex-valued data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=("Real part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=("Imaginary part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Image intensity as a complex number as an alternative to real and "
            "imag fields if values are stored as interleaved complex numbers."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-axis-j-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fast dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-axis-i-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fastest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-2d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fastest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ImageImage3d(Data):
    """
    Three-dimensional image.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=(
            "Intensity for real-valued images as an alternative for real. "
            "Magnitude of the image intensity for complex-valued data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=("Real part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=("Imaginary part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=(
            "Image intensity as a complex number as an alternative to real and "
            "imag fields if values are stored as interleaved complex numbers."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-axis-k-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the slow dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-axis-k-long-name-attribute"
        ],
        description=("Point coordinate along the slow dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-axis-j-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fast dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-axis-i-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fastest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-3d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fastest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ImageImage4d(Data):
    """
    Four-dimensional image.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="image_4d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=(
            "Intensity for real-valued images as an alternative for real. "
            "Magnitude of the image intensity for complex-valued data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=("Real part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=("Imaginary part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=(
            "Image intensity as a complex number as an alternative to real and "
            "imag fields if values are stored as interleaved complex numbers."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    axis_m = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-m-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the slowest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_m",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_m__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-m-long-name-attribute"
        ],
        description=("Point coordinate along the slowest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_m",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-k-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the slow dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-k-long-name-attribute"
        ],
        description=("Point coordinate along the slow dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-j-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fast dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-i-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fastest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-image-4d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fastest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ImageStack1d(Data):
    """
    Collection of one-dimensional images.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_1d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Intensity for real-valued images as an alternative for real. "
            "Magnitude of the image intensity for complex-valued data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=("Real part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=("Imaginary part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*"],
        description=(
            "Image intensity as a complex number as an alternative to real and "
            "imag fields if values are stored as interleaved complex numbers."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Group identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-indices-group-long-name-attribute"
        ],
        description=("Group identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_group",
        ),
    )
    indices_image = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-indices-image-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Image identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="indices_image",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_image__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-indices-image-long-name-attribute"
        ],
        description=("Image identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_image",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-axis-i-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fastest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-1d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fastest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ImageStack2d(Data):
    """
    Collection of two-dimensional images.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_2d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=(
            "Intensity for real-valued images as an alternative for real. "
            "Magnitude of the image intensity for complex-valued data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=("Real part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=("Imaginary part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*"],
        description=(
            "Image intensity as a complex number as an alternative to real and "
            "imag fields if values are stored as interleaved complex numbers."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Group identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-indices-group-long-name-attribute"
        ],
        description=("Group identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_group",
        ),
    )
    indices_image = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-indices-image-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Image identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="indices_image",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_image__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-indices-image-long-name-attribute"
        ],
        description=("Image identifier."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_image",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-axis-j-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fast dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-axis-i-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fastest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-2d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fastest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class ImageStack3d(Data):
    """
    Collection of three-dimensional images.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="stack_3d",
            name_type="specified",
            optionality="optional",
        ),
    )

    intensity = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-intensity-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=(
            "Intensity for real-valued images as an alternative for real. "
            "Magnitude of the image intensity for complex-valued data."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="intensity",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    real = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-real-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=("Real part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="real",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    imag = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-imag-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=("Imaginary part of the image intensity per point."),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="imag",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    complex = Quantity(
        type=np.complex128,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-complex-field"
        ],
        dimensionality="dimensionless",
        shape=["*", "*", "*", "*"],
        description=(
            "Image intensity as a complex number as an alternative to real and "
            "imag fields if values are stored as interleaved complex numbers."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="complex",
            type="NX_COMPLEX",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-indices-group-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Group identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="indices_group",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_group__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-indices-group-long-name-attribute"
        ],
        description=("Group identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_group",
        ),
    )
    indices_image = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-indices-image-field"
        ],
        dimensionality="dimensionless",
        shape=["*"],
        description=("Image identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="indices_image",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    indices_image__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-indices-image-long-name-attribute"
        ],
        description=("Image identifier"),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="indices_image",
        ),
    )
    axis_k = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-axis-k-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the slow dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_k",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_k__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-axis-k-long-name-attribute"
        ],
        description=("Point coordinate along the slow dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_k",
        ),
    )
    axis_j = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-axis-j-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fast dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_j",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_j__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-axis-j-long-name-attribute"
        ],
        description=("Point coordinate along the fast dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_j",
        ),
    )
    axis_i = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-axis-i-field"
        ],
        shape=["*"],
        description=(
            "Point coordinate along the fastest dimension. Different NeXus Unit "
            "Category are allowed: * NX_LENGTH for images slicing real space. * "
            "NX_WAVENUMBER or NX_UNITLESS respectively for images slicing "
            "reciprocal space."
        ),
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="axis_i",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
    )
    axis_i__long_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXimage.html#nximage-stack-3d-axis-i-long-name-attribute"
        ],
        description=("Point coordinate along the fastest dimension."),
        a_nexus_quantity=NeXusQuantity(
            kind="attribute",
            name="long_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="axis_i",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
