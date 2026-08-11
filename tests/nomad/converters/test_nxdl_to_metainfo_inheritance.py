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
"""Tests for cross-application named-concept inheritance.

For groups appearing across multiple application definitions in an
``extends`` chain, these tests verify that generated concepts inherit from
the nearest ancestor contributing structural content (fields, attributes,
links, or nested groups). This guards against inheritance errors that would
otherwise silently omit metadata from intermediate ancestors.
"""

from __future__ import annotations

import pytest

try:
    from pynxtools.nomad.converters.nxdl_to_metainfo import (
        _discover_applications,
        _parent_generates_concept_at,
    )
except ImportError:
    pytest.skip("nomad not installed", allow_module_level=True)

from pynxtools.nexus.nexus_tree import NexusGroup, generate_tree_from

# Known, deliberately-unfixed gap: NXmonopd declares "polar_angle"/"data" in
# its own DATA group as <link>s; NXxrd (which extends NXmonopd) redeclares
# the same names as <field>s. The tree-merge in nexus_tree.py resolves both
# to a single NexusField per name and drops NXmonopd's <link> declaration
# entirely — it never appears in the merged field's own `.inheritance`, so
# there is no trace left for the generator to recover. Fixing this needs a
# change in the tree-merge itself (nexus_tree.py), not in the generator's
# inheritance decision, and is out of scope for this test.
KNOWN_GAPS = {("NXxrd", "NXdata", "DATA")}


def _app_file_basenames() -> set[str]:
    """NXDL file basenames for every application definition in the corpus."""
    return {f"{name}.nxdl.xml" for name in _discover_applications()}


def _is_app_file(base_path: str, app_file_basenames: set[str]) -> bool:
    """True if base_path is an application definition's own NXDL file."""
    return base_path.rsplit("/", maxsplit=1)[-1] in app_file_basenames


def _has_structural_content(elem) -> bool:
    """True if a raw XML element has any child other than <doc>."""
    return any(child.tag.split("}")[-1] != "doc" for child in elem)


def _walk(node, app_name, app_file_basenames, seen, findings):
    """Recurse through node's tree, collecting inheritance-gap findings.

    Each (nx_class, chain) combination is checked once across the whole
    corpus via seen.
    """
    if isinstance(node, NexusGroup):
        app_levels = [
            i
            for i, e in enumerate(node.inheritance)
            if _is_app_file(e.base, app_file_basenames)
        ]
        if len(app_levels) >= 2:
            key = (
                node.nx_class,
                tuple(node.inheritance[i].base.split("/")[-1] for i in app_levels),
            )
            if key not in seen:
                seen.add(key)
                chosen = next(
                    (
                        idx
                        for idx in app_levels[1:]
                        if _parent_generates_concept_at(node, idx)
                    ),
                    None,
                )
                structural = [
                    idx
                    for idx in app_levels[1:]
                    if _has_structural_content(node.inheritance[idx])
                ]
                nearest_structural = structural[0] if structural else None
                if (chosen is None and structural) or (
                    chosen is not None
                    and nearest_structural is not None
                    and nearest_structural < chosen
                ):
                    findings.append(
                        {
                            "app": app_name,
                            "nx_class": node.nx_class,
                            "name": node.name,
                            "chain": [
                                node.inheritance[i].base.split("/")[-1]
                                for i in app_levels
                            ],
                            "chosen": node.inheritance[chosen].base.split("/")[-1]
                            if chosen is not None
                            else None,
                            "nearest_structural": node.inheritance[
                                nearest_structural
                            ].base.split("/")[-1]
                            if nearest_structural is not None
                            else None,
                        }
                    )
    for c in getattr(node, "children", ()):
        _walk(c, app_name, app_file_basenames, seen, findings)


def test_no_undetected_cross_app_inheritance_gaps():
    """Verify that every group touched by multiple application ancestors
    inherits from the nearest one with structural content, rather than
    skipping past it to a more generic ancestor.
    """
    app_file_basenames = _app_file_basenames()
    seen: set = set()
    findings: list = []
    for app_name in sorted(_discover_applications()):
        try:
            root = generate_tree_from(app_name)
        except Exception:  # noqa: BLE001 - unrelated generator errors, not this test's concern
            continue
        _walk(root, app_name, app_file_basenames, seen, findings)

    unexpected = [
        f for f in findings if (f["app"], f["nx_class"], f["name"]) not in KNOWN_GAPS
    ]
    assert not unexpected, (
        "Found group(s) where a nearer application ancestor has structural "
        "content that wasn't picked as the inheritance base:\n"
        + "\n".join(
            f"  {f['app']}: {f['nx_class']} (name={f['name']}) "
            f"chain={f['chain']} chosen={f['chosen']} "
            f"nearest_with_content={f['nearest_structural']}"
            for f in unexpected
        )
    )
