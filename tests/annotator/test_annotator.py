"""Tests for pynxtools.annotator.Annotator — reference-log comparison."""

import difflib
import logging
from pathlib import Path

import numpy as np
import pytest

from pynxtools.annotator.annotator import Annotator
from pynxtools.nexus.handler import NexusFileHandler

EXAMPLE_NXS = str(
    Path(__file__).parent.parent.parent
    / "src"
    / "pynxtools"
    / "data"
    / "201805_WSe2_arpes.nxs"
)
REF_DIR = Path(__file__).parent.parent / "data" / "annotator"


def _get_log(
    nxs_file, tmp_path, log_name, *, handler_level=logging.DEBUG, **annotator_kwargs
):
    """Run Annotator on nxs_file without a formatter; return list of lines.

    Logger setup mirrors pynxtools.annotator.cli.read().
    """
    logger = logging.getLogger(__file__)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    log_path = Path(tmp_path) / log_name
    handler = logging.FileHandler(log_path, "w", encoding="utf-8")
    handler.setLevel(handler_level)
    logger.addHandler(handler)
    NexusFileHandler(nxs_file).process(Annotator(logger, **annotator_kwargs))

    return log_path.read_text(encoding="utf-8").splitlines(keepends=True)


def _compare_logs(gen_lines: list[str], ref_lines: list[str]):
    """Fail with a unified diff if logs differ (after optional line filtering)."""

    def _extra_lines(lines1: list[str], lines2: list[str]) -> list[str | None]:
        """Return lines in lines1 but not in lines2, with line numbers, and ignoring
        specified lines."""
        diffs: list[str | None] = []
        for ind, line in enumerate(lines1):
            if line not in lines2:
                diffs.append(f"{line.strip()} (line: {ind})")
        return diffs

    # Case 1: line counts differ
    if len(gen_lines) != len(ref_lines):
        diffs_gen = _extra_lines(gen_lines, ref_lines)
        diffs_ref = _extra_lines(ref_lines, gen_lines)

        fail_msg = (
            f"Log files are different: mismatched line counts. "
            f"Generated file has {len(gen_lines)} lines, "
            f"while reference file has {len(ref_lines)} lines."
        )
        if diffs_gen:
            fail_msg += "\n\nExtra lines in generated:\n" + "\n".join(diffs_gen)
        if diffs_ref:
            fail_msg += "\n\nExtra lines in reference:\n" + "\n".join(diffs_ref)

        raise pytest.fail(fail_msg)

    # Case 2: same line counts, check for diffs
    diffs = []

    for ind, (gen_l, ref_l) in enumerate(zip(gen_lines, ref_lines)):
        if gen_l != ref_l:
            diffs.append(
                f"Log files are different at line {ind}:\n  generated: {gen_l}\n  reference: {ref_l}"
            )
    if diffs:
        pytest.fail("\n".join(diffs))


def test_nexus(tmp_path):
    """Full annotation of the example NXS file matches Ref_nexus_test.log."""
    np.set_printoptions(edgeitems=3, threshold=1000, precision=8, linewidth=75)
    actual = _get_log(EXAMPLE_NXS, tmp_path, "nexus_test.log")
    reference = (
        (REF_DIR / "Ref_nexus_test.log")
        .read_text(encoding="utf-8")
        .splitlines(keepends=True)
    )
    # "Path" lines contain machine-specific absolute filesystem paths
    _compare_logs(actual, reference)


def test_d_option(tmp_path):
    """-d mode output for /entry/instrument/analyser/data matches Ref_d_option_test.log."""
    actual = _get_log(
        EXAMPLE_NXS,
        tmp_path,
        "d_option.log",
        documentation="/entry/instrument/analyser/data",
    )
    reference = (
        (REF_DIR / "Ref_d_option_test.log")
        .read_text(encoding="utf-8")
        .splitlines(keepends=True)
    )
    _compare_logs(actual, reference)


def test_c_option(tmp_path):
    """-c mode concept queries match reference files and expected paths."""
    # NXbeam: full reference comparison
    actual_beam = _get_log(
        EXAMPLE_NXS,
        tmp_path,
        "c_beam.log",
        handler_level=logging.INFO,
        concept="NXbeam",
    )
    reference = (
        (REF_DIR / "Ref1_c_option_test.log")
        .read_text(encoding="utf-8")
        .splitlines(keepends=True)
    )
    _compare_logs(actual_beam, reference)

    # appdef path: spot-check
    actual_analyser = _get_log(
        EXAMPLE_NXS,
        tmp_path,
        "c_analyser.log",
        handler_level=logging.INFO,
        concept="NXarpes/ENTRY/INSTRUMENT/analyser",
    )
    assert any("entry/instrument/analyser" in ln for ln in actual_analyser)

    # attribute query: spot-check
    actual_signal = _get_log(
        EXAMPLE_NXS,
        tmp_path,
        "c_signal.log",
        handler_level=logging.INFO,
        concept="NXdata@signal",
    )
    assert any("entry/data@signal" in ln for ln in actual_signal)
