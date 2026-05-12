"""Regenerate tests/data/nexus/Ref_nexus_test.log."""

import logging
from pathlib import Path

import numpy as np

from pynxtools.annotator.annotator import Annotator
from pynxtools.nexus.handler import NexusFileHandler

ROOT = Path(__file__).parent.parent
EXAMPLE_NXS = str(ROOT / "src" / "pynxtools" / "data" / "201805_WSe2_arpes.nxs")
REF_PATH = ROOT / "tests" / "data" / "nexus" / "Ref_nexus_test.log"


def generate_ref_log():
    np.set_printoptions(edgeitems=3, threshold=1000, precision=8, linewidth=75)
    logger = logging.getLogger("pynxtools")
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    handler = logging.FileHandler(REF_PATH, "w", encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    NexusFileHandler(EXAMPLE_NXS).process(Annotator(logger))
    handler.flush()
    logger.removeHandler(handler)
    handler.close()
    print(f"Written: {REF_PATH}")


if __name__ == "__main__":
    generate_ref_log()
