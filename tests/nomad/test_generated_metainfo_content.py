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
"""Content checks for the statically generated NOMAD metainfo classes
produced from NXDL definitions.

Expected dtypes, units, shapes, enumerations, inheritance, and field
ownership are derived directly from the parsed NXDL definitions via
pynxtools.nexus.nexus_tree.generate_tree_from, providing an independent
reference against which the generated classes are validated.

The tests cover representative generated classes, including base classes,
application definitions, and inherited concepts, verifying that metadata is
generated and propagated correctly.
"""

from __future__ import annotations

import pytest

try:
    from nomad.datamodel.data import EntryData
    from nomad.datamodel.metainfo import basesections
    from nomad.metainfo.data_type import Enum as NomadEnum
except ImportError:
    pytest.skip("nomad not installed", allow_module_level=True)

from pynxtools.nexus.nexus_tree import NexusField, NexusGroup, generate_tree_from
from pynxtools.nomad.metainfo.applications.apm_paraprobe_clusterer_config import (
    ApmParaprobeClustererConfigCamecaToNexusReconstruction,
)
from pynxtools.nomad.metainfo.applications.apm_paraprobe_tool_config import (
    ApmParaprobeToolConfigTaskconfigReconstruction,
)
from pynxtools.nomad.metainfo.applications.ellipsometry import (
    EllipsometryDataCollection,
)
from pynxtools.nomad.metainfo.applications.iv_temp import IvTempSample
from pynxtools.nomad.metainfo.applications.monopd import MonopdSample
from pynxtools.nomad.metainfo.applications.optical_spectroscopy import (
    OpticalSpectroscopyData,
)
from pynxtools.nomad.metainfo.applications.sensor_scan import SensorScanSample
from pynxtools.nomad.metainfo.applications.spm import (
    SpmInstrumentBiasSpectroscopyEnvironment,
)
from pynxtools.nomad.metainfo.applications.sts import (
    StsInstrumentBiasSpectroscopyEnvironment,
)
from pynxtools.nomad.metainfo.applications.xbase import (
    Xbase,
    XbaseData,
    XbaseInstrumentDetector,
)
from pynxtools.nomad.metainfo.applications.xeuler import XeulerName
from pynxtools.nomad.metainfo.applications.xlaueplate import (
    XlaueplateInstrumentDetector,
)
from pynxtools.nomad.metainfo.applications.xrd_pan import XrdPanSample
from pynxtools.nomad.metainfo.applications.xrot import XrotInstrumentDetector
from pynxtools.nomad.metainfo.base_classes.beam_stop import BeamStop
from pynxtools.nomad.metainfo.base_classes.detector import Detector
from pynxtools.units import NXUnitSet, ureg

# ---------------------------------------------------------------------------
# Helpers: derive ground truth from the NXDL tree, not from generated code.
# ---------------------------------------------------------------------------


def _top_level_field(nx_class: str, field_name: str) -> NexusField:
    """The named field as directly declared on a base class's own NXDL root
    (e.g. NXdetector, NXbeam_stop) — no application/entry wrapping.
    """
    root = generate_tree_from(nx_class)
    return next(
        c for c in root.children if isinstance(c, NexusField) and c.name == field_name
    )


def _expected_shape(node: NexusField) -> list[str]:
    """NXDL <dimensions> rank/value, translated to NOMAD's Quantity.shape
    convention: no <dimensions> at all -> [], each dimension -> "*" (this
    corpus only uses symbolic/unbounded dims, never fixed integers).
    """
    if node.shape is None:
        return []
    assert all(d is None for d in node.shape), (
        "helper assumes symbolic/unbounded dims; extend if a fixed-size "
        "dimension shows up in a case this test covers"
    )
    return ["*"] * len(node.shape)


def _expected_unit(node: NexusField):
    """Pint unit for a field's NX_UNIT category (e.g. NX_LENGTH -> meter),
    via pynxtools.units.NXUnitSet — shared domain data used across
    pynxtools, not part of the generator's own decision logic.
    """
    return ureg(NXUnitSet.get_default_unit(node.unit)).units


def _entry_child_group(app_name: str, *path: str | tuple[str, str]) -> NexusGroup:
    """Return the group at ``path`` in an application definition.

    Traversal starts at ``NXentry``. Each path element is either an NX_class
    name or an ``(nx_class, name)`` tuple to disambiguate between sibling
    groups sharing the same NX_class. When only the NX_class is given, the
    first matching group is selected.
    """
    node = generate_tree_from(app_name)
    for step in ("NXentry", *path):
        nx_class, name = step if isinstance(step, tuple) else (step, None)
        candidates = [
            c
            for c in node.children
            if isinstance(c, NexusGroup) and c.nx_class == nx_class
        ]
        node = next(c for c in candidates if c.name == name) if name else candidates[0]
    return node


def _own_child_element_names(elem, tag: str) -> set[str]:
    """Return the names of an XML element's direct ``<tag>`` children.

    Used to inspect an application's own NXDL declarations without merged or
    inherited content.
    """
    return {
        child.attrib["name"]
        for child in elem
        if child.tag.split("}")[-1] == tag and "name" in child.attrib
    }


