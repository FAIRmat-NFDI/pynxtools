"""Regenerate the reference files in tests/data/nomad/converter/.

Run after changing a fixture NXDL or the metainfo Jinja2 template, then review
the diff: a structural change there is what the reference tests exist to show.
"""

from pathlib import Path

from pynxtools.nomad.converters.nxdl_to_metainfo import build_context, render

ROOT = Path(__file__).parent.parent
REF_DIR = ROOT / "tests" / "data" / "nomad" / "converter"

# NXDL fixture -> reference module, named as the converter names its output.
FIXTURES = {
    "NXtestBase": "testbase.py",
    "NXtest": "test.py",
    "NXtest_extended": "test_extended.py",
}


def generate_reference_files() -> None:
    for nx_name, file_name in FIXTURES.items():
        path = REF_DIR / file_name
        source = render(build_context(nx_name))
        # The fixture NXDLs sit outside definitions/, so the documentation URLs
        # the converter builds for them keep the absolute path of this checkout.
        # Strip it, or the generating machine's layout ends up in the reference.
        path.write_text(source.replace(f"{ROOT}/", ""), encoding="utf-8")
        print(f"Written: {path}")


if __name__ == "__main__":
    generate_reference_files()
