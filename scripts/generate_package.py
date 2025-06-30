import logging
import os

from pynxtools.nomad.utils import get_package_filepath

logger = logging.getLogger("pynxtools")

nxs_filepath = get_package_filepath()

if not os.path.exists(nxs_filepath):
    logger.info(f"Generating NeXus package at {nxs_filepath}.")
    import pynxtools.nomad.schema
else:
    logger.info(f"NeXus package already existed at {nxs_filepath}.")