def _own_child_group_names(elem) -> set[str]:
    """Return the subsection names of an XML element's direct ``<group>`` children.

    Named groups use their explicit name; anonymous groups use the lowercased
    NXDL type name with any ``NX`` prefix removed.
    """
    names = set()
    for child in elem:
        if child.tag.split("}")[-1] != "group":
            continue
        name = child.attrib.get("name")
        if name is None:
            nx_type = child.attrib.get("type", "")
            name = (nx_type[2:] if nx_type.startswith("NX") else nx_type).lower()
        names.add(name)
    return names


def _inheritance_index(node: NexusGroup, nxdl_filename: str) -> int:
    """Index of nxdl_filename's own declaration in node's inheritance chain."""
    return next(
        i
        for i, e in enumerate(node.inheritance)
        if e.base.split("/")[-1] == nxdl_filename
    )


# ---------------------------------------------------------------------------
# Base classes: own quantities, dtype, unit, shape/dims
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("field_name", ["beam_center_x", "beam_center_y"])
def test_base_class_quantity_unit_matches_nxdl(field_name):
    """Verify that Detector field units and shapes match the NXDL definition."""
    node = _top_level_field("NXdetector", field_name)
    quantity = Detector.m_def.all_quantities[field_name]
    assert quantity.unit == _expected_unit(node)
    assert quantity.shape == _expected_shape(node)


@pytest.mark.parametrize("field_name", ["polar_angle", "x_pixel_size"])
def test_base_class_quantity_shape_matches_nxdl_dimensions(field_name):
    """polar_angle (<dimensions rank="3">) and x_pixel_size (rank="2") on
    NXdetector must produce Quantity.shape with exactly that many "*"
    entries.
    """
    node = _top_level_field("NXdetector", field_name)
    quantity = Detector.m_def.all_quantities[field_name]
    assert quantity.shape == _expected_shape(node)
    assert len(quantity.shape) == len(node.shape)


def test_base_class_enum_values_match_nxdl_enumeration():
    """BeamStop's "description"/"status" fields are NX_CHAR with an
    <enumeration> in NXbeam_stop.nxdl.xml — the generator should turn those
    into MEnum quantities with exactly the NXDL item values.
    """
    quantities = BeamStop.m_def.all_quantities
    for field_name in ("description", "status"):
        node = _top_level_field("NXbeam_stop", field_name)
        assert node.items is not None, f"{field_name} has no NXDL enumeration"
        quantity_type = quantities[field_name].type
        assert isinstance(quantity_type, NomadEnum)
        assert set(quantity_type._list) == set(node.items)


# ---------------------------------------------------------------------------
# Application definitions: entry-level structure
# ---------------------------------------------------------------------------


def test_appdef_entry_class_has_expected_base_sections_and_subsections():
    """Xbase should be both an EntryData and a basesections.Measurement,
    and should carry a SubSection for every top-level group NXbase.nxdl.xml's
    own NXentry declares.
    """
    assert issubclass(Xbase, EntryData)
    assert issubclass(Xbase, basesections.Measurement)

    entry = generate_tree_from("NXxbase")
    entry_group = next(
        c
        for c in entry.children
        if isinstance(c, NexusGroup) and c.nx_class == "NXentry"
    )
    expected_group_names = {
        c.name.lower() if c.name_type == "any" else c.name
        for c in entry_group.own_children()
        if isinstance(c, NexusGroup)
    }
    assert expected_group_names  # sanity: NXbase does declare top-level groups
    assert expected_group_names <= set(Xbase.m_def.all_sub_sections)


# ---------------------------------------------------------------------------
# Cross-application inheritance: "created classes" for named concepts,
# and the inherited terms they must expose
# ---------------------------------------------------------------------------


def test_single_level_named_concept_exposes_own_and_inherited_terms():
    """Verify that a generated named concept includes its own quantities while
    retaining those inherited from its parent."""
    assert XrotInstrumentDetector.__bases__ == (XbaseInstrumentDetector,)

    detector = _entry_child_group("NXxrot", "NXinstrument", "NXdetector")
    xrot_idx = _inheritance_index(detector, "NXxrot.nxdl.xml")
    xbase_idx = _inheritance_index(detector, "NXxbase.nxdl.xml")
    xrot_own_fields = _own_child_element_names(detector.inheritance[xrot_idx], "field")
    xbase_own_fields = _own_child_element_names(
        detector.inheritance[xbase_idx], "field"
    )
    assert xrot_own_fields, "NXxrot's own detector declares no fields"
    assert xbase_own_fields, "NXxbase's own detector declares no fields"

    quantities = XrotInstrumentDetector.m_def.all_quantities
    for name in xrot_own_fields:
        assert name in quantities, f"{name} (NXxrot's own) missing"
    for name in xbase_own_fields:
        # A field named like a reserved BaseSection quantity gets a
        # "_quantity" suffix if array-shaped (see converters/_mapping.py's
        # _BASESECTION_RESERVED_NAMES) — "data" is exactly this case.
        assert name in quantities or f"{name}_quantity" in quantities, (
            f"{name} (NXxbase's own, inherited) missing"
        )


