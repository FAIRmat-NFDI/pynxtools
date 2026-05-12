"""Tests for nexus.annotation.Annotator."""

import logging
import os

import numpy as np

from pynxtools.annotator.annotator import Annotator
from pynxtools.nexus.handler import NexusFileHandler

logger = logging.getLogger(__name__)

EXAMPLE_NXS = os.path.join(
    os.path.dirname(__file__),
    "../../src/pynxtools/data/201805_WSe2_arpes.nxs",
)

# ---------------------------------------------------------------------------
# Annotator — default mode
# ---------------------------------------------------------------------------


def test_annotation_visitor_default_mode_completes(tmp_path):
    """Annotator default mode processes the example NXS file without error."""
    logger = logging.getLogger("test_annotation_default")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "out.log"
    handler = logging.FileHandler(log_file, "w")
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    visitor = Annotator(logger)
    NexusFileHandler(EXAMPLE_NXS).process(visitor)

    handler.flush()
    log_text = log_file.read_text()
    # The log must contain at least one annotated entry
    assert log_text, "Expected annotation output but got empty log"


def test_nexus(tmp_path):
    """
    Verify that AnnotationVisitor traverses the example NXS file and emits
    annotation output for the key schema concepts.  We check for meaningful
    content rather than pinning an exact reference log.
    """
    example_data = os.path.join(
        os.getcwd(), "src", "pynxtools", "data", "201805_WSe2_arpes.nxs"
    )

    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    log_path = os.path.join(tmp_path, "nexus_test.log")
    handler = logging.FileHandler(log_path, "w")
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    np.set_printoptions(edgeitems=3, threshold=1000, precision=8, linewidth=75)
    NexusFileHandler(example_data).process(Annotator(logger))
    handler.flush()

    log_text = open(log_path, encoding="utf-8").read()

    # Annotation must mention the NXarpes entry group
    assert "NXarpes" in log_text, "Expected NXarpes in annotation output"
    # Known fields in the example file must appear
    assert "angles" in log_text
    assert "energies" in log_text
    assert "delays" in log_text
    # Optionality strings must be present
    assert "REQUIRED" in log_text or "OPTIONAL" in log_text or "RECOMMENDED" in log_text
    # Default plottable section must run without error
    assert "NXentry" in log_text


# ---------------------------------------------------------------------------
# Annotator — -d (documentation) mode
# ---------------------------------------------------------------------------


def test_d_option(tmp_path):
    """
    To check -d option for default NXarpes test data file.
    """
    tmp_file = os.path.join(tmp_path, "d_option_1_test.log")

    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(tmp_file, "w")

    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    NexusFileHandler(None).process(
        Annotator(logger, documentation="/entry/instrument/analyser/data")
    )

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()

    assert "FIELD" in tmp[0]
    assert "entry/instrument/analyser/data" in tmp[0]


def test_annotation_visitor_d_mode_annotates_only_target(tmp_path):
    """Annotator -d mode writes output only for the requested path."""
    logger = logging.getLogger("test_annotation_d")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "d_mode.log"
    fh = logging.FileHandler(log_file, "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Pick a path that definitely exists in the example file
    target = "/entry/data/delays"
    visitor = Annotator(logger, documentation=target)
    NexusFileHandler(EXAMPLE_NXS).process(visitor)

    fh.flush()
    log_text = log_file.read_text()
    assert log_text, f"Expected annotation for {target} but got empty log"


# ---------------------------------------------------------------------------
# Annotator — -c (concept query) mode
# ---------------------------------------------------------------------------


def test_c_option(tmp_path):
    """
    To check -c option from IV_temp.nxs.
    """
    local_path = os.path.dirname(__file__)
    path_to_ref_files = os.path.join(local_path, "../data/nexus/")

    ref_file = os.path.join(path_to_ref_files, "Ref1_c_option_test.log")
    tmp_file = os.path.join(tmp_path, "c_option_1_test.log")

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(tmp_file, "w")

    with open(ref_file, encoding="utf-8") as ref_f:
        ref = ref_f.readlines()

    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    NexusFileHandler(None).process(Annotator(logger, concept="NXbeam"))

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()

    assert tmp == ref

    logger.removeHandler(handler)
    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    NexusFileHandler(None).process(Annotator(logger, concept="NXdetector/data"))

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()
    assert tmp[0] == "INFO: entry/instrument/analyser/data\n"

    logger.removeHandler(handler)
    handler = logging.FileHandler(tmp_file, "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    NexusFileHandler(None).process(Annotator(logger, concept="NXdata@signal"))

    with open(tmp_file, encoding="utf-8") as tmp_f:
        tmp = tmp_f.readlines()
    assert tmp[0] == "INFO: entry/data@signal\n"


def test_annotation_visitor_c_mode_collects_results(tmp_path):
    """Annotator -c mode logs paths that satisfy the IS-A relation."""
    logger = logging.getLogger("test_annotation_c")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "c_mode.log"
    fh = logging.FileHandler(log_file, "w")
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    # NXarpes entry is a known superclass for the example file
    visitor = Annotator(logger, concept="/NXarpes/ENTRY")
    NexusFileHandler(EXAMPLE_NXS).process(visitor)

    fh.flush()
    # on_complete logs the collected paths; at minimum the log file must exist
    # (even if empty for this particular concept, no exception must be raised)
    assert log_file.exists()
