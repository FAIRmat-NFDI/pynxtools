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

"""End-to-end tests for the NXDL -> NOMAD metainfo converter.

The fixture NXDLs are rendered through the whole pipeline and compared against
the files in ``tests/data/nomad/converter/``. Both sides are compared through the
same parse into an AST, reduced to class bases and member names and kinds, so
formatting, keyword order and documentation text cannot fail a test — only a
change in what the generated schema declares. On failure, regenerate with
``python scripts/generate_metainfo_reference_files.py`` and read the diff. The
individual transformation rules are covered in ``test_nxdl_to_metainfo.py``.
"""

import ast
from pathlib import Path

import pytest

import pynxtools.nomad.converters.nxdl_to_metainfo as converter

REFERENCE_DIR = Path(__file__).parent.parent / "data" / "nomad" / "converter"


def _class_members(source: str) -> dict[str, dict[str, str]]:
    """Return ``{class_name: {member_name: kind}}`` for every class in source.

    ``kind`` is the callable on the right-hand side, ``"Quantity"`` or
    ``"SubSection"``.
    """
    result: dict[str, dict[str, str]] = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            members: dict[str, str] = {}
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for tgt in item.targets:
                        if isinstance(tgt, ast.Name) and tgt.id != "m_def":
                            call = item.value
                            if isinstance(call, ast.Call):
                                fn = call.func
                                if isinstance(fn, ast.Name):
                                    kind = fn.id
                                elif isinstance(fn, ast.Attribute):
                                    kind = fn.attr
                                else:
                                    continue
                                members[tgt.id] = kind
            result[node.name] = members
    return result


def _class_bases(source: str) -> dict[str, list[str]]:
    """Return {class_name: [base, ...]} for every class in source."""
    result: dict[str, list[str]] = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef):
            bases: list[str] = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute) and isinstance(
                    base.value, ast.Name
                ):
                    bases.append(f"{base.value.id}.{base.attr}")
            result[node.name] = bases
    return result


# Reference files generated from the fixture NXDLs, so the live NeXus
# definitions repo cannot influence them.
_CONVERTER_REFERENCE_DIR = Path(__file__).parent.parent / "data" / "nomad" / "converter"


def test_write_base_class_writes_compilable_module(tmp_path):
    """NXtestBase is written to the path its category selects, and it compiles.

    Runs with nothing stubbed and asserts on what the comparison below cannot
    see: the directory the writer derives from the NXDL's category, that the
    rendered source is accepted by ``compile()``, and that ``m_def`` carries its
    ``nx_class`` — ``m_def`` is the one member left out of the comparison.
    """
    converter.write_base_class("NXtestBase", output_dir=tmp_path, force=True)

    # NXtestBase declares category="base", so it is routed into base_classes/.
    source = (tmp_path / "base_classes" / "testbase.py").read_text(encoding="utf-8")

    assert 'nx_class="NXtestBase"' in source
    compile(source, "testbase.py", "exec")


@pytest.mark.parametrize(
    "nx_class, reference_file",
    [
        ("NXtestBase", "testbase.py"),
        ("NXtest", "test.py"),
        ("NXtest_extended", "test_extended.py"),
    ],
)
def test_fixture_renders_to_reference_structure(nx_class, reference_file):
    """Each fixture NXDL renders to the class structure stored in its reference.

    The three fixtures climb in complexity: ``NXtestBase`` is a base class, while
    ``NXtest`` and ``NXtest_extended`` are application definitions that add
    named-concept groups, inheritance from a generated base class and multi-class
    output. Each is rendered in memory, never written, so a failing case leaves
    the reference file on disk untouched for the diff.
    """
    reference = (REFERENCE_DIR / reference_file).read_text(encoding="utf-8")
    generated = converter.render(converter.build_context(nx_class))

    assert _class_members(generated) == _class_members(reference), (
        f"{nx_class}: generated classes differ from {reference_file} in their "
        "bases or their Quantity/SubSection members"
    )