def test_multi_level_named_concept_exposes_terms_from_every_ancestor():
    """Verify that multi-level named-concept inheritance preserves quantities,
    units, and shapes from every ancestor."""
    assert XlaueplateInstrumentDetector.__bases__ == (XrotInstrumentDetector,)
    base_names = [b.name for b in XlaueplateInstrumentDetector.m_def.all_base_sections]
    assert base_names.index("XbaseInstrumentDetector") < base_names.index(
        "XrotInstrumentDetector"
    )

    detector = _entry_child_group("NXxlaueplate", "NXinstrument", "NXdetector")
    quantities = XlaueplateInstrumentDetector.m_def.all_quantities
    for nxdl_file in ("NXxlaueplate.nxdl.xml", "NXxrot.nxdl.xml", "NXxbase.nxdl.xml"):
        idx = _inheritance_index(detector, nxdl_file)
        own_fields = _own_child_element_names(detector.inheritance[idx], "field")
        assert own_fields, f"{nxdl_file}'s own detector declares no fields"
        for name in own_fields:
            # A field named like a reserved BaseSection quantity gets a
            # "_quantity" suffix if array-shaped (NXxbase's own "data").
            assert name in quantities or f"{name}_quantity" in quantities, (
                f"{name} (from {nxdl_file}) missing"
            )

    # dtype/shape from the raw NXDL node must survive the full chain unchanged.
    polar_angle_node = next(
        c
        for c in detector.children
        if isinstance(c, NexusField) and c.name == "polar_angle"
    )
    assert quantities["polar_angle"].shape == _expected_shape(polar_angle_node)
    assert quantities["polar_angle"].unit == _expected_unit(polar_angle_node)


def test_sample_named_concept_inherits_across_applications():
    """Verify named-concept inheritance across application definitions for sample concepts."""
    assert IvTempSample.__bases__ == (SensorScanSample,)
    quantities = IvTempSample.m_def.all_quantities
    assert "lab_id" in quantities  # inherited via basesections.Entity


@pytest.mark.parametrize(
    "cls,expected_base",
    [
        (XrdPanSample, MonopdSample),
        (EllipsometryDataCollection, OpticalSpectroscopyData),
        (
            ApmParaprobeClustererConfigCamecaToNexusReconstruction,
            ApmParaprobeToolConfigTaskconfigReconstruction,
        ),
    ],
)
def test_further_cross_app_chains_found_by_the_corpus_audit(cls, expected_base):
    """Verify nearest-ancestor inheritance for representative cross-application concepts."""
    assert cls.__bases__ == (expected_base,)


def test_three_level_named_concept_chain_preserves_middle_ancestor():
    """Verify that a generated named concept inherits subsections from every
    application-specific ancestor in a multi-level inheritance chain.
    """
    assert StsInstrumentBiasSpectroscopyEnvironment.__bases__ == (
        SpmInstrumentBiasSpectroscopyEnvironment,
    )
    environment = _entry_child_group(
        "NXsts",
        "NXinstrument",
        ("NXenvironment", "bias_spectroscopy_environment"),
    )
    spm_idx = _inheritance_index(environment, "NXspm.nxdl.xml")
    spm_own_groups = _own_child_group_names(environment.inheritance[spm_idx])
    assert spm_own_groups, (
        "NXspm's own bias_spectroscopy_environment declares no groups"
    )

    sub_sections = StsInstrumentBiasSpectroscopyEnvironment.m_def.all_sub_sections
    for name in spm_own_groups:
        assert name in sub_sections, f"{name} (NXspm's own, inherited) missing"


def test_link_only_named_concept_exposes_links_as_quantities():
    """Verify that links declared by a named concept are generated as quantities
    and remain available through cross-application inheritance, even when no
    fields or subsections are declared.
    """
    assert XeulerName.__bases__ == (XbaseData,)

    name_group = _entry_child_group("NXxeuler", ("NXdata", "name"))
    xeuler_idx = _inheritance_index(name_group, "NXxeuler.nxdl.xml")
    xbase_idx = _inheritance_index(name_group, "NXxbase.nxdl.xml")
    xeuler_own_links = _own_child_element_names(
        name_group.inheritance[xeuler_idx], "link"
    )
    xbase_own_links = _own_child_element_names(
        name_group.inheritance[xbase_idx], "link"
    )
    assert xeuler_own_links, "NXxeuler's own name group declares no links"
    assert xbase_own_links, "NXxbase's own DATA group declares no links"

    quantities = XeulerName.m_def.all_quantities
    for name in xeuler_own_links:
        assert name in quantities, f"{name} (NXxeuler's own link) missing"
    # xbase's own link name ("data") collides with the reserved BaseSection
    # quantity name and gets suffixed; check the underlying NXDL link is at
    # least still represented under its renamed form.
    for name in xbase_own_links:
        assert name in quantities or f"{name}_quantity" in quantities, (
            f"{name} (NXxbase's own link, inherited) missing"
        )
