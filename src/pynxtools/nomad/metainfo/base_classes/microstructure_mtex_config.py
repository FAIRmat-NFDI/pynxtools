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
# Run `pynx nomad generate-metainfo --nxdl NXmicrostructure_mtex_config` to regenerate.
# Additive-only: the generator will never remove or rename existing members.
# Add normalize() logic directly; it will be preserved on regeneration.
#
# NOTE: This class is generated from a community-contributed NXDL definition.
# The NXDL source may change across versions. Regenerate after updating definitions.
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
from pynxtools.nomad.metainfo.base_classes.collection import Collection
from pynxtools.nomad.metainfo.base_classes.parameters import Parameters

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["MicrostructureMtexConfig"]


class MicrostructureMtexConfig(Parameters):
    """
    Base class to store the configuration when using the MTex/Matlab software.

    MTex is a Matlab package for texture analysis used in the Materials and
    Earth Sciences. See `R. Hielscher et al.
    <https://mtex-toolbox.github.io/publications>`_ and the `MTex source code
    <https://github.com/mtex-toolbox>`_ for details.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config"
        ],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXmicrostructure_mtex_config",
            category="base",
            symbols={
                "n_def_color_map": "Number of entries in the default color map",
                "n_color_map": "Number of entries in color map",
            },
        ),
    )

    conventions = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_mtex_config.MicrostructureMtexConfigConventions",
        repeats=False,
        description=(
            "MTex reference frame and orientation conventions. Consult the `MTex "
            "docs <https://mtex-toolbox.github.io/EBSDReferenceFrame.html>`_ for "
            "details."
        ),
    )
    plotting = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_mtex_config.MicrostructureMtexConfigPlotting",
        repeats=False,
        description=("Settings relevant for generating plots."),
    )
    miscellaneous = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_mtex_config.MicrostructureMtexConfigMiscellaneous",
        repeats=False,
        description=("Miscellaneous other settings of MTex."),
    )
    numerics = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_mtex_config.MicrostructureMtexConfigNumerics",
        repeats=False,
        description=("Miscellaneous settings relevant for numerics."),
    )
    system = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_mtex_config.MicrostructureMtexConfigSystem",
        repeats=False,
        description=("Miscellaneous settings relevant of the system where MTex runs."),
    )
    path = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.microstructure_mtex_config.MicrostructureMtexConfigPath",
        repeats=False,
        description=("Collection of paths from where MTex reads information and code."),
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


class MicrostructureMtexConfigConventions(Collection):
    """
    MTex reference frame and orientation conventions. Consult the `MTex docs
    <https://mtex-toolbox.github.io/EBSDReferenceFrame.html>`_ for details.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-conventions-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="conventions",
            name_type="specified",
            optionality="optional",
        ),
    )

    x_axis_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-conventions-x-axis-direction-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="x_axis_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    z_axis_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-conventions-z-axis-direction-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="z_axis_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    a_axis_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-conventions-a-axis-direction-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="a_axis_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    b_axis_direction = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-conventions-b-axis-direction-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="b_axis_direction",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    euler_angle = Quantity(
        type=MEnum(["unknown", "undefined", "bunge"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-conventions-euler-angle-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="euler_angle",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["unknown", "undefined", "bunge"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureMtexConfigPlotting(Collection):
    """
    Settings relevant for generating plots.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="plotting",
            name_type="specified",
            optionality="optional",
        ),
    )

    font_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-font-size-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="font_size",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    inner_plot_spacing = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-inner-plot-spacing-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="inner_plot_spacing",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    outer_plot_spacing = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-outer-plot-spacing-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="outer_plot_spacing",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    marker_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-marker-size-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="marker_size",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    figure_size = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-figure-size-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="figure_size",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    show_micron_bar = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-show-micron-bar-field"
        ],
        description=("True, if MTex renders a scale bar with figures."),
        a_nexus_field=NeXusField(
            name="show_micron_bar",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    show_coordinates = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-show-coordinates-field"
        ],
        description=("True, if MTex renders a grid with figures."),
        a_nexus_field=NeXusField(
            name="show_coordinates",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    pf_anno_fun_hdl = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-pf-anno-fun-hdl-field"
        ],
        description=(
            "Code for the function handle used for annotating pole figure plots."
        ),
        a_nexus_field=NeXusField(
            name="pf_anno_fun_hdl",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    color_map = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-color-map-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="color_map",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    default_color_map = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-default-color-map-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        shape=["*", 3],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="default_color_map",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
    )
    color_palette = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-color-palette-field"
        ],
        a_nexus_field=NeXusField(
            name="color_palette",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    degree_char = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-degree-char-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="degree_char",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    arrow_char = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-arrow-char-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="arrow_char",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    marker = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-marker-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="marker",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    marker_edge_color = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-marker-edge-color-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="marker_edge_color",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    marker_face_color = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-marker-face-color-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="marker_face_color",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    hit_test = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-plotting-hit-test-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="hit_test",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureMtexConfigMiscellaneous(Collection):
    """
    Miscellaneous other settings of MTex.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-miscellaneous-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="miscellaneous",
            name_type="specified",
            optionality="optional",
        ),
    )

    mosek = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-miscellaneous-mosek-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="mosek",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    generating_help_mode = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-miscellaneous-generating-help-mode-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="generating_help_mode",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    methods_advise = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-miscellaneous-methods-advise-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="methods_advise",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    stop_on_symmetry_mismatch = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-miscellaneous-stop-on-symmetry-mismatch-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="stop_on_symmetry_mismatch",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    inside_poly = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-miscellaneous-inside-poly-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="inside_poly",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    text_interpreter = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-miscellaneous-text-interpreter-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="text_interpreter",
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


class MicrostructureMtexConfigNumerics(Collection):
    """
    Miscellaneous settings relevant for numerics.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-numerics-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="numerics",
            name_type="specified",
            optionality="optional",
        ),
    )

    eps = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-numerics-eps-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("Return value of the Matlab eps command."),
        a_nexus_field=NeXusField(
            name="eps",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "dimensionless"},
    )
    fft_accuracy = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-numerics-fft-accuracy-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="fft_accuracy",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    max_stwo_bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-numerics-max-stwo-bandwidth-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="max_stwo_bandwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    max_sothree_bandwidth = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-numerics-max-sothree-bandwidth-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="max_sothree_bandwidth",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureMtexConfigSystem(Collection):
    """
    Miscellaneous settings relevant of the system where MTex runs.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-system-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="system",
            name_type="specified",
            optionality="optional",
        ),
    )

    memory = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-system-memory-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="memory",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    open_gl_bug = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-system-open-gl-bug-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="open_gl_bug",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    save_to_file = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-system-save-to-file-field"
        ],
        description=("TODO with MTex developers"),
        a_nexus_field=NeXusField(
            name="save_to_file",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class MicrostructureMtexConfigPath(Collection):
    """
    Collection of paths from where MTex reads information and code.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="path",
            name_type="specified",
            optionality="optional",
        ),
    )

    mtex = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-mtex-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="mtex",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    data_quantity = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-data-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="data",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    cif = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-cif-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="cif",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    ebsd = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-ebsd-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="ebsd",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    pf = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-pf-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="pf",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    odf = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-odf-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="odf",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    tensor = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-tensor-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="tensor",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    example = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-example-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="example",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    import_wizard = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-import-wizard-field"
        ],
        description=("Absolute path to specific component of MTex source code."),
        a_nexus_field=NeXusField(
            name="import_wizard",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    pf_extensions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-pf-extensions-field"
        ],
        description=(
            "List of file type suffixes for which MTex assumes texture/pole "
            "figure information."
        ),
        a_nexus_field=NeXusField(
            name="pf_extensions",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    ebsd_extensions = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmicrostructure_mtex_config.html#nxmicrostructure_mtex_config-path-ebsd-extensions-field"
        ],
        description=("List of file type suffixes for which MTex assumes EBSD content."),
        a_nexus_field=NeXusField(
            name="ebsd_extensions",
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
