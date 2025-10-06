import logging
import os

try:
    from pynxtools.nomad.utils import get_package_filepath
except ImportError as e:
    raise ImportError(
        "The 'pynxtools' package is required but not installed. "
        "Please install it before running this script."
    ) from e
logger = logging.getLogger("pynxtools")

nxs_filepath = get_package_filepath()

if not os.path.exists(nxs_filepath):
    logger.info(f"Generating NeXus package at {nxs_filepath}.")
    import pynxtools.nomad.schema  # noqa: F401
else:
    logger.info(f"NeXus package already existed at {nxs_filepath}.")
