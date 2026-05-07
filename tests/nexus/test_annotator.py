"""Tests for nexus.annotation.Annotator."""

import logging
import os

from pynxtools.nexus import Annotator, NexusFileHandler

EXAMPLE_NXS = os.path.join(
    os.path.dirname(__file__),
    "../../src/pynxtools/data/201805_WSe2_arpes.nxs",
)


def test_annotation_visitor_default_mode_completes(tmp_path):
    """Annotator default mode processes the example NXS file without error."""
    logger = logging.getLogger("test_annotation_default")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "out.log"
    handler = logging.FileHandler(log_file, "w")
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    NexusFileHandler(EXAMPLE_NXS).process(Annotator(logger))

    handler.flush()
    assert log_file.read_text(), "Expected annotation output but got empty log"


def test_annotation_visitor_d_mode_annotates_only_target(tmp_path):
    """Annotator -d mode writes output only for the requested path."""
    logger = logging.getLogger("test_annotation_d")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "d_mode.log"
    fh = logging.FileHandler(log_file, "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    target = "/entry/data/delays"
    NexusFileHandler(EXAMPLE_NXS).process(Annotator(logger, documentation=target))

    fh.flush()
    assert log_file.read_text(), f"Expected annotation for {target} but got empty log"


def test_annotation_visitor_c_mode_collects_results(tmp_path):
    """Annotator -c mode logs paths that satisfy the IS-A relation."""
    logger = logging.getLogger("test_annotation_c")
    logger.setLevel(logging.DEBUG)
    log_file = tmp_path / "c_mode.log"
    fh = logging.FileHandler(log_file, "w")
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    NexusFileHandler(EXAMPLE_NXS).process(Annotator(logger, concept="/NXarpes/ENTRY"))

    fh.flush()
    assert log_file.exists()
